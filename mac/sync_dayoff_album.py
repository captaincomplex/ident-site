#!/usr/bin/env python3
"""
sync_dayoff_album.py — Apple Photos album → Ident's day-off pictures.

Reads a named album from the Apple Photos library on your Mac, resizes each
picture for the panel, and sends it to the display's control panel over your
home network. It mirrors the album: a photo added to the album appears on the
wall, a photo taken out leaves it. Ident then shows one of them per day off,
chosen by the date, so it is steady all day and different tomorrow.

Pair it once, then run it (or let launchd run it hourly):

    python3 sync_dayoff_album.py --pair      # paste the code from the panel
    python3 sync_dayoff_album.py             # sync now

WHY THE CONTROL PANEL AND NOT SSH (19 Sep 2026)
  This used to copy the pictures with SSH and rsync straight into Ident's
  data folder. On the SD image Ident runs as its own account, so your login
  cannot write there - and a new display has no SSH unless you set it up. The
  panel route needs neither. The pairing code it uses can change the album
  and nothing else, and it is kept in your Mac's Keychain, not in a file.

  Nothing passes through a server: your Mac sends straight to the display.
  Re-encoding here, and again on the display, drops the camera metadata -
  location, device, timestamps - so what lands on the wall is the picture and
  nothing else.

Adapted from the same script in the Spotipi Photos project. It resizes to
*cover* the panel and does not crop (Ident crops to fill at render time), and
saves JPEG, not PNG - these are photographs, not LED frames.

Requirements (on the Mac):
    pip3 install osxphotos pillow pillow-heif

The first run asks permission to read the Photos library. Grant it to your
terminal in System Settings → Privacy & Security → Photos.
"""

import argparse
import getpass
import hashlib
import io
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

# Every Inky panel Ident supports, largest first. 1600x1200 covers them all.
PANELS = {"4.0": (600, 400), "5.7": (600, 448), "7.3": (800, 480), "13.3": (1600, 1200)}

DEFAULT_HOST = "ident.local"
DEFAULT_PORT = 8080
KEYCHAIN_SERVICE = "Ident album sync"
SETTINGS = os.path.expanduser("~/Library/Application Support/Ident/album-sync.json")


# ---------- pure logic: no Mac, no network, no Photos (tested on Linux) ----------

def photo_name(uuid: str, jpeg: bytes) -> str:
    """<Photos UUID>-<8 hex of the picture's SHA-256>.jpg

    The UUID keeps one file per photo; the hash changes when the photo is
    edited in Photos, so the edit arrives as a new file and the old version
    leaves. Must satisfy ident.album_sync.NAME_RE on the display.
    """
    return f"{uuid}-{hashlib.sha256(jpeg).hexdigest()[:8]}.jpg"


def plan(local: set, remote: set) -> tuple:
    """(to_send, to_remove), each sorted. Sending happens before removing, so
    the wall never goes blank part-way through a sync."""
    return sorted(local - remote), sorted(remote - local)


def refuse_to_empty(local: set, remote: set, allow_empty: bool) -> bool:
    """True if this run would clear every picture off the display.

    An album that is empty or misspelt looks exactly like "delete everything".
    rsync --delete used to do just that; now it takes --allow-empty to mean it.
    """
    return not local and bool(remote) and not allow_empty


def uuid_of(name: str) -> str:
    """The Photos UUID in a name made by photo_name(), or "" for any other name."""
    stem, dot, ext = name.rpartition(".")
    uuid, dash, digest = stem.rpartition("-")
    ok = dot and ext == "jpg" and dash and len(digest) == 8 and len(uuid) >= 8
    return uuid if ok else ""


def explain_remote(remote, lookup, album_uuids) -> list:
    """One line per picture on the display, saying where it came from.

    *lookup(uuid)* returns (original filename, [album titles]) or None.
    Written for "the wall shows photos that are not in the album": each line
    says whether the picture is a photo in this album, a
    photo that is not in it, or one this Mac's library does not have at all.
    """
    lines = []
    for name in sorted(remote):
        uuid = uuid_of(name)
        found = lookup(uuid) if uuid else None
        if uuid in album_uuids:
            where = "in this album"
        elif found:
            where = "NOT in this album - in: " + (", ".join(sorted(set(found[1]))) or "no album")
        else:
            where = "not in this Mac's Photos library"
        lines.append(f"    {found[0] if found else name}: {where}")
    return lines


def raw_to_jpeg(src_path: str) -> bytes:
    """A file Pillow cannot open - camera RAW such as Canon .CR3 - as JPEG bytes.

    Uses `sips`, which is on every Mac and decodes RAW with the same system
    decoder Photos uses. [Unverified 19 Sep 2026] that sips reads every camera's
    RAW; the Mac's own RAW support decides.
    """
    import shutil
    import tempfile
    if not shutil.which("sips"):
        raise ValueError("Pillow can't read it, and there is no `sips` to convert it")
    with tempfile.TemporaryDirectory() as d:
        out = os.path.join(d, "converted.jpg")
        r = subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "best",
                            src_path, "--out", out], capture_output=True, text=True)
        if r.returncode != 0 or not os.path.exists(out):
            raise ValueError("sips could not convert it: "
                             + ((r.stderr or r.stdout).strip()[:200] or f"exit {r.returncode}"))
        with open(out, "rb") as f:
            return f.read()


