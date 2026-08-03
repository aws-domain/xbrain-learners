# Requirements Document

## Introduction

The **Cloud Journey** feature is an interactive learning roadmap for the XBrain AWS DevOps/CloudOps Foundation Program repository. It gives learners a single, visual overview of the full curriculum — spanning all 10 topic domains — and lets them track their personal progress as they move from beginner concepts through to advanced CloudOps practices.

The feature lives as a standalone HTML page (`cloud-journey.html`) that integrates with the existing repo structure. It reads the domain folders (`01_Compute` through `10_Cost_Governance`) and the `Others/topic_ranking.md` file to derive path ordering and priority context, rendering a node-based roadmap where each node represents a topic domain or a key resource (note, quiz, practice lab). Learners can mark items complete, view their overall progress, and navigate directly to the relevant files.

---

## Glossary

- **Cloud_Journey**: The feature described in this document — a visual, interactive learning-path roadmap for the XBrain curriculum.
- **Domain**: One of the 10 numbered topic folders in the repository (e.g., `01_Compute`, `05_Security_Identity`).
- **Roadmap**: The directed graph of Domains rendered as connected nodes with a recommended traversal order.
- **Node**: A visual card on the Roadmap representing a single Domain or Resource.
- **Resource**: A file inside a Domain folder — note, quiz, troubleshooting guide, or practice lab.
- **Learner**: A student enrolled in the XBrain AWS DevOps/CloudOps Foundation Program who uses this repository.
- **Progress_State**: The completion status of a Node — one of `not_started`, `in_progress`, or `completed`.
- **Progress_Store**: The browser localStorage object used to persist a Learner's Progress_State entries.
- **Topic_Ranking**: The priority ordering of Domains sourced from `Others/topic_ranking.md`, used to suggest the recommended traversal sequence.
- **Portal**: The Cloud Learning Portal (`cloud-journey.html`) — the HTML page that renders the Cloud Journey feature.
- **Filter**: A UI control that limits which Nodes are visible on the Roadmap (e.g., by Domain category or Progress_State).
- **Search**: A text input that narrows visible Nodes to those whose title or content matches a query string.

---

## Requirements

### Requirement 1: Render the Learning Roadmap

**User Story:** As a Learner, I want to see all 10 AWS topic domains laid out as a connected roadmap, so that I understand the full curriculum scope and the recommended learning sequence at a glance.

#### Acceptance Criteria

1. THE Portal SHALL render all 10 Domains as Nodes arranged in a directed, top-to-bottom Roadmap on initial page load.
2. THE Portal SHALL display each Node with the Domain number, Domain name, a representative emoji/icon, and a short one-line description.
3. THE Portal SHALL draw directional connectors between Nodes that reflect the recommended traversal sequence from the Topic_Ranking data.
4. WHEN the Roadmap contains more than 5 Nodes in a single column, THE Portal SHALL wrap Nodes into a two-column grid to avoid excessive vertical scrolling on desktop viewports ≥ 1024 px wide.
5. THE Portal SHALL be fully usable on mobile viewports ≥ 320 px wide, displaying Nodes in a single-column vertical list.

---

### Requirement 2: Track and Persist Learner Progress

**User Story:** As a Learner, I want to mark domains and resources as "in progress" or "completed" and have the portal remember my choices, so that I can return to my learning journey across browser sessions without losing my progress.

#### Acceptance Criteria

1. THE Portal SHALL display a progress control on each Node that allows the Learner to cycle through the three Progress_States: `not_started` → `in_progress` → `completed`.
2. WHEN a Learner changes a Node's Progress_State, THE Portal SHALL update the Progress_Store within 100 ms and re-render the Node's visual state immediately.
3. THE Portal SHALL load all previously saved Progress_State values from the Progress_Store on page load, applying them to their corresponding Nodes before the first render is shown.
4. IF the Progress_Store is unavailable (e.g., private browsing mode), THEN THE Portal SHALL display a non-blocking inline warning informing the Learner that progress will not be saved, and SHALL continue operating normally for the current session.
5. THE Portal SHALL persist Progress_State data exclusively in browser localStorage under the key prefix `cloud-journey:` to avoid key collisions with other features.

---

### Requirement 3: Display an Overall Progress Summary

**User Story:** As a Learner, I want to see a summary bar showing how many domains I have completed, so that I feel motivated and can quickly gauge how far through the curriculum I am.

#### Acceptance Criteria

1. THE Portal SHALL display a summary bar at the top of the Roadmap showing the count of Domains in each Progress_State and a percentage completion figure calculated as `(completed_count / total_domain_count) × 100`, rounded to the nearest integer.
2. WHEN the Learner changes any Node's Progress_State, THE Portal SHALL update the summary bar within 200 ms to reflect the new totals.
3. THE Portal SHALL display a filled progress indicator (e.g., progress bar or arc) whose filled length is proportional to the percentage completion figure.
4. WHEN all 10 Domains reach `completed` Progress_State, THE Portal SHALL display a congratulatory message to the Learner.

