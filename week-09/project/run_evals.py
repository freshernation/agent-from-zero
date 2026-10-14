"""Score your agent against a real model. Run from the repo root:

    python3 week-09/project/run_evals.py

Needs AGENT_PROVIDER set to claude or openai in .env. Uses its own data file
(eval_data.json), so your real data is not touched.
"""

import os

os.environ["DATA_FILE"] = "eval_data.json"
os.environ["MEMORY_FILE"] = "eval_memory.json"

from app import SYSTEM  # noqa: E402
from cases import CASES  # noqa: E402
from evals import report, run_case  # noqa: E402
from llm import connect  # noqa: E402
from tools import DANGEROUS, SCHEMAS, TOOLS  # noqa: E402


def allow(call):
    return True


def deny(call):
    return False


model = connect()
print(f"Provider: {model.name}\n")

outcomes = []
for case in CASES:
    approve = allow if case.get("user_approves") else deny
    outcomes.append(run_case(model, case, SCHEMAS, TOOLS, system=SYSTEM,
                             dangerous=DANGEROUS, approve=approve))
print(report(outcomes))
