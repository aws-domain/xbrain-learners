# Design Document — Cloud Journey

## Overview

Cloud Journey is a single, self-contained HTML page (`cloud-journey.html`) that renders the XBrain AWS DevOps/CloudOps Foundation Program curriculum as a visual, interactive learning roadmap. It gives students a bird's-eye view of all 10 topic domains, lets them track their personal progress across sessions, drill into each domain's resources, and quickly filter or search for specific topics.

The page has no build step, no server, and no runtime dependencies beyond a modern browser. All CSS and JavaScript live inline in the one file. It reads the file system only through the hardcoded manifest that is baked in at "build" time (i.e., when the file is authored/updated), and persists learner progress entirely in `localStorage`.

**Key goals:**

- Zero-friction access: open via `file://` protocol on any modern desktop or mobile browser.
- Persistent, private progress tracking using `localStorage`.
- WCAG 2.1 AA accessible, fully keyboard-navigable.
- Offline-capable — no external network requests at runtime.
- Immediately useful from day one; adding new repo content only requires updating the domain manifest.

---

## Architecture

### High-Level View

```
┌──────────────────────────────────────────────────────┐
│                  cloud-journey.html                  │
│  ┌─────────────┐  ┌────────────────┐  ┌──────────┐  │
│  │  Manifest   │  │ State Manager  │  │  Render  │  │
│  │  (JS const) │→ │ (localStorage) │→ │  Engine  │  │
│  └─────────────┘  └────────────────┘  └──────────┘  │
│        ↑                                     │       │
│  Static domain                          DOM nodes    │
│  + resource data                        + SVG lines  │
└──────────────────────────────────────────────────────┘
```

Because the file is opened via `file://`, JavaScript cannot read the local file system at runtime (cross-origin security). The domain manifest — the list of all 10 domains with their resources and priority data — is therefore **embedded as a JavaScript constant** inside the HTML file. Updating the manifest means editing `cloud-journey.html` directly, which is an acceptable trade-off for a purely static offline tool.

### Execution Flow

1. **Parse** — Browser parses the single HTML file; inline `<style>` is applied; inline `<script>` runs.
2. **Hydrate state** — `StateManager.load()` reads `localStorage` and returns a `ProgressMap` (domain-id → Progress_State).
3. **Render roadmap** — `RoadmapRenderer.render(manifest, progressMap, filters)` builds DOM nodes and SVG connector lines.
4. **Bind events** — Event delegation on the roadmap container handles click (expand/collapse, progress cycle), keyboard (Enter/Space), filter buttons, and search input.
5. **Persist on change** — Any progress mutation calls `StateManager.save(key, state)` synchronously; DOM is patched in-place without a full re-render.
6. **Filter/search** — Applied as a CSS visibility toggle + connector hide/show; no DOM reconstruction.

### Module Boundaries (all inside one `<script>` tag)

| Module | Responsibility |
|--------|---------------|
| `MANIFEST` | Hardcoded constant — domain metadata, resource lists, priority ranking |
| `StateManager` | `localStorage` read/write with try/catch and fallback in-memory store |
| `RoadmapRenderer` | Build DOM nodes, SVG connectors, progress controls; patch on update |
| `ProgressSummary` | Recompute and update the summary bar |
| `FilterEngine` | Apply filter + search predicates to determine node visibility |
| `AccessibilityLayer` | ARIA attribute management, focus ring enforcement, keyboard routing |

---

## Components and Interfaces

### 1. Domain Node Card

Each domain is rendered as a `<article>` with `role="region"`:

```
┌──────────────────────────────────────────────┐
│  🔵 Rank #2  [not_started ▼]                │
│  04_Networking · 🌐                          │
│  VPC, Subnets, Security Groups, Load Balancers│
│  ──────────────────────────────────────────── │
│  [Resources panel — hidden by default]        │
└──────────────────────────────────────────────┘
```

**Attributes on the `<article>` element:**
- `data-domain-id` — e.g. `"04_Networking"`
- `data-progress` — one of `"not_started"` | `"in_progress"` | `"completed"`
- `data-rank` — integer rank from manifest
- `aria-expanded` — `"true"` | `"false"` for the resources panel

**Progress control** — a `<button>` with `aria-label="Progress: not_started. Click to change."` that cycles states on click and Enter/Space.

