---
name: self-evolution
description: >-
  Runs retro after task completion. Quick mode = 3-question self-check. Full mode = 11-dimension deep
  analysis with knowledge upgrade and action-item triage. Trigger when the user says "全面复盘 / 周汇总 /
  retro / 记住这个 / capture / 经验沉淀" or after task completion — even without explicit keywords.
  Do not trigger for deep review of written artifacts (use deep-review-loop) or session wrap-up (use mem-wrap-up).
  任务完成后的复盘 skill。快速模式 = 3 问自检；全面模式 = 11 维度深度分析 + 知识层升级 + 行动项分流。
  用户说「全面复盘/周汇总/retro/记住这个/capture/经验沉淀」或任务完成时触发（即使未点名）。
  不触发：书面产物深度复检（用 deep-review-loop）、session 收尾（用 mem-wrap-up）。
license: Apache-2.0
compatibility: Agent-agnostic. Requires file read/write tools and a memory directory convention.
metadata:
  version: "1.0.0"
---

# self-evolution

> 复盘沉淀 skill：快速模式 3 问自检（任务完成自动触发）；全面模式 11 维度深度分析 + 知识层升级（experience → pattern → heuristic → policy）+ 行动项 P0/P1/P2/P3 分流。

**Announce at start:** "I'm using the self-evolution skill to run retro (quick / full mode)."

## 工具名映射（跨平台）

正文中的工具名按「通用能力」描述，实际执行时映射到你所在平台的等价工具：

| 正文写法 | 通用能力 | 常见平台实现 |
|:---|:---|:---|
| subagent / Task | 派独立子代理（可并行） | TRAE Task / Codex spawn_agent / Claude Code Task |
| RunCommand | 执行 shell 命令 | PowerShell / bash / sh |
| Grep 工具 | 文本搜索 | TRAE Grep / `rg` / `grep` / Select-String |
| Read / Edit / Write | 文件读写 | 各平台内建文件工具 / apply_patch |
| LS / Glob | 枚举文件与目录 | `ls` / `Get-ChildItem` / glob |
| Skill 工具 | 调用另一个 skill | 各平台 skill 机制；无则按对应 SKILL.md 手动执行 |
| NEEDS_CONTEXT | 子代理缺上下文的回退信号 | TRAE 内建；其他平台等价于子代理报「信息不足」，按 fallback 处理 |

**PowerShell 示例的 POSIX 等价命令**：

| 目的 | PowerShell | POSIX |
|:---|:---|:---|
| 行数统计 | `(Get-Content FILE).Count` | `wc -l FILE` |
| 文件/路径存在 | `Test-Path FILE` | `test -e FILE` / `test -f FILE` |
| 递归枚举 | `Get-ChildItem -Recurse -File` | `find . -type f` |
| 超大文件 | `Get-ChildItem -Recurse \| Where-Object {$_.Length -gt 50KB}` | `find . -type f -size +50k` |
| 软链目标 | `Get-Item LINK \| Select-Object Target` | `readlink -f LINK` / `ls -l LINK` |
| 命中计数 | Grep output_mode=count | `grep -c PATTERN FILE` / `rg -c PATTERN FILE` |

## 在 skill 闭环中的位置

