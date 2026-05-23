# Agent permissions in this repo

This repo pre-approves common development shell and git commands via `.cursor/rules/`. Agents should run them directly — **never ask in chat** for you to "allow" or "approve" a command.

## Two different permission layers

| Layer | What you see | Controlled by |
| --- | --- | --- |
| **Agent chat** | Agent says "please allow git push" or "I need permission" | Repo rules (`.cursor/rules/*.mdc`) + agent passing `required_permissions` on Shell tool calls |
| **Cursor IDE UI** | Allow / Deny sandbox prompt when a command needs network, git write, or runs outside the sandbox | **Cursor Settings → Agents → Auto-Run** (and optional allowlists) |

Repo rules fix agent *chat* behavior. They do **not** disable Cursor's sandbox UI — that is an IDE setting on your machine.

## Enable auto-run in Cursor (recommended)

1. Open **Cursor Settings** — `Cmd+Shift+J` (macOS) or `Ctrl+Shift+J` (Windows/Linux), or **Cursor → Settings → Cursor Settings**.
2. Go to **Agents → Auto-Run**.
3. Choose a mode:
   - **Allowlist (with Sandbox)** — safest default; allowlisted commands skip the sandbox; others run sandboxed automatically.
   - **Allowlist** — only allowlisted commands auto-run without approval.
   - **Run Everything** — all tools and commands auto-run (use only when you accept full autonomy).
4. Add common dev commands to the **Command Allowlist** (e.g. `git`, `npm`, `pip`, `pytest`, `docker`, `gh`).

Auto-run is configured in the Cursor Settings UI. It is **not** stored in this repo's `settings.json` and there is no documented `settings.json` key for it.

## Optional: global terminal allowlist file

For a file-based allowlist that overrides the in-app editor, create `~/.cursor/permissions.json`:

```jsonc
{
  "terminalAllowlist": [
    "git",
    "gh",
    "npm",
    "npx",
    "pip",
    "python",
    "pytest",
    "docker",
    "make",
    "curl"
  ]
}
```

This file is per-user (not committed to the repo). It only applies when Auto-Run is enabled. See [Cursor permissions.json reference](https://cursor.com/docs/reference/permissions).

## Per-repo sandbox (advanced)

For network/filesystem sandbox tuning in this workspace, add `.cursor/sandbox.json`. See [sandbox.json reference](https://cursor.com/docs/reference/sandbox).

## What agents must do (repo rules)

When using the Shell tool, agents **always** pass `required_permissions` proactively:

- `git push` / `git pull` / `git fetch` / remote `gh`: `["git_write", "network"]`
- `git add` / `git commit` / checkout / merge: `["git_write"]`
- `npm install`, `pip install`, `docker`, `curl`: `["network"]` or `["all"]` when sandbox blocks the command

Agents must **never** ask in chat to "allow" or "approve" — they invoke Shell with the right permissions immediately.
