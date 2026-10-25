# Capabilities Matrix (S0 - S22 Lifecycle Mapping)

This document provides an explicit mapping between the **S0-S22 engineering lifecycle stages** and the three categories of executable assets: **Tool (Scripts/CLI)**, **Knowledge (Schemas/Guides)**, and **Skill (Workflows)**.

## Asset Classifications

* **Tool**: Executable Python helper scripts (`scripts/`). Hard gates and enforcement commands.
* **Knowledge**: Structured documentation, templates, pain-point cards, and JSON schemas (`references/`).
* **Skill**: Procedural guidance and agent workflow triggers defined in `SKILL.md`.

## Full Lifecycle Asset Matrix

| Lifecycle Stage | Stage Name | Category | Primary Asset | Secondary Reference / Tool |
|:---:|---|---|:---:|---|
| **S0** | Startup & Authorization | **Skill** / **Knowledge** | `SKILL.md` (S0 Section) | `references/templates.md` (Permission Plan) |
| **S1** | Raw Idea & CoT Intake | **Skill** / **Knowledge** | `references/pain-points.md` (agent-side S(C) scoring) | `SKILL.md` (Core Rule 2: Pain-Point Card Matching) |
| **S2** | Repository Scan | **Tool** | `scripts/scaffold_docs.py --auto-detect` | `references/methodology.md` (S2) |
| **S3** | Formal Solution Draft (DRY Architecture) | **Knowledge** | `references/templates.md` (Formal Solution) | `references/methodology.md` (S3 DRY & Unified Client) |
| **S4** | Independent Solution Review | **Knowledge** | `references/review-gates.md` | `references/templates.md` (Review Rubric) |
| **S5** | Solution Finalization | **Knowledge** | `references/methodology.md` (S5) | `docs/product.md` |
| **S6** | Pre-Dev UX Alignment & Image Prototyping | **Tool** / **Skill** | `codex-doc-first-ui-ux-prototyping` companion skill / `scripts/scaffold_docs.py` | `docs/ux.md` (Multimodal UI Mockups & Bindings) |
| **S7** | Docs Review | **Tool** / **Skill** | `codex-doc-first-doc-sync` companion skill (`scripts/check_docs_links.py`) | `references/review-gates.md` (Docs Gate) |
| **S8** | Docs Finalization & Baseline Lock | **Knowledge** | `references/methodology.md` (S8) | `docs/README.md` |
| **S9** | Phase Plan & Task Breakdown (Foundation First) | **Knowledge** | `references/templates.md` (Phase Plan) | `references/methodology.md` (S9 Foundation First) |
| **S10** | Context / Task Pack Generation | **Tool** / **Skill** | `codex-doc-first-task-pack-gate` companion skill (`scripts/check_task_pack.py`) | `references/templates.md` (Task Pack) |
| **S11** | Execution Strategy Selection | **Skill** | `SKILL.md` (Goal/Plan/Build Modes) | `references/methodology.md` (S11) |
| **S12** | Branch & Concurrency Control | **Knowledge** | `references/agent-git-ci.md` | `docs/delivery/locks.yml` |
| **S13** | Spec-Driven Agent Implementation (DRY) | **Tool** / **Skill** | `scripts/verify_runtime_trace.py` | `references/schemas.md` (ExecutionTraceSchema) |
| **S14** | Test Quality & DRY Review | **Knowledge** | `references/review-gates.md` (Test & DRY Gate) | `references/methodology.md` (S14) |
| **S15** | Validation (L1 - L4) | **Knowledge** | `references/review-gates.md` (3-Tier Gate) | `scripts/verify_runtime_trace.py` (Exit Codes) |
| **S16** | Acceptance & Code-Doc Traceability | **Tool** | `scripts/verify_runtime_trace.py` | `references/review-gates.md` (Acceptance & Traceability) |
| **S17** | Git Conflict Handling | **Knowledge** | `references/agent-git-ci.md` | `references/methodology.md` (S17) |
| **S18** | Change Classification & Sync Doc Update | **Knowledge** / **Skill** | `references/methodology.md` (S18) / `codex-doc-first-doc-sync` companion skill | `docs/delivery/permission-audit.log` |
| **S19** | Phase Integration Acceptance | **Knowledge** | `references/review-gates.md` | `docs/delivery/phase-xxx.md` |
| **S20** | Documentation Writeback & Sync | **Knowledge** / **Skill** | `references/methodology.md` (S20 DFX Gate) / `codex-doc-first-doc-sync` companion skill | `references/pain-points.md` (Ingestion Gate) |
| **S21** | Merge / PR Preparation | **Knowledge** | `references/agent-git-ci.md` | `references/review-gates.md` (Merge Gate) |
| **S22** | Phase Archive | **Knowledge** | `references/methodology.md` (S22) | `docs/archive/` |
