# Troubleshooting

This note records problems that have been encountered with **math-mcp-server** and how they were resolved.

---

## Fixed: `SyntaxError: '(' was never closed` when running FastMCP

**Symptom**

Running the MCP Inspector or loading the server fails with an error similar to:

```text
File "...\main.py", line 10
    return float(x
                ^
SyntaxError: '(' was never closed
```

**Cause**

The `_as_number` helper in `main.py` had a **broken `return` statement** (missing closing parenthesis and incomplete expression), so Python could not parse the file.

**Fix**

Ensure the string branch returns a full call, for example:

```python
if isinstance(x, str):
    return float(x.strip())
```

Run a quick syntax check after editing:

```powershell
uv run python -m py_compile main.py
```

Then retry:

```powershell
uv run fastmcp dev inspector main.py --no-reload
```

---

## `uv run fastmcp version` appears to hang on first run

**Symptom**

The first invocation of `uv run fastmcp version` (or other `fastmcp` commands) takes a long time or stops in the middle of importing FastMCP.

**What happened**

In one session this looked like a hang but was followed by `KeyboardInterrupt`, which means the process was still loading when it was interrupted. FastMCP pulls in a large dependency tree; the **first** import can be slow on Windows (disk, antivirus scanning).

**What to do**

- Wait for the command to finish the first time (can take a minute or more on some machines).
- If it truly never returns, confirm the venv is the one used by `uv run` (`uv sync` from repo root) and try again without interrupting.

---

## MCP Inspector / dev server and Ctrl+C on Windows

**Symptom**

Stopping the dev inspector with Ctrl+C may show:

- `Terminate batch job (Y/N)?`
- `[ERROR] Dev server failed`
- `The system cannot open the device or file specified`

**Cause**

This is common when a **child process** (proxy server, browser, stdio bridge) is torn down abruptly from the console.

**What to do**

- To exit cleanly, prefer closing the inspector tab or using the UI stop control if available.
- If you see `Terminate batch job`, answer `Y` to allow the batch wrapper to exit, or close the terminal.

---

## Tool inputs: numbers as strings

**Behavior**

Tools are annotated with `float`, but JSON payloads may send numeric values as strings. The `_as_number` helper accepts `int`, `float`, or numeric **strings** (with surrounding whitespace stripped) so the server returns predictable errors for truly invalid input instead of failing opaquely.

If you add new tools, keep the same coercion pattern if you need string-number compatibility.
