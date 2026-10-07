"""Generate the animated SVG cards used in the profile README.

The look follows https://asayed18.top: black canvas, white type, grey accents,
a spinning ring around the avatar and a night-city career journey.

Run with: uv run python assets/build_cards.py
"""

import base64
import random
from datetime import date
from html import escape
from pathlib import Path

OUT = Path(__file__).parent
FONT = "system-ui,-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

BG = "#000"
FG = "#fff"
MUTED = "#a1a1aa"
DIM = "#52525b"
LINE = "#27272a"
PILL = "#18181b"

REDUCED_MOTION = "@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }"

# Same data as the journey on asayed18.top.
EXPERIENCE = [
    ("Link Datacenter", "Cloud-Solutions Engineer", "Feb 2018", "Feb 2019"),
    ("Seedstars", "Full-Stack Engineer", "Feb 2019", "Mar 2020"),
    ("Huawei", "Senior Full-Stack Engineer", "Mar 2020", "Jul 2021"),
    ("Amazon", "Senior Software Engineer", "Jul 2021", "Sep 2022"),
    ("Babbel", "Senior Software Engineer", "Sep 2022", "Present"),
]

PROJECTS = [
    {
        "file": "card-awsf.svg",
        "icon": "🔍",
        "title": "AWSF",
        "subtitle": "AWS Fuzzy Finder",
        "desc": ["Keyboard-driven fuzzy search across Lambda,", "S3, SQS, DynamoDB, RDS, Kinesis & API Gateway."],
        "tags": ["Python", "AWS", "fzf"],
    },
    {
        "file": "card-icop.svg",
        "icon": "🛡️",
        "logo": "logo-icop.png",  # from asayed18/icop assets/branding
        "title": "ICOP",
        "subtitle": "AI Content Filter for VLC",
        "desc": ["Privacy-first local AI video filtering with", "ONNX Runtime on Windows and Linux."],
        "tags": ["C/C++", "ONNX", "Vision"],
    },
    {
        "file": "card-tynamo.svg",
        "icon": "⚡",
        "title": "Tynamo",
        "subtitle": "DynamoDB Client Library",
        "desc": ["Simple TypeScript interface for DynamoDB:", "nested attributes, batch ops, local dev."],
        "tags": ["TypeScript", "DynamoDB", "npm"],
    },
    {
        "file": "card-portfolio.svg",
        "icon": "🌐",
        "title": "Portfolio",
        "subtitle": "asayed18.top",
        "desc": ["Scroll through my career as a 3D night", "city, one building per company."],
        "tags": ["Three.js", "React", "Journey"],
    },
]

