# UI_Test - Visual QA Pipeline with Claude Code

> A visual QA execution pipeline built around Claude Code hooks and Playwright MCP.
> Instead of presenting it as a fully autonomous agent system, this repository documents what is automated, what is measured, and where human QA judgment is still required.

## Data Disclaimer

All target sites in this repository are public demo sites, such as `practicesoftwaretesting.com`. No current or former company or customer service URL, screen, internal data, or production workflow is included. `targets.json` is the source of truth for the inspected URLs.

## Problem

Visual QA work often includes repeated manual checks across desktop, tablet, and mobile viewports. It also requires consistent evidence: screenshots, console logs, and issue summaries.

This project aims to make the repeated parts automatic while keeping the human decision point clear: QA decides what should be inspected by editing `targets.json`.

## What Was Built

| Component | Role |
| --- | --- |
| Playwright MCP calls | Open pages, inspect viewports, capture screenshots, and gather browser evidence |
| Claude Code hooks | Add guardrails around execution, reporting, session summaries, and optional notifications |
| `targets.json` | Defines the public demo sites and focus areas |
| Standard output folders | Stores `SUMMARY.md`, issue details, screenshots, and reports in a repeatable structure |

## Hook Design

| Hook | Timing | Purpose |
| --- | --- | --- |
| `PreToolUse` | Before browser navigation | Checks target availability and blocks unavailable targets |
| `PostToolUse` | After result files are written | Generates reports and can create follow-up records |
| `Stop` | When Claude finishes | Summarizes PASS/FAIL/WARN counts |
| `SessionStart` | When a session starts | Shows the latest result and next target context |

The important design point is that the inspection procedure and side effects are kept outside the model's main reasoning flow.

## Inspection Areas

| Category | Checks |
| --- | --- |
| Page loading | HTTP response and resource loading |
| Layout/UI | Broken layout, overlap, alignment, clipped text |
| Navigation | Menu and link behavior |
| Forms/interactions | Input, buttons, validation messages |
| Responsive layout | Desktop, tablet, and mobile viewports |
| Content | Images and text rendering |
| Error handling | Invalid input and console errors |

## Severity Guide

| Level | Criteria |
| --- | --- |
| P1 Critical | Core function is blocked |
| P2 Major | Major feature damage, responsive breakage, or console error |
| P3 Minor | Text clipping, visual polish issue, or UX inconvenience |

## Quick Start

Edit `targets.json` with public demo targets only:

```json
{
  "targets": [
    {
      "url": "https://your-public-demo-site.example",
      "name": "demo_site",
      "focus": ["responsive", "login", "search"]
    }
  ]
}
```

Then run in Claude Code:

```text
Read targets.json and run a QA inspection.
```

## Outputs

After an inspection, the pipeline stores:

- `[date]_[domain]/SUMMARY.md` - issue summary report
- `[date]_[domain]/issues/ISSUE-XXX_*/` - issue details and screenshots
- `report.html` - generated HTML report when enabled

## QA Value

| Manual approach | Pipeline approach |
| --- | --- |
| Manually capture every viewport | Capture desktop/tablet/mobile evidence in a repeatable way |
| Result format changes by person | `SUMMARY.md` and `issues/` follow a standard structure |
| Evidence is scattered in chat or email | Git history can preserve inspection outputs over time |

The value is less about one inspection and more about quality changes over time.

## Outcome

| Item | Measurement |
| --- | --- |
| One site across three viewports | Manual about 25 to 30 minutes -> automated about 5 to 8 minutes |
| Output consistency | Same `SUMMARY.md` plus `issues/` structure each run |
| Traceability | Results can be tracked through git history |
| Human input point | Edit `targets.json` once per target set |

## Limits

- This is not a complete agentic QA system. It is a Claude Code hook plus Playwright MCP pipeline.
- Judgment accuracy has not been fully benchmarked. False positives and false negatives still need measurement.
- Targets should remain public demo sites unless a separate security review is done.
- Runtime cost depends on Claude reasoning and inspection frequency.

## Tech Stack

| Technology | Purpose |
| --- | --- |
| Claude Code | Execution environment |
| Claude Code skill | Inspection procedure and output format |
| Claude Code hooks | Guardrails and post-processing |
| Playwright MCP | Browser automation |
| Git | Versioned evidence and result tracking |

## Roadmap

- Add false-positive and false-negative benchmark cases
- Visualize quality trends across repeated inspections
- Add a separate secure mode for authenticated demo targets