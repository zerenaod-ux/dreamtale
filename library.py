"""Pre-write the free LIBRARY: personalisable story texts with {NAME}/{ANIMAL} placeholders (3 age bands x themes), saved to library/*.json.
The web page fills the child's name + animal in the browser (nothing leaves the device) and reads aloud with the browser voice.
Run weekly (library.yml) to add a few new safe stories; each passes safety.check before it is saved."""
import json, re, sys
from pathlib import Path
import safety, story
LIB = Path(__file__).parent / 'library'
def add(band, theme):
    st = story.write(band, theme, 'NAMEX', 'bunny')
    if st.get('source') != 'llm': return None
    for s in st['scenes']:
        s['text'] = re.sub(r'\bNAMEX\b', '{NAME}', s['text']); s['text'] = re.sub(r'\b(bunny|bunnies)\b', '{ANIMAL}', s['text'], flags=re.I)
    st['title'] = re.sub(r'\bNAMEX\b', '{NAME}', st['title']); st['band'] = band
    slug = re.sub(r'[^a-z0-9]+', '-', st['title'].lower().replace('{name}', 'x')).strip('-')[:40]
    f = LIB / ('%s-%s.json' % (band, slug)); f.write_text(json.dumps(st, indent=1, ensure_ascii=False)); return f
def index():
    items = [json.loads(f.read_text()) | {'file': f.name} for f in sorted(LIB.glob('*-*.json'))]
    (LIB / 'index.json').write_text(json.dumps([{'file': i['file'], 'title': i['title'], 'band': i['band'], 'scenes': len(i['scenes'])} for i in items], indent=1))
    Path(__file__).parent.joinpath('docs/library.json').write_text(json.dumps(items, ensure_ascii=False))
if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3; LIB.mkdir(exist_ok=True)
    import random
    for _ in range(n):
        b = random.choice(list(story.BANDS)); t = random.choice(story.THEMES[b]); print(b, t, '->', add(b, t))
    index()
