# Language Coach — Documentation Portal

Welcome to the comprehensive documentation directory for **Language Coach: AI-Based Multilingual Pronunciation Learning System**.

---

## 1. For My Mentor & Project Evaluators
*High-level architectural overviews, progress audits, and live presentation materials:*

- **[Project Overview](project/OVERVIEW.md)** — One-page executive summary: problem, solution, features, stack, and architecture.
- **[System Architecture](project/ARCHITECTURE.md)** — System topology, Mermaid flow/sequence diagrams, data contracts, and design rationales.
- **[Progress Report](project/PROGRESS_REPORT.md)** — Quantitative progress calculation, timeline (Nov–Apr), risks, and feature completion matrix.
- **[Live Demo Guide](project/DEMO_GUIDE.md)** — 3-minute live demonstration script, preparation checklist, and mentor Q&A.
- **[Product Requirements Document (PRD)](PRD.md)** — Stable data contracts, subsystem boundaries, and architectural decisions.
- **[Academic Report Materials](report/)** — Report outline, literature review, and user testing protocols.

---

## 2. For Teammates & Developers
*Step-by-step installation, troubleshooting, design tokens, and daily collaboration routines:*

- **[Setup & Installation Guide](setup/SETUP.md)** — Zero-to-running local guide with Windows PowerShell, macOS, and Linux instructions.
- **[Troubleshooting Matrix](setup/TROUBLESHOOTING.md)** — Symptom &rarr; Cause &rarr; Fix table for 14+ common environment and audio issues.
- **[Team & Contribution Guide](team/TEAM_GUIDE.md)** — Roles R1–R5, onboarding checklist, daily standup format, and Git routine.
- **[Task Tracker (Single Source of Truth)](TASKS.md)** — Granular task status tables for each role (`DONE`, `DOING`, `TODO`).
- **[Design System Specification](design/DESIGN.md)** — CSS variables, color tokens, glassmorphism components, and accessibility rules.
- **[Visual Design Preview](design/home-preview.html)** — Standalone static HTML preview of the approved user interface.
- **[Screenshot Assets Registry](assets/README.md)** — Registry of required application screenshots.

---

## 3. For AI Assistants (Strict Token-Saving Read Order)
*To conserve token context and prevent hallucinations, AI assistants must follow this strict reading sequence:*

1. `AI_CONTEXT.md` (root directory, 20 lines).
2. `docs/MEMORY.md` (STATUS block + your assigned role's log only; do not read other roles).
3. `docs/TASKS.md` (Header + your assigned role's table only).
4. `docs/PRD.md` (Only the specific numbered section required by your active task).
5. `docs/GUIDELINES.md` (Read once per session for coding and secrets rules).

> **Token-Saving Rule:** Do **NOT** open or read `docs/setup/`, `docs/project/`, `docs/team/`, `docs/design/`, or `docs/report/` unless a user prompt explicitly requests modification of those specific files.