def build_jpeg(src_path: str, box, quality: int, convert=None) -> bytes:
    """EXIF-orient, resize to cover *box* without cropping, return JPEG bytes.

    A file Pillow cannot identify goes through *convert* (raw_to_jpeg by
    default) first. Before 19 Sep 2026 such files were skipped: 27 of the 168
    in one owner's album were Canon .CR3 and never reached the wall.
    """
    from PIL import Image, ImageOps, UnidentifiedImageError
    W, H = box
    try:
        im = Image.open(src_path)
    except UnidentifiedImageError:
        im = Image.open(io.BytesIO((convert or raw_to_jpeg)(src_path)))
    with im:
        im = ImageOps.exif_transpose(im)
        im = im.convert("RGB")
        sw, sh = im.size
        scale = max(W / sw, H / sh)
        if scale < 1.0:                          # never upscale a small original
            im = im.resize((max(1, round(sw * scale)), max(1, round(sh * scale))),
                           Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=quality, optimize=True)
        return buf.getvalue()


# ---------- the display's control panel ----------

class Panel:
    def __init__(self, host: str, port: int, code: str, timeout: int = 60):
        self.base = f"http://{host}:{port}"
        self.code = code
        self.timeout = timeout

    def _call(self, method: str, path: str, body: bytes = None, ctype: str = None):
        req = urllib.request.Request(self.base + path, data=body, method=method)
        req.add_header("Authorization", f"Bearer {self.code}")
        if ctype:
            req.add_header("Content-Type", ctype)
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as r:
                return json.loads(r.read().decode() or "{}")
        except urllib.error.HTTPError as e:
            try:
                msg = json.loads(e.read().decode()).get("error") or e.reason
            except Exception:
                msg = e.reason
            raise SystemExit(f"The display said no ({e.code}): {msg}")
        except (urllib.error.URLError, OSError) as e:
            raise SystemExit(f"Can't reach the display at {self.base} ({e}). Is it on, "
                             f"and is this Mac on the same network?")

    def manifest(self) -> dict:
        return self._call("GET", "/api/album/sync")

    def send(self, name: str, jpeg: bytes) -> dict:
        return self._call("PUT", f"/api/album/sync/{name}", jpeg, "image/jpeg")

    def remove(self, name: str) -> dict:
        return self._call("DELETE", f"/api/album/sync/{name}")

    def done(self, album: str) -> bool:
        """Tell the display which album it now holds. Best effort: a display
        older than 4.21.0 has no such call, and the sync itself has worked."""
        try:
            self._call("POST", "/api/album/sync/done",
                       json.dumps({"album": album}).encode(), "application/json")
            return True
        except SystemExit:
            return False


# ---------- where the code and the address are kept ----------

def load_settings() -> dict:
    try:
        with open(SETTINGS) as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def save_settings(host: str, port: int) -> None:
    os.makedirs(os.path.dirname(SETTINGS), exist_ok=True)
    with open(SETTINGS, "w") as f:
        json.dump({"host": host, "port": port}, f, indent=2)


