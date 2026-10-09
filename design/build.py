#!/usr/bin/env python3
"""Build the profile header SVGs from the Zidos design tokens.

Inputs are vendored next to this script and are not edited by hand:
  tokens.json  colour roles copied from zidos-core app/design-export/tokens.json
  fonts/       Onest and JetBrains Mono subsets from the same export (OFL-1.1)
  done.svg     the "done" status mark, icon set b

Each header is written twice, for the light and the dark pole. The fonts are
subset to the characters each file uses and embedded, because GitHub renders
README images as <img>, which cannot fetch external fonts.

Usage: python3 design/build.py   (needs fonttools and brotli)
Running it twice produces identical files.
"""

import base64
import io
import json
from pathlib import Path
from xml.sax.saxutils import escape

from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
TOKENS = json.loads((ROOT / "tokens.json").read_text())
FONTS = {
    "Onest": ROOT / "fonts" / "Onest-subset.ttf",
    "JB": ROOT / "fonts" / "JetBrainsMono-subset.ttf",
}

W, H = 1200, 400
MONO_ADVANCE = 0.6  # JetBrains Mono advance width, in em

HEADERS = {
    "personal": {
        "out": REPO / "assets",
        "title": "Sergei Ivanov, systems architect",
        "desc": "Systems architect working on distributed platforms, middleware "
        "and governed AI execution, building the Zidos agent runtime.",
        "label": "SYSTEMS ARCHITECT",
        "name": "Sergei Ivanov",
        "lines": [
            [("Distributed platforms, middleware", "ink-2")],
            [("and governed AI execution.", "ink-2")],
            [("Building ", "ink-2"), ("Zidos", "accent"), (".", "ink-2")],
        ],
        "log_title": "run 7f3a · event log",
        "log": [
            ("041", "inv.dispatched", "configure · apply"),
            ("042", "inv.result", "read back"),
            ("043", "finish.claimed", "“it works”"),
            ("044", "verify.verdict", "real client path → pass"),
            ("045", "run.succeeded", "evidence recorded"),
        ],
    },
    "org": {
        "out": REPO / "zidos-dev" / "profile" / "assets",
        "title": "Zidos, an agent runtime with provable execution",
        "desc": "Zidos runs agent tasks as durable objects with an append-only "
        "event log; completion is decided by a verifier the runtime executes.",
        "label": "AGENT RUNTIME · PRE-1.0",
        "name": "Zidos",
        "lines": [
            [("An agent runtime with", "ink-2")],
            [("provable execution.", "ink-2")],
            [("Durable runs · runtime authority · verified completion", "ink-3")],
        ],
        "log_title": "run 7f3a · event log",
        "log": [
            ("01", "run.created", "objective · budgets fixed"),
            ("02", "inv.dispatched", "file_edit · key 9f3c…"),
            ("03", "inv.result", "committed"),
            ("04", "finish.claimed", "the model says done"),
            ("05", "verify.verdict", "go test ./... → pass"),
            ("06", "run.succeeded", "decided by the gate"),
        ],
    },
}


def font_face(family, path, text):
    font = TTFont(path, recalcTimestamp=False)
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["*"]
    opts.name_IDs = ["*"]
    opts.notdef_outline = True
    sub = subset.Subsetter(opts)
    sub.populate(text=text)
    sub.subset(font)
    buf = io.BytesIO()
    font.flavor = "woff2"
    font.save(buf)
    data = base64.b64encode(buf.getvalue()).decode()
    return (
        f'@font-face{{font-family:"{family}";font-weight:100 900;'
        f'src:url(data:font/woff2;base64,{data}) format("woff2")}}'
    )


def text(x, y, s, family, size, weight, role, extra=""):
    return (
        f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
        f'font-weight="{weight}" fill="var(--{role})"{extra}>{escape(s)}</text>'
    )


def tspans(x, y, parts, size, weight):
    inner = "".join(
        f'<tspan fill="var(--{role})">{escape(s)}</tspan>' for s, role in parts
    )
    return (
        f'<text x="{x}" y="{y}" font-family="Onest" font-size="{size}" '
        f'font-weight="{weight}">{inner}</text>'
    )


def done_mark(x, y, size):
    # icon set b "done": circle r6 and a tick, on a 16-unit grid
    k = size / 16
    return (
        f'<g transform="translate({x} {y}) scale({k})" fill="none" '
        f'stroke="var(--ok)" stroke-width="1.5" stroke-linecap="round" '
        f'stroke-linejoin="round"><circle cx="8" cy="8" r="6"/>'
        f'<path d="M5.2 8.2 L7.1 10 L10.8 6.2"/></g>'
    )


