"""Calm narration with free neural voices (edge-tts). DREAMTALE_FAKE_VOICE=1 -> silent placeholder (tests, offline)."""
import asyncio, os, subprocess, re
VOICE = os.environ.get('DREAMTALE_VOICE', 'en-US-AnaNeural')   # child-friendly, soft; alt: en-GB-SoniaNeural
RATE = os.environ.get('DREAMTALE_RATE', '-18%'); PITCH = os.environ.get('DREAMTALE_PITCH', '-4Hz')
def dur(p):
    o = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True).stdout.strip()
    return float(o or 0)
def speak(text, out):
    text = re.sub(r'\s+', ' ', text).strip()
    if os.environ.get('DREAMTALE_FAKE_VOICE'):
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'lavfi', '-i', 'anullsrc=r=24000:cl=mono', '-t', '%.2f' % max(2, len(text.split()) / 2.0), '-q:a', '9', out], check=True); return out
    import edge_tts
    async def go(): await edge_tts.Communicate(text, VOICE, rate=RATE, pitch=PITCH).save(out)
    for i in range(3):
        try: asyncio.run(go()); break
        except Exception as e:
            if i == 2: raise
    return out
