---
name: hawk-mobile-ui-builder
description: >-
  Build mobile app UI from provided screenshots as pure, reusable presentation
  components with directly relevant presentation states. Use only when the user
  explicitly invokes or names
  `hawk-mobile-ui-builder`, including `$hawk-mobile-ui-builder` and
  `/hawk-mobile-ui-builder`. Do not auto-trigger from an ordinary request to
  recreate, copy, implement, decompose, or build mobile UI from screenshots when
  that skill name is absent.
---

# Hawk Mobile UI Builder

## Overview

Build the provided UI and its directly relevant presentation states. Analyze the visual structure and requested scope first, resolve reuse and placement from project evidence or user clarification, then implement presentation-layer components or screens. Expose callbacks for actions; do not expand an action into its destination screen or downstream workflow. A screenshot is a reference for the pictured state, not an exhaustive specification of presentation states.

This skill is UI-only. Do not implement business logic, data fetching, persistence, analytics, permissions, domain workflows, or global state. When non-UI behavior is needed, leave `TODO:` comments at the exact integration points and report the logic plan separately.

## Clarify ambiguous requests

Resolve material ambiguity before acting on a user message.

- Inspect the current message, relevant recent chat context, and available project evidence before asking.
- If one reasonable interpretation is low-risk and does not materially change scope, behavior, files, output, or external state, state the assumption and continue.
- If two or more plausible interpretations would lead to materially different work, pause and ask a targeted clarification. Name the likely meanings and their practical difference; prefer “Did you mean A or B?” over “Can you clarify?”
- Use the host's questions or structured user-input tool when available. Offer 2–3 mutually exclusive choices, put the recommended interpretation first when evidence supports one, and allow a free-form answer when the host supports it. Otherwise ask the same concise question in normal chat.
- Ask only the smallest set of blocking questions. Do not repeat questions answered by the request or context, and do not treat ambiguity as permission to broaden scope or make a consequential change.

## Start Here

1. Inspect the project before planning:
   - Framework and platform: React Native/Expo, SwiftUI, Flutter, native Android/iOS, or mobile web.
   - Existing screen/page folders, route files, navigation patterns, component folders, style/theme/token files, asset/icon/font locations, and verification commands.
   - Existing reusable components that look relevant to the screenshot.
2. Look for `.codex/mobile-ui-builder.md` in the target project.
   - If it exists, read it before proposing placement.
   - If it does not exist, infer conventions from the repo and create it after placement is settled through repository evidence or user confirmation.
3. Analyze all provided screenshots before writing code.

## Screenshot Analysis

For each screenshot, produce a concise component plan before implementation:

- Target component or screen/page name and requested scope, grounded in the request, screenshot, and relevant existing code.
- Visible sections and layout hierarchy.
- Likely pure reusable components.
- One-off layout pieces.
- Visible text, images, icons, colors, spacing, typography, and component states.
- Proposed screen/page file placement.
- Proposed reusable component placement.
- Non-UI behavior, data, callbacks, navigation, or integration work that must remain TODO-only.

### State scope

Distinguish the presentation being requested from the workflow behind its actions:

- **Component:** consider its appearance and supported interaction states, not the surrounding screen's lifecycle. A clickable card needs its default appearance, pressed feedback, and an `onPress` callback. Clickability alone does not justify loading, success, error, or disabled states, navigation wiring, or building the destination screen.
- **Screen:** consider states directly tied to the content and controls being built. Existing fetched content can justify loading, populated, empty, and load-error presentations; a supported form submission can justify pending and supplied-error presentations. For a narrow edit, consider only affected states rather than expanding to the whole screen.

Each additional state needs a concrete reason in the request, reference, or existing code. Inspect relevant data/action contracts where available. If a screen's data source or action behavior is not established, propose loading/error support as an assumption rather than automatically adding it. Do not invent workflows, business rules, or backend capabilities. Refresh, pagination, offline, permission, and success states belong only where supported; no universal state checklist applies to every component or screen.

Add a brief **State scope** to the existing component plan: what is being built, selected states with their reasons and controlling props, and the action callbacks where presentation ends. Mark states inferred beyond the screenshot and style them consistently with existing patterns and the reference. State ordinary presentation assumptions and proceed; ask only when an unresolved product decision materially changes scope or behavior. Do not add a separate state-approval checkpoint.

Keep the state model proportional. Reuse existing types and conventions; avoid contradictory combinations such as a full-screen initial loader and empty state at once. When supported, distinguish no search results from an empty collection, and refresh from initial loading. Preserve usable content or entered values during refresh and action failures. Model independent sections separately only when they can actually load or fail independently.

Implement these states as renderable UI controlled by props, with callbacks for supported actions such as retry or submit. Rendering an externally supplied error is UI work; deciding validation rules, issuing requests, retrying, or transitioning real application state is integration work. Disable repeated submission while pending and expose busy, disabled, and error semantics through the framework's accessibility conventions.

Make selected states reproducible using the project's existing preview/story/example mechanism or a small development-only harness when needed. Simple interaction states can be exercised directly; do not create a fixture framework for a clickable card. Keep mock data and state controls out of production behavior; no fake network timers, random failures, or new preview dependencies are needed. Preview the actual components that later integration will consume.

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

Use this template, omitting empty or redundant sections. For a small component, summarize placement, states, and the callback boundary in a few lines.

