# Ident — Beginner's Guide

This guide gets a small screen onto your wall that shows your next flight, the
flight you are on, and when you will be home. It assumes you have **never written
code or used a Raspberry Pi before**. If you can follow a recipe, you can do this.
Take it slowly; nothing here can break your computer.

> **Correct as of version 4.26.0** (October 2026).
> Ident updates itself, so if your display reports a newer version some screens
> here may have moved on. The version is shown in the control panel.

## Pick your route

| | **Route A — ready-made card** | **Route B — build it yourself** |
|---|---|---|
| **For** | Everyone. Start here. | People who like to see how it works |
| **You do** | Write a ready-made memory card, plug in, set up from your phone | Install Raspberry Pi's operating system, then Ident, by typing commands |
| **Typing commands** | **None.** No Terminal, no SSH | About 15 lines, copy-pasted |
| **Time** | About an hour, mostly waiting | About two hours |
| **Where** | Part 3 | Part 4 |

Both routes end in the same place: the same setup page on your phone (Part 5) and the
same control panel. Everything from Part 5 onward is the same for both.

---

## Part 1 — What you're building, in plain English

A **Raspberry Pi** is a tiny, cheap computer. It has no screen or keyboard of its
own.

An **e-paper display** (the "Inky") is a screen like a Kindle's — it looks like
printed paper, uses almost no power, and holds its picture even when switched off.
It clips onto the Raspberry Pi. This is what shows your flight on the wall.

The Pi runs the **Ident** software. It reads your roster, works out what to show,
and draws it on the screen. **Your roster stays on the Pi in your house** — it is
not sent to us or anyone else. You control everything from a web page on your phone.

That's the whole thing: **a tiny computer + a paper-like screen + the software.**

---

## Part 2 — Shopping list

Prices are from The Pi Hut in August 2026 and include VAT. They move, so check the
page. Raspberry Pi stock changes week to week (see the note under the table).

