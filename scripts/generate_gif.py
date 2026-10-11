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
font_title = ImageFont.truetype(FONT_PATH, 25)
font_mono = ImageFont.truetype(FONT_PATH, 11)
font_small = ImageFont.truetype(FONT_PATH, 10)

# Full physical kinematics: Both blades AND handles move synchronously
FRAME_OPEN = [
    r"       \                   /       ",
    r"       |\                 /|       ",
    r"       | \               / |       ",
    r"       |  \             /  |       ",
    r"        \  \           /  /        ",
    r"         \  \         /  /         ",
    r"          \  \       /  /          ",
    r"           \  \     /  /           ",
    r"            \  \   /  /            ",
    r"             \  \ /  /             ",
    r"              \-(X)-/              ",
    r"              /     \              ",
    r"             /       \             ",
    r"           /           \           ",
    r"        ( O )         ( O )        ",
    r"         \_/           \_/         ",
]

FRAME_CLOSING = [
    r"                                   ",
    r"         \               /         ",
    r"         |\             /|         ",
    r"         | \           / |         ",
    r"          \ \         / /          ",
    r"           \ \       / /           ",
    r"            \ \     / /            ",
    r"             \ \   / /             ",
    r"              \ \ / /              ",
    r"               \ | /               ",
    r"              \-(X)-/              ",
    r"              / / \ \              ",
    r"             / /   \ \             ",
    r"            / /     \ \            ",
    r"          ( O )     ( O )          ",
    r"           \_/       \_/           ",
]

FRAME_SNIP = [
    r"                 |                 ",
    r"                | |                ",
    r"                | |   .  *  .      ",
    r"                | |  * SNIP! *     ",
    r"                | |   *  .  *      ",
    r"                | |                ",
    r"                | |                ",
    r"                | |                ",
    r"                | |                ",
    r"                | |                ",
    r"              \-(X)-/              ",
    r"               / | \               ",
    r"              /  |  \              ",
    r"             (   |   )             ",
    r"            ( O )( O )             ",
    r"             \_/  \_/              ",
]

FRAME_SPARKS = [
    r"                 |                 ",
    r"                | |     +  .       ",
    r"                | |   . *  +       ",
    r"                | |     ·  +       ",
    r"                | |                ",
    r"                | |                ",
    r"                | |                ",
    r"                | |                ",
    r"                | |                ",
    r"                | |                ",
    r"              \-(X)-/              ",
    r"               / | \               ",
    r"              /  |  \              ",
    r"             (   |   )             ",
    r"            ( O )( O )             ",
    r"             \_/  \_/              ",
]

FRAME_RECOIL = [
    r"                                   ",
    r"         \               /         ",
    r"         |\             /|         ",
    r"         | \           / |         ",
    r"          \ \         / /          ",
    r"           \ \       / /           ",
    r"            \ \     / /            ",
    r"             \ \   / /             ",
    r"              \ \ / /              ",
    r"               \ | /               ",
    r"              \-(X)-/              ",
    r"              / / \ \              ",
    r"             / /   \ \             ",
    r"            / /     \ \            ",
    r"          ( O )     ( O )          ",
    r"           \_/       \_/           ",
]

# Deliberate, realistic mechanical rhythm:
ANIM_SEQUENCE = [
    (FRAME_OPEN, 300),
    (FRAME_CLOSING, 110),
    (FRAME_SNIP, 150),
    (FRAME_SPARKS, 110),
    (FRAME_RECOIL, 110),
    (FRAME_OPEN, 350),
    (FRAME_CLOSING, 110),
    (FRAME_SNIP, 150),
    (FRAME_SPARKS, 110),
    (FRAME_RECOIL, 110),
]

images = []
durations = []