```markdown
Component/screen: `<name>`
Placement: `<proposed screen/page path>`

Reusable components:
- Create `<ComponentName>` in `<proposed path>` because `<reason>`.
- Reuse `<ExistingComponent>` from `<path>` for `<part of screenshot>`.

Screen-only sections:
- `<section>` -> `<notes>`

Existing UI to check:
- `<component/token/asset>`

State scope:
- Building: `<component or screen; requested boundary>`
- States: `<selected states, reasons, and controlling props; mark inferred states>`
- Action boundary: `<callbacks exposed; downstream behavior left to integration>`

TODO-only logic:
- `<behavior>` -> `<planned prop/callback/TODO location>`
```

## Placement and clarification checkpoint

After screenshot analysis, settle placement and reuse before creating or editing UI files. Established repository conventions and a completed search for reusable components can satisfy this checkpoint, as can prior user answers or clear project memory. State the chosen path and proceed when these resolve the decision; ask only when material ambiguity or a genuinely new convention remains.

Prefer suggestions over open-ended questions. Propose one recommended path and, only when genuinely useful, one alternate path.

When user input is needed, use the relevant parts of this checkpoint format:

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

Resolve these points from available evidence; ask only about unresolved material decisions:

- Whether the recommended placement is right.
- Whether any proposed new component already exists.
- Whether the alternate path is preferred.
- Which confirmed placement rules and project conventions should be saved in `.codex/mobile-ui-builder.md`.
- Any screenshot-specific ambiguity.

Do not ask the user to repeat settled placement or reuse decisions. A newly proposed component following established conventions does not itself require confirmation after the reuse search.

If the user says “looks good,” “go with your recommendation,” or equivalent, proceed without another confirmation loop. Ask again only when a new ambiguity affects placement, component reuse, UI fidelity, theme creation, or non-UI scope.

## Project Memory

Use `.codex/mobile-ui-builder.md` as durable, project-local memory.

- Read it at the start of every run when present.
- Create or update it with placement or project-specific UI conventions established by repository evidence or user confirmation.
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

- Implement UI for the requested component or screen and its selected presentation states: layout, styling, component composition, preview fixtures where useful, and simple local UI-only toggles needed for preview.
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
- Finish the presentation for each selected state; do not leave loading, empty, error, or pending UI as TODOs.
- Add `TODO:` comments at actual integration boundaries where missing behavior belongs, not inside pure components merely because their props will later come from real data.
- Keep TODOs specific, for example `TODO: Wire this action to the saved payment method flow.`
- Include a short integration handoff with the state props, action callbacks, fixture/preview locations, and missing behavior. Reuse existing code/types as the contract rather than creating a separate handoff document. Later feature work should be able to supply data and actions without rebuilding these states.

## Verification

Run the project’s normal build, typecheck, or test command when available. Scale visual verification to the size of the change: use full preview/simulator/browser screenshot verification for complete screens or high-impact layout work, and use lightweight inspection plus build/typecheck for small component-only changes. When visual verification is practical, capture or inspect the implemented UI and compare it against the provided screenshot. Report the evidence used: simulator screenshot path, browser screenshot path, preview command, inspected viewport, or the reason visual verification was not practical.

Exercise each selected state directly or through its fixtures. Compare the reference state at the intended viewport; inspect inferred states for consistency and, where applicable, usable recovery actions, preserved content/input, and stable layout with representative long text and errors. For forms, check keyboard visibility and action reachability. Verify that pending submissions cannot be repeated and available callbacks fire as intended, without claiming the underlying operation works. Correct material visual mismatches and recheck affected states. Report which states were exercised and which remain unverified; a successful typecheck alone does not verify their appearance or interaction.

Report verification concisely:

- `Build: pass/fail/not run`
- `Visual copy: pass/fail/not verified`
- `UI states: <implemented states; exercised states and evidence, or unverified>`
- `Logic: not implemented; TODOs added` when applicable

When `Logic: not implemented; TODOs added` applies, list each TODO location with file, component/function, and the missing behavior.

If anything fails, include only the main mismatch or the next fix needed.

Use this final response template:

```markdown
Build: pass/fail/not run
Visual copy: pass/fail/not verified
UI states: <implemented; exercised/unverified; fixture/preview location>
Logic: not implemented; TODOs added/not needed
Project memory: updated/not updated

Changed UI:
- `<file>`: `<what changed>`

TODO logic:
- `<file>` `<component/function>`: `<missing behavior; state props/action callbacks to wire>`
```

For small successful changes with no TODO logic, use a compact final instead:

```markdown
Build: pass. Visual copy: verified via `<evidence>`. Updated `<files>`.
```

## Examples

For a requested clickable transaction card, build its reference appearance and pressed feedback, expose `onPress`, and verify that callback. Do not infer a loader or build a transaction-details screen. Add other states only when supported by the request or existing component behavior.

If the request is for a mobile finance home screen backed by existing queries, with a header, balance card, transaction list, and bottom CTA:

- Plan `ScreenHeader`, `BalanceCard`, `TransactionRow`, and `PrimaryAction` as reusable components if similar UI repeats or already exists.
- Keep account fetching, transaction loading, and button actions out of scope.
- Build initial loading, populated, no-transactions, and load-failure presentations using the existing loading ownership (whole screen or independent sections). Add refresh presentation only if refresh is supported.
- Expose balance, transactions, selected state, and supported retry/CTA callbacks as props; provide deterministic previews for those states. An empty transaction list should not hide an available balance.
- Add `TODO:` comments where those props or callbacks need real app wiring.
- Keep the screen/page file focused on composing the pure UI components.