MONTHS = {m: i for i, m in enumerate("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split())}


def months_between(start: str, end: str) -> int:
    def parse(s: str) -> tuple[int, int]:
        if s == "Present":
            today = date.today()
            return today.year, today.month - 1
        m, y = s.split()
        return int(y), MONTHS[m]

    (y1, m1), (y2, m2) = parse(start), parse(end)
    return max((y2 - y1) * 12 + (m2 - m1), 1)


def pill(x: float, y: float, label: str) -> tuple[str, float]:
    w = 16 + len(label) * 6.6
    svg = (
        f'<g transform="translate({x:.1f},{y})">'
        f'<rect width="{w:.1f}" height="22" rx="6" fill="{PILL}" stroke="{LINE}"/>'
        f'<text x="{w / 2:.1f}" y="15" text-anchor="middle" class="pill">{escape(label)}</text></g>'
    )
    return svg, w


def hero() -> str:
    w, h = 840, 330
    cx, cy, r = w / 2, 108, 62
    rng = random.Random(7)
    avatar = base64.b64encode((OUT / "avatar.jpg").read_bytes()).decode()
    stars = "".join(
        f'<circle cx="{rng.uniform(10, w - 10):.0f}" cy="{rng.uniform(10, h - 40):.0f}" '
        f'r="{rng.choice([0.6, 0.8, 1.1]):.1f}" fill="{FG}" class="star" '
        f'style="animation-delay:{rng.uniform(0, 4):.2f}s"/>'
        for _ in range(55)
    )
    circ = 2 * 3.14159 * (r + 9)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs>
    <clipPath id="av"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>
    <radialGradient id="halo"><stop offset="0" stop-color="{FG}" stop-opacity=".10"/><stop offset="1" stop-color="{FG}" stop-opacity="0"/></radialGradient>
  </defs>
  <style>
    .name {{ font: 700 34px {FONT}; fill: {FG}; letter-spacing: -.5px; }}
    .tag {{ font: 400 15px {FONT}; fill: {MUTED}; }}
    .hint {{ font: 500 11px {FONT}; fill: {DIM}; letter-spacing: 2px; }}
    .ring {{ transform-origin: {cx}px {cy}px; animation: spin 6s linear infinite; }}
    .ring2 {{ transform-origin: {cx}px {cy}px; animation: spin 10s linear infinite reverse; }}
    .star {{ animation: twinkle 4s ease-in-out infinite; }}
    .chev {{ animation: bounce 2s ease-in-out infinite; }}
    .up {{ animation: up .9s ease-out both; }}
    .d1 {{ animation-delay: .25s; }} .d2 {{ animation-delay: .5s; }}
    @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
    @keyframes twinkle {{ 0%,100% {{ opacity: .15; }} 50% {{ opacity: .8; }} }}
    @keyframes bounce {{ 0%,100% {{ transform: translateY(0); opacity: .4; }} 50% {{ transform: translateY(6px); opacity: 1; }} }}
    @keyframes up {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: none; }} }}
    {REDUCED_MOTION}
  </style>
  <rect width="{w}" height="{h}" rx="16" fill="{BG}"/>
  {stars}
  <circle cx="{cx}" cy="{cy}" r="{r + 40}" fill="url(#halo)"/>
  <image href="data:image/jpeg;base64,{avatar}" x="{cx - r}" y="{cy - r}" width="{2 * r}" height="{2 * r}" clip-path="url(#av)" preserveAspectRatio="xMidYMid slice"/>
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{DIM}" stroke-width="1.5"/>
  <circle class="ring" cx="{cx}" cy="{cy}" r="{r + 9}" fill="none" stroke="{FG}" stroke-width="2.5" stroke-linecap="round" stroke-dasharray="{circ * 0.28:.1f} {circ:.1f}"/>
  <circle class="ring2" cx="{cx}" cy="{cy}" r="{r + 15}" fill="none" stroke="{MUTED}" stroke-width="1" stroke-linecap="round" stroke-dasharray="{circ * 0.12:.1f} {circ * 0.5:.1f}"/>
  <text class="name up" x="{cx}" y="{cy + r + 52}" text-anchor="middle">Ahmed Sayed</text>
  <text class="tag up d1" x="{cx}" y="{cy + r + 80}" text-anchor="middle" xml:space="preserve">Software Engineer  |  AI Enthusiast  |  ex-Amazon  |  ex-Huawei</text>
  <g class="up d2"><text class="hint" x="{cx}" y="{h - 26}" text-anchor="middle">SCROLL TO JOURNEY FORWARD</text>
    <path class="chev" d="M{cx - 6} {h - 16} l6 6 l6 -6" fill="none" stroke="{DIM}" stroke-width="1.5" stroke-linecap="round"/></g>