def keychain_get(account: str) -> str:
    r = subprocess.run(["security", "find-generic-password", "-s", KEYCHAIN_SERVICE,
                        "-a", account, "-w"], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ""


def keychain_set(account: str, code: str) -> None:
    # -U updates an existing entry rather than failing on a second pairing.
    # The code is passed as an argument, so it is visible to other accounts on
    # this Mac in the process list for the instant `security` runs. On a
    # one-person Mac that is nobody; and the code can only touch the album.
    r = subprocess.run(["security", "add-generic-password", "-U", "-s", KEYCHAIN_SERVICE,
                        "-a", account, "-w", code], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"Could not save the code to the Keychain: {r.stderr.strip()}")


# ---------- commands ----------

def pair(host: str, port: int) -> None:
    print(f"Pairing with the display at {host}:{port}.")
    print("In its control panel, under Days off, press 'Pair a Mac' and copy the code.")
    code = getpass.getpass("Paste the code here (it won't show): ").strip()
    if not code:
        raise SystemExit("No code entered.")
    info = Panel(host, port, code).manifest()          # proves the code works
    keychain_set(f"{host}:{port}", code)
    save_settings(host, port)
    print(f"Paired. The display expects the album {info.get('album')!r} and has "
          f"{len(info.get('photos', []))} picture(s) from before.")
    print("Now run this script without --pair to send the album.")


def sync(host: str, port: int, album: str, box, quality: int,
         dry_run: bool, allow_empty: bool, listing: bool = False) -> None:
    code = keychain_get(f"{host}:{port}")
    if not code:
        raise SystemExit(f"This Mac isn't paired with {host}:{port}. Run with --pair first.")
    panel = Panel(host, port, code)
    info = panel.manifest()
    album = album or info.get("album") or "Ident"
    remote = set(info.get("photos", []))

    try:
        import osxphotos
    except ImportError:
        raise SystemExit("Missing dependency: osxphotos. Run: pip3 install osxphotos")
    try:
        import pillow_heif                       # iPhone photos are HEIC
        pillow_heif.register_heif_opener()
    except Exception:
        pass

    print(f"Reading Apple Photos album {album!r}; targeting {box[0]}x{box[1]}")
    db = osxphotos.PhotosDB()
    photos = [p for p in db.photos(albums=[album]) if p.isphoto]
    if listing:
        print(f"  on the display now: {len(remote)} picture(s)")
        def lookup(uuid):
            try:
                hit = db.photos(uuid=[uuid])
            except Exception:
                hit = []
            return (hit[0].original_filename, hit[0].albums) if hit else None
        for line in explain_remote(remote, lookup, {p.uuid for p in photos}):
            print(line)
        same = [a for a in db.album_info if a.title == album]
        print(f"  albums called {album!r} in this library: {len(same)}"
              + ("".join(f"\n    - {a.title} ({len(a.photos)} items, folder: "
                         f"{'/'.join(a.folder_names) or 'none'})" for a in same)))
        for p in photos:
            print(f"  {p.original_filename}  {p.date:%Y-%m-%d}  "
                  f"albums: {', '.join(sorted(set(p.albums))) or '-'}")
    built = {}
    for p in photos:
        src = p.path_edited if (p.hasadjustments and p.path_edited) else p.path
        if not src or not os.path.exists(src):
            print(f"  ! not downloaded (open it in Photos first): {p.original_filename}")
            continue
        try:
            jpeg = build_jpeg(src, box, quality)
        except Exception as e:
            print(f"  ! skip {p.original_filename}: {e}")
            continue
        built[photo_name(p.uuid, jpeg)] = jpeg
    print(f"Built {len(built)} picture(s); the display has {len(remote)}.")

    if refuse_to_empty(set(built), remote, allow_empty):
        raise SystemExit(f"The album {album!r} gave no pictures, so this run would clear "
                         f"all {len(remote)} off the display. Nothing was changed. Check "
                         f"the album name, or pass --allow-empty if you mean it.")

    to_send, to_remove = plan(set(built), remote)
    if listing:
        print(f"  on the display now: {len(remote)}; would send {len(to_send)}, "
              f"would remove {len(to_remove)}")
    if dry_run:
        print(f"DRY RUN - would send {len(to_send)} and remove {len(to_remove)}.")
        return
    for i, name in enumerate(to_send, 1):
        panel.send(name, built[name])
        print(f"  sent {i}/{len(to_send)}")
    for name in to_remove:
        panel.remove(name)
    panel.done(album)
    print(f"Done: {len(to_send)} sent, {len(to_remove)} removed, "
          f"{len(built)} on the display.")
    if to_send and not remote:
        print("Turn on 'Use the synced Apple Photos album instead' in the control panel.")


def main(argv=None):
    saved = load_settings()
    ap = argparse.ArgumentParser(
        description="Send an Apple Photos album to Ident's day-off pictures.")
    ap.add_argument("--pair", action="store_true",
                    help="Pair this Mac with the display, using the code from its control panel.")
    ap.add_argument("--host", default=saved.get("host", DEFAULT_HOST),
                    help=f"The display's address (default: {DEFAULT_HOST}, or the one you paired with).")
    ap.add_argument("--port", type=int, default=saved.get("port", DEFAULT_PORT),
                    help=f"The control panel's port (default: {DEFAULT_PORT}).")
    ap.add_argument("--album", default=None,
                    help="Apple Photos album to send. Omit it and the name set in the "
                         "control panel is used, so that is the only place to set it.")
    ap.add_argument("--panel", choices=sorted(PANELS), default="13.3",
                    help="Panel size to target (default: 13.3, which covers them all).")
    ap.add_argument("--quality", type=int, default=88, help="JPEG quality (default: 88).")
    ap.add_argument("--dry-run", action="store_true",
                    help="Work out what would change, and change nothing.")
    ap.add_argument("--allow-empty", action="store_true",
                    help="Let an empty album clear every picture off the display.")
    ap.add_argument("--list", action="store_true",
                    help="Print every photo found, with its date and the albums it is in.")
    args = ap.parse_args(argv)

    if args.pair:
        pair(args.host, args.port)
    else:
        sync(args.host, args.port, args.album, PANELS[args.panel], args.quality,
             args.dry_run, args.allow_empty, args.list)


if __name__ == "__main__":
    main()
