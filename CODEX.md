# CODEX.md

## Role

Use Codex for codebase edits, static-site implementation, embed refinement, repo hygiene, and repeatable development tasks.

## Default Task Context

Repository: `JFeimster/ecommerce-fee-audit.vercel.app`

Local project path:

```text
C:\Users\jason\OneDrive\Desktop\The Prompt Lab\AI Platform Fee Audit Copilot
```

Vercel root directory:

```text
site
```

## Codex Rules

- Do not rename the repo or local root folder unless explicitly asked.
- Do not convert the static site into React, Next.js, Astro, or another framework unless explicitly requested.
- Preserve `site/index.html`, `site/styles.css`, `site/script.js`, and `site/embed.html` as the public static shell.
- Keep embeds portable and iframe-friendly.
- Use vanilla HTML, CSS, and JavaScript by default.
- Do not add npm packages without a specific reason.
- Do not commit secrets, credentials, private uploads, or real customer financial data.

## Recommended Codex Prompt

```text
You are working inside the existing repository:
C:\Users\jason\OneDrive\Desktop\The Prompt Lab\AI Platform Fee Audit Copilot

Repository:
https://github.com/JFeimster/ecommerce-fee-audit.vercel.app

Goal:
[describe task]

Rules:
- Preserve the static site architecture under site/.
- Use plain HTML, CSS, and JavaScript unless I explicitly ask otherwise.
- Keep Vercel root directory as site/.
- Keep embeds portable for Wix and WordPress.
- Do not commit private financial data, credentials, or real client exports.
- Use compliance-safe funding language.
- Provide full changed files, not vague snippets.
```

## Output Expectations

Codex should report:

- files changed
- commands run
- tests or checks performed
- deployment impact
- any assumptions or unresolved questions
