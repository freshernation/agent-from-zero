# Day 4 - the loop, with a budget and retries.
#
# Copy your day-3 agent.py here, then add three arguments at the end:
#
#   run_agent(..., token_budget=None, retries=2, wait=time.sleep)
#
#   - Call the model through call_with_retry (from retry.py), passing
#     retries and wait along.
#   - After adding a reply's usage: if the model asked for tools AND the total
#     tokens (input + output) are over token_budget, stop:
#         stopped "budget", answer "I reached my token budget before finishing."
#   - token_budget=None means no limit.
