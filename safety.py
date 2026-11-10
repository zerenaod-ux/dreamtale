"""Child-safety rules enforced in code (see SAFETY.md). Used by every story before it is shown or voiced."""
import re
BANNED = re.compile(r"\b(?:die|dies|died|dying|dead|death|kill|kills|killed|blood|bloody|gun|knife|weapon|weapons|monster|monsters|ghost|ghosts|demon|devil|scary|terrify|terrified|terrifying|nightmare|nightmares|hate|hated|stupid|dumb|ugly|fight|fights|fighting|war|hurt|hurts|cry|cries|crying|cried|scream|screamed|screaming|danger|dangerous|abandoned|orphan|poison|fire|burn|burning|drown|drowning|witch|zombie|beer|wine|drug|drugs|cigarette|hospital|sick|sickness|afraid|fear|frightened|lonely|alone)\b", re.I)
CALM_END = re.compile(r"\b(sleep|dream|snug|cozy|warm|safe|quiet|rest|yawn|goodnight|good night|peaceful|moon)\w*", re.I)
def check(story, minw=220):
    """Return (ok, reasons). story = {'title','scenes':[{'text','place','emoji'}]}"""
    why = []; sc = story.get('scenes') or []
    if not 5 <= len(sc) <= 12: why.append('scene count %d' % len(sc))
    text = ' '.join(s.get('text', '') for s in sc)
    words = len(text.split())
    if not minw <= words <= 1100: why.append('length %d words' % words)
    m = BANNED.search(text + ' ' + story.get('title', ''))
    if m: why.append('banned word: ' + m.group(0))
    if sc and not CALM_END.search(sc[-1].get('text', '')): why.append('ending not calm')
    if re.search(r'https?://|@\w+|\d{3}[- ]\d{3,}', text): why.append('link/contact in text')
    return (not why, why)
def clean_name(n):
    """First name only: letters, max 20 chars. Anything else is dropped (no surnames, numbers, links)."""
    n = re.sub(r"[^A-Za-zÀ-ɏ' -]", '', (n or '')).strip().split(' ')[0][:20]
    return n.capitalize() if n else 'Little One'
ANIMALS = ['bunny', 'bear', 'fox', 'owl', 'kitten', 'puppy', 'elephant', 'turtle', 'deer', 'penguin', 'dolphin', 'lion', 'koala', 'hedgehog', 'duckling', 'dragon', 'unicorn', 'panda', 'giraffe', 'frog']
EMOJI = {'bunny': '🐰', 'bear': '🐻', 'fox': '🦊', 'owl': '🦉', 'kitten': '🐱', 'puppy': '🐶', 'elephant': '🐘', 'turtle': '🐢', 'deer': '🦌', 'penguin': '🐧', 'dolphin': '🐬', 'lion': '🦁', 'koala': '🐨', 'hedgehog': '🦔', 'duckling': '🐥', 'dragon': '🐲', 'unicorn': '🦄', 'panda': '🐼', 'giraffe': '🦒', 'frog': '🐸'}
def clean_animal(a):
    a = re.sub(r'[^a-z ]', '', (a or '').lower()).strip()
    for k in ANIMALS:
        if k in a: return k
    return 'bunny'   # only animals from the fixed list are ever used (no free text reaches the story)