</svg>
"""


def journey() -> str:
    """Night skyline: one building per company, height grows with tenure (like the site)."""
    w, h = 840, 400
    ground = 300
    slot = w / len(EXPERIENCE)
    rng = random.Random(18)
    parts = []
    x = 0
    while x < w:  # background skyline silhouettes
        bw = rng.randint(26, 60)
        bh = rng.randint(30, 110)
        parts.append(f'<rect x="{x}" y="{ground - bh}" width="{bw}" height="{bh}" fill="#0b0b0d"/>')
        x += bw + rng.randint(0, 6)
    for i, (company, title, start, end) in enumerate(EXPERIENCE):
        months = months_between(start, end)
        units = 4 + (min(max(months, 6), 48) - 6) / 42 * 12  # same formula as the site
        bh = units * 11
        bw = 92
        bx = slot * i + (slot - bw) / 2
        by = ground - bh
        current = end == "Present"
        delay = 0.4 + i * 0.45
        win = []
        rows = int((bh - 18) // 20)
        for r in range(rows):
            for c in range(4):
                wx = bx + 12 + c * 19
                wy = by + 14 + r * 20
                if rng.random() < (0.55 if current else 0.35):
                    win.append(
                        f'<rect x="{wx:.1f}" y="{wy:.1f}" width="11" height="13" rx="1" fill="{FG}" class="lit" '
                        f'style="animation-delay:{rng.uniform(0, 6):.2f}s"/>'
                    )
                else:
                    win.append(f'<rect x="{wx:.1f}" y="{wy:.1f}" width="11" height="13" rx="1" fill="#1c1c1f"/>')
        sign_w = max(len(company) * 8.2 + 20, 70)
        sx = bx + bw / 2 - sign_w / 2
        beacon = (
            f'<circle cx="{bx + bw / 2}" cy="{by - 42}" r="4" fill="{FG}" class="beacon"/>'
            f'<circle cx="{bx + bw / 2}" cy="{by - 42}" r="4" fill="none" stroke="{FG}" class="ping"/>'
            if current
            else ""
        )
        parts.append(
            f'<g class="rise" style="animation-delay:{delay:.2f}s">'
            f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="#121214" stroke="{LINE}"/>'
            f"{''.join(win)}"
            f'<line x1="{bx + bw / 2}" y1="{by}" x2="{bx + bw / 2}" y2="{by - 8}" stroke="{DIM}"/>'
            f'<rect x="{sx:.1f}" y="{by - 30}" width="{sign_w:.1f}" height="22" rx="3" fill="#1c1c1f" stroke="{DIM}"/>'
            f'<text x="{bx + bw / 2}" y="{by - 15}" text-anchor="middle" class="sign">{escape(company)}</text>'
            f"{beacon}</g>"
            f'<g class="up" style="animation-delay:{delay + 0.3:.2f}s">'
            f'<text x="{bx + bw / 2}" y="{ground + 40}" text-anchor="middle" class="role">{escape(title)}</text>'
            f'<text x="{bx + bw / 2}" y="{ground + 58}" text-anchor="middle" class="period">{start} – {end}</text></g>'
        )
    stars = "".join(
        f'<circle cx="{rng.uniform(8, w - 8):.0f}" cy="{rng.uniform(50, 130):.0f}" r="{rng.choice([0.6, 0.9]):.1f}" '
        f'fill="{FG}" class="star" style="animation-delay:{rng.uniform(0, 4):.2f}s"/>'
        for _ in range(45)
    )
    start_x, end_x = slot / 2, slot * (len(EXPERIENCE) - 0.5)
    travel = end_x - start_x
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000"/><stop offset="1" stop-color="#0d0d10"/></linearGradient>
    <radialGradient id="glow"><stop offset="0" stop-color="{FG}" stop-opacity=".9"/><stop offset="1" stop-color="{FG}" stop-opacity="0"/></radialGradient>
  </defs>
  <style>
    .title {{ font: 600 13px {FONT}; fill: {MUTED}; letter-spacing: 3px; }}
    .sign {{ font: 700 12px {FONT}; fill: {FG}; }}
    .role {{ font: 600 12px {FONT}; fill: {FG}; }}
    .period {{ font: 400 11px {FONT}; fill: {MUTED}; }}
    .lit {{ animation: flicker 6s ease-in-out infinite; }}
    .star {{ animation: twinkle 4s ease-in-out infinite; }}
    .rise {{ animation: rise .9s cubic-bezier(.2,.8,.2,1) both; }}
    .up {{ animation: fade .8s ease-out both; }}
    .beacon {{ animation: blink 1.6s ease-in-out infinite; }}
    .ping {{ transform-box: fill-box; transform-origin: center; animation: ping 1.6s ease-out infinite; }}
    .car {{ animation: drive 7s cubic-bezier(.45,0,.2,1) infinite; }}
    @keyframes flicker {{ 0%,100% {{ opacity: .95; }} 40% {{ opacity: .55; }} 45% {{ opacity: .15; }} 55% {{ opacity: .85; }} }}
    @keyframes twinkle {{ 0%,100% {{ opacity: .15; }} 50% {{ opacity: .8; }} }}
    @keyframes rise {{ from {{ opacity: 0; transform: translateY(30px); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes fade {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
    @keyframes blink {{ 50% {{ opacity: .3; }} }}
    @keyframes ping {{ from {{ transform: scale(1); opacity: .8; }} to {{ transform: scale(4); opacity: 0; }} }}
    @keyframes drive {{ 0% {{ transform: translateX(0); opacity: 0; }} 8% {{ opacity: 1; }} 85% {{ transform: translateX({travel:.0f}px); opacity: 1; }} 100% {{ transform: translateX({travel:.0f}px); opacity: 0; }} }}
    {REDUCED_MOTION}
  </style>
  <rect width="{w}" height="{h}" rx="16" fill="url(#sky)"/>
  {stars}
  <text x="28" y="38" class="title">THE JOURNEY</text>
  <circle cx="{w * 0.55:.0f}" cy="58" r="18" fill="#e4e4e7" opacity=".9"/><circle cx="{w * 0.55 + 8:.0f}" cy="52" r="16" fill="#000"/>
  {"".join(parts)}
  <rect x="0" y="{ground}" width="{w}" height="2" fill="{LINE}"/>
  <line x1="{start_x}" y1="{ground + 14}" x2="{end_x}" y2="{ground + 14}" stroke="{DIM}" stroke-dasharray="6 8"/>
  <g class="car"><circle cx="{start_x}" cy="{ground + 14}" r="14" fill="url(#glow)" opacity=".5"/><circle cx="{start_x}" cy="{ground + 14}" r="3.5" fill="{FG}"/></g>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="15" fill="none" stroke="{LINE}"/>
</svg>
"""


