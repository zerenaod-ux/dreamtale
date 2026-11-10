"""One story -> out/<slug>/{story.json, story.mp3, story.mp4, cover.jpg}.  python make_story.py NAME ANIMAL [AGE_BAND]
No data is stored beyond the first name and chosen animal in story.json; nothing else is ever asked."""
import json, os, re, subprocess, sys, shutil
from pathlib import Path
import art, narrate, safety, story
def build(name='Little One', animal='bunny', band='4-6', out='out', st=None, theme=None):
    name, animal = safety.clean_name(name), safety.clean_animal(animal)
    st = st or story.write(band, theme, name, animal)
    slug = re.sub(r'[^a-z0-9]+', '-', ('%s-%s' % (name, st['title'])).lower()).strip('-')[:50]
    d = Path(out) / slug; d.mkdir(parents=True, exist_ok=True); hero = safety.EMOJI[animal]
    clips = []; parts = []
    title_img = art.title_card(st['title'], name, hero); title_img.convert('RGB').save(d / 'cover.jpg', quality=90)
    seq = [('Tonight\'s story is called. %s.' % st['title'], title_img)] + [(s['text'], art.scene(s['place'], hero, s['emoji'], i + 1)) for i, s in enumerate(st['scenes'])]
    for i, (text, img) in enumerate(seq):
        a = d / ('a%02d.mp3' % i); narrate.speak(text, str(a)); L = narrate.dur(str(a)) + 1.4
        png = d / ('s%02d.png' % i); img.save(png); v = d / ('v%02d.mp4' % i)
        fr = int(L * 15)
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-i', str(png), '-i', str(a), '-filter_complex',
                        "[0:v]scale=1400:788,zoompan=z='min(zoom+0.0003,1.08)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=%d:s=1280x720:fps=15,fade=t=in:st=0:d=0.8,fade=t=out:st=%.2f:d=0.8[v];[1:a]apad=pad_dur=1.4,afade=t=in:d=0.2[a]" % (fr, L - 0.8),
                        '-map', '[v]', '-map', '[a]', '-t', '%.2f' % L, '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '26', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '96k', str(v)], check=True)
        clips.append(v); parts.append(a)
    lst = d / 'list.txt'; lst.write_text(''.join("file '%s'\n" % c.name for c in clips))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', str(lst), '-c', 'copy', str(d / 'story.mp4')], check=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(d / 'story.mp4'), '-vn', '-c:a', 'libmp3lame', '-q:a', '5', str(d / 'story.mp3')], check=True)
    (d / 'story.json').write_text(json.dumps({'name': name, 'animal': animal, 'band': band, **st}, indent=1, ensure_ascii=False))
    for f in list(d.glob('a*.mp3')) + list(d.glob('s*.png')) + list(d.glob('v*.mp4')) + [lst]: f.unlink()
    print('built', d, 'mp4 %.1f MB' % (os.path.getsize(d / 'story.mp4') / 1e6)); return d
if __name__ == '__main__':
    a = sys.argv[1:]; build(*(a[0:1] or ['Mia']), *(a[1:2] or ['bunny']), *(a[2:3] or ['4-6']))
