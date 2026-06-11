---
name: hawk-mobile-ui-builder
description: Build mobile app UI from provided screenshots as pure, reusable presentation components. Use when asked to recreate, copy, implement, decompose, or build mobile screens from screenshots in React Native/Expo, SwiftUI, Flutter, native mobile, or mobile web projects; especially when component placement, screen/page structure, UI-only implementation boundaries, and project-specific UI memory are important.
---

# Hawk Mobile UI Builder

## Overview

Build mobile UI from screenshots by analyzing the visual structure first, confirming reuse and placement with the user, then implementing only presentation-layer components and screens.

This skill is UI-only. Do not implement business logic, data fetching, persistence, analytics, permissions, domain workflows, or global state. When non-UI behavior is needed, leave `TODO:` comments at the exact integration points and report the logic plan separately.

## Start Here

1. Inspect the project before planning:
   - Framework and platform: React Native/Expo, SwiftUI, Flutter, native Android/iOS, or mobile web.
   - Existing screen/page folders, route files, navigation patterns, component folders, style/theme/token files, asset/icon/font locations, and verification commands.
   - Existing reusable components that look relevant to the screenshot.
2. Look for `.codex/mobile-ui-builder.md` in the target project.
   - If it exists, read it before proposing placement.
   - If it does not exist, infer conventions from the repo and create it only after the user confirms placement decisions.
3. Analyze all provided screenshots before writing code.

## Screenshot Analysis

For each screenshot, produce a concise component plan before implementation:

- Target screen/page name.
- Visible sections and layout hierarchy.
- Likely pure reusable components.
- One-off layout pieces.
- Visible text, images, icons, colors, spacing, typography, and component states.
- Proposed screen/page file placement.
- Proposed reusable component placement.
- Non-UI behavior, data, callbacks, navigation, or integration work that must remain TODO-only.

If multiple screenshots are provided, analyze them together first. Group shared components across screenshots, propose shared reusable components once, then describe each screen’s specific composition separately.

If provided screenshots have issues, notify the user before implementation instead of silently guessing or copying broken UI. Screenshot issues include unreadable text, labels that appear clipped or incorrectly displayed, likely unintended element overlap, incoherent spacing, cropped or missing regions, conflicting screenshots, unclear navigation/state, low resolution, hidden content that affects layout, or UI that cannot be inferred safely. Present one recommended path and, when useful, one alternate path:

```markdown
I noticed an issue with the screenshot: `<issue>`.

Recommended:
- `<best next step>` because `<reason>`.

Optional alternate:
- `<alternate path>` if you prefer `<tradeoff>`.

Reply with approval, edits, or a clearer screenshot.
```

If the issue is minor and does not affect the component plan, state the assumption and continue. If it looks like a design/UI defect in the screenshot, recommend the most likely intended correction instead of reproducing the defect blindly. If it affects layout, component reuse, theme values, or TODO boundaries, wait for the user’s decision.

Use these fidelity priorities:

- Must match: hierarchy, spacing rhythm, typography scale, colors, and major shapes.
- Approximate: exact shadows, native font rendering, and tiny icon differences.
- Do not fake: real behavior, real data, hidden interactions, or any non-UI implementation.

Infer colors, spacing, typography, radius, and elevation from screenshots, then map them to existing project tokens before adding values. Use existing theme values when they are close matches. Add missing values only to the project’s existing theme/token system and only when needed. If no theme/token system exists, recommend a minimal one and ask before creating it.

Keep the plan short and concrete. Prefer the project’s existing terms for screens, components, widgets, views, routes, modules, and features.

Use this template:

```markdown
Screen: `<name>`
Placement: `<proposed screen/page path>`

Reusable components:
- Create `<ComponentName>` in `<proposed path>` because `<reason>`.
- Reuse `<ExistingComponent>` from `<path>` for `<part of screenshot>`.

Screen-only sections:
- `<section>` -> `<notes>`

Existing UI to check:
- `<component/token/asset>`

TODO-only logic:
- `<behavior>` -> `<planned prop/callback/TODO location>`
```

## Required User Checkpoint

After screenshot analysis and before creating or editing UI files, suggest a concrete path and let the user approve, modify, or discuss it.

Prefer suggestions over open-ended questions. Propose one recommended path and, only when genuinely useful, one alternate path.

Use this checkpoint format:

```markdown
I recommend:
- Put the screen at `<path>` because `<repo convention>`.
- Create `<ComponentName>` in `<path>` because `<reason>`.
- Reuse `<ExistingComponent>` from `<path>` for `<part of screenshot>`.
- Save these conventions to `.codex/mobile-ui-builder.md`: `<rules>`.

Optional alternate:
- `<different placement/reuse approach>` if you prefer `<tradeoff>`.

Reply with approval, edits, or questions.
```

The checkpoint must confirm:

- Whether the recommended placement is right.
- Whether any proposed new component already exists.
- Whether the alternate path is preferred.
- Which confirmed placement rules and project conventions should be saved in `.codex/mobile-ui-builder.md`.
- Any screenshot-specific ambiguity.

Do not skip this checkpoint unless the user has already provided these answers in the current request or the project memory file clearly answers them.

If `.codex/mobile-ui-builder.md` clearly answers placement and reuse conventions, do not ask those questions again. Only ask about screenshot-specific ambiguities or newly proposed components.

If the user says “looks good,” “go with your recommendation,” or equivalent, proceed without another confirmation loop. Ask again only when a new ambiguity affects placement, component reuse, UI fidelity, theme creation, or non-UI scope.

## Project Memory

Use `.codex/mobile-ui-builder.md` as durable, project-local memory.

- Read it at the start of every run when present.
- Create or update it after the user confirms placement or project-specific UI conventions.
- Store only durable UI-building facts:
  - reusable component directories
  - screen/page directories
  - asset, icon, and font locations
  - styling, token, and theme conventions
  - naming conventions
  - known existing reusable components
  - preferred verification commands
  - project-specific UI-only boundaries

Keep the memory file brief. Do not store transient screenshot analysis, one-off implementation notes, secrets, user preferences unrelated to UI building, or copied source code.

Suggested structure:

```markdown
# Mobile UI Builder Map

## Placement
- Reusable components:
- Screens/pages:
- Assets/icons/fonts:

## Styling
- Tokens/theme:
- Naming:

## Existing UI
- Components:

## Verification
- Commands:

## Boundaries
- UI-only notes:
```

## Implementation Rules

- Implement only UI directly related to the screenshot: layout, styling, component composition, static placeholder data, visible presentational states, and simple local UI-only toggles needed for preview.
- Make components as pure as practical: props in, UI out.
- Prefer existing project components, tokens, styles, assets, and naming conventions.
- Create reusable components for repeated or semantically meaningful UI, not every individual visual atom.
- Keep screen/page files focused on composition.
- Avoid one large screenshot-shaped file unless the project already uses that pattern.
- Do not invent app workflows or domain behavior.
- Do not wire real data, networking, persistence, analytics, permissions, or global state.
- Do not add new dependencies unless the user explicitly approves them.

Before proposing a new reusable component, search for existing buttons, cards, list rows, headers/nav bars, tabs, chips, badges, empty states, loading states, tokens, assets, and icons that could be reused or adapted.

Name new reusable components so they are searchable and project-agnostic unless the app already has a strong domain-specific component naming convention. Prefer UI-role names such as `ProfileHeader`, `MetricCard`, `ActionRow`, `StatusBadge`, `EmptyState`, and `PrimaryAction`. Avoid one-off or screenshot-specific names such as `HomeTopBlueThing` or `CheckoutScreenshotCard`. Use domain-specific names only when the component represents a reusable domain concept in the app.

When logic is needed:

- Expose props or callback props where the UI needs data or actions.
- Add `TODO:` comments exactly where the missing behavior belongs.
- Keep TODOs specific, for example `TODO: Wire this action to the saved payment method flow.`
- Include a short logic implementation plan in the final response instead of implementing the logic.

## Verification

Run the project’s normal build, typecheck, or test command when available. Scale visual verification to the size of the change: use full preview/simulator/browser screenshot verification for complete screens or high-impact layout work, and use lightweight inspection plus build/typecheck for small component-only changes. When visual verification is practical, capture or inspect the implemented UI and compare it against the provided screenshot. Report the evidence used: simulator screenshot path, browser screenshot path, preview command, inspected viewport, or the reason visual verification was not practical.

Report verification concisely:

- `Build: pass/fail/not run`
- `Visual copy: pass/fail/not verified`
- `Logic: not implemented; TODOs added` when applicable

When `Logic: not implemented; TODOs added` applies, list each TODO location with file, component/function, and the missing behavior.

If anything fails, include only the main mismatch or the next fix needed.

Use this final response template:

```markdown
Build: pass/fail/not run
Visual copy: pass/fail/not verified
Logic: not implemented; TODOs added/not needed
Project memory: updated/not updated

Changed UI:
- `<file>`: `<what changed>`

TODO logic:
- `<file>` `<component/function>`: `<missing behavior>`
```

For small successful changes with no TODO logic, use a compact final instead:

```markdown
Build: pass. Visual copy: verified via `<evidence>`. Updated `<files>`.
```

## Example

If a screenshot shows a mobile finance home screen with a header, balance card, transaction list, and bottom CTA:

- Plan `ScreenHeader`, `BalanceCard`, `TransactionRow`, and `PrimaryAction` as reusable components if similar UI repeats or already exists.
- Keep account fetching, transaction loading, and button actions out of scope.
- Expose balance, transactions, loading/empty states, and CTA callbacks as props.
- Add `TODO:` comments where those props or callbacks need real app wiring.
- Keep the screen/page file focused on composing the pure UI components.
