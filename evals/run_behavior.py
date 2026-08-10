#!/usr/bin/env python3
"""Executable behavior evals for self-evolution (deterministic mode, CI-safe)."""

from __future__ import annotations
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVALS_DIR = ROOT / "evals"


def scene_checks(eval_id: int, ws: Path) -> list[tuple[str, bool]]:
    """Return [(description, holds)] assertions for this eval's fixture workspace."""
    checks: list[tuple[str, bool]] = []

    if eval_id == 1:
        # quick-retro: fixture 是快速复盘产出的 experience-log，核心是 3 问自检落盘经验日志
        f = ws / "experience-log.md"
        text = f.read_text(encoding="utf-8") if f.exists() else ""
        checks.append(("experience-log.md 存在（3 问自检有发现时产出经验日志）", f.exists()))
        checks.append((
            "日志条目按模板落盘：日期 + 任务 + Tags（## YYYY-MM-DD — 任务 | Tags: [...]）",
            bool(re.search(r"^## \d{4}-\d{2}-\d{2} .*Tags: \[", text, re.M)),
        ))
        checks.append(("含 3 问自检的「新发现」条目（有发现须逐问落盘）", "新发现" in text))
        checks.append(("含「下次怎么做」（根因 + 落地指引）", "下次怎么做" in text))
        checks.append(("含追加不覆盖规则（单一事实源，不编造/不覆盖经验）", "追加" in text and "覆盖" in text))

    elif eval_id == 2:
        # full-retro-11dim: fixture 是全面复盘的分层输入素材 work-log，覆盖 11 维度所需素材
        f = ws / "work-log.md"
        text = f.read_text(encoding="utf-8") if f.exists() else ""
        checks.append(("work-log.md 存在（全面复盘先做分层数据收集）", f.exists()))
        m = re.search(r"commits:\s*(\d+)\s*个", text)
        checks.append(("含 commits 计数且 >0（数值可机械校验）", m is not None and int(m.group(1)) > 0))
        checks.append(("含变更清单（变更维度素材）", "变更" in text))
        checks.append(("含踩坑记录（根因/复盘维度素材）", "踩坑" in text))
        checks.append(("含一次性脚本（dim 9 一次性工具沉淀素材）", "一次性脚本" in text))
        checks.append(("含待复盘维度清单（维度覆盖驱动）", "待复盘维度" in text))

    elif eval_id == 3:
        # knowledge-upgrade: fixture 是含可升级经验的 experience-log（同类 ≥3 次 → pattern 链路）
        f = ws / "experience-log.md"
        text = f.read_text(encoding="utf-8") if f.exists() else ""
        checks.append(("experience-log.md 存在（升级链路起点 experience）", f.exists()))
        entries = re.findall(r"^## \d{4}-\d{2}-\d{2}", text, re.M)
        checks.append((f"同类条目数 ≥3 触发模式升级（实测 {len(entries)} 条）", len(entries) >= 3))
        checks.append(("含升级触发标记「已出现 N 次」", bool(re.search(r"已出现 \d+ 次", text))))
        checks.append((
            "同类 Tags 标签 ≥3（跨任务同模式：Tags: [migration]）",
            len(re.findall(r"Tags: \[migration\]", text)) >= 3,
        ))
        checks.append(("根因一致（跨文件改动漏搜引用）", "漏搜引用" in text))

    elif eval_id == 4:
        # action-triage: fixture 是复盘产出的行动项计划，核心是 P0/P1/P2/P3 分级分流
        f = ws / "action-plan.md"
        text = f.read_text(encoding="utf-8") if f.exists() else ""
        checks.append(("action-plan.md 存在（复盘产出行动项计划）", f.exists()))
        checks.append(("含 P0/P1/P2/P3 全部分级标记", all(p in text for p in ("P0", "P1", "P2", "P3"))))
        checks.append(("P0 生产阻断 → 立即执行", "P0" in text and "立即执行" in text))
        checks.append(("P3 nice-to-have → 只记录", "P3" in text and "只记录" in text))
        checks.append(("行动项按表格结构化（任务/优先级/类型列齐全）", "优先级" in text and "类型" in text))

    return checks


def main() -> None:
    data = json.loads((EVALS_DIR / "evals.json").read_text(encoding="utf-8"))
    failures = 0
    for ev in data["evals"]:
        ws = ROOT / ev["files"][0]
        if not ws.is_dir():
            print(f"FAIL: eval {ev['id']} fixture missing: {ws}"); failures += 1; continue
        checks = scene_checks(ev["id"], ws)
        failed = [(d, ok) for d, ok in checks if not ok]
        if failed:
            failures += 1
            for d, ok in failed:
                print(f"  FAIL: {d}")
        else:
            print(f"PASS: eval {ev['id']} ({ev['name']}) - {len(checks)} assertions hold")
    if failures:
        sys.exit(f"{failures} behavior eval(s) failed")
    print(f"self-evolution: all behavior evals passed ({len(data['evals'])} evals)")


if __name__ == "__main__":
    main()