def project_card(p: dict) -> str:
    w, h = 420, 170
    tags, x = [], 24.0
    for t in p["tags"]:
        svg, tw = pill(x, 128, t)
        tags.append(svg)
        x += tw + 8
    desc = "".join(
        f'<text x="24" y="{92 + i * 18}" class="desc">{escape(line)}</text>' for i, line in enumerate(p["desc"])
    )
    per = 2 * (w + h - 8)
    if "logo" in p:
        data = base64.b64encode((OUT / p["logo"]).read_bytes()).decode()
        icon = f'<image href="data:image/png;base64,{data}" x="350" y="26" width="36" height="36"/>'
    else:
        icon = f'<text x="368" y="53" text-anchor="middle" class="icon">{p["icon"]}</text>'
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs>
    <linearGradient id="shine" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{FG}" stop-opacity="0"/><stop offset=".5" stop-color="{FG}" stop-opacity=".06"/><stop offset="1" stop-color="{FG}" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="clip"><rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14"/></clipPath>
  </defs>
  <style>
    .title {{ font: 700 22px {FONT}; fill: {FG}; }}
    .sub {{ font: 500 13px {FONT}; fill: {MUTED}; }}
    .desc {{ font: 400 13px {FONT}; fill: {MUTED}; }}
    .pill {{ font: 500 11px {FONT}; fill: {MUTED}; }}
    .icon {{ font: 26px {FONT}; filter: grayscale(1); }}
    .trace {{ stroke-dasharray: 90 {per - 90}; animation: trace 5s linear infinite; }}
    .shine {{ animation: sweep 5s ease-in-out infinite; }}
    .ring {{ transform-origin: 368px 44px; animation: spin 6s linear infinite; }}
    .up {{ animation: up .8s ease-out both; }}
    .d1 {{ animation-delay: .1s; }} .d2 {{ animation-delay: .35s; }} .d3 {{ animation-delay: .6s; }}
    @keyframes trace {{ to {{ stroke-dashoffset: -{per}; }} }}
    @keyframes sweep {{ 0% {{ transform: translateX(-{w}px); }} 60%,100% {{ transform: translateX({w}px); }} }}
    @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
    @keyframes up {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: none; }} }}
    {REDUCED_MOTION}
  </style>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="{BG}"/>
  <g clip-path="url(#clip)"><rect class="shine" width="{w}" height="{h}" fill="url(#shine)"/></g>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="none" stroke="{LINE}" stroke-width="1.5"/>
  <rect class="trace" x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="none" stroke="{FG}" stroke-width="1.5" stroke-linecap="round"/>
  <circle cx="368" cy="44" r="24" fill="#0e0e10" stroke="{LINE}"/>
  <circle class="ring" cx="368" cy="44" r="28" fill="none" stroke="{MUTED}" stroke-width="1.5" stroke-linecap="round" stroke-dasharray="40 200"/>
  {icon}
  <g class="up d1"><text x="24" y="42" class="title">{escape(p["title"])}</text><text x="24" y="64" class="sub">{escape(p["subtitle"])}</text></g>
  <g class="up d2">{desc}</g>
  <g class="up d3">{"".join(tags)}</g>
