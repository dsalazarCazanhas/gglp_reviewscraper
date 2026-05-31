# Skill Registry — gglp_reviewscraper

**Project**: gglp-reviewscraper  
**Updated**: 2026-05-05  
**Scope**: Python data pipeline + web scraping  

---

## Available Skills

### Core SDD Workflow

| Skill | Trigger | Purpose |
|-------|---------|---------|
| `sdd-init` | `/sdd-init` | Initialize SDD context and detect stack |
| `sdd-explore` | `/sdd-explore <topic>` | Research and investigate before proposing |
| `sdd-propose` | Auto-invoked after explore | Create proposal with scope and approach |
| `sdd-spec` | `/sdd-spec <change>` | Write delta specs with scenarios |
| `sdd-design` | Auto-invoked after spec | Technical design and architecture decisions |
| `sdd-tasks` | Auto-invoked after design | Break down into implementation tasks |
| `sdd-apply` | `/sdd-apply [batch]` | Implement code from tasks |
| `sdd-verify` | `/sdd-verify [change]` | Validate against specs and design |
| `sdd-archive` | Auto-invoked after verify | Archive completed change |
| `sdd-onboard` | `/sdd-onboard` | Guided walkthrough of SDD workflow |

### Project & Documentation

| Skill | Trigger | Purpose |
|-------|---------|---------|
| `skill-registry` | `/skill-registry` or `update skills` | Scan and update skill registry |
| `cognitive-doc-design` | When writing docs | Design readable, low-cognitive-load documentation |
| `comment-writer` | When writing comments | Write warm, direct PR/issue comments |

### GitHub & Collaboration

| Skill | Trigger | Purpose |
|-------|---------|---------|
| `issue-creation` | When creating issues | GitHub issue workflow |
| `branch-pr` | When creating PRs | PR creation and branch workflow |
| `chained-pr` | When splitting large changes | Split large PRs into manageable slices |
| `address-pr-comments` | When addressing review | Handle review feedback on PRs |

### Review & Quality

| Skill | Trigger | Purpose |
|-------|---------|---------|
| `judgment-day` | `judgment day` or `dual review` | Parallel adversarial dual-agent review |

### Commits & Patterns

| Skill | Trigger | Purpose |
|-------|---------|---------|
| `work-unit-commits` | When planning commits | Structure commits as deliverable work units |

### Testing & Verification

| Skill | Note | Purpose |
|--------|------|---------|
| `go-testing` | Go/Bubbletea only | Not applicable to this Python project |

---

## Project Conventions

**Stack**: Python 3.14+, Poetry, pandas, requests, google-play-scraper  
**Architecture**: Data pipeline (CLI → scraper → DataFrame → CSV)  
**Testing**: No test framework currently installed  
**Strict TDD Mode**: Disabled (no test runner detected)  

---

## Next Steps

- Use `/sdd-new <feature>` to start a new change through the full SDD workflow
- Use `/sdd-explore <topic>` to research before proposing
- Update this registry with `/skill-registry` if new skills are added to the project