for idx, (lines, dur) in enumerate(ANIM_SEQUENCE):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # 1. Outer Frame Border
    draw.rectangle([10, 10, WIDTH - 11, HEIGHT - 11], outline=BORDER_COLOR, width=1)
    draw.rectangle([13, 13, WIDTH - 14, HEIGHT - 14], outline=(16, 18, 26), width=1)

    # 2. Top Header Bar
    hazard_text = "/// THE PIT // SECTOR 07 // THE CLEANERS // JINKI: THE RIPPER ///"
    draw.text((24, 20), hazard_text, font=font_small, fill=TEXT_MUTED)
    draw.text((WIDTH - 155, 20), "STATUS: ARMED [OK]", font=font_small, fill=TEXT_RED)
    draw.line([(24, 36), (WIDTH - 25, 36)], fill=BORDER_COLOR, width=1)

    # 3. Left Column: Scissor Box
    draw.rectangle([24, 46, 268, 252], fill=(10, 12, 17), outline=BORDER_COLOR, width=1)
    draw.text((34, 52), "[ JINKI // SCISSORS ]", font=font_small, fill=TEXT_MUTED)

    sy = 68
    for line in lines:
        c = TEXT_RED if ("SNIP" in line or "(X)" in line) else TEXT_WHITE
        draw.text((29, sy), line, font=font_mono, fill=c)
        sy += 11

    # 4. Right Column: Hero Title & Dossier
    rx = 286
    draw.text((rx, 46), "RIYO REAPER", font=font_title, fill=TEXT_WHITE)
    draw.text((rx + 195, 54), "[THE CLEANERS // GIVER]", font=font_mono, fill=TEXT_RED)
    draw.line([(rx, 78), (WIDTH - 25, 78)], fill=(20, 23, 34), width=1)

    dossier = [
        ("OPERATIVE", "Riyo (Reei-dp)", TEXT_RED),
        ("ROLE", "Full-Stack Engineer // Automations & Systems", TEXT_WHITE),
        ("ARSENAL", "Go • Python • TypeScript • Docker • Linux", TEXT_CYAN),
        ("SPECIALTY", "High-Load Bot Architectures & Scalable APIs", TEXT_WHITE),
        ("TELEGRAM", "t.me/gachi_riyo", TEXT_RED),
        ("COMMITS", "12,123+ Verified [Public & Restricted]", TEXT_WHITE),
    ]

    ty = 88
    for key, val, val_col in dossier:
        draw.text((rx, ty), f"> {key:<10}:", font=font_mono, fill=TEXT_MUTED)
        draw.text((rx + 115, ty), val, font=font_mono, fill=val_col)
        ty += 19

    # 5. Interactive Prompt Box
    cursor = "█" if (idx % 2 == 0) else " "
    prompt_box_y = 214
    draw.rectangle([rx, prompt_box_y, WIDTH - 25, prompt_box_y + 36], fill=(12, 14, 21), outline=BORDER_COLOR, width=1)
    draw.text((rx + 12, prompt_box_y + 10), "riyo@cleaners:~$", font=font_mono, fill=TEXT_RED)
    draw.text((rx + 140, prompt_box_y + 10), "./riyo --snip --all-trash", font=font_mono, fill=TEXT_WHITE)
    draw.text((rx + 335, prompt_box_y + 10), cursor, font=font_mono, fill=TEXT_RED)

    images.append(img)
    durations.append(dur)

out_gif = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "cleaner-scissors.gif")
images[0].save(out_gif, save_all=True, append_images=images[1:], duration=durations, loop=0)

out_gif2 = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "riyo-scissors.gif")
images[0].save(out_gif2, save_all=True, append_images=images[1:], duration=durations, loop=0)

out_gif3 = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "scissors.gif")
images[0].save(out_gif3, save_all=True, append_images=images[1:], duration=durations, loop=0)

out_gif4 = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "banner.gif")
images[0].save(out_gif4, save_all=True, append_images=images[1:], duration=durations, loop=0)

print(f"Generated realistic kinematic scissors GIF at {out_gif}")
