"""Soft night-time illustrations drawn in code (no stock images, no licensing). 1280x720 scenes."""
import math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W, H = 1280, 720
EMOJI_FONT = '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'
PAL = {'night_sky': ((18, 24, 66), (62, 52, 120)), 'meadow': ((40, 52, 110), (92, 120, 150)), 'forest': ((14, 36, 54), (42, 84, 86)),
       'sea': ((16, 38, 86), (60, 110, 150)), 'snow': ((40, 56, 100), (150, 170, 210)), 'room': ((46, 34, 72), (120, 84, 110)),
       'clouds': ((52, 50, 120), (150, 130, 190)), 'garden': ((22, 40, 80), (70, 110, 130))}
GROUND = {'meadow': (40, 84, 70), 'forest': (18, 56, 50), 'snow': (200, 214, 236), 'garden': (36, 80, 70), 'room': (84, 56, 76), 'sea': (24, 70, 120), 'night_sky': (30, 36, 90), 'clouds': (190, 180, 225)}
def emoji(ch, size):
    f = ImageFont.truetype(EMOJI_FONT, 109)
    im = Image.new('RGBA', (136, 128), (0, 0, 0, 0)); ImageDraw.Draw(im).text((0, 0), ch, font=f, embedded_color=True)
    bb = im.getbbox() or (0, 0, 136, 128); im = im.crop(bb)
    s = size / max(im.size); return im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS)
def scene(place='night_sky', hero='🐰', prop='⭐', seed=0):
    r = random.Random(seed); top, bot = PAL.get(place, PAL['night_sky'])
    im = Image.new('RGB', (W, H))
    px = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H; px.line([(0, y), (W, y)], fill=tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3)))
    d = ImageDraw.Draw(im, 'RGBA')
    for _ in range(70):   # stars
        x, y, s = r.randint(0, W), r.randint(0, int(H * .55)), r.choice([1, 2, 2, 3]); d.ellipse([x - s, y - s, x + s, y + s], fill=(255, 250, 220, r.randint(120, 255)))
    mx, my = (r.choice([200, 1050]), r.randint(90, 170))   # moon with glow
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow); gd.ellipse([mx - 120, my - 120, mx + 120, my + 120], fill=(255, 245, 200, 70))
    im.paste(glow.filter(ImageFilter.GaussianBlur(40)), (0, 0), glow.filter(ImageFilter.GaussianBlur(40))); d = ImageDraw.Draw(im, 'RGBA')
    d.ellipse([mx - 55, my - 55, mx + 55, my + 55], fill=(255, 246, 214, 255)); d.ellipse([mx - 28, my - 38, mx + 12, my - 4], fill=(240, 228, 190, 120))
    g = GROUND.get(place, (30, 40, 90))
    for k, (base, amp, shade) in enumerate([(520, 40, .75), (570, 50, 1.0)]):   # soft hills
        pts = [(0, H)] + [(x, base + amp * math.sin(x / 190 + k * 1.7 + seed)) for x in range(0, W + 20, 20)] + [(W, H)]
        d.polygon(pts, fill=tuple(int(c * shade) for c in g) + (255,))
    if place == 'sea':
        for i in range(8): y = 540 + i * 22; d.arc([100 + i * 90, y, 300 + i * 90, y + 30], 0, 180, fill=(200, 225, 255, 120), width=3)
    hs = emoji(hero, 250); im.paste(hs, (W // 2 - hs.width // 2 - 120, 330 - hs.height // 2 + 40), hs)
    pr = emoji(prop, 150); im.paste(pr, (W // 2 + 170, 250), pr)
    fl = Image.new('RGBA', (W, H), (255, 200, 120, 0)); return im
def title_card(title, name, hero='🐰'):
    im = scene('night_sky', hero, '🌙', 7); d = ImageDraw.Draw(im, 'RGBA'); d.rectangle([0, 0, W, 190], fill=(10, 12, 40, 150))
    f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf', 58)
    t = title if len(title) < 36 else title[:34] + '…'; tw = d.textlength(t, font=f); d.text(((W - tw) / 2, 52), t, font=f, fill=(255, 240, 200))
    f2 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf', 30); s = 'a bedtime story for %s' % name; sw = d.textlength(s, font=f2); d.text(((W - sw) / 2, 130), s, font=f2, fill=(210, 205, 240)); return im
