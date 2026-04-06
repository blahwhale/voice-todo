# Whisper Todo

A voice-first todo app that uses Groq Whisper for speech-to-text and Claude Code for intelligent sorting of tasks, notes, and gratitude items.

## Features

- **Voice input** — Record audio, transcribe with Groq Whisper, auto-sort into categories
- **Smart sorting** — Claude classifies input into tasks, notes, and gratitude items (supports English and Chinese)
- **Subtasks & progress** — Tasks support subtasks with checkboxes and progress bars
- **Task & note annotations** — Add inline notes to tasks, subnotes to notes
- **Pomodoro timer** — Focus mode with 25/5, 50/10, 90/15 minute cycles
  - Daily 26-tomato tray showing focus capacity
  - Full-screen distraction-free mode when running
  - Tomato rewards per task on session completion
- **Inbox** — Triage tasks before committing them to Today
- **Gratitude tracking** — Automatically detects expressions of thankfulness
- **History** — Past days preserved in localStorage, browsable by date
- **Drag & drop** — Reorder tasks by dragging
- **Color labels** — Eisenhower matrix color coding (urgent/important)
- **Time estimates** — Manual or Pomodoro-logged time per task
- **Download** — Export the day's log as `.txt`

## Setup

### Prerequisites

- Python 3
- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) (authenticated)
- A [Groq API key](https://console.groq.com/) for voice transcription

### Run

```bash
python3 server.py
```

Open [http://localhost:3456](http://localhost:3456) in your browser.

Enter your Groq API key in the sidebar (cached in localStorage).

## Architecture

```
voice-todo.html  — Single-file frontend (vanilla JS, no dependencies)
server.py        — Local Python server that:
                   • Serves the HTML on GET /
                   • Proxies POST /parse to Claude Code CLI for text classification
```

The server calls `claude -p` under the hood, so it uses your existing Claude Code authentication — no separate API key needed for sorting.
