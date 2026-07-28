# Agent Workflows

## Purpose

This file centralizes how to use AI coding assistants and local scripts without letting every tool invent a new architecture.

## Recommended Routing

| Tool | Best use |
|---|---|
| Codex | Multi-file repo patches, static-site implementation, Vercel-ready code |
| Jules | Issue-driven implementation, cleanup, focused static-site work |
| Cursor | Local full-file editing and interactive refactoring |
| PowerShell | Local filesystem setup, backups, Git sync, static checks |

## Standard Workflow

1. Read `AGENTS.md`.
2. Read the tool-specific file: `CODEX.md`, `JULES.md`, `CURSOR.md`, or `POWERSHELL.md`.
3. Confirm the target folder: `site/`, `widget/`, `knowledge/`, `docs/`, or `scripts/`.
4. Make the smallest useful change.
5. Verify links, paths, and no-secret rules.
6. Summarize deployment impact.

## Do Not Do

- Do not introduce a framework without approval.
- Do not move Vercel root away from `site/` without approval.
- Do not commit private client data.
- Do not make funding guarantees.
- Do not create fake statistics, testimonials, ratings, or recovery claims.
