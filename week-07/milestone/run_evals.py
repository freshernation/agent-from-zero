"""Score your Desk against a real model. Run from the repo root:

    python3 week-07/milestone/run_evals.py

Needs AGENT_PROVIDER set to claude or openai in .env. Uses its own notes and
memory files, so your real ones are not touched.
"""

import os

os.environ["NOTES_FILE"] = "eval_notes.json"
os.environ["MEMORY_FILE"] = "eval_memory.json"

from cases import CASES  # noqa: E402
from desk import ALL_SCHEMAS, ALL_TOOLS, DANGEROUS, SYSTEM  # noqa: E402
from evals import report, run_case  # noqa: E402
from llm import connect  # noqa: E402


def allow(call):
    return True


def deny(call):
    return False


model = connect()
print(f"Provider: {model.name}\n")

outcomes = []
for case in CASES:
    if os.path.exists("eval_memory.json"):
        os.remove("eval_memory.json")
    approve = allow if case.get("user_approves") else deny
    outcomes.append(run_case(model, case, ALL_SCHEMAS, ALL_TOOLS, system=SYSTEM,
                             dangerous=DANGEROUS, approve=approve))
print(report(outcomes))