def build(spec, mode):
    t = TOKENS[mode]
    roles = ";".join(f"--{k}:{v}" for k, v in t.items())

    # ── left column: label, name, three lines ──
    left = [
        text(64, 104, spec["label"], "JB", 15, 500, "ink-3", ' letter-spacing="1.8"'),
        text(60, 186, spec["name"], "Onest", 68, 600, "ink", ' letter-spacing="-1.4"'),
    ]
    for i, parts in enumerate(spec["lines"]):
        size = 24 if i < 2 else 19
        y = 240 + i * 34 + (10 if i == 2 else 0)
        left.append(tspans(64, y, parts, size, 400))

    # ── right: the event log card ──
    fs, row_h = 16, 34
    seq_w = max(len(r[0]) for r in spec["log"]) + 2
    ev_w = max(len(r[1]) for r in spec["log"]) + 2
    det_w = max(len(r[2]) for r in spec["log"])
    adv = fs * MONO_ADVANCE
    card_w = round(28 * 2 + (seq_w + ev_w + det_w) * adv + 28)
    card_h = 58 + row_h * len(spec["log"]) + 14
    cx, cy = W - 64 - card_w, (H - card_h) // 2

    card = []
    if mode == "light":
        card.append(
            f'<rect x="{cx}" y="{cy}" width="{card_w}" height="{card_h}" rx="13" '
            f'fill="var(--surface)" filter="url(#lift)"/>'
        )
    else:
        # dark pole: no shadows; lift is a light top edge (zidos tokens §5.2)
        card.append(
            f'<rect x="{cx}" y="{cy}" width="{card_w}" height="{card_h}" rx="13" fill="var(--edge-lift)"/>'
            f'<rect x="{cx}" y="{cy + 1}" width="{card_w}" height="{card_h - 1}" rx="13" fill="var(--surface)"/>'
        )
    card.append(text(cx + 28, cy + 38, spec["log_title"], "JB", 14, 500, "ink-3"))
    card.append(
        f'<rect x="{cx + 28}" y="{cy + 54}" width="{card_w - 56}" height="1" fill="var(--hairline)"/>'
    )
    for i, (seq, ev, det) in enumerate(spec["log"]):
        y = cy + 58 + row_h * i + 24
        last = i == len(spec["log"]) - 1
        claimed = ev == "finish.claimed"
        x0 = cx + 28
        card.append(text(x0, y, seq, "JB", fs, 400, "ink-3"))
        card.append(
            text(x0 + seq_w * adv, y, ev, "JB", fs, 600 if last else 500,
                 "ok" if last else ("awaiting" if claimed else "ink"))
        )
        card.append(text(x0 + (seq_w + ev_w) * adv, y, det, "JB", fs, 400, "ink-2"))
        if last:
            card.append(done_mark(cx + card_w - 28 - 18, y - 14, 18))

    # ── narrow variant: no card, larger type ──
    narrow = [
        text(64, 118, spec["label"], "JB", 30, 500, "ink-3", ' letter-spacing="2.4"'),
        text(58, 236, spec["name"], "Onest", 112, 600, "ink", ' letter-spacing="-2.4"'),
        tspans(64, 312, spec["lines"][0], 40, 400),
        tspans(64, 362, spec["lines"][1], 40, 400),
    ]

    used_onest = spec["name"] + "".join(s for l in spec["lines"] for s, _ in l)
    used_jb = spec["label"] + spec["log_title"] + "".join("".join(r) for r in spec["log"])

    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
            f'<title id="title">{escape(spec["title"])}</title>',
            f'<desc id="desc">{escape(spec["desc"])}</desc>',
            "<style>",
            font_face("Onest", FONTS["Onest"], used_onest),
            font_face("JB", FONTS["JB"], used_jb),
            f"svg{{{roles}}}",
            ".narrow{display:none}",
            "@media (max-width:600px){.wide{display:none}.narrow{display:inline}}",
            "</style>",
            "<defs>",
            '<filter id="lift" x="-10%" y="-10%" width="120%" height="130%">'
            '<feDropShadow dx="0" dy="8" stdDeviation="4" flood-color="#000" flood-opacity=".075"/></filter>',
            "</defs>",
            # module tile with a directional hairline: sides and bottom, no top edge
            f'<rect width="{W}" height="{H}" rx="20" fill="var(--edge)"/>',
            f'<rect x="1" width="{W - 2}" height="{H - 1}" rx="19" fill="var(--module)"/>',
            '<g class="wide">',
            *left,
            *card,
            "</g>",
            '<g class="narrow">',
            *narrow,
            "</g>",
            "</svg>",
            "",
        ]
    )


def main():
    for key, spec in HEADERS.items():
        spec["out"].mkdir(parents=True, exist_ok=True)
        for mode in ("light", "dark"):
            path = spec["out"] / f"header-{mode}.svg"
            path.write_text(build(spec, mode))
            print(f"{path.relative_to(REPO)}  {path.stat().st_size // 1024} KiB")


if __name__ == "__main__":
    main()