**Priority badge** — a `<span>` with `aria-label="Priority rank 2"` and a `<span role="tooltip">` sibling containing the rationale text. The tooltip is shown on badge focus/hover via CSS only (no JS positioning needed for simple inline tooltips).

### 2. Resource Panel

Rendered inside the domain card as a `<div role="region" aria-label="Resources for {domainName}">`. Hidden by default via `aria-hidden="true"` + CSS `display:none`.

Resources are grouped under `<h3>` sub-headings (Notes, Quizzes, Troubleshooting, Practice). Each resource is an `<a href="relative/path/to/file" target="_blank" rel="noopener">`.

When a domain folder has no resources in a category, that category heading is omitted. If the domain has zero resources across all categories, a `<p>No content yet.</p>` placeholder is shown.

### 3. Progress Summary Bar

Fixed or sticky at the top of the page. Contains:
- Three counters: `not_started (N)`, `in_progress (N)`, `completed (N)`
- A `<progress value="40" max="100">40%</progress>` element (native, styled via CSS)
- A congratulatory `<div role="alert" aria-live="polite">` that becomes visible when `completed_count === 10`

### 4. Connector Lines (SVG)

Directional arrows between domain nodes are rendered as `<svg>` elements positioned absolutely behind the node grid. Each connector is a `<path>` with `marker-end` arrowhead. Connectors are `aria-hidden="true"` (decorative). They are redrawn on window resize via a debounced `ResizeObserver`.

On filter/search, connectors between hidden nodes get `visibility:hidden`; the SVG element itself remains in the DOM.

### 5. Filter Controls

A `<fieldset>` with `<legend>Filter by progress</legend>` containing three `<button role="button" aria-pressed="true|false">` toggle buttons (one per Progress_State). Pressing a button toggles that state in/out of the visible set.

A "Clear Filters" `<button>` resets all toggles to `aria-pressed="true"` and clears the search input.

### 6. Search Input

`<input type="search" aria-label="Search domains and resources" maxlength="100">` with a debounced `input` event handler (300 ms timeout).

---

## Data Models

### Domain Manifest (embedded constant)

```js
const MANIFEST = {
  domains: [
    {
      id: "01_Compute",
      number: 1,
      name: "Compute",
      emoji: "⚙️",
      description: "EC2, ECS, Fargate — where your workloads actually run",
      rank: 4,                     // from topic_ranking.md
      rankRationale: "Apps must run somewhere. Always present in every project.",
      resources: [
        {
          type: "note",            // "note" | "quiz" | "troubleshooting" | "practice"
          title: "EC2 Placement Groups",
          path: "01_Compute/notes/placement_groups.md"
        },
        {
          type: "troubleshooting",
          title: "SSH Connection Timeout",
          path: "01_Compute/troubleshooting/ssh_connection_timeout.md"
        }
        // ...
      ]
    },
    // ... all 10 domains
  ],
  // Ordered list of domain IDs for connector rendering
  traversalOrder: [
    "01_Compute",
    "02_Storage",
    "03_Database",
    "04_Networking",
    "05_Security_Identity",
    "06_AI_ML",
    "07_Data_Engineering",
    "08_Serverless_IaC",
    "09_Observability_Operations",
    "10_Cost_Governance"
  ]
};
```

The `traversalOrder` array drives which connector lines are drawn. It follows the numeric folder order, with the option of reordering later without changing domain IDs.

### Progress Map (localStorage)

All keys are prefixed with `cloud-journey:` to avoid collisions.

```
localStorage["cloud-journey:progress:01_Compute"]       = "not_started" | "in_progress" | "completed"
localStorage["cloud-journey:progress:04_Networking"]    = "in_progress"
...
localStorage["cloud-journey:version"]                   = "1"   // for future migration
```

### State Manager Interface

```js
const StateManager = {
  // Returns { "01_Compute": "not_started", "04_Networking": "in_progress", ... }
  load()  → ProgressMap,

  // Persists a single domain's progress; returns true on success, false if storage unavailable
  save(domainId, progressState) → boolean,

  // True when localStorage is available (detected once on init)
  isAvailable → boolean
};
```

`StateManager.load()` initialises missing domain IDs to `"not_started"`, so the caller always receives a complete map for all 10 domains.

