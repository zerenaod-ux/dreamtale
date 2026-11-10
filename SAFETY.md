# Safety rules (children's product). Enforced in safety.py + story prompt.
- Data: ONLY a first name (letters, max 20, first word) and one animal from a fixed list of 20. No surname, age in years, email, location, photo, account. Nothing stored in the browser; web page makes no network call except loading library.json.
- Content: calm, warm, no danger/violence/scary/sadness/sickness/death/brands/links; last scene must end with sleep/safe/cozy words; length per age band; banned-word list; unsafe LLM output is rejected and a hand-written fallback story is used.
- Ages covered 2-8 (not babies, not 9+). Free LLM output never shown without passing the check.
- Legal to check before taking money (see TODO-OWNER): COPPA applies to data collected FROM children; we collect from parents only (first name of a child is personal data in some laws) -> privacy note on page + Gumroad terms. No ads, no tracking, no analytics on the page.
- Narration voices are Microsoft Edge neural voices via edge-tts (unofficial free service: same dependency risk already accepted in the 3 channel systems; see DEPENDENCIES in shelfmade-notes).
