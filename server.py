#!/usr/bin/env python3
import json
import os
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 3456
DIR = os.path.dirname(os.path.abspath(__file__))

PROMPT = """Parse this text into exactly 3 categories. Return ONLY valid JSON, no markdown fences.
Keep the ORIGINAL language (do not translate). Chinese stays Chinese, English stays English.

Categories (check in this order):
1. gratitudes — MUST come first. Any expression of thankfulness, appreciation, gratitude, blessing, or positive reflection about people/things/life. Keywords: grateful, thankful, appreciate, blessed, glad, lucky, thanks, 感恩, 感谢, 谢谢, 幸运, 庆幸. Each: {"text":"..."}
2. todos — action items, tasks, reminders. Each: {"text":"concise imperative","priority":"high|med|low","context":"optional context"}. Priority: high=urgent/deadline, low=someday/maybe, med=default.
3. notes — everything else: facts, ideas, info that is NOT actionable and NOT gratitude. Each: {"text":"..."}

IMPORTANT: If something expresses gratitude or appreciation, it MUST go in "gratitudes", NOT "notes".

Example: "I'm grateful for my team. Buy milk. The weather is nice." ->
{"todos":[{"text":"Buy milk","priority":"med","context":""}],"notes":[{"text":"The weather is nice"}],"gratitudes":[{"text":"I'm grateful for my team"}]}

Text:
"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            html_path = os.path.join(DIR, "voice-todo.html")
            with open(html_path, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def do_POST(self):
        if self.path != "/parse":
            self.send_response(404)
            self.end_headers()
            return
        length = int(self.headers.get("Content-Length", 0))
        text = self.rfile.read(length).decode()
        raw = ""
        try:
            result = subprocess.run(
                ["claude", "-p", PROMPT + text, "--output-format", "text"],
                capture_output=True,
                text=True,
                timeout=60,
            )
            raw = result.stdout.strip()
            # strip markdown fences if present
            raw = raw.replace("```json", "").replace("```", "").strip()
            parsed = json.loads(raw)
            self._respond(200, parsed)
        except json.JSONDecodeError:
            self._respond(500, {"error": "Claude returned invalid JSON", "raw": raw})
        except Exception as e:
            self._respond(500, {"error": str(e)})

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _respond(self, code, data):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self._cors()
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def log_message(self, format, *args):  # noqa: A002
        print(f"[server] {args[0]}")


if __name__ == "__main__":
    print(f"Voice-todo server on http://localhost:{PORT}")
    HTTPServer(("localhost", PORT), Handler).serve_forever()
