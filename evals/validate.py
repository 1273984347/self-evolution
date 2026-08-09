#!/usr/bin/env python3
"""Deterministic structural regression checks for the self-evolution skill.

Validates that SKILL.md stays compliant with the Agent Skills standard AND keeps the
retro protocol contracts (dual mode, 11 dimensions with mandatory dim 9/11, knowledge
upgrade chain, action triage P0-P3, single source of truth) intact, plus consistency
between the skill and its eval fixtures. Runs in CI (pure stdlib, no third-party deps).
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
EVALS_DIR = ROOT / "evals"

# Trigger markers that must stay in the description (see agentskills.io trigger contract).
EXPLICIT_MARKERS = ("retro", "全面复盘", "周汇总")

# Protocol phrases that must stay in the SKILL.md body — losing any of these breaks the retro.
REQUIRED_PHRASES = (
    "快速模式",        # quick 3-question mode
    "全面模式",        # full 11-dimension mode
    "11 维度",        # dimension count
    "dim 9",         # mandatory: one-off tool sedimentation
    "dim 11",        # mandatory: retro-of-the-retro
    "知识层升级",    # experience → pattern → heuristic → policy
    "experience-log",  # single source of truth
    "单一事实源",       # no duplicated truth
    "retrospective",  # full-mode report
    "5Why",          # root-cause depth
    "P0", "P1", "P2", "P3",  # action triage levels
    "必走",           # mandatory dimensions
    "禁词",           # verdict-word ban
)


def folded_description(frontmatter: str) -> str:
    """Reconstruct the folded description scalar from YAML frontmatter."""
    lines = frontmatter.splitlines()
    captured: list[str] = []
    active = False
    for line in lines:
        if line.startswith("description:"):
            active = True
            continue
        if active and re.match(r"^[a-z][a-z0-9-]*:", line):
            break
        if active:
            captured.append(line.strip())
    return " ".join(part for part in captured if part)


def validate_skill() -> None:
    text = SKILL.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    assert len(parts) == 3, "SKILL.md frontmatter is missing"
    description = folded_description(parts[1])

    # Agent Skills spec hard limits
    assert 1 <= len(description) <= 1024, (
        f"description violates Agent Skills 1024-char limit (got {len(description)})"
    )
    assert len(text.splitlines()) < 500, "SKILL.md exceeds progressive-disclosure 500-line budget"

    # Trigger contract: explicit markers + negative-trigger clause
    for marker in EXPLICIT_MARKERS:
        assert marker in description, f"description lost explicit trigger marker: {marker}"
    assert "Do not trigger" in description, "description lost negative-trigger clause"

    # Protocol contract
    for phrase in REQUIRED_PHRASES:
        assert phrase in text, f"SKILL.md lost protocol phrase: {phrase}"

    # Version metadata (semver)
    assert re.search(r'version: "\d+\.\d+\.\d+"', parts[1]), "version metadata is missing"

    print(f"PASS: SKILL.md ({len(text.splitlines())} lines, description {len(description)} chars)")


def validate_evals() -> None:
    evals = json.loads((EVALS_DIR / "evals.json").read_text(encoding="utf-8"))
    assert evals["skill_name"] == "self-evolution", "evals.json targets the wrong skill"
    assert len(evals["evals"]) >= 3, "evals.json needs >=3 behavior evals"
    for e in evals["evals"]:
        assert e["id"] and e["name"] and e["prompt"] and e["expected_output"], (
            f"eval missing required fields: {e.get('name')}"
        )
        assert e["expectations"], f"eval '{e['name']}' has empty expectations"
        for f in e.get("files", []):
            assert (ROOT / f).exists(), f"eval '{e['name']}' fixture missing: {f}"

    trig = json.loads((EVALS_DIR / "trigger-eval.json").read_text(encoding="utf-8"))
    queries = trig["queries"]
    assert len(queries) >= 10, "trigger-eval.json needs >=10 queries"
    assert any(q["should_trigger"] for q in queries), "trigger-eval has no should-trigger queries"
    assert any(not q["should_trigger"] for q in queries), (
        "trigger-eval has no should-not-trigger queries"
    )

    print(f"PASS: evals.json ({len(evals['evals'])} evals) + trigger-eval.json ({len(queries)} queries)")


def main() -> None:
    validate_skill()
    validate_evals()
    print("self-evolution: all structural regression checks passed")


if __name__ == "__main__":
    main()
