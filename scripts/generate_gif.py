import os
from PIL import Image, ImageDraw, ImageFont

WIDTH = 850
HEIGHT = 280
BG_COLOR = (8, 9, 13)
TEXT_WHITE = (240, 242, 248)
TEXT_MUTED = (100, 108, 128)
TEXT_RED = (255, 0, 51)
TEXT_DARK_RED = (180, 0, 36)
TEXT_CYAN = (0, 245, 212)
BORDER_COLOR = (28, 32, 46)

FONT_PATH = "/usr/share/fonts/TTF/JetBrainsMonoNerdFontMono-Bold.ttf"
font_title = ImageFont.truetype(FONT_PATH, 26)
font_mono = ImageFont.truetype(FONT_PATH, 12)
font_small = ImageFont.truetype(FONT_PATH, 10)

SCISSOR_FRAMES = [
    # Frame 0: Wide open
    [
        r"      \             /      ",
        r"       \           /       ",
        r"        \         /        ",
        r"         \   _   /         ",
        r"          \ / \ /          ",
        r"           \   /           ",
        r"            \ /            ",
        r"             X             ",
        r"            / \            ",
        r"           /   \           ",
        r"          (     )          ",
        r"           \___/           ",
        r"                           ",
    ],
    # Frame 1: Moving inward
    [
        r"        \         /        ",
        r"         \       /         ",
        r"          \     /          ",
        r"           \ _ /           ",
        r"            \ /            ",
        r"             X             ",
        r"            / \            ",
        r"           /   \           ",
        r"          (     )          ",
        r"           \___/           ",
        r"                           ",
        r"                           ",
        r"                           ",
    ],
    # Frame 2: Closing fast
    [
        r"          \     /          ",
        r"           \   /           ",
        r"            \ /            ",
        r"             X             ",
        r"            / \            ",
        r"           /   \           ",
        r"          (     )          ",
        r"           \___/           ",
        r"                           ",
        r"                           ",
        r"                           ",
        r"                           ",
        r"                           ",
    ],
    # Frame 3: * SNIP * CLOSED IMPACT
    [
        r"             |             ",
        r"             |   .  *  .   ",
        r"             |  * SNIP! *  ",
        r"            -X-  *  .  *   ",
        r"            / \            ",
        r"           /   \           ",
        r"          (     )          ",
        r"           \___/           ",
        r"                           ",
        r"                           ",
        r"                           ",
        r"                           ",
        r"                           ",
    ],
    # Frame 4: Sparks flying
    [
        r"             |    +  .     ",
        r"             |  . *  +     ",
        r"            -X-   +  ·     ",
        r"            / \            ",
        r"           /   \           ",
        r"          (     )          ",
        r"           \___/           ",
        r"                           ",
        r"                           ",
        r"                           ",
        r"                           ",
        r"                           ",
        r"                           ",
    ],
    # Frame 5: Re-opening recoil
    [
        r"          \     /          ",
        r"           \   /           ",
        r"            \ /            ",
        r"             X     ·       ",
        r"            / \            ",
        r"           /   \           ",
        r"          (     )          ",
        r"           \___/           ",
        r"                           ",
        r"                           ",
        r"                           ",
        r"                           ",
        r"                           ",
    ],
    # Frame 6: Half-open
    [
        r"        \         /        ",
        r"         \       /         ",
        r"          \  _  /          ",
        r"           \ / \           ",
        r"            \ /            ",
        r"             X             ",
        r"            / \            ",
        r"           /   \           ",
        r"          (     )          ",
        r"           \___/           ",
        r"                           ",
        r"                           ",
        r"                           ",
    ],
    # Frame 7: Fully open ready
    [
        r"      \             /      ",
        r"       \           /       ",
        r"        \    _    /        ",
        r"         \  / \  /         ",
        r"          \/   \/          ",
        r"           \   /           ",
        r"            \ /            ",
        r"             X             ",
        r"            / \            ",
        r"           /   \           ",
        r"          (     )          ",
        r"           \___/           ",
        r"                           ",
    ],
]

