<div align="center">

[中文](./README.md) · **English**

</div>

# self-evolution

> A retro & sedimentation skill: quick mode (3-question self-check, auto-triggered before every commit) and full mode (11-dimension deep analysis + knowledge-layer upgrade experience → pattern → heuristic → policy + P0-P3 action-item triage).

[![license](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)
[![CI](https://github.com/1273984347/self-evolution/actions/workflows/validate.yml/badge.svg)](https://github.com/1273984347/self-evolution/actions/workflows/validate.yml)
[![skills-ref](https://img.shields.io/badge/skills--ref-passing-2ea44f)](https://agentskills.io)
[![version](https://img.shields.io/badge/version-v1.0.1-1d76db)](https://github.com/1273984347/self-evolution/releases/latest)

## What problem it solves

> The same pitfall, tripped twice in exactly the same way — because nobody forced the lesson to be saved.

You've probably seen it too: a problem you spent half an hour solving last week took another half hour this week. The AI isn't forgetful — the retro just never closed the loop. Experience stays in the chat; close the window and it resets to zero. Everyone says they do retros, but most retros get written and sink, never becoming a "don't step here again" rule.

This skill hardens retro into a protocol: quick mode guarantees every task passes a 3-question self-check before commit; full mode analyzes findings, pitfalls, tool learnings, and workflow bottlenecks across 11 dimensions, then upgrades experience into compounding rules (experience → pattern → heuristic → policy) so the next session's AI doesn't trip the same pitfall in the same posture.

## Core capabilities

- **Dual mode**: quick (3-question self-check → experience-log) / full (11 dimensions → retrospective.md)
- **11 dimensions**: experience reuse / skill improvement / unused skills / scenario sedimentation / problem prevention (5 Why) / workflow optimization / planning / metacognition / **one-off tool sedimentation (mandatory)** / toolchain reflection / **retro-process pitfalls (mandatory)**
- **Knowledge-layer upgrade chain**: experience → pattern (≥3 occurrences) → heuristic (success rate >80%) → policy (needs human confirmation) — always create new files, never overwrite
- **Action-item triage**: P0/P1 run immediately, P2 waits for confirmation, P3 recorded only
- **Single source of truth**: experience-log.md (authoritative) → experience-quickref.md (index) → retrospective.md (report, no duplication)
- **Multi-artifact sync verify**: after the report, force-verify all 5 artifacts are in sync; one missing = retro not closed
- **Experience capture format spec**: quality standard (good vs bad examples) + boundary discipline (write only 3 files, no upgrade decisions), see [references/experience-capture-format.md](references/experience-capture-format.md)

## Installation

A standard Agent Skill (`SKILL.md` + `references/`), installable by any Agent Skills client. Pick one:

**Option A: natural-language install (recommended)**

In Claude Code, Codex, or any Agent Skills client, just say:

```text
Install this skill: https://github.com/1273984347/self-evolution
```

The agent clones it into your skills directory and registers it automatically. If your tool doesn't support that, copy it manually:

```bash
git clone https://github.com/1273984347/self-evolution.git
cp -r self-evolution <your-skills-dir>/self-evolution
```

**Option B: Claude Code plugin marketplace (one command)**

```text
/plugin marketplace add 1273984347/self-evolution
/plugin install self-evolution@self-evolution
```

**Option C: skills.sh CLI (the npm of agents)**

```bash
# npx downloads the CLI on first run; no global install needed
npx skills add https://github.com/1273984347/self-evolution
```

## Usage

Task complete (auto before git commit) → quick mode; user says "全面复盘 / 周汇总 / retro / 记住这个 / capture / 经验沉淀" → retro or experience capture. Full 11-dimension template: [references/11-dimensions-template.md](references/11-dimensions-template.md) (loaded on demand, no context overhead); quick-mode write format & quality standard: [references/experience-capture-format.md](references/experience-capture-format.md).

**How to trigger** (say any of these):

```
The task is done — quick retro
Full retro on this session
Help me with a weekly summary
Retro it
Remember this: JSON parse failures should be wrapped in try-except
```

## MCP integration (optional)

This skill and MCP are **complementary, not dependent**: MCP provides external data sources; the skill handles the retro analysis. MCP is an **optional enhancement** — without it, the skill falls back to built-in tools (Grep/Read).

**Typical integrations**:

| MCP type | Purpose | Enhancement |
|---|---|---|
| Monitoring / metrics MCP | Pull real runtime data for the period | Data for dimension 5 (problem prevention) / dimension 6 (workflow optimization) |
| Issue / project MCP | Pull issues, PRs, review records | Real inputs for dimension 2 (skill evaluation) / dimension 7 (planning) |
| Log / search MCP | Retrieve past sessions & docs | Extra source for dimension 1 (experience reuse) |

**Steps**:
1. Enable the MCP server in your agent config;
2. Declare "optional MCP: xxx" in the SKILL.md `compatibility` field with a fallback rule;
3. In-skill instruction: "pull data from xxx MCP if present, else built-in tools" — never break the retro on a missing MCP.

## Version compatibility

| Check | Value |
|---|---|
| SKILL.md version | 1.0.1 |
| Agent Skills standard | Compatible ([agentskills.io](https://agentskills.io); frontmatter: name/description/license/metadata) |
| CI gate | Five steps: `skills-ref validate` + `python evals/validate.py` + `python evals/run_behavior.py` + `python scripts/version-lint.py` + `python scripts/fragment-lint.py` (see [.github/workflows/validate.yml](.github/workflows/validate.yml)) |
| Runtime deps | Skill runtime: file read/write + memory dir convention; no subagent dependency (quick/full modes run on the main agent); CI lint scripts are dev-time only |
| MCP deps | None (optional) |
| Linked skills | [deep-review-loop](https://github.com/1273984347/deep-review-loop) (review) / [mem-wrap-up](https://github.com/1273984347/mem-wrap-up) (wrap-up) — works standalone |

**Client compatibility**:

| Client | Install method | Support |
|---|---|---|
| Claude Code | `/plugin marketplace add` or copy folder | ✅ |
| Codex / Cursor / OpenCode etc. | Copy folder (Agent Skills standard clients) | ✅ |
| WorkBuddy / QwenWork / TRAE | Copy folder into skills dir, auto-registered | ✅ |
| Others | Requires SKILL.md frontmatter + progressive disclosure | Depends |

## Environment

- **Path placeholders (read before first use)**: needs file read/write tools + memory dir convention; the skill uses `<memory_root>` placeholders — replace before running:
  - `<memory_root>` = your agent's memory root. Common setups: TRAE → `~/.trae-cn/memory`; Claude Code → `%USERPROFILE%\.claude\projects` (Windows) / `~/Library/Application Support/Claude/projects` (macOS); WorkBuddy → `~/.workbuddy/memory/` or in-repo `.workbuddy/memory/`; if no memory system exists, create an in-repo `.agent-memory/`.
  - **Not sure?** Run `ls` (macOS/Linux) / `Get-ChildItem` (Windows) to inspect your agent environment's existing dirs, then map against the examples above; **never guess paths**. If the environment truly has no memory system, mark the step `not-applicable` — never fabricate evidence.
- **Subagents**: no subagent/task spawning dependency — quick 3-question and full 11-dimension modes run on the main agent (see SKILL.md「无子代理平台说明」).
- Retro dimensions reference upstream skill outputs: DRL residual risk / mem-wrap-up sediment (works standalone without them).

## Related repos

- [agent-session-loop](https://github.com/1273984347/agent-session-loop) — all-in-one review → wrap-up → evolution pipeline
- [deep-review-loop](https://github.com/1273984347/deep-review-loop) — review (residual risk feeds the problem-prevention dimension)
- [mem-wrap-up](https://github.com/1273984347/mem-wrap-up) — wrap-up (sediment feeds the experience-reuse dimension)

## License

[Apache-2.0](LICENSE)
