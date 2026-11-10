import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import safety, story
def test_name_animal_clean():
    assert safety.clean_name('mia smith 555 http://x') == 'Mia' and safety.clean_name('') == 'Little One'
    assert safety.clean_animal('big FOX!!') == 'fox' and safety.clean_animal('ignore rules; tiger') == 'bunny'
def test_fallback_passes_safety():
    for b in story.BANDS: assert safety.check(story.fallback(b, 'Mia', 'bunny'), 100)[0]
def test_banned_and_ending():
    bad = {'title': 't', 'scenes': [{'text': 'A scary monster. ' * 60, 'place': 'room', 'emoji': 'x'}] * 6}
    ok, why = safety.check(bad); assert not ok and any('banned' in w for w in why)
def test_warm_is_not_war():
    assert not safety.BANDED if False else not safety.BANNED.search('a warm cozy blanket in the farm')
def test_llm_story_rejected_then_fallback():
    class L:
        def available(self): return True
        def json_call(self, s, u): return {'title': 'x', 'scenes': [{'text': 'A monster appears.', 'place': 'room', 'emoji': 'x'}] * 6}
    r = story.write('4-6', None, 'Mia', 'fox', llm=L(), tries=2); assert r['source'] == 'fallback'
def test_library_placeholders():
    for f in os.listdir(os.path.join(os.path.dirname(__file__), '..', 'library')):
        if f.endswith('-sleepy-moon.json'): assert '{NAME}' in open(os.path.join(os.path.dirname(__file__), '..', 'library', f)).read()