### Filter State

```js
const FilterState = {
  visibleStates: Set<"not_started" | "in_progress" | "completed">,  // defaults to all three
  searchQuery: string   // defaults to ""
};
```

`FilterEngine.apply(manifest, progressMap, filterState)` returns a `Set<domainId>` of visible domain IDs.

---

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system — essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Progress persistence round-trip

*For any* domain ID and any valid Progress_State value, saving that state via `StateManager.save()` and then loading it back via `StateManager.load()` SHALL return the same Progress_State.

**Validates: Requirements 2.2, 2.3, 2.5**

---

### Property 2: localStorage key isolation

*For any* call to `StateManager.save()`, the keys written to `localStorage` SHALL all begin with the prefix `"cloud-journey:"`, and no keys outside that prefix SHALL be modified or created.

**Validates: Requirements 2.5**

---

### Property 3: Progress cycle completeness

*For any* starting Progress_State, cycling through the three states by repeatedly triggering the progress control SHALL visit each of the three states (`not_started`, `in_progress`, `completed`) exactly once before returning to the original state.

**Validates: Requirements 2.1**

---

### Property 4: Filter predicate correctness

*For any* `ProgressMap` and any `FilterState`, every domain returned by `FilterEngine.apply()` SHALL have a Progress_State that is a member of `FilterState.visibleStates`; no domain whose Progress_State is NOT in `FilterState.visibleStates` SHALL appear in the result.

**Validates: Requirements 5.1, 5.2**

---

### Property 5: Search substring matching

*For any* non-empty search query string and any domain, `FilterEngine.apply()` SHALL include that domain in the visible set if and only if the domain's name OR any of its resource titles contains the query string as a case-insensitive substring.

**Validates: Requirements 5.3, 5.4**

---

### Property 6: Summary bar accuracy

*For any* `ProgressMap`, the summary bar's `completed_count`, `in_progress_count`, and `not_started_count` displayed SHALL equal the exact counts of domains in each corresponding state in the `ProgressMap`, and `(completed_count / 10) × 100` rounded to the nearest integer SHALL equal the displayed percentage.

**Validates: Requirements 3.1, 3.2**

---

### Property 7: Expand/collapse toggle idempotence

*For any* domain node, toggling its expand state twice (expand then collapse) SHALL leave the DOM in the same state as before the first toggle — in particular, `aria-expanded` SHALL return to its original value and no other domain SHALL have changed its `aria-expanded` state.

**Validates: Requirements 4.1, 4.4**

---

### Property 8: At-most-one-expanded invariant

*For any* sequence of expand-click events across any subset of the 10 domain nodes, at any point in time the count of domain nodes with `aria-expanded="true"` SHALL be at most 1.

**Validates: Requirements 4.5**

---

## Error Handling

### localStorage Unavailable

Detected once at startup with a try/catch write-and-delete probe. If unavailable:

- `StateManager.isAvailable` is set to `false`.
- An in-memory fallback store (a plain JS object) is used for the session.
- A non-blocking inline banner is inserted below the summary bar: `"⚠️ Progress cannot be saved in this browsing mode. Your progress will be lost when you close the tab."` The banner has `role="status"` and `aria-live="polite"`.
- All other functionality works normally.

### Topic_Ranking Data Missing / Corrupt

`MANIFEST` is a hardcoded JS constant, so it cannot be "unavailable" at runtime. If a developer accidentally corrupts the constant, the JavaScript runtime will throw a SyntaxError, which will surface as a blank page. To mitigate:
- A `try/catch` wraps the initial `RoadmapRenderer.render()` call.
- On catch, a visible fallback message is injected: `"Unable to render the roadmap. Please check the browser console for details."`
- Each domain's `rank` and `rankRationale` fields are optional — if absent, priority badges are simply not rendered (Requirement 6.3).

### CDN Font/Icon Failure

Fonts are loaded via a single `<link rel="stylesheet">` CDN call (Google Fonts — Inter). The `<link>` uses `media="print" onload="this.media='all'"` progressive loading. If it fails:
- The CSS `font-family` stack falls back to `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`.
- No layout breaks occur because all sizing uses `rem`/`em` rather than absolute pixel widths dependent on a specific font metric.
- Icons use Unicode emoji characters (inlined in the manifest), which are always available.

