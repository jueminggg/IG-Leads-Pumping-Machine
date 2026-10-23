# IG Leads Pumping Machine — playbook

The owner is a financial advisor (FA). This repo finds promising prospects among
their Instagram followers, researches what each person is up to, drafts a genuine
first message, and tracks every conversation to the next step.

## Ideal prospect
- Young: students (poly / uni / NS) or fresh grads in their first 1–3 years of work.
- Roughly under 30.
- Skip: married, has kids, clearly 30+, already in finance/insurance (competitors),
  businesses, meme/fan pages, private accounts with nothing visible.
- Age and marital status are guesses from public signals (grad posts, uni in bio,
  "first day at work", wedding photos). Record the signal, not just the verdict.

## Every prospect report has exactly 4 parts
1. **What they're up to**: 2–4 facts from their last few posts/stories/bio, with dates.
2. **The message**: the DM to send.
3. **Why I wrote it this way**: which detail it hooks on and why it fits them.
4. **Lead-gen plan**: next 2–3 steps depending on how they reply.

Save each report to `reports/<handle>.md` and update `data/leads.csv`.

## Message rules (be genuine)
- First message is about THEM, never the product. No mention of insurance,
  investment, "financial planning" or "coffee to share something".
- Hook on one specific, recent thing (a trip, a new job, graduation, a hobby).
- Short: 1–3 sentences, casual, sounds like the owner typing on their phone.
  No emojis spam, no em dashes, no "Hope you're doing well!".
- End with an easy question they'd want to answer.
- If you can't find anything real to say, mark them `skip` rather than force it.
- The owner sends every message by hand. Never send DMs, like, follow or comment.

## Conversation stages (status column in leads.csv)
`new` → `researched` → `messaged` → `replied` → `rapport` → `value_offered`
→ `meeting_booked` → `client`, or `not_fit` / `no_reply` / `skip`.

- Bridge to money topics only after real back-and-forth (`rapport`), and only
  through their life event: first pay cheque, moving out, travel savings,
  grad school, buying a car, parents asking them to "get insured".
- `value_offered`: something useful with no strings (e.g. a first-salary budget
  breakdown, a quick CPF/savings explainer). Ask permission before sending.
- No reply after 5–7 days: at most ONE light follow-up on a new post of theirs,
  then `no_reply`. Never chase twice.
- When the owner pastes a reply, update the row, set `next_step` and
  `next_followup`, and draft the response.

## Browsing Instagram (Claude in Chrome, owner's logged-in browser)
- Only read public info a follower would see. Human pace: max ~25 profiles per
  day, pauses between profiles, no rapid scrolling through follower lists.
- Stop immediately on any "Try again later", challenge, or unusual-activity
  screen and tell the owner.
- Never type in DMs, never change account settings.

## Compliance reminders
- Treat collected info as personal data (PDPA): keep it in `data/` and
  `reports/` (gitignored), use it only for this outreach, delete on request.
- Follow the owner's firm/regulator rules on prospecting and fair dealing.
  Don't make product, return, or "guaranteed" claims in DMs.

## Files
- `scripts/parse_followers.py`: Instagram data export → `data/leads.csv`.
- `data/leads.csv`: the tracker (one row per follower).
- `reports/<handle>.md`: the 4-part report per prospect.
