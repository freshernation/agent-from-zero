# Day 4 - trying again, politely.
#
#   call_with_retry(model, messages, system=None, tools=None,
#                   retries=2, wait=time.sleep)
#
#       Call model.chat(messages, system=system, tools=tools); return the reply.
#       On a ModelError whose .retryable is True: wait(1), try again; then
#       wait(2), then wait(4) ...  - at most `retries` extra attempts.
#       A non-retryable error, or running out of retries, passes the error on.