### Resize / Connector Recomputation

SVG connector redraws are wrapped in a `try/catch`. On error, connectors are hidden (`visibility:hidden`) rather than leaving a broken SVG fragment. The page remains fully functional without decorative connectors.

---

## Testing Strategy

### Applicability Assessment

This feature is primarily a rendered HTML page. The core interactive logic — `StateManager`, `FilterEngine`, `ProgressSummary` calculations, and the toggle/cycle functions — are **pure or near-pure JavaScript functions** that are highly suitable for property-based testing. UI rendering and connector SVG geometry are best covered by example-based snapshot/integration tests.

### Unit Tests (Vitest)

Target the extracted pure-function modules:

- `StateManager.load()` — seed a mock `localStorage`, verify the returned `ProgressMap`.
- `StateManager.save()` — verify key format, value serialization, return value on full storage error.
- `FilterEngine.apply()` — test filter and search combinations with representative data sets.
- `ProgressSummary.compute(progressMap)` — verify count and percentage arithmetic.
- Progress cycle function — verify the three-step cycle wraps correctly.

### Property-Based Tests (fast-check)

Use [fast-check](https://github.com/dubzzz/fast-check) for JavaScript. Each test runs a minimum of **100 iterations**.

Mapping to design properties:

| Property | Test Description | Arbitraries |
|----------|-----------------|-------------|
| P1 – Progress persistence round-trip | `fc.property(domainIdArb, progressStateArb, ...)` — save then load returns same value | `fc.constantFrom(...domainIds)`, `fc.constantFrom("not_started","in_progress","completed")` |
| P2 – localStorage key isolation | Generate random domain IDs and states; verify no key outside `"cloud-journey:"` prefix is touched | `fc.string()`, `fc.record(...)` |
| P3 – Progress cycle completeness | Generate a starting state; verify three cycles visit all states and return to start | `fc.constantFrom(...)` |
| P4 – Filter predicate correctness | Generate arbitrary `ProgressMap` and `FilterState`; verify output set invariant | `fc.record(...)` with all 10 domain IDs mapped to random states |
| P5 – Search substring matching | Generate random domain names + query strings; verify inclusion/exclusion | `fc.string()`, `fc.array(...)` |
| P6 – Summary bar accuracy | Generate arbitrary `ProgressMap`; verify counts and percentage | `fc.record(...)` |
| P7 – Expand/collapse toggle idempotence | Simulate two toggling events on a DOM node; assert final ARIA state | `fc.constantFrom(...domainIds)` |
| P8 – At-most-one-expanded invariant | Generate random sequence of expand clicks; assert count ≤ 1 after each event | `fc.array(fc.constantFrom(...domainIds))` |

Each test is tagged:
```js
// Feature: cloud-journey, Property 1: Progress persistence round-trip
```

### Integration / Smoke Tests (Playwright)

Run against the actual `cloud-journey.html` opened via `file://` in Chromium:

- **Smoke**: Page loads within 2 seconds (Requirement 7.3).
- **Smoke**: All 10 domain nodes are rendered on load (Requirement 1.1).
- **Integration**: Clicking a progress control changes the visible badge and updates `localStorage` (Requirements 2.1, 2.2).
- **Integration**: Expanding a node shows its resources; expanding another collapses the first (Requirements 4.1, 4.5).
- **Integration**: Filter and search controls hide/show the correct nodes (Requirements 5.1–5.5).
- **Integration**: Summary bar updates after a progress state change (Requirements 3.2, 3.3).
- **Accessibility smoke**: `axe-core` audit run on initial page load reports zero WCAG 2.1 AA violations (Requirement 8.5).

### Manual / Accessibility Verification

Full WCAG 2.1 AA validation requires manual testing with assistive technologies (VoiceOver, NVDA, JAWS). Automated tooling (`axe-core`) catches a large portion of contrast and ARIA issues but does not substitute for manual review.

Keyboard navigation checklist:
- Tab order follows visual left-to-right, top-to-bottom sequence (Requirement 8.1).
- Focus ring visible (≥ 2 px) on all interactive elements (Requirement 8.2).
- Enter/Space expands/collapses nodes and cycles progress (Requirement 8.3).
- Screen reader announces progress control label correctly (Requirement 8.4).
