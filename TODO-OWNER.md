# Things only the owner can do (noted on the side; nothing is blocked by them)
1. **Create the GitHub repo** zerenaod-ux/dreamtale (empty, public so Pages + free Actions work) - the cloud session cannot create repos. Then tell Claude "dreamtale repo ready" and the code (kept in shelfmade-notes/business-ideas/dreamtale-code/ until then) is moved in.
2. Repo secrets (Settings > Secrets > Actions): GEMINI_API_KEY, GROQ_API_KEY, CEREBRAS_API_KEY (same free keys as the dashboard repo). Settings > Pages > Source = GitHub Actions.
3. **Gumroad product** "Personalised bedtime story" ($3-5): 2 custom fields (child's first name, favorite animal) + a note "we only need a first name". Put the product URL into docs/index.html (cfg.product) - or tell Claude the URL.
4. Order intake: Gumroad token (read sales) as secret GUMROAD_TOKEN so a poller can read new sales into orders/queue.json (Claude builds the poller once the token exists). Until then: paste an order line into orders/queue.json.
5. Delivery message: Gumroad "send to customer" text with the Release link (manual until step 4 + an email route exist).
6. Decide price + whether to add a subscription ("a new story every week", $4-6/mo).
7. Optional: privacy page wording check (legal).
