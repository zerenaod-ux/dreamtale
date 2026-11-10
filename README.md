# Dreamtale - personalised bedtime stories (separate from ShelfMade / MindLore / Doodles)
Faceless, free, automatic. A parent types a child's FIRST NAME + a favorite animal; a calm, safe bedtime story is made with that name in it.
**This project shares NOTHING with the three channel systems** (own folder/repo, own workflows, own data). Code was copied once (llm.py) and can be changed freely.

## What exists (built 2026-11-09, tested offline)
| Piece | File | Status |
|---|---|---|
| Child-safety rules in code (banned words, calm ending, name/animal sanitising, fixed animal list) | safety.py, SAFETY.md | done + tests |
| Story writer (free LLM keys; 3 age bands; rejects unsafe stories; safe built-in fallback) | story.py | done |
| Illustrations drawn in code (night sky, hills, moon, animal emoji) | art.py | done (looked at frames) |
| Calm neural narration (edge-tts en-US-AnaNeural, slow) | narrate.py | done (voice call needs GitHub runner; tested with silent stand-in here) |
| Story -> narrated video (mp4) + audio (mp3) + cover | make_story.py | done |
| Order queue -> builds stories -> Release assets | build_orders.py, build-orders.yml | done, waits for orders |
| Free web page: name + animal -> story read aloud in the browser, nothing leaves the device | docs/index.html, library/, library.py | done (browser-tested) |
| Library grows by itself (3 new safe stories twice a week) | library.yml | done, needs repo + keys |
| Website hosting | pages.yml (GitHub Pages) | ready |

## End-to-end flow
1. FREE path (no orders, fully automatic): parent opens the page -> types name + animal + age -> page fills a library story and reads it aloud with the browser voice. Library is written by library.yml.
2. PAID path (narrated video, personal name spoken by a neural voice): Gumroad product with 2 custom fields (first name, animal) -> order line goes into orders/queue.json -> build-orders.yml builds mp4/mp3 -> delivered by unlisted link. Order intake + delivery steps that need the owner are in TODO-OWNER.md.
3. Money: Gumroad product(s) + affiliate/bio link from the 3 channels pointing here; free page is the funnel.

## Cost: $0 (GitHub Actions free minutes, free LLM keys, edge-tts, ffmpeg, GitHub Pages). Build time ~3-6 min per story.

## Run locally
`pip install pillow edge-tts pytest`, ffmpeg + NotoColorEmoji font installed; `python make_story.py Mia fox 4-6`; tests: `pytest tests`.
DREAMTALE_FAKE_VOICE=1 uses silent audio (offline tests).

## HISTORY
- 2026-11-09 21:10 CT: project created from owner voice session (idea 2 in shelfmade-notes/business-ideas). First full build.
