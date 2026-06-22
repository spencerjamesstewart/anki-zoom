# anki-zoom

A minimal Anki add-on that zooms the card reviewer in and out with the classic
**`Cmd +`** / **`Cmd -`** hotkeys (`Ctrl +` / `Ctrl -` on Windows/Linux).

Anki has zoom in/out in the **View** menu but binds no shortcut to them. This
adds the shortcuts, scopes the zoom to the reviewer, and remembers your level
between sessions.

## Features

- `Cmd/Ctrl +` and `Cmd/Ctrl -` to zoom the card view while reviewing.
- Level is **persisted** across restarts.
- **Reviewer only** — other screens keep their normal zoom.

## Install

### From a release file

1. Download `anki_zoom.ankiaddon` (or build it — see below).
2. In Anki: **Tools → Add-ons → Install from file…** and pick it.
3. Restart Anki.

### From source (development)

Anki loads an add-on by its folder name, which must be a valid Python
identifier — so it's installed as **`anki_zoom`**, not `anki-zoom`.

```sh
git clone https://github.com/spencerjamesstewart/anki-zoom.git
cd anki-zoom
make link      # symlinks this repo into Anki's add-ons dir as "anki_zoom"
```

Restart Anki. Edits to `__init__.py` take effect on the next restart.
`make unlink` removes the symlink.

## Build a distributable

```sh
make build     # produces anki_zoom.ankiaddon
```

## Configuration

**Tools → Add-ons → Reviewer Zoom (Cmd +/-) → Config**, or edit
[`config.json`](config.json):

| Key           | Default | Meaning                                        |
| ------------- | ------- | ---------------------------------------------- |
| `zoom_factor` | `1.0`   | Saved zoom level (updated as you zoom).        |
| `zoom_step`   | `0.1`   | Zoom change per keypress (10%).                |
| `min_zoom`    | `0.5`   | Lower clamp.                                   |
| `max_zoom`    | `5.0`   | Upper clamp.                                   |

There's no separate reset key (zoom in/out only by design). With the default
step, `Cmd/Ctrl -` lands exactly back on 100%.

## How it works

The reviewer renders into the shared main webview (`mw.web`), and Qt carries a
webview's zoom factor across Anki's same-origin screens. To keep zoom
reviewer-only, the add-on:

- adds the shortcuts to the reviewer's state shortcut list (`Ctrl` maps to
  `Cmd` on macOS automatically);
- re-applies the saved factor on each `reviewer_did_show_question`;
- captures the non-reviewer zoom when entering review and restores it on exit.

Tested against Anki 25.09 (Qt6).

## License

[MIT](LICENSE)