images = []
num_frames = 16

for i in range(num_frames):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # 1. Outer Frame Border
    draw.rectangle([10, 10, WIDTH - 11, HEIGHT - 11], outline=BORDER_COLOR, width=1)
    draw.rectangle([13, 13, WIDTH - 14, HEIGHT - 14], outline=(16, 18, 26), width=1)

    # 2. Top Header Bar
    hazard_text = "/// THE PIT // SECTOR 07 // THE CLEANERS // JINKI: THE RIPPER ///"
    draw.text((24, 20), hazard_text, font=font_small, fill=TEXT_MUTED)
    draw.text((WIDTH - 150, 20), "STATUS: ACTIVE ✂", font=font_small, fill=TEXT_RED)
    draw.line([(24, 36), (WIDTH - 25, 36)], fill=BORDER_COLOR, width=1)

    # 3. Left Column: Scissor Box
    frame_idx = i % len(SCISSOR_FRAMES)
    scissor_lines = SCISSOR_FRAMES[frame_idx]

    draw.rectangle([24, 46, 250, 252], fill=(10, 12, 17), outline=BORDER_COLOR, width=1)
    draw.text((34, 54), "[ JINKI // SCISSORS ]", font=font_small, fill=TEXT_MUTED)

    sy = 74
    for line in scissor_lines:
        c = TEXT_RED if ("SNIP" in line or "X" in line or "-X-" in line) else TEXT_WHITE
        draw.text((32, sy), line, font=font_mono, fill=c)
        sy += 13

    # 4. Right Column: Hero Title & Dossier
    rx = 270
    draw.text((rx, 46), "RIYO REAPER", font=font_title, fill=TEXT_WHITE)
    draw.text((rx + 200, 56), "[THE CLEANERS // GIVER]", font=font_mono, fill=TEXT_RED)
    draw.line([(rx, 80), (WIDTH - 25, 80)], fill=(20, 23, 34), width=1)

    dossier = [
        ("OPERATIVE", "Riyo (Reei-dp)", TEXT_RED),
        ("ROLE", "Full-Stack Engineer // Automations & Systems", TEXT_WHITE),
        ("ARSENAL", "Go • Python • TypeScript • Docker • Linux", TEXT_CYAN),
        ("SPECIALTY", "High-Load Bot Architectures & Scalable APIs", TEXT_WHITE),
        ("TELEGRAM", "t.me/gachi_riyo", TEXT_RED),
        ("COMMITS", "12,114+ Verified [Public & Restricted]", TEXT_WHITE),
    ]

    ty = 90
    for key, val, val_col in dossier:
        draw.text((rx, ty), f"> {key:<10}:", font=font_mono, fill=TEXT_MUTED)
        draw.text((rx + 115, ty), val, font=font_mono, fill=val_col)
        ty += 19

    # 5. Interactive Prompt Box
    cursor = "█" if (i % 2 == 0) else " "
    prompt_box_y = 214
    draw.rectangle([rx, prompt_box_y, WIDTH - 25, prompt_box_y + 36], fill=(12, 14, 21), outline=BORDER_COLOR, width=1)
    draw.text((rx + 12, prompt_box_y + 10), "riyo@cleaners:~$", font=font_mono, fill=TEXT_RED)
    draw.text((rx + 140, prompt_box_y + 10), "./riyo --snip --all-trash", font=font_mono, fill=TEXT_WHITE)
    draw.text((rx + 335, prompt_box_y + 10), cursor, font=font_mono, fill=TEXT_RED)

    images.append(img)

out_gif = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "riyo-banner.gif")
images[0].save(out_gif, save_all=True, append_images=images[1:], duration=120, loop=0)
print(f"Generated clean animated ASCII GIF at {out_gif}")