本 skill 是「审查 → 收尾 → 沉淀」三 skill 闭环的**沉淀端（闭环末端，反向喂回审查端）**，与 [deep-review-loop](https://github.com/1273984347/deep-review-loop)（审查）和 [mem-wrap-up](https://github.com/1273984347/mem-wrap-up)（收尾）联动：

**正向触发**（本 skill → 反向喂回）:
- 复盘发现流程撞坑 → 升级 **deep-review-loop** 协议（5 轮细节）
- 从 **deep-review-loop** residual risk + **mem-wrap-up** sediment/audit/work-log 提取经验

**反向触发**（上游 → 本 skill）:
- **deep-review-loop** R3 residual risk → 喂给问题预防维度（含 P2 残留经验：按 5Why 处理但标记「接受残留」，不强制升级）
- **deep-review-loop** R1b class-level findings → 喂给一次性工具沉淀维度（P3 由 DRL backlog 兜底）
- **mem-wrap-up** Step 5 sediment → 喂给经验复用维度
- **mem-wrap-up** Step 2 audit findings → 喂给问题预防维度
- **mem-wrap-up** Step 4 work-log → 喂给一次性工具沉淀维度

**P2/P3 跨 skill 语义统一**:
- DRL P2 = 体验问题（记录但不强制修复，允许残留 N 条）= 本 skill P2 = 等用户确认
- DRL P3 = 不报（class-level instance 例外升级 P2）= 本 skill P3 = nice-to-have（只记录）
- 行动项 P0/P1/P2/P3 优先级与 DRL 收敛判定表对齐：P0/P1 必须降到 0，P2 允许残留 N，P3 不计入

## memory 路径约定

本 skill 涉及 memory 操作时，使用占位符路径，按你的环境替换：

- `<memory_root>` = agent 的 memory 根目录（如 TRAE `.trae-cn/memory`、Claude Code 的 projects 目录，或项目内 `.agent-memory`）
- `<project-slug>` = 当前 workspace 对应的 memory 项目目录名（执行时按当前 cwd 映射）
- `<date>` = 当日日期目录（`YYYYMMDD`）
- `<skills_root>` = skill 安装目录（如 `.claude/skills`、`.trae-cn/skills` 或插件目录），执行时按当前环境映射

## 两种模式

| 模式 | 触发 | 深度 | 输出 |
|:---|:---|:---|:---|
| **快速** | 任务完成时自动 | 3 问自检 | experience-log.md |
| **全面** | 手动触发 | 11 维度分析 | retrospective.md + experience-log |

---

## 模式 A：快速复盘（任务完成后自动执行）

每个任务完成时，在 git commit 之前执行。

> **与整合版并用时**：若与 [agent-session-loop](https://github.com/1273984347/agent-session-loop)（审查→收尾→沉淀流水线）一起安装，触发与裁剪遵循整合版的场景裁剪规则（如纯调试 session 可标 `not-applicable`）；独立安装时按本节执行。

### 触发条件
- 任务标记为 completed 时
- git commit 前
- 不需要用户显式触发

### 执行步骤

**Step 1：3 问自检（必须回答，全否也要写出「全否」）**

```
① 有新发现？→ 方法/模式/工具首次使用或优化
② 踩了坑？→ 错误、根因、修复方案
③ 有 Skill 缺口？→ 本该用但没用的 Skill
```

**Step 2：根据答案决定动作**

| 答案 | 动作 |
|:---|:---|
| 全否 | 跳过，不写文件 |
| 有发现/踩坑/缺口 | 执行写入（见下方） |

**写入步骤**（直接执行，不需要调用其他 skill；格式与质量标准详见 [references/experience-capture-format.md](references/experience-capture-format.md)，激活本节时读取）：

1. 追加到 `<memory_root>/projects/<project-slug>/experience-log.md`（Edit 工具，末尾追加，无则 Write 创建）：
```markdown
## [日期] — [任务名称] | **Tags:** [tag1, tag2]

### [新发现 / 踩坑 / Skill 缺口]
[具体内容]

### 根因（如果是踩坑）
[分析]

### 下次怎么做
[具体行动方案]
```

2. 如有明确规则的经验，追加到 `<memory_root>/projects/<project-slug>/experience-quickref.md`：
```
[编号] [关键词] — [一句话规则]
```

3. 如有 Skill 缺口，追加到 `<memory_root>/projects/<project-slug>/skill-usage-checklist.md`：
```
| [Skill名] | [场景] | [为什么没用] |
```

**Step 3：模式升级检查**

如果同类问题在 experience-log.md 中出现 ≥3 次，触发升级：提案写入 `<memory_root>/knowledge/patterns/` 或 `<memory_root>/knowledge/heuristics/`（本 step 负责）。

---
## 模式 B：全面复盘（手动触发）

说「全面复盘」「跑一下验收」「周汇总」「复盘」「retro」时执行。覆盖整个会话或一段时间的工作。

### 执行步骤

**Step 1：数据收集（分层读取，避免 token 爆炸）**

```
第一层：摘要（必须，~2k tokens）
□ git log --oneline（本次会话的 commit 列表）
□ git diff --stat（文件变更统计）
□ experience-log.md 最后 50 行（最新条目）

第二层：按需读取（只在对应维度需要时读取）
□ 经验复用维度需要 → Grep experience-quickref.md 匹配本次关键词
□ 技能优化维度需要 → 读取本次使用的 Skill 的 SKILL.md（只读 description）
□ 未用技能维度需要 → Grep skill-usage-checklist.md 匹配本次任务类型
□ 问题预防维度需要 → Grep experience-log.md 匹配同类问题
□ 场景沉淀维度需要 → 读取 knowledge/patterns/ 相关文件

第三层：深度读取（只在发现异常时读取）
□ 某个经验条目需要详细分析 → 读取该条目完整内容
□ 某个 Skill 需要优化 → 读取完整 SKILL.md
```

**原则**：先读摘要，发现需要深入时再读全文。不要一次性把所有文件读入上下文。

**Step 2：11 维度分析**

按 11 个维度逐一分析，每个维度输出结论。**完整维度模板见 [references/11-dimensions-template.md](references/11-dimensions-template.md)**，激活本步时读取。

**11 维度清单**（dim 9 必走，不可跳过）：
1. 经验复用梳理 | 2. 技能优化评估 | 3. 未用技能审视 | 4. 场景沉淀识别 | 5. 问题与预防机制
6. 工作流优化方案 | 7. 问题总结与计划制定 | 8. 元认知反思 | 9. 一次性工具沉淀（必走）
10. 工具链 sub-protocol 反思（可选） | 11. 复盘过程中出现的问题（必走）

**Step 3：生成报告**

报告写入 `<memory_root>/projects/<project-slug>/<date>/retrospective.md`，格式：

```markdown
# YYYY-MM-DD 全面复盘

**项目**: [项目名]
**工作内容**: [概述]
**产出**: N 个 commit，N 文件变更，N 行代码

---

## 1. 经验复用梳理
[维度 1 输出]

## 2. 技能优化评估
[维度 2 输出]

## 3. 未用技能审视
[维度 3 输出]

## 4. 场景沉淀识别
[维度 4 输出]

## 5. 问题与预防机制
[维度 5 输出]

## 6. 工作流优化方案
[维度 6 输出]

## 7. 问题总结与计划制定
[维度 7 输出：行动计划 + 经验升级评估表]

## 8. 元认知反思
[维度 8 输出：本次复盘的质量评估 + 改进方向]

## 9. 一次性工具沉淀清单（必走）
[维度 9 输出：4 类决策表 + 沉淀价值评分 + 沉淀形式]

## 10. 工具链 sub-protocol 反思（可选）
[维度 10 输出：工具链层撞坑反思 + sub-protocol vN.0 沉淀]

## 11. 复盘过程中出现的问题（必走）
[维度 11 输出：撞坑分类表 + 5Why 元层根因 + 反模式识别 + 升 E/H 候选]
```

**Step 3.5：多件套同步 verify（强制）**

> **触发证据**：复盘类指令必同步多个真理源，漏任一件 = 复盘未闭环。

报告生成后，**强制 verify 以下多件套全部同步**：

| # | 件 | 路径 | 检查方法 |
|:--|:---|:-----|:--------|
| 1 | **复盘主 file** | `<memory_root>/projects/<project-slug>/<date>/retrospective.md` | RunCommand Test-Path 必存在 |
| 2 | **project_memory 更新** | `<memory_root>/projects/<project-slug>/project_memory.md` | Grep 本次 session 关键词 ≥ 1 |
| 3 | **user_profile 更新**（如涉及用户级偏好） | `<memory_root>/user_profile.md` | Grep 本次新增条目 ≥ 1（如适用） |
| 4 | **experience-log 备忘段** | `<memory_root>/projects/<project-slug>/experience-log.md` | Grep 本次 session 编号 ≥ 1 |
| 5 | **E-rule 候选** | `<memory_root>/projects/<project-slug>/experience-quickref.md` | Grep 新增候选编号 ≥ 1 |

**verify 失败时**：立即补漏（每件 < 5 min），不要等下次 session。

**Step 4：知识层升级（experience → pattern → heuristic → policy）**

只负责经验→规则的知识层级升级，不涉及具体行动项（行动项在 Step 5）。

| 条件 | 升级动作 | 执行方式 |
|:---|:---|:---|
| 同类经验 ≥3 次 + 跨任务 + 根因一致 | 创建 `<memory_root>/knowledge/patterns/[name].md` | **自动创建新文件** |
| 某 pattern 成功率 >80% + 不引入新问题 | 创建 `<memory_root>/knowledge/heuristics/[name].md` | **自动创建新文件** |
| 某 heuristic 效果显著 | 写入 `<memory_root>/knowledge/policies/` | **需人工确认** |

**knowledge/ 文件 frontmatter 标准**：
```yaml
---
name: [short-kebab-case]
description: [one-line summary]
type: pattern / heuristic / policy
id: [optional]
level: [optional]
tags: [optional]
---
```

**安全规则**：
- 只创建新文件，不覆盖已有文件
- 目标文件已存在 → 追加内容，不覆盖
- `knowledge/policies/` 一律需人工确认

每个升级动作执行后：`✅ 已写入 [路径]` 或 `⚠️ 需确认 [原因]`。

**Step 5：执行行动计划（按优先级分流）**

维度 7 产出的行动计划，按优先级决定执行方式：

| 优先级 | 执行方式 | 说明 |
|:---|:---|:---|
| **P0**（崩溃/安全/数据丢失） | **立即自动执行** | 不等确认，执行后报告 |
| **P1**（核心功能失效） | **立即自动执行** | 不等确认，执行后报告 |
| **P2**（体验优化/非核心） | **等用户确认** | 列出待确认项，用户说「执行」再动 |
| **P3**（nice-to-have） | **只记录** | 写入计划文件，不主动执行 |

**自动执行的动作类型 + 具体格式**：

| 动作类型 | 执行方式 | 输出格式 |
|:---|:---|:---|
| 创建模板文件 | Write `<memory_root>/templates/[name].md` | 文件必须有 frontmatter + 使用示例 |
| 更新 Skill | Edit `<skills_root>/<name>/SKILL.md` | 修改前先 Read，自动备份 |
| 追加经验条目 | Edit `<memory_root>/projects/<project-slug>/experience-log.md`（末尾追加） | 格式见模式 A |
| 更新速查表 | Edit `<memory_root>/projects/<project-slug>/experience-quickref.md` | 格式：`[编号] [关键词] — [规则]` |
| 写入 knowledge/patterns/ | Write `<memory_root>/knowledge/patterns/[name].md` | frontmatter + When/Pattern/Evidence/Related |
| 写入 knowledge/heuristics/ | Write `<memory_root>/knowledge/heuristics/[name].md` | frontmatter + Rule/Success Rate/Evidence |
| 更新 skill-usage-checklist | Edit `<memory_root>/projects/<project-slug>/skill-usage-checklist.md` | 格式：`| [Skill] | [场景] | [触发词] |` |

**每个动作执行前必须**：
1. 检查目标文件是否存在（RunCommand Test-Path）
2. 存在 → 追加（Edit），不覆盖
3. 不存在 → 创建（Write），带完整 frontmatter

---

## 与现有系统的关系（含三 skill 闭环）

### 三 skill 闭环

**闭环方向**：deep-review-loop（审查）→ mem-wrap-up（收尾）→ self-evolution（沉淀）

**本 skill 位置**：沉淀端（闭环末端，反向喂回 DRL）

**维度级联动点**：

| 本 skill 维度 | 输入来源 | 上游 skill / 步骤 |
|:---|:---|:---|
| 经验复用 | DRL residual + mem-wrap-up sediment | deep-review-loop R3 + mem-wrap-up Step 5 |
| 问题预防 | DRL residual（含 P2 残留经验）+ mem-wrap-up audit | deep-review-loop R3 + mem-wrap-up Step 2 |
| 一次性工具沉淀 | DRL class-level + mem-wrap-up work-log | deep-review-loop R1b + mem-wrap-up Step 4 |
| 复盘撞坑 | 反向喂回 → 升级 DRL 协议 | → deep-review-loop 5 轮细节 |

### 系统分工表

| 系统 | 角色 | 分工边界 |
|:---|:---|:---|
| self-evolution（本 skill） | **分析 + 升级 + 执行** | 快速模式直接写入 3 个文件；全面模式做 11 维度分析 + 知识层升级 + 行动项执行 |
| experience-log.md | 唯一的经验记录源（权威源） | self-evolution 快速模式写入 |
| experience-quickref.md | 速查表（从 experience-log.md 提取） | self-evolution 快速模式更新 |
| skill-usage-checklist.md | Skill 使用检查清单 | self-evolution 快速模式记录缺口 |
| deep-review-loop skill | 5 轮深度审查 | 问题预防/工具沉淀输入源；复盘撞坑反向升级目标 |
| mem-wrap-up skill | session 收尾 7 步流水线 | 经验复用/问题预防/工具沉淀输入源；与 self-evolution 互补 |

### 单一事实源原则

```
experience-log.md（权威源）→ 每次任务的发现和教训
  ↓
experience-quickref.md（索引）→ 速查表
  ↓
retrospective.md（分析报告）→ 引用 experience-log.md，不重复内容
```

---

## 边界限制

- 不改变已有 Skills 的核心职责
- 不自动删除 Skill
- 快速复盘是完成协议的一部分，不可跳过
- 全面复盘的 dim 9（一次性工具沉淀）和 dim 11（复盘过程撞坑）必走，不可跳过

## Verdict 字眼合规自检
- 全文 Grep 禁词：`完成|PASS|12/12|闭环|OK|没问题|looks good`
- 用「数据 + 实证 + residual risk 列表」代替 verdict 字眼
- 历史 log 文件例外（引用过往 verdict 不算违规）

## Self-Disclosure
- 0 verdict 字眼
- 11 维度完整（dim 1-11，模板见 references/），dim 9 + dim 11 必走
- 多件套 sync verify 强制（Step 3.5）
- 知识层升级安全规则（只创建新文件，policies 需人工确认）
- 行动项 P0/P1 立即执行，P2 等确认，P3 只记录

## Reference
- **设计来源**：从真实编码会话中蒸馏的双模式复盘 + 11 维度模板 + 知识层升级链路（多次「复盘未闭环 / 单一事实源漂移」教训固化）
- **相关 skill**：[deep-review-loop](https://github.com/1273984347/deep-review-loop)（审查）、[mem-wrap-up](https://github.com/1273984347/mem-wrap-up)（收尾）、[agent-session-loop](https://github.com/1273984347/agent-session-loop)（整合版）
