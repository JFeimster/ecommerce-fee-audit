# CURSOR.md

## Role

Use Cursor for local, multi-file editing across the static site, documentation, product docs, and embed architecture.

## Local Path

```text
C:\Users\jason\OneDrive\Desktop\The Prompt Lab\AI Platform Fee Audit Copilot
```

## Cursor Context Files

Open these first:

1. `AGENTS.md`
2. `PROJECT_CONTEXT.md`
3. `REPO_STRUCTURE.md`
4. `site/index.html`
5. `site/styles.css`
6. `site/script.js`
7. `site/embed.html`

## Editing Rules

- Use full-file edits when changes are broad.
- Avoid hunting-and-pecking one-line edits across multiple files.
- Keep public site files in `site/`.
- Keep portable embeds in `widget/` or `site/embed.html`.
- Keep product and sales documentation in `knowledge/`.
- Keep scripts in `scripts/`.
- Do not add real client financial data.
- Do not add credentials or `.env` files.

## Recommended Cursor Prompt

```text
You are editing the local repo:
C:\Users\jason\OneDrive\Desktop\The Prompt Lab\AI Platform Fee Audit Copilot

Read AGENTS.md, PROJECT_CONTEXT.md, and REPO_STRUCTURE.md first.

Task:
[describe task]

Rules:
- Preserve the static Vercel architecture under site/.
- Use vanilla HTML/CSS/JS.
- Keep copy compliance-safe.
- Provide complete changed files or a clear patch.
- Do not add secrets, private data, or real financial exports.
```

## Local QA

Before committing from Cursor, check:

- `site/index.html` opens locally.
- `site/embed.html` opens locally.
- CSS and JS paths are relative and valid.
- Mobile width does not overflow.
- No private files are staged.
