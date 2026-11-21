"""Render index.html from index.template.html, filling the palette from squiggle.json."""
import json, os
H = os.path.dirname(os.path.abspath(__file__))
c = json.load(open(os.path.join(H, "..", "squiggle.json")))["colors"]
ROWS = [("canvas", "Canvas", "The page behind the chat"), ("sidebar", "Sidebar", "Lemon, with terrazzo"),
        ("messageSurface", "Message", "User bubbles and the composer"), ("codeBackground", "Code block", "Mint, inked edge"),
        ("text", "Ink", "Every word. 15.7:1 on canvas"), ("textMuted", "Muted ink", "Timestamps and hints"),
        ("accent", "Accent", "Cobalt: send, links, switches"), ("secondary", "Secondary", "Sunny yellow buttons"),
        ("focus", "Focus", "Hot pink rings and active work"), ("sidebarRowSelected", "Open thread", "The sticker in the sidebar"),
        ("update", "Update", "Teal"), ("warning", "Warning", "Burnt orange"), ("error", "Error", "Raspberry")]
out = "\n".join(
    f"      <button type=\"button\" data-hex=\"{c[k]}\"><span class=\"sw\" style=\"background:{c[k]}\"></span>"
    f"<span>{n}<small>{d}</small></span><code>{c[k]}</code></button>" for k, n, d in ROWS)
t = open(os.path.join(H, "index.template.html")).read().replace("__PALETTE__", out)
open(os.path.join(H, "..", "index.html"), "w").write(t)
print("index.html", len(t))