| # | What | Why you need it | Price | Where |
|---|------|-----------------|-------|-------|
| 1 | **Raspberry Pi 3 Model A+** | The tiny computer. The header (the row of pins) is already fitted, so **no soldering**. | £24.00 | [The Pi Hut](https://thepihut.com/products/raspberry-pi-3-model-a-plus) |
| 2 | **Pimoroni Inky Impression 7.3" (2025 Edition)** | The colour e-paper screen with the four buttons. Clips straight onto the Pi's pins. | £79.50 | [The Pi Hut](https://thepihut.com/products/inky-impression-7-3-2025-edition) |
| 3 | **Official Raspberry Pi 12.5W micro-USB power supply** | Powers the Pi. A phone charger *might* work, but the official one avoids "not enough power" problems. | £7.70 | [The Pi Hut](https://thepihut.com/products/raspberry-pi-zero-uk-power-supply) |
| 4 | **microSD card, 16–32GB (A1/A2 class)** | The Pi's "hard drive". 16GB is plenty. **Route A:** if you bought the card from us it already has Ident on it. | ~£8 | [The Pi Hut](https://thepihut.com/products/sandisk-microsd-card-class-10-a1) |
| 5 | **microSD-to-USB adapter** *(only if your computer has no SD slot)* | Lets you plug the card into your computer to write it. | ~£6 | [The Pi Hut](https://thepihut.com/products/microsd-card-usb-reader) |

**Optional:** a small desk stand or a 5×7" photo frame to mount it in.

> **Which Pi, and what is in stock.** The smallest, lowest-power choice is the **Pi Zero 2 W**, but
> on 10 October 2026 I could not confirm it can be bought anywhere: the most recent stock
> report I found, [from 14 September](https://raspberry.tips/en/raspberrypi-infos/raspberry-pi-zero-2-w-alternative-sold-out),
> had it sold out at Pimoroni and The Pi Hut. That is why the list says **Pi 3 Model A+**.
> A search snapshot showed the 3A+ [in stock at The Pi Hut](https://thepihut.com/products/raspberry-pi-3-model-a-plus)
> but its date was unclear, so check the page before you order. The **Pi 4 (1GB)** also works;
> it needs a **USB-C** power supply instead of the micro-USB one above. The Pi 5 should work but is
> not a board we test on. Don't pay for more memory than 1GB; it makes no difference here.
>
> **Wi-Fi bands.** The Pi Zero 2 W only does **2.4GHz** Wi-Fi. If you use one and your router only
> broadcasts 5GHz (or hides both bands behind one name), it will never connect, so turn 2.4GHz on
> first. The 3A+ and the 4 do both bands.
>
> **Screens.** The older **5.7" Inky Impression** is discontinued; Ident still supports it if you
> own one, but buy the 7.3" for a new build. The 4.0" and 13.3" panels also work.

---

## Part 3 — Route A: the ready-made card (start here)

You will use the **Ident card image**: a complete, ready-made memory card with the operating
system and Ident already on it. When you have your licence key you get an email with a
download link. You write that download to the card, plug it in, and do the rest from your
phone. **You never type a command.**

*Bought the card from us?* It is already written. Skip step 1.

### Step 1 — Put Ident on the memory card (on your computer, not the Pi)

1. Open your order email and click **Download the SD card image**. It is about 1 GB.
   **Do not unzip it** — keep it exactly as it downloaded.
2. Download and install **Raspberry Pi Imager** from <https://www.raspberrypi.com/software/>.
   It is a free, official app.
3. Put the card in your computer (use the USB adapter if needed) and open Imager:
   - **Choose Device** → the Pi you bought.
   - **Choose OS** → scroll to the bottom → **Use custom** → pick the file you downloaded.
   - **Choose Storage** → your card. **Double-check** it is the card and not your
     computer's own drive.
   - **Write.** If it asks whether to apply settings, say **No**.
4. Wait for it to finish (a few minutes; it erases the card), then take the card out.

### Step 2 — Fit the display

Switch everything **off** first. Line up the 40 pins of the Inky with the Pi's pins and press
straight down, evenly. All 40 pins should be engaged, with no pin hanging over at either end.
Hold both boards by their **edges**: the screen is glass and cracks if you press on it. If
your kit came with standoffs (little spacers), use those screws — longer ones can crack the glass.

### Step 3 — Card in, power on

Put the card in the Pi's card slot, contacts down. Plug the power into the socket marked
**PWR IN**. On a Pi Zero that is the micro-USB socket nearest the corner, *not* the middle one
(the middle one is data only).

**Now wait 3 to 5 minutes.** The display does not know your Wi-Fi yet, so after about two
minutes it starts its own Wi-Fi network called **Ident-Setup**. A flickering green light is
normal, and the screen may stay blank for now.

### Step 4 — Tell it your Wi-Fi, from your phone

1. On your phone open **Settings → Wi-Fi** and join **Ident-Setup**. The password is
   **identsetup**. It is the same on every display and public on purpose: it only stops a
   neighbour's phone joining by accident. Nothing private goes over it.
2. Your phone may say there is no internet. That is expected: stay connected.
3. In your phone's browser, go to **`10.42.0.1:8080`**. A page called *Connect your display*
   opens. (It will not pop up by itself; you type the address.)
4. Pick your home Wi-Fi from the list, type its password, and press **Connect**. With a
   Pi Zero 2 W it must be a 2.4GHz network.
5. The display leaves Ident-Setup and joins your Wi-Fi. Join **your own Wi-Fi** on the phone again.

### Step 5 — Finish setting up

Now on your own Wi-Fi, open **`ident.local:8080`** in your phone's browser. Fill in the setup
page (Part 5 explains each box) and press **Finish setup**. You will need your **licence key**
(`IDNT-XXXX-…`, in your email); it is checked online, once. Then add it to your home screen
(iPhone: **Share → Add to Home Screen**; Android: **⋮ → Add to Home screen**).

If `ident.local` does not open, use the display's IP address from your router's device list,
with `:8080` on the end.

**That's it — you're done.** Go on to Part 5 and Part 6. Move it to the wall, plug it in, and a
minute or so later it lights up.

> **Not yet tried on real hardware.** This route is written from how the software behaves. The
> exact words on Imager's screens, the 3–5 minute wait and what your phone says on Ident-Setup
> have not been run through on a real card and phone. If a screen differs, trust the screen and
> tell us.

---

## Part 4 — Route B: build it yourself

For people who want to build it by hand: you install Raspberry Pi's operating system, then copy
Ident on. You will use a Terminal (a window where you type instructions). Everything is
copy-and-paste. Route A needs none of this.

### B1 — Flash Raspberry Pi OS

1. On your computer install **Raspberry Pi Imager** (<https://www.raspberrypi.com/software/>).
2. Put the card in. **Choose Device** → your Pi. **Choose OS** → *Raspberry Pi OS (other)* →
   *Raspberry Pi OS Lite (64-bit)*. ("Lite" means no desktop; we don't need one.)
   **Choose Storage** → the card (double-check it).
3. Click **Next**, then **Edit Settings**. This is the important screen:
   - **Hostname:** `ident`
   - **Username and password:** username `pilot`, and a password you will remember. **Write it down.**
   - **Wireless LAN:** your Wi-Fi name and password exactly (capitals matter), country `GB`.
     On a Pi Zero 2 W it must be a **2.4GHz** network.
   - **Locale / time zone:** `Europe/London`.
   - **Services** tab → **Enable SSH** → *Use password authentication*. ("SSH" is how your
     computer sends instructions to the Pi.)
4. **Save**, **Yes**, and wait. Take the card out.

### B2 — First switch-on

Push the Inky onto the Pi's pins (40 pins, one way round, **edges only**). Put the card in, plug
the power into **PWR IN**, and wait **2–3 minutes**.

### B3 — Talk to the Pi

Open a Terminal (Mac: `Cmd + Space`, type `Terminal`; Windows: Start, type `Terminal`). Type this
and press Enter:

```
ssh pilot@ident.local
```

Type `yes` if asked about continuing. Type your password when asked — **nothing appears as you
type; that is normal.** When the line ends in `ident:~ $`, you're in.

If it can't connect, wait a few more minutes, check your computer is on the same Wi-Fi, or use the
Pi's IP address from your router (`ssh pilot@192.168.1.81`). If the Pi never reached your Wi-Fi it
makes its own **Ident-Setup** network after two minutes: do Route A step 4 instead.

### B4 — Switch on the screen connection

The screen talks to the Pi over two data channels called SPI and I2C. Type these one line at a time:

```
sudo raspi-config nonint do_spi 0
sudo raspi-config nonint do_i2c 0
echo "dtoverlay=spi0-0cs" | sudo tee -a /boot/firmware/config.txt
sudo reboot
```

(`sudo` means "do this as administrator". The reboot disconnects you.) The third line matters as
much as the first two: skip it and Ident stops with "Woah there, some pins we need are in use!".
Wait a minute, then `ssh pilot@ident.local` again.

### B5 — Install the helper software and fonts

```
sudo apt update
sudo apt full-upgrade -y
sudo apt install -y python3-venv python3-pip unzip fonts-dejavu-core python3-lgpio
```

### B6 — Put Ident on the Pi

You have a file called `ident.zip`. In a **second** Terminal on your computer (do not `ssh` in this
one), with the zip in Downloads:

```
scp ~/Downloads/ident.zip pilot@ident.local:~/
```

Back in the Pi's Terminal:

```
cd ~
unzip -o ident.zip
cd ident
python3 -m venv .venv --system-site-packages
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-epaper.txt
pip install gpiozero
```

Lots of text scrolls by; that is normal.

### B7 — Test it

```
python -m ident.main
```

You should see lines like `found a impression_7_3 panel (800x480, spectra6) — output set to
e-paper`. Ident asks the screen what it is; there is nothing to choose. If it says nothing about a
panel, the screen wasn't found: check SPI **and** I2C are both on (B4).

Leave it running and, on your phone, open `http://ident.local:8080` to do the setup page (Part 5).
When you have finished, press `Ctrl + C` in the Terminal to stop the test.

### B8 — Make it start by itself

Copy-paste this **whole block** (if your username isn't `pilot`, change both `pilot`s):

```
sudo tee /etc/systemd/system/ident.service >/dev/null <<EOF
[Unit]
Description=Ident
After=network-online.target

[Service]
User=pilot
WorkingDirectory=/home/pilot/ident
ExecStart=/home/pilot/ident/.venv/bin/python -m ident.main
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF
sudo systemctl daemon-reload
sudo systemctl enable --now ident
```

Check it (press `q` to leave the view): `systemctl status ident`. You're done: move it to the wall,
plug it in, and it starts by itself. The short, technical version of this route is
[`INSTALL_PI.md`](../../INSTALL_PI.md).

---

## Part 5 — The setup page and the control panel

Both routes land here. On the first visit to `ident.local:8080` you get a **setup page**. Fill in:

- **Display style** — how the wall looks. You can change it later.
- **Display name** — anything you like ("Kitchen"). Useful if you ever run two.
- **Home base** — your base airport code, e.g. `LGW`.
- **Airline code** — e.g. `U2` for easyJet.
- **Roster calendar URL** — your calendar link. Leave it blank and add it later if you like;
  **Part 6 explains where to find it**, the one thing that isn't obvious.
- **Licence key** — `IDNT-XXXX-…`, from your email.
- **Username and password** — locks the control panel, and it is required: at least six
  characters. The panel shows your roster and holds your calendar link, which is effectively a
  password for your whole schedule.

  **If you ever forget it:** take the SD card out, put a file called `ident-reset.txt` on the
  small drive that appears when you plug the card into a computer, put it back, and switch the
  display on. It clears the password and deletes the file. No Terminal, no reflashing.

Press **Finish setup** and you land on the control panel. From here you can:

- **Roster:** paste your roster calendar (iCal) link, or upload a `.ics` file, and
  tap **Pull feed now**.
- **Add a personal flight:** type a flight number and date for a non-work trip — it
  looks up the route and times and tracks it (with a 90-minute "report" time).
- **Airline logos:** upload your easyJet logo (use code `U2`) so the boarding-pass
  style shows it; add others (e.g. `BA`) for personal flights. Use PNG images with a
  see-through background for the best look.
- **Display style:** tap a thumbnail to choose how the wall looks. The departure board
  comes in three colours (**Board colours**). The month calendar is on a button
  (**Buttons**), not a style.
- **Timing sliders:** set your commute, walk-to-car, and debrief minutes so the
  "home" time is right for you.
- **All settings:** the section at the very bottom exposes every option if you ever
  want to fine-tune.

---

## Part 6 — Where to find your calendar link

This trips people up, so it gets its own part.

Ident wants a **web address that serves your calendar**, not a calendar file you
downloaded. The difference matters: a file is a snapshot of today, while an
address is re-read every half hour, so a roster change appears on the wall
without you doing anything.

Every provider names it differently — *secret address*, *private address*,
*subscription link*, *ICS link* — and they all mean the same thing: a long,
unguessable URL, usually ending in `.ics`.

> **Treat that link like a password.** Anyone who has it can read your whole
> roster, forever, without logging in to anything. Don't email it, don't post it
> in a forum, and don't put it in a message to support — Ident deliberately hides
> it from its own diagnostics for the same reason.

### Getting your roster from eCrew

eCrew doesn't give you a calendar link to paste. What it does instead is copy
your duties into a calendar on your phone or iPad. You then get the link from
*that* calendar. There are three steps.

**Step 1 — Have eCrew write your roster into a calendar.** In the eCrew app,
open Settings, turn on **Upload to Calendar** and **Auto Sync**, and choose which
calendar it writes to. (These are the names used in the eCrew Mobile user guide;
your airline's version may word them slightly differently.) Then open your
phone's Calendar app and check your duties have appeared.

- Pick a calendar that lives in your **Google** or **iCloud** account — not one
  marked *On My iPhone* or *On My iPad*. Only an online calendar has a link that
  Ident can read.
- Ident has been tested with one calendar event per flight. eCrew's **Combined
  Flights** option, which merges a day's flights, has not been tested with
  Ident yet, so leave it off for now.
- eCrew can only copy what it has downloaded. After a roster change, open eCrew
  so it syncs. (How often Auto Sync runs on its own with the app closed hasn't
  been checked.)

**Step 2 — Get that calendar's link.** Follow the Google or iCloud steps below.
Google's is called the *secret address in iCal format*; iCloud's is the *public
calendar* link. Ident has been tested with Google's. The iCloud route should
work the same way but **has not been tested with Ident yet**.

**Step 3 — Give the link to Ident.** Paste it into the control panel (Pi), the
setup page (reTerminal), or the settings sheet (iPad).

**On an iPad there's a simpler route.** The iPad version can't read Google
calendar links directly — Google doesn't allow web pages to — so instead an
iPad Shortcut reads the calendar eCrew writes to and hands it to the board.
Nothing passes through anyone else, and the calendar doesn't need to be
online. Tap the board, open **Roster from eCrew (no link to paste)**, and follow
the steps there. That Shortcut has been tested with sample data but not yet on a
real iPad with a real eCrew calendar.


**From Google Calendar** — the usual route if you already mirror your roster
there:

1. Open Google Calendar on a computer (not the phone app — the option isn't there).
2. Settings (the gear, top right) → **Settings**.
3. On the left, under *Settings for my calendars*, click the calendar's name.
4. Click **Integrate calendar**.
5. Copy the link under **Secret address in iCal format**.

If you ever share it by accident, there's a **Reset** button in the same place
that kills the old link and issues a new one. ([Google's own
instructions](https://support.google.com/calendar/answer/37648).)

**From Apple / iCloud Calendar:**

1. Go to iCloud.com/calendar and sign in.
2. Click the information button next to the calendar's name.
3. Turn on **Public Calendar**.
4. Click **Copy**.

That link begins `webcal://` rather than `https://`. Paste it exactly as it is —
Ident understands it. ([Apple's own
instructions](https://support.apple.com/guide/icloud/share-a-calendar-mm6b1a9479/icloud).)

**From Outlook.com or Microsoft 365:**

1. In Calendar, go to Settings → **Calendar** → **Shared calendars**.
2. Under *Publish a calendar*, pick the calendar and the option that shows all
   details.
3. Click **Publish**, then copy the **ICS** link — there's an HTML one beside it,
   which is a web page, not a feed.

([Microsoft's own
instructions](https://support.microsoft.com/en-us/outlook/share-your-calendar-in-outlook-com).)

**How to tell you've got the right link.** Paste it into a browser. You should
get a download, or a screen full of text starting `BEGIN:VCALENDAR`. If you get a
login page or a normal-looking calendar, that's the wrong link — it's the *view*
of the calendar, not the feed.

---

---

## The four buttons on the screen

Out of the box:

- **Button A** — turn the display on/off
- **Button B** — change the style (it remembers your choice)
- **Button C** — show the flight's QR code full-screen, to scan with a phone
- **Button D** — show a **next-duty card** for 7 seconds: the date, where you're going,
  your report time and first departure. Handy on a day off without reaching for a phone.

Hold any button for two seconds to switch stronger colours on or off.

You can change what each button does in the control panel, under **Buttons**.

---

---

## If something goes wrong

**Either route**

- **Can't reach the web page:** the address ends in **:8080**, and your phone must be on the same
  Wi-Fi as the display. Failing that, use the display's IP address from your router.
- **Moved house, or the router changed:** you don't need a computer. After two minutes offline the
  display raises its own **Ident-Setup** network. Join it from a phone with the password
  **identsetup**, open `10.42.0.1:8080`, and point it at the new Wi-Fi.
- **Forgot the panel password:** use the `ident-reset.txt` trick in Part 5.
- **A Pi Zero 2 W won't join your Wi-Fi:** it only does 2.4GHz.

**Route B only**

- **Text is tiny:** the fonts didn't install. Run `sudo apt install -y fonts-dejavu-core` then
  `sudo systemctl restart ident`.
- **"Woah there, some pins we need are in use":** you missed the third line in B4. Run it now and
  reboot.
- **Change Wi-Fi from the Terminal:** `sudo nmtui`, then *Activate a connection*.
- **Updating by hand:** copy the new `ident.zip` across (B6), then on the Pi: `cd ~ && unzip -o ident.zip`,
  then `find ~/ident -name __pycache__ -type d -exec rm -rf {} +`, then `sudo systemctl restart ident`.

---

## A few honest notes

- The e-paper screen is **glass and fragile** — handle it by the edges.
- It refreshes slowly (20-35 seconds) and isn't a touchscreen — that's normal for
  this kind of display and is why it sips power and reads like paper.
- **The screen flashes while it redraws.** A colour panel runs through its colours
  several times before it settles. That's normal, not a fault.
- Live flight tracking uses an online service (AeroDataBox by default, or
  Flightradar24 if you have a token) that needs a free or cheap API key — add it
  later in the control panel's Advanced section. The wall works without one; you
  just won't get live times or the in-air position, so on a delayed day it will
  show the scheduled times, which is precisely the day they are wrong. Your
  commute home is a slider you set once. If you would rather it asked how long
  the drive home really is, with traffic, there is a **Live drive time home**
  switch in Advanced — it needs a Google Maps key and your home and car-park
  coordinates, and it only asks while you are actually flying, so it costs very
  little. It is off unless you turn it on.
- Airline logos are trademarks, so the app doesn't come with any — it simply shows
  the image files *you* upload, which is exactly what you want for your own display.

---

---

## Keeping it up to date

Ident checks `ident.xpdr.aero` once a day for a newer version — your own display asks
our website; nothing is reported back to us.

A new version **installs itself** (on both routes), but only once it has been published for three days,
and never in the middle of a duty — only on a day off or between duties. The three-day
wait is the safety net: a bad release sits on the author's own wall for three days
before it can reach yours. The control panel shows your version and a button to install
a waiting update immediately if you would rather not wait, and a switch to turn the
automatic part off completely. Every download is checked against a published checksum
and your working version is backed up first, so a failed update leaves it alone.

---

*Correct as of version 4.26.0 — October 2026.*
*When Ident is updated, this guide is reviewed and this line is updated with it.*
