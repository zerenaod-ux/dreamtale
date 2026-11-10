"""Write a calm bedtime story. LLM first (free keys), safe built-in fallback if the LLM fails or the safety check rejects it."""
import json, re, sys
import safety
BANDS = {'2-4': dict(scenes=6, words='250-380', style='very simple sentences, gentle repetition (a repeated soothing phrase), one tiny kind problem solved in a snuggly way'),
         '4-6': dict(scenes=7, words='400-600', style='simple plot with a cosy problem and a kind friend, a gentle surprise, happy calm ending'),
         '6-8': dict(scenes=9, words='650-950', style='a small adventure told softly with wonder, a little lesson about kindness or courage, never scary, slows down at the end')}
THEMES = {'2-4': ['finding the perfect cozy blanket', 'saying goodnight to the farm animals', 'a sleepy little cloud', 'the moon gives a hug', 'a teddy who cannot yawn yet', 'tiny boats on a bubble bath sea'],
          '4-6': ['a lost sparkle found by friends', 'the night garden where flowers sing lullabies', 'a train that carries sleepy dreams', 'the sleepy lighthouse and the kind whale', 'a baker who bakes sleepy bread', 'stars that need help to shine'],
          '6-8': ['the map of dream islands', 'a library where books whisper goodnight', 'a gentle dragon who guards the quiet moon', 'the clockmaker of slow time', 'a lantern boat on a calm river of stars', 'the forest of sleepy lanterns']}
PLACES = ['night_sky', 'meadow', 'forest', 'sea', 'snow', 'room', 'clouds', 'garden']
SYS = 'You are a gentle children\'s bedtime storyteller. Reply JSON only.'
def prompt(band, theme, name, animal):
    b = BANDS[band]
    return ('Write a bedtime story for a child aged %s about: %s.\nHero: a child named %s with their favorite animal friend, a %s.\n'
            'Style: %s. Exactly %d scenes, %s words total. Every scene: 2-5 short read-aloud sentences. '
            'Rules: calm, warm, never scary, no danger, no sadness, no violence, no sickness, no real brands, no links. The tone gets slower and softer toward the end; the LAST scene ends with %s falling peacefully asleep, snug and safe.\n'
            'JSON only: {"title":"","scenes":[{"text":"","place":"one of %s","emoji":"ONE emoji that shows what is in the scene (not the hero animal)"}]}'
            % (band, theme, name, animal, b['style'], b['scenes'], b['words'], name, '/'.join(PLACES)))
def fallback(band, name, animal):
    n, a = name, animal
    sc = [("It was nearly bedtime, and %s the little child sat by the window with a soft, sleepy %s." % (n, a), 'room', '🌙'),
          ("The moon was big and round and smiling. \"Time to rest,\" it whispered. \"Time to rest.\"", 'night_sky', '🌕'),
          ("%s and the %s tiptoed out into the quiet garden, where the flowers were folding their petals." % (n, a), 'garden', '🌷'),
          ("A little breeze hummed a slow song. The %s yawned a very big yawn, and %s yawned too." % (a, n), 'meadow', '🍃'),
          ("They found a cloud as soft as a pillow, floating just above the grass. \"Time to rest,\" it whispered." , 'clouds', '☁️'),
          ("%s and the %s climbed on, and the cloud carried them gently over the hills and the sleepy sea." % (n, a), 'sea', '⭐'),
          ("The stars twinkled slowly, one by one, like tiny lights saying goodnight. Everything was calm and warm." , 'night_sky', '✨'),
          ("Soon the cloud floated back to the window. %s snuggled into bed with the %s close by." % (n, a), 'room', '🛏️'),
          ("The moon smiled once more. \"Time to rest,\" it whispered. And %s closed their eyes, safe and cozy, and fell fast asleep. Goodnight, %s." % (n, n), 'room', '🌙')]
    k = {'2-4': 7, '4-6': 8, '6-8': 9}[band]
    pick = sc[:k - 1] + [sc[-1]]
    return {'title': "%s and the Sleepy Moon" % n, 'scenes': [{'text': t, 'place': p, 'emoji': e} for t, p, e in pick], 'source': 'fallback'}
def write(band='4-6', theme=None, name='Little One', animal='bunny', llm=None, tries=3):
    import random
    name, animal = safety.clean_name(name), safety.clean_animal(animal)
    theme = theme or random.choice(THEMES[band]); last = []
    try:
        llm = llm or __import__('llm')
        if getattr(llm, 'available', lambda: True)():
            for _ in range(tries):
                try:
                    r = llm.json_call(SYS, prompt(band, theme, name, animal))
                    for s in r.get('scenes', []):
                        s['place'] = s.get('place') if s.get('place') in PLACES else 'night_sky'; s['emoji'] = (s.get('emoji') or '⭐')[:4]
                    ok, why = safety.check(r)
                    if ok: r['source'] = 'llm'; r['theme'] = theme; return r
                    last = why; print('story rejected:', why, file=sys.stderr)
                except Exception as e: print('llm story failed:', str(e)[:120], file=sys.stderr)
    except Exception as e: print('llm unavailable:', str(e)[:120], file=sys.stderr)
    f = fallback(band, name, animal); f['theme'] = theme; return f
if __name__ == '__main__':
    print(json.dumps(write(*(sys.argv[1:2] or ['4-6'])), indent=1, ensure_ascii=False))