---

### Requirement 4: Expand a Domain Node to See Its Resources

**User Story:** As a Learner, I want to expand a domain node to see all the notes, quizzes, and practice labs it contains, so that I can navigate directly to the specific file I want to study.

#### Acceptance Criteria

1. WHEN a Learner clicks a Domain Node, THE Portal SHALL toggle an expanded panel beneath the Node listing all Resources found in the Domain's folder, grouped by sub-category (Notes, Quizzes, Troubleshooting, Practice).
2. THE Portal SHALL display each Resource as a clickable link that opens the corresponding file in a new browser tab when activated.
3. WHEN a Domain folder contains zero Resources, THE Portal SHALL display a placeholder message "No content yet" inside the expanded panel.
4. WHEN a Learner clicks a Domain Node that is already expanded, THE Portal SHALL collapse the panel.
5. THE Portal SHALL allow at most one Domain Node to be expanded at a time; expanding a second Node SHALL automatically collapse the previously expanded Node.

---

### Requirement 5: Filter and Search Nodes

**User Story:** As a Learner, I want to filter the roadmap by progress state and search for topics by keyword, so that I can quickly focus on what I need to study next.

#### Acceptance Criteria

1. THE Portal SHALL provide Filter controls that allow the Learner to show only Nodes matching one or more selected Progress_States (`not_started`, `in_progress`, `completed`).
2. WHEN a Filter is applied, THE Portal SHALL hide all Nodes whose Progress_State is not in the selected set; directional connectors between hidden Nodes SHALL also be hidden.
3. THE Portal SHALL provide a Search input that accepts a query string of 1 to 100 characters.
4. WHEN a Learner types in the Search input, THE Portal SHALL update the visible Nodes within 300 ms to show only Nodes whose Domain name or Resource titles contain the query string (case-insensitive substring match).
5. WHEN no Nodes match the active Filter and Search combination, THE Portal SHALL display a "No results found" message in the Roadmap area.
6. THE Portal SHALL provide a "Clear Filters" control that resets all active Filters and the Search input to their default states.

---

### Requirement 6: Display Topic Priority Context

**User Story:** As a Learner, I want to see which domains are highest priority for real-world DevOps work, so that I can make informed decisions about where to invest study time.

#### Acceptance Criteria

1. THE Portal SHALL render a visible priority badge on each Domain Node showing its rank from the Topic_Ranking data (e.g., "Rank #1", "Rank #5").
2. THE Portal SHALL display a tooltip or expandable callout on each priority badge containing the rationale text from the Topic_Ranking data for that Domain.
3. WHEN the Topic_Ranking data is unavailable or cannot be parsed, THE Portal SHALL render Domain Nodes without priority badges and SHALL NOT display an error page.

---

### Requirement 7: Self-Contained, Static HTML Delivery

**User Story:** As a Learner, I want to open the Cloud Journey directly from the file system in any modern browser without running a server, so that I can use it offline or share it with classmates easily.

#### Acceptance Criteria

1. THE Portal SHALL be delivered as a single self-contained HTML file (`cloud-journey.html`) at the repository root with all CSS and JavaScript inlined or bundled within the file.
2. THE Portal SHALL function correctly when opened via the `file://` protocol in Chrome ≥ 108, Firefox ≥ 108, and Safari ≥ 16 without requiring a local HTTP server.
3. THE Portal SHALL load and render the initial Roadmap within 2 seconds on a modern laptop (≥ 2018, SSD) when opened from local disk.
4. THE Portal SHALL NOT make any outbound network requests to external domains; all assets (fonts, icons, styles) SHALL be embedded inline or sourced from CDN links that gracefully degrade when offline.
5. WHERE a CDN asset fails to load, THE Portal SHALL fall back to a system font stack and continue rendering without broken layout.

---

### Requirement 8: Accessible and Keyboard-Navigable Interface

**User Story:** As a Learner, I want to navigate the entire roadmap using only a keyboard, so that the portal is usable regardless of input method or accessibility need.

#### Acceptance Criteria

1. THE Portal SHALL assign a logical tab order to all interactive elements (Node cards, progress controls, Filter buttons, Search input, Resource links) following the visual left-to-right, top-to-bottom reading sequence.
2. WHEN a Node or control receives keyboard focus, THE Portal SHALL display a clearly visible focus indicator with a minimum 2 px contrast border.
3. WHEN the Enter key or Space key is pressed on a focused Node, THE Portal SHALL perform the same expand/collapse action as a mouse click.
4. THE Portal SHALL provide ARIA labels on all icon-only buttons and progress controls so that screen readers announce their purpose.
5. THE Portal SHALL meet WCAG 2.1 Level AA colour contrast requirements for all text-on-background combinations used in the interface.
