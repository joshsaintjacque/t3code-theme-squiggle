"""Build the Squiggle theme for T3 Code: squiggle.json + SVG layers.

Every animation period divides 30s, so a 30s recording loops seamlessly.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
INK, BL, PK, YL, MT, OR, LV = "#1b1340", "#2f3cff", "#ff5c9d", "#ffd23f", "#3fdcb4", "#ff8a3d", "#b9a6ff"
CANVAS, LEMON = "#f6f2ff", "#ffee9a"


def data_uri(svg):
    out = svg.replace("%", "%25").replace("#", "%23").replace('"', "'").replace("<", "%3C").replace(">", "%3E")
    return 'url("data:image/svg+xml,' + out + '")'


# ------------------------------------------------------------------ SVG art
# Two renderings of each collage: a calm pastel one for idle (shapes near the reading column are
# washed out further) and a saturated, animated one that is swapped in only while a turn runs.
PAST = {BL: "#c9ceff", PK: "#ffc7dc", YL: "#ffeaa3", MT: "#c5f2e3", OR: "#ffd6b8", LV: "#e2d9ff", INK: "#9a90c8"}
IDLE = False
# every keyframe passes through the rest pose (0%), so the idle<->working handoff does not jump
MOTION = (
    ".b,.s,.r,.w,.g{transform-box:fill-box;transform-origin:center}"
    ".b{animation:b var(--d,5s) ease-in-out infinite}@keyframes b{0%,100%{translate:0}25%{translate:0 -7px}75%{translate:0 7px}}"
    ".s{animation:s var(--d,10s) cubic-bezier(.65,0,.35,1) infinite}@keyframes s{0%{rotate:0}100%{rotate:360deg}}"
    ".r{animation:r var(--d,30s) linear infinite}@keyframes r{0%{rotate:0}100%{rotate:360deg}}"
    ".w{animation:w var(--d,6s) ease-in-out infinite}@keyframes w{0%,100%{rotate:0}25%{rotate:-7deg}75%{rotate:7deg}}"
    ".g{animation:g var(--d,6s) ease-in-out infinite}@keyframes g{0%,100%{rotate:0}25%{rotate:-3deg}75%{rotate:3deg}}"
    "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
)


def pc(col, n=False):
    return PAST.get(col, col) if IDLE else col


def wrap(inner, kind=None, d=None):
    """Nest a shape in a motion group. kind: b bob, s tumble, r spin, w wiggle."""
    if not kind:
        return inner
    return f"<g class='{kind}'" + (f" style='--d:{d}s'" if d else "") + f">{inner}</g>"


def S(w=4, n=False):
    return f"stroke='{pc(INK, n)}' stroke-width='{w}' stroke-linejoin='round'"


def tri(x1, y1, x2, y2, x3, y3, fill, n=False):
    return f"<path d='M{x1} {y1}L{x2} {y2}L{x3} {y3}Z' fill='{pc(fill, n)}' {S(4, n)}/>"


def circ(cx, cy, r, fill, w=4, n=False):
    return f"<circle cx='{cx}' cy='{cy}' r='{r}' fill='{pc(fill, n)}' {S(w, n) if w else ''}/>"


def wave(x, y, n_, col, w, amp=34, seg=40, n=False):
    return (f"<path d='M{x} {y}q{seg/2:g} {-amp} {seg} 0" + f"t{seg} 0" * (n_ - 1) +
            f"' fill='none' stroke='{pc(col, n)}' stroke-width='{w}' stroke-linecap='round'/>")


def zig(x, y, n_, col, w, seg=20, h=24, n=False):
    d = f"M{x} {y}" + "".join(f"l{seg} {-h if i % 2 == 0 else h}" for i in range(n_))
    return f"<path d='{d}' fill='none' stroke='{pc(col, n)}' stroke-width='{w}' stroke-linejoin='miter' stroke-linecap='butt'/>"


def plus(cx, cy, r, col, w=12, n=False):
    return f"<path d='M{cx} {cy-r}v{2*r}M{cx-r} {cy}h{2*r}' stroke='{pc(col, n)}' stroke-width='{w}' fill='none'/>"


def dots(x, y, cols, rows, gap=24, r=5, n=False):
    return "".join(f"<circle cx='{x + i * gap + (gap // 2 if j % 2 else 0)}' cy='{y + j * gap}' r='{r}' fill='{pc(INK, n)}'/>"
                   for j in range(rows) for i in range(cols))


def chip(cx, cy, col, kind=0, s=9):
    col = pc(col, True)
    if kind == 0:
        return f"<rect x='{cx-s}' y='{cy-s/2}' width='{2*s}' height='{s}' rx='2' transform='rotate(25 {cx} {cy})' fill='{col}'/>"
    if kind == 1:
        return f"<path d='M{cx-s} {cy+s*.6}L{cx} {cy-s}L{cx+s} {cy+s*.5}Z' fill='{col}'/>"
    return f"<circle cx='{cx}' cy='{cy}' r='{s*.55}' fill='{col}'/>"


def stripes_def():
    return (f"<defs><pattern id='st' width='12' height='12' patternUnits='userSpaceOnUse' patternTransform='rotate(40)'>"
            f"<rect width='12' height='12' fill='{pc(YL)}'/><rect width='6' height='12' fill='{pc(INK)}'/></pattern></defs>")


def svg(body, w, h, anim, pad=24):
    style = f"<style>{MOTION}</style>" if anim else ""
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='{-pad} {-pad} {w + 2*pad} {h + 2*pad}'>{style}{body}</svg>")


def _mode(anim, sat=False):
    global IDLE
    IDLE = not anim and not sat
    return (lambda inner, *a: wrap(inner, *a)) if anim else (lambda inner, *a: inner)


# Left collage: the reading column sits to its right (x near 300), so "near" shapes are x > ~230.
def art_left(anim, sat=False):
    k = _mode(anim, sat)
    g = [
        k(circ(86, 96, 58, BL) + f"<circle cx='100' cy='110' r='58' fill='none' {S(4)}/>", "b", 5),
        k(tri(200, 200, 246, 270, 154, 270, YL, True), "g", 6),
        k(wave(28, 350, 4, PK, 12) + wave(28, 378, 4, INK, 4), "w", 6),
        dots(40, 440, 5, 3),
        k(f"<path d='M150 600a48 48 0 0 1 96 0z' fill='{pc(MT, True)}' {S(4, True)}/>", "g", 10),
        zig(24, 660, 6, INK, 7),
        k(plus(238, 700, 22, OR, 11, True), "g", 5),
        k(f"<rect x='64' y='690' width='56' height='56' rx='5' transform='rotate(-14 92 718)' fill='{pc(OR)}' {S(4, True)}/>", "s", 10),
    ]
    chips = (chip(40, 190, PK, 0, 10) + chip(150, 320, LV, 1, 10) + chip(268, 440, MT, 2, 12) + chip(140, 540, YL, 0, 9)
             + chip(60, 620, LV, 2, 10) + chip(262, 780, PK, 1, 9))
    return svg(f"{stripes_def()}{chips}{''.join(g)}", 300, 800, anim)


# Right collage: the reading column is to its left (x near 0), so "near" shapes are x < ~70.
def art_right(anim, sat=False):
    k = _mode(anim, sat)
    g = [
        k(f"<path d='M44 150a82 82 0 0 1 164 0z' fill='{pc(PK, True)}' {S(4, True)}/><path d='M68 150a58 58 0 0 1 116 0' fill='none' stroke='{pc(INK, True)}' stroke-width='4'/>", "g", 6),
        zig(24, 250, 10, BL, 9, n=True),
        k(f"<circle cx='120' cy='350' r='48' fill='url(#st)' {S(4, True)}/>", "r", 30),
        k(tri(220, 340, 266, 410, 174, 410, MT), "s", 15),
        k(wave(36, 520, 4, YL, 12, 30, 38, True) + wave(36, 548, 4, INK, 4, 30, 38, True), "g", 5),
        k(plus(66, 640, 24, BL, 11, True), "g", 10),
        k(f"<circle cx='196' cy='660' r='44' fill='none' stroke='{pc(INK)}' stroke-width='7' stroke-dasharray='1 15' stroke-linecap='round'/>", "r", 10),
        f"<rect x='24' y='738' width='46' height='26' rx='13' fill='{pc(PK, True)}' {S(4, True)}/>",
    ]
    chips = (chip(260, 230, MT, 0, 10) + chip(30, 330, YL, 2, 12) + chip(262, 300, PK, 1, 10) + chip(150, 470, OR, 2, 9)
             + chip(250, 560, LV, 0, 10) + chip(130, 760, MT, 1, 10) + chip(268, 770, YL, 0, 9))
    return svg(f"{stripes_def()}{chips}{''.join(g)}", 300, 800, anim)


# Slim collage for mid-width windows (gutters about 100-196px): one column of calm shapes.
def art_slim(anim, flip=False, sat=False):
    k = _mode(anim, sat)
    x = (lambda v: 90 - v) if flip else (lambda v: v)
    g = [
        k(circ(x(42), 56, 30, BL if not flip else PK, 4, True), "b", 5),
        k(tri(x(40), 150, x(70), 200, x(10), 200, YL if not flip else MT, True), "g", 6),
        k(wave(8, 290, 2, PK if not flip else BL, 10, 26, 38, True), "g", 6),
        k(f"<path d='M{x(42) - 28} 410a28 28 0 0 1 56 0z' fill='{pc(MT if not flip else YL, True)}' {S(4, True)}/>", "g", 10),
        k(plus(x(44), 510, 18, OR, 9, True), "s", 10),
        k(f"<rect x='{x(44) - 22}' y='590' width='44' height='44' rx='5' transform='rotate(-14 {x(44)} 612)' fill='{pc(PK if not flip else OR, True)}' {S(4, True)}/>", "s", 10),
        k(circ(x(46), 720, 24, LV, 4, True), "b", 3),
    ]
    return svg("".join(g), 90, 780, anim, pad=16)


# Dock: lives at the sidebar foot, working-only, padded so tumbling shapes never clip.
def art_dock(anim):
    global IDLE
    k = _mode(anim)
    IDLE = True  # the dock is pastel in both states: it can sit near thread text
    g = [
        k(circ(48, 48, 30, BL, 4, True), "b", 5),
        k(tri(150, 24, 184, 76, 116, 76, YL, True), "s", 10),
        k(wave(18, 112, 4, PK, 9, 20, 24, True) + wave(18, 128, 4, INK, 3, 20, 24, True), "w", 6),
        k(f"<path d='M140 156a28 28 0 0 1 56 0z' fill='{pc(MT, True)}' {S(3, True)}/>", "s", 15),
    ]
    return svg("".join(g), 220, 170, anim, pad=20)


def tile_canvas():
    """Terrazzo chips on the canvas, scattered, in tints close to the ground colour."""
    cs = [("#ffd0e2", 0), ("#c5f2e3", 2), ("#ffe58a", 0), ("#d3d0ff", 1), ("#ffd9bd", 2), ("#c5f2e3", 1)]
    pts = [(18, 22), (70, 96), (130, 30), (160, 120), (40, 150), (100, 170), (178, 70), (112, 76)]
    out = "".join(chip(x, y, cs[i % len(cs)][0], cs[i % len(cs)][1], 7) for i, (x, y) in enumerate(pts))
    return f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 190 190'>{out}</svg>"


def tile_side():
    cs = [("#ffc2d6", 0), ("#d6c8ff", 2), ("#ffc9a6", 1), ("#bdeedd", 2)]
    pts = [(7, 22), (7, 62), (7, 104), (7, 144)]
    out = "".join(chip(x, y, cs[i % len(cs)][0], cs[i % len(cs)][1], 5) for i, (x, y) in enumerate(pts))
    return f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 14 170'>{out}</svg>"


def wave_tile(col, w, h, amp, sw):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} {h}'><path d='M0 {h/2}q{w/4} {-amp} {w/2} 0t{w/2} 0' fill='none' stroke='{col}' stroke-width='{sw}'/></svg>")


def corner_dot():
    return f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><circle cx='12' cy='12' r='9' fill='{YL}' stroke='{INK}' stroke-width='3'/></svg>"


def corner_tri():
    return f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><path d='M3 21L12 3l9 18z' fill='{BL}' stroke='{INK}' stroke-width='3' stroke-linejoin='round'/></svg>"


# ------------------------------------------------------------------ colour roles
colors = {
    "canvas": CANVAS, "chrome": LEMON, "toolbar": CANVAS, "toolbarForeground": INK, "toolbarBorder": INK,
    "toolbarControl": "#ffffff", "toolbarControlForeground": INK, "toolbarControlHover": "#ffd9ea",
    "surface": "#fbf9ff", "surfaceRaised": "#ffffff", "surfaceOverlay": "#ffffff",
    "text": INK, "textMuted": "#4f4380", "border": "#d2c9f7", "input": INK, "focus": "#ff2e88",
    "accent": BL, "accentForeground": "#ffffff", "secondary": YL, "secondaryForeground": INK,
    "muted": "#ece6ff", "mutedForeground": "#4f4380", "placeholder": "#6d60a3", "secondaryLabel": "#4f4380",
    "iconMuted": "#5b4f93", "error": "#d1003f", "errorForeground": "#8c0029", "errorSurface": "#ffdbe5",
    "warning": "#b85c00", "warningForeground": "#6e3700", "warningSurface": "#ffe7b3",
    "update": "#007d73", "updateForeground": "#004a44", "updateSurface": "#c9f6ee",
    "accentSurface": "#dde0ff", "accentSurfaceForeground": "#1c24b0",
    "messageSurface": "#ffffff", "messageForeground": INK, "messageAction": INK,
    "messageActionForeground": "#ffffff", "messageActionHover": "#3a2c7a",
    "codeBackground": "#d8f7eb", "codeForeground": INK,
    "searchMatchBackground": "#ffe58a", "searchMatchForeground": INK,
    "searchMatchActiveBackground": "#ff8fbf", "searchMatchActiveForeground": INK,
    "sidebar": LEMON, "sidebarForeground": INK, "sidebarMutedForeground": "#4d3f86",
    "sidebarControlSurface": "#ffffff", "sidebarRowHover": "#ffe066", "sidebarRowActive": "#ffd23f",
    "sidebarRowSelected": "#ff9ec8", "sidebarBorder": INK,
    "terminalBackground": "#fff8d6", "terminalForeground": INK, "terminalCursor": "#ff2e88",
    "terminalSelection": "#cfd4ff", "terminalScrollbar": "#c9bcff", "terminalScrollbarHover": PK,
}

# ------------------------------------------------------------------ CSS
CW = "var(--chat-content-max-width,46rem)"
G = f"(100% - {CW})/2"
BUSY = ('body:has([data-timeline-row-kind="working"])',
        'body:has([data-thread-item] [aria-busy="true"][aria-current]:not([aria-current="false"]))')


def busy(sel):
    return ",".join(f"{b} {sel}" for b in BUSY)


def gutter_w(thr, maxw):
    return f"min({maxw}px,clamp(0px,({G} - {thr}px)*1000,{G} - 36px)) auto"


CONV = '[data-workspace-area="conversation"]'
GW = gutter_w(196, 336)
SGW = gutter_w(104, 96)
DOCK = "left 14px bottom 10px/64px auto no-repeat"
SCRIM = "linear-gradient(rgba(255,238,154,0),rgba(255,238,154,.55) 30%,rgba(255,238,154,.55)) 0 100%/100% 120px no-repeat"
COMPOSER_BUSY = busy('[data-slot="composer-host"]')
LS, RS = "left 12px top 8px", "right 12px top 8px"
PSEUDO_BUSY = ",".join(f"{b} {CONV}{e}" for b in BUSY for e in ("::before", "::after"))
HEAD_TILE = "var(--sq-hw) var(--sq-x) calc(100% + 1px)/28px 10px repeat-x"
SBI = '[data-slot="sidebar-inner"]'
NM = "@media (prefers-reduced-motion:no-preference)"
WORK_BUSY = busy('[data-timeline-row-kind="work"]')
HEAD = "Futura,'Avenir Next','Trebuchet MS',sans-serif"
BODY = "ui-rounded,'SF Pro Rounded','Avenir Next Rounded','Avenir Next',system-ui,sans-serif"

css = (
    ":root{"
    f"--sq-l:{data_uri(art_left(False))};--sq-la:{data_uri(art_left(True))};"
    f"--sq-r:{data_uri(art_right(False))};--sq-ra:{data_uri(art_right(True))};"
    f"--sq-sl:{data_uri(art_slim(False))};--sq-sla:{data_uri(art_slim(True))};"
    f"--sq-sr:{data_uri(art_slim(False, True))};--sq-sra:{data_uri(art_slim(True, True))};"
    f"--sq-ls:{data_uri(art_left(False, True))};--sq-rs:{data_uri(art_right(False, True))};"
    f"--sq-sls:{data_uri(art_slim(False, False, True))};--sq-srs:{data_uri(art_slim(False, True, True))};"
    f"--sq-t:{data_uri(tile_canvas())};--sq-ts:{data_uri(tile_side())};"
    f"--sq-hw:{data_uri(wave_tile(BL, 28, 10, 8, 3))};--sq-bw:{data_uri(wave_tile(PK, 20, 8, 6, 2.5))};"
    f"--sq-cd:{data_uri(corner_dot())};--sq-ct:{data_uri(corner_tri())}}}"
    f"body{{font-family:{BODY}!important}}"
    # confetti ground with the two pastel gutter compositions. The saturated, animated collages live on
    # ::before/::after (gutter-sized) and fade in under busy(); that needs position:relative + isolation
    # on the conversation element so z-index:-1 art stays above its background and below the content.
    f"{CONV}{{position:relative;isolation:isolate;background:var(--sq-l) {LS}/{GW} no-repeat,var(--sq-r) {RS}/{GW} no-repeat,var(--sq-t) 0 0/190px 190px,{CANVAS}!important}}"
    f"{CONV}::before,{CONV}::after{{content:\"\";position:absolute;top:8px;bottom:0;z-index:-1;pointer-events:none;width:min(336px,clamp(0px,({G} - 196px)*1000,{G} - 36px));background-repeat:no-repeat;background-size:100% auto;background-position:0 0;opacity:0;visibility:hidden;transition:opacity .7s ease,visibility 0s .7s}}"
    f"{CONV}::before{{left:12px;background-image:var(--sq-la)}}{CONV}::after{{right:12px;background-image:var(--sq-ra)}}"
    f"{NM}{{{PSEUDO_BUSY}{{opacity:1;visibility:visible;transition:opacity .7s ease,visibility 0s}}}}"
    f"@media (prefers-reduced-motion:reduce){{{CONV}::before,{CONV}::after{{display:none}}}}"
    f"@media (max-width:1459px){{{CONV}{{background:var(--sq-sl) {LS}/{SGW} no-repeat,var(--sq-sr) {RS}/{SGW} no-repeat,var(--sq-t) 0 0/190px 190px,{CANVAS}!important}}"
    f"{CONV}::before,{CONV}::after{{width:min(96px,clamp(0px,({G} - 104px)*1000,{G} - 24px))}}"
    f"{CONV}::before{{background-image:var(--sq-sla)}}{CONV}::after{{background-image:var(--sq-sra)}}}}"
    # once the saturated layer has faded in, drop the pastel twins (no delay on the way back, so pastel is in place first)
    f"{NM}{{{busy(CONV)}{{background-size:0 0,0 0,190px 190px,auto!important;transition:background-size 0s .7s}}}}"
    # reduced motion: working state is a still saturated collage in the margins
    f"@media (prefers-reduced-motion:reduce){{{busy(CONV)}{{background:var(--sq-ls) {LS}/{GW} no-repeat,var(--sq-rs) {RS}/{GW} no-repeat,var(--sq-t) 0 0/190px 190px,{CANVAS}!important}}}}"
    f"@media (prefers-reduced-motion:reduce) and (max-width:1459px){{{busy(CONV)}{{background:var(--sq-sls) {LS}/{SGW} no-repeat,var(--sq-srs) {RS}/{SGW} no-repeat,var(--sq-t) 0 0/190px 190px,{CANVAS}!important}}}}"
    # the reading column: a sheet with inked edges over the confetti
    f"{CONV} .messages-timeline-scroll{{background:"
    f"linear-gradient(rgba(27,19,64,.45) calc(100% - 40px),rgba(27,19,64,0)) calc(50% - {CW}/2 - 16px) 0/2px 100% no-repeat,"
    f"linear-gradient(rgba(27,19,64,.45) calc(100% - 40px),rgba(27,19,64,0)) calc(50% + {CW}/2 + 14px) 0/2px 100% no-repeat,"
    f"linear-gradient(90deg,transparent calc(50% - {CW}/2 - 16px),{CANVAS} calc(50% - {CW}/2 - 16px),{CANVAS} calc(50% + {CW}/2 + 16px),transparent calc(50% + {CW}/2 + 16px))!important}}"
    # header: a squiggle for a bottom border that slides while working
    f"[data-chat-header]{{background:{HEAD_TILE},{CANVAS}!important;border:0!important;transition:background-size .5s cubic-bezier(.3,1.9,.5,1)}}"
    f"{NM}{{{busy('[data-chat-header]')}{{animation:sq-slide 3s steps(14) infinite}}}}"
    "@property --sq-x{syntax:\"<length>\";inherits:false;initial-value:0px}@keyframes sq-slide{to{--sq-x:28px}}"
    # live row + busy threads get a crawling pink squiggle
    "[data-timeline-row-kind=\"working\"],[data-thread-item] [aria-busy=\"true\"]{background-image:var(--sq-bw)!important;background-size:20px 8px!important;background-position:var(--sq-x) 100%!important;background-repeat:repeat-x!important}"
    f"{NM}{{[data-timeline-row-kind=\"working\"],[data-thread-item] [aria-busy=\"true\"]{{animation:sq-crawl 3s steps(10) infinite}}}}"
    "@keyframes sq-crawl{to{--sq-x:20px}}"
    "[data-thread-item] [aria-busy=\"true\"][aria-current]:not([aria-current=\"false\"]){background-size:20px 6px!important;background-position:var(--sq-x) calc(100% - 4px)!important}"
    # sidebar: lemon with terrazzo (no dock: art never sits behind thread text)
    f"[data-slot=\"sidebar\"]{{border-right:3px solid {INK}!important}}"
    f"[data-slot=\"sidebar-inner\"]{{background:var(--sq-ts) left 2px top 0/14px 170px repeat-y,var(--sq-ts) right 2px top 0/14px 170px repeat-y,{LEMON}!important}}"
    # thread rows: hover leans in, the open one is a sticker
    "[data-thread-item]{border-radius:10px!important;transition:translate .2s cubic-bezier(.3,1.6,.5,1)}"
    "[data-thread-item]:hover{translate:4px 0}"
    f"[data-thread-item] [aria-current]:not([aria-current=\"false\"]){{box-shadow:inset 0 0 0 2px {INK},3px 3px 0 {INK}}}"
    "[data-slot=\"project-monogram\"]{border-radius:6px!important;border:1.5px solid " + INK + ";box-shadow:2px 2px 0 " + INK + "}"
    "[data-slot=\"sidebar\"] [data-slot=\"button\"]:not([aria-label]){background-color:#fff!important}"
    # messages
    f"[data-user-message-bubble]{{background:#fff!important;border:2.5px solid {INK}!important;border-radius:18px 18px 4px 18px!important;box-shadow:4px 4px 0 {PK}}}"
    # turn complete: while busy the composer floats on a yellow shadow; when the selector stops matching the
    # base transition springs it back to rest, so the hop plays only on a real end (a transition never runs on mount)
    f"{COMPOSER_BUSY}{{box-shadow:9px 9px 0 {YL}}}"
    f"{NM}{{{COMPOSER_BUSY}{{translate:-5px -8px}}}}"
    f"{NM}{{{busy('[data-chat-header]')}{{background-size:28px 14px,auto!important}}}}"
    f".chat-markdown :is(h1,h2,h3,h4){{font-family:{HEAD};font-weight:800;letter-spacing:.01em;width:fit-content;background:linear-gradient(transparent 62%,{YL} 62%);padding:0 .15em;margin-left:-.15em}}"
    f".chat-markdown a{{color:{BL}!important;text-decoration:underline wavy {PK} 1.5px!important;text-underline-offset:4px}}"
    f".chat-markdown :not(pre)>code{{background:#ffe0ee;color:{INK};border:1.5px solid {INK};padding:.02em .32em;border-radius:6px}}"
    f".chat-markdown-codeblock{{background:#d8f7eb!important;border:2.5px solid {INK}!important;border-radius:12px!important;box-shadow:3px 3px 0 {INK};font-family:ui-monospace,Menlo,monospace}}"
    f".chat-markdown :not(pre)>code{{font-family:ui-monospace,Menlo,monospace}}"
    f".chat-markdown blockquote{{border-left:4px solid {PK}!important;background:#ffe0ee;border-radius:0 10px 10px 0;padding:.3em .9em;color:{INK}}}"
    ".chat-markdown hr{border:0!important;height:10px;background:var(--sq-hw) 0 50%/28px 10px repeat-x!important}"
    f".chat-markdown table{{border-collapse:separate;border-spacing:0;border:2px solid {INK};border-radius:10px}}"
    f".chat-markdown th{{background:{LEMON}!important;color:{INK}!important;border-bottom:2px solid {INK}!important}}"
    ".chat-markdown td{border-color:#d2c9f7!important}"
    ".chat-markdown li::marker{color:#ff2e88;font-weight:800}"
    f"[data-timeline-row-kind=\"work\"]{{border-left:3px solid #3fdcb4;margin-left:-13px;padding-left:10px;transition:border-color .6s}}"
    f"{WORK_BUSY}{{border-left-color:{PK}}}"
    f"[data-thread-details-card]{{border:2.5px solid {INK}!important;border-radius:14px!important;box-shadow:4px 4px 0 {LV}!important;background-color:#fff!important}}"
    f"[data-thread-terminal-drawer]{{border-top:3px solid {INK}!important;box-shadow:0 -4px 0 {PK}}}"
    f"[data-settings-page-scroll]{{background-color:{CANVAS}!important;font-family:{BODY}}}"
    f"[data-settings-page-scroll] :is(h1,h2),[data-chat-header] :is(h1,h2){{font-family:{HEAD}}}"
    f"[data-slot=\"sidebar\"] [data-thread-item]{{font-family:{HEAD};letter-spacing:.01em}}"
    ".composer-tiptap,.composer-tiptap:focus,.composer-tiptap:focus-visible{outline:none!important}"
    # composer: a white card with a hard shadow; focus pops it and unfolds confetti in two corners
    f"[data-slot=\"composer-host\"]{{background:var(--sq-cd) right 14px top -4px/0 0 no-repeat,var(--sq-ct) left 14px bottom -4px/0 0 no-repeat,#fff!important;border:2.5px solid {INK}!important;border-radius:16px!important;box-shadow:5px 5px 0 {MT};translate:0 0;transition:translate .55s cubic-bezier(.3,1.9,.5,1),box-shadow .7s,background-size .3s cubic-bezier(.3,1.6,.5,1)}}"
    f"[data-slot=\"composer-host\"]:focus-within{{box-shadow:8px 8px 0 {PK};translate:-2px -2px;background-size:24px 24px,24px 24px,auto!important}}"
    # controls and overlays
    "svg.lucide{stroke-width:2.3}"
    f"::selection{{background:{YL};color:{INK}}}"
    f"[data-slot=\"dialog-popup\"],[data-slot=\"popover-popup\"],[data-slot=\"menu-popup\"]{{border:2.5px solid {INK}!important;border-radius:14px!important;box-shadow:6px 6px 0 {PK}!important}}"
    f"[data-slot=\"tooltip-popup\"]{{background:{INK}!important;color:#fff!important;border-radius:8px!important}}"
    f"[data-slot=\"input\"],[data-slot=\"select-trigger\"]{{border:2px solid {INK}!important;border-radius:10px!important}}"
    "[data-slot=\"button\"]{border-radius:10px!important;transition:translate .12s,box-shadow .12s}"
    f"[data-slot=\"button\"]:not([aria-label]):not(:is([data-slot=\"composer-host\"],[data-slot=\"menu-popup\"],[data-slot=\"popover-popup\"],[data-slot=\"dialog-popup\"]) *){{border:2px solid {INK}!important;box-shadow:2px 2px 0 {INK}}}"
    f"[data-slot=\"button\"]:not([aria-label]):not(:is([data-slot=\"composer-host\"],[data-slot=\"menu-popup\"],[data-slot=\"popover-popup\"],[data-slot=\"dialog-popup\"]) *):hover{{translate:-1px -1px;box-shadow:3px 3px 0 {INK}}}"
    "[data-slot=\"button\"]:not([aria-label]):not(:is([data-slot=\"composer-host\"],[data-slot=\"menu-popup\"],[data-slot=\"popover-popup\"],[data-slot=\"dialog-popup\"]) *):active{translate:2px 2px;box-shadow:none}"
    "[data-slot=\"button\"][aria-label]:hover{background-color:#ffd9ea!important}"
    "[data-slot=\"button\"]:focus-visible,[data-slot=\"input\"]:focus-visible,[data-slot=\"select-trigger\"]:focus-visible,[data-slot=\"switch\"]:focus-visible{outline:3px solid #ff2e88!important;outline-offset:2px!important}"
    "[data-slot=\"input\"]:focus-visible,[data-slot=\"select-trigger\"]:focus-visible{box-shadow:3px 3px 0 #ff2e88}"
    "::-webkit-scrollbar{width:12px;height:12px}::-webkit-scrollbar-track,[data-slot=\"scroll-area-scrollbar\"]{background:#ece6ff!important}"
    f"::-webkit-scrollbar-thumb,[data-slot=\"scroll-area-thumb\"]{{background:#c9bcff!important;border-radius:99px!important;border:1.5px solid {INK}}}"
    f"::-webkit-scrollbar-thumb:hover{{background:{PK}!important}}"
    "@media (prefers-reduced-motion:reduce){[data-thread-item],[data-slot=\"composer-host\"],[data-slot=\"button\"],[data-message-role],[data-chat-header],[data-timeline-row-kind],[data-thread-item] [aria-busy]{transition:none!important;animation:none!important}}"
)

theme = {"version": 1, "id": "squiggle", "name": "Squiggle", "appearance": "light", "accent": BL, "canvas": CANVAS,
         "colors": colors, "css": css}

out = os.path.join(HERE, "..", "squiggle.json")
with open(out, "w") as fh:
    json.dump(theme, fh, ensure_ascii=False)
print("css chars:", len(css))
os.makedirs(os.path.join(HERE, "..", "assets", "svg"), exist_ok=True)
for n, s in (("left", art_left(True)), ("right", art_right(True)), ("dock", art_dock(True))):
    with open(os.path.join(HERE, "..", "assets", "svg", f"{n}.svg"), "w") as fh:
        fh.write(s)
