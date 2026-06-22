"""anki-zoom: reviewer-only zoom with the classic Cmd/Ctrl +/- hotkeys.

Anki ships zoom in/out only as View-menu items with no keyboard shortcut
(just Reset Zoom is bound, to Cmd/Ctrl+0). This add-on adds the classic
Cmd/Ctrl + and Cmd/Ctrl - shortcuts, scoped to the card reviewer, and
remembers the zoom level across sessions.

The reviewer renders into the shared main webview (mw.web), and Qt keeps a
webview's zoom factor across Anki's same-origin screens. So to keep zoom
"reviewer only" we manage it explicitly: re-apply our saved factor while
reviewing, and restore the previous (non-reviewer) factor on the way out.
"""

from __future__ import annotations

from aqt import gui_hooks, mw

# Defaults mirror config.json; used when a key is missing or getConfig() is None.
_DEFAULTS = {
    "zoom_factor": 1.0,  # persisted reviewer zoom level (1.0 == 100%)
    "zoom_step": 0.1,    # change applied per keypress
    "min_zoom": 0.5,
    "max_zoom": 5.0,
}

# Zoom level in use outside the reviewer, captured on entry so we can restore it
# on exit (mw.web is shared between screens and Qt carries the factor across).
_outside_factor = 1.0


def _config() -> dict:
    conf = mw.addonManager.getConfig(__name__) or {}
    return {**_DEFAULTS, **conf}


def _save_factor(factor: float) -> None:
    conf = mw.addonManager.getConfig(__name__) or {}
    conf["zoom_factor"] = factor
    mw.addonManager.writeConfig(__name__, conf)


def _clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def _apply(factor: float) -> None:
    if mw.web is not None:
        mw.web.setZoomFactor(factor)


def _zoom_by(delta: float) -> None:
    conf = _config()
    factor = _clamp(
        round(conf["zoom_factor"] + delta, 2), conf["min_zoom"], conf["max_zoom"]
    )
    _save_factor(factor)
    _apply(factor)


def _zoom_in() -> None:
    _zoom_by(_config()["zoom_step"])


def _zoom_out() -> None:
    _zoom_by(-_config()["zoom_step"])


def _on_state_shortcuts(state: str, shortcuts: list) -> None:
    if state != "review":
        return
    # Qt maps "Ctrl" to the Command key on macOS, so these read as Cmd +/- there
    # and Ctrl +/- on Windows/Linux. "Ctrl+=" catches the unshifted key that
    # carries "+"; "Ctrl+Shift+=" catches the shifted press. Mutate in place so
    # Anki actually sees the additions.
    shortcuts += [
        ("Ctrl+=", _zoom_in),
        ("Ctrl+Shift+=", _zoom_in),
        ("Ctrl+-", _zoom_out),
    ]


def _on_show_question(card) -> None:
    # Re-apply the saved factor for each card. Cards render via JS without a
    # reload, so this is a no-op once set; it also (re)applies our zoom right
    # after the page loads on entering review.
    _apply(_config()["zoom_factor"])


def _on_state_will_change(new_state: str, old_state: str) -> None:
    global _outside_factor
    if new_state == "review" and old_state != "review":
        # entering review: remember the zoom level used elsewhere
        if mw.web is not None:
            _outside_factor = mw.web.zoomFactor()
    elif old_state == "review" and new_state != "review":
        # leaving review: restore it so our zoom stays reviewer-only
        _apply(_outside_factor)


gui_hooks.state_shortcuts_will_change.append(_on_state_shortcuts)
gui_hooks.reviewer_did_show_question.append(_on_show_question)
gui_hooks.state_will_change.append(_on_state_will_change)
