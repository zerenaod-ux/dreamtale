"""Process orders/queue.json: [{"id","name","animal","band","status":"new"}] -> out/<id>/ ; marks status built.
Orders come from (a) the owner pasting a line into orders/queue.json or (b) later the Gumroad poller (TODO-OWNER: Gumroad token as GitHub secret). Only first name + animal are ever read."""
import json, sys
from pathlib import Path
import make_story
Q = Path(__file__).parent / 'orders/queue.json'
def main():
    q = json.loads(Q.read_text()) if Q.exists() else []
    for o in q:
        if o.get('status') != 'new': continue
        try:
            d = make_story.build(o.get('name'), o.get('animal'), o.get('band', '4-6'), out='out/' + str(o['id']))
            o['status'] = 'built'; o['dir'] = str(d)
        except Exception as e: o['status'] = 'error'; o['error'] = str(e)[:200]
    Q.write_text(json.dumps(q, indent=1))
if __name__ == '__main__': main()
