# ident-site

The website for [Ident](https://ident.xpdr.aero) — a flight-duty display for pilots.

Served by GitHub Pages at **ident.xpdr.aero** (custom domain in `CNAME`).
Static HTML and CSS; no build step.

The application source lives in a separate, private repository. Changes here are
copied from its `docs/` folder — edit there, then sync:

```sh
rsync -a --delete --exclude .git ../docs/ ./
git add -A && git commit -m "Sync site" && git push
```