</svg>
"""


TERMINAL_LINES = [
    ("cmd", "whoami"),
    ("out", "Ahmed Sayed · Sr. Software Engineer · Berlin"),
    ("cmd", "cat impact.txt"),
    ("out", "130M+ CRM profiles at sub-second latency   (Babbel)"),
    ("out", "35% faster APIs for 10M+ user profiles     (Amazon)"),
    ("out", "Data pipelines over 100M+ records          (Huawei)"),
    ("cmd", "ls focus/"),
    ("out", "ai-products/  backend/  platform-tooling/  aws/"),
    ("cmd", "echo $LEARNING"),
    ("out", "Rust · local AI systems"),
]


def terminal() -> str:
    w = 840
    step, lh, top = 0.7, 23, 72
    h = top + len(TERMINAL_LINES) * lh + 16
    rows = []
    for i, (kind, text) in enumerate(TERMINAL_LINES):
        y = top + i * lh
        body = (
            f'<tspan class="p">➜</tspan> <tspan class="dir">~</tspan> <tspan class="cmd">{escape(text)}</tspan>'
            if kind == "cmd"
            else f'<tspan class="out">{escape(text)}</tspan>'
        )
        rows.append(
            f'<text x="28" y="{y}" class="line" style="animation-delay:{i * step:.2f}s" xml:space="preserve">{body}</text>'
        )
    cy = top + len(TERMINAL_LINES) * lh
    rows.append(
        f'<g class="line" style="animation-delay:{len(TERMINAL_LINES) * step:.2f}s"><text x="28" y="{cy}">'
        f'<tspan class="p">➜</tspan> <tspan class="dir">~</tspan></text>'
        f'<rect class="cursor" x="62" y="{cy - 13}" width="9" height="16" fill="{FG}"/></g>'
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <style>
    text {{ font: 14px {MONO}; }}
    .p {{ fill: {FG}; }} .dir {{ fill: {MUTED}; }} .cmd {{ fill: {FG}; font-weight: 600; }} .out {{ fill: {MUTED}; }}
    .ttl {{ font: 500 12px {FONT}; fill: {DIM}; }}
    .line {{ animation: show .35s ease-out both; }}
    .cursor {{ animation: blink 1s steps(1) infinite; }}
    @keyframes show {{ from {{ opacity: 0; transform: translateX(-6px); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    {REDUCED_MOTION}
  </style>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="12" fill="{BG}" stroke="{LINE}"/>
  <path d="M1 13 a12 12 0 0 1 12 -12 h{w - 26} a12 12 0 0 1 12 12 v24 h-{w - 2} z" fill="#0e0e10"/>
  <line x1="1" y1="37" x2="{w - 1}" y2="37" stroke="{LINE}"/>
  <circle cx="24" cy="19" r="6" fill="#3f3f46"/><circle cx="44" cy="19" r="6" fill="#3f3f46"/><circle cx="64" cy="19" r="6" fill="#3f3f46"/>
  <text x="{w / 2}" y="23" text-anchor="middle" class="ttl">ahmed@berlin — zsh</text>
  {"".join(rows)}
</svg>
"""


if __name__ == "__main__":
    (OUT / "hero.svg").write_text(hero())
    (OUT / "journey.svg").write_text(journey())
    (OUT / "terminal.svg").write_text(terminal())
    for p in PROJECTS:
        (OUT / p["file"]).write_text(project_card(p))
    print("wrote", len(PROJECTS) + 3, "cards")
