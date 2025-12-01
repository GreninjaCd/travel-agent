#!/usr/bin/env python3
"""
CLI wrapper for AgentRunner. Reads JSON from stdin, calls AgentRunner.run, outputs JSON to stdout.
Accepts optional `session_id` field in the input to resume/save sessions.
"""
import sys
import os
import json
import asyncio

# Ensure project root is on sys.path so `import app.*` works when this file is
# executed directly (e.g. via `python app/agent_cli.py`). This makes the CLI
# robust to different working directories and how the Python process is spawned.
proj_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if proj_root not in sys.path:
    sys.path.insert(0, proj_root)

from app.agent_runner import AgentRunner


async def _main_async():
    try:
        input_data = sys.stdin.read()
        request = json.loads(input_data) if input_data.strip() else {}

        session_id = request.get("session_id")

        runner = AgentRunner()
        result = await runner.run(request, session_id=session_id)

        print(json.dumps(result))
    except Exception as e:
        error_response = {"error": str(e)}
        print(json.dumps(error_response), file=sys.stderr)
        sys.exit(1)


def main():
    asyncio.run(_main_async())


if __name__ == "__main__":
    main()
