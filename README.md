<div align="center">

**中文** · [English](./README.en.md)

</div>

# self-evolution

> 复盘沉淀 skill：快速模式 3 问自检（任务完成自动触发）；全面模式 11 维度深度分析 + 知识层升级（experience → pattern → heuristic → policy）+ 行动项 P0/P1/P2/P3 分流。

[![license](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)
[![CI](https://github.com/1273984347/self-evolution/actions/workflows/validate.yml/badge.svg)](https://github.com/1273984347/self-evolution/actions/workflows/validate.yml)
[![skills-ref](https://img.shields.io/badge/skills--ref-passing-2ea44f)](https://agentskills.io)
[![version](https://img.shields.io/badge/version-v1.0.1-1d76db)](https://github.com/1273984347/self-evolution/releases/latest)

## 解决什么问题

> 同一个坑，AI 会以一模一样的姿势踩第二遍——因为没人逼它把教训存下来。

你大概也遇到过：上次花半小时解决的问题，这周又花半小时解决。不是 AI 记性差，是复盘没闭环——经验只留在对话里，关了窗口就归零。复盘人人都说要做，但大多数复盘写完就沉底，从没变成"下次不踩坑"的规则。

本 skill 把复盘固化为协议：快速模式保证每个任务提交前都过一遍 3 问自检；全面模式用 11 个维度把 session 的发现、踩坑、工具沉淀、流程瓶颈分析透，并把经验升级为可复利的规则（experience → pattern → heuristic → policy），让下次的 AI 不再用同一个姿势踩同一个坑。

## 核心能力

- **双模式**：快速（3 问自检 → experience-log）/ 全面（11 维度 → retrospective.md）
- **11 维度**：经验复用 / 技能优化 / 未用技能 / 场景沉淀 / 问题预防（5Why）/ 工作流优化 / 计划制定 / 元认知 / **一次性工具沉淀（必走）** / 工具链反思 / **复盘过程撞坑（必走）**
- **知识层升级链路**：experience → pattern（≥3 次）→ heuristic（成功率 >80%）→ policy（需人工确认），只创建新文件不覆盖
- **行动项分流**：P0/P1 立即执行、P2 等用户确认、P3 只记录
- **单一事实源**：experience-log.md（权威源）→ experience-quickref.md（索引）→ retrospective.md（报告，不重复内容）
- **多件套 sync verify**：报告生成后强制验证 5 件套全部同步，漏任一件 = 复盘未闭环
- **经验捕获格式规范**：质量标准（好/差经验示例）+ 边界纪律（只写 3 文件、不越权做升级决策），见 [references/experience-capture-format.md](references/experience-capture-format.md)

## 安装

标准 Agent Skill（`SKILL.md` + `references/`），任何支持 Agent Skills 的客户端都能装。三种方式任选：

**方式 A：自然语言安装（推荐）**

在 Claude Code、Codex 等支持 Agent Skills 的工具里，直接说：

```text
帮我安装这个 skill：https://github.com/1273984347/self-evolution
```

Agent 会自动 clone 到 skills 目录并注册，不用手动找路径。工具不支持时，手动复制：

```bash
git clone https://github.com/1273984347/self-evolution.git
cp -r self-evolution <your-skills-dir>/self-evolution
```

**方式 B：Claude Code 插件市场（一条命令）**

```text
/plugin marketplace add 1273984347/self-evolution
/plugin install self-evolution@self-evolution
```

**方式 C：skills.sh CLI（Agent 界的 npm）**

```bash
# npx 首次运行会自动下载 skills CLI，无需全局安装
npx skills add https://github.com/1273984347/self-evolution
```

## 使用

任务完成（git commit 前自动）→ 快速模式；用户说「全面复盘 / 周汇总 / retro / 记住这个 / capture / 经验沉淀」→ 复盘或经验捕获。完整 11 维度模板见 [references/11-dimensions-template.md](references/11-dimensions-template.md)（按需加载，不占上下文）；快速模式写入格式与质量标准见 [references/experience-capture-format.md](references/experience-capture-format.md)。

**怎么触发**（说这些就会跑起来）：

```
任务做完了，快速复盘一下
全面复盘这个 session
帮我做个周汇总
retro 一下
记住这个：JSON 解析失败要用 try-except 包一层
```

## MCP 接入（可选）

本 skill 与 MCP **互补而非依赖**：MCP 提供外部数据源，本 skill 负责复盘分析。MCP 作为**可选增强**，无 MCP 时自动回退到内建工具（Grep/Read）。

**典型接入场景**：

| MCP 类型 | 用途 | 增强点 |
|---|---|---|
| 监控 / 指标 MCP | 拉取周期内真实运行数据 | 维度 5 问题预防 / 维度 6 工作流优化的数据支撑 |
| Issue / 项目 MCP | 拉取 issue、PR、评审记录 | 维度 2 技能评估 / 维度 7 计划制定的真实输入 |
| 日志 / 搜索 MCP | 检索历史会话与文档 | 维度 1 经验复用的补充来源 |

**接入步骤**：
1. 在你的 agent 配置中启用对应 MCP server；
2. 在 SKILL.md 的 `compatibility` 字段声明「可选 MCP：xxx」，并注明 fallback 规则；
3. skill 内写「有 xxx MCP 则拉取数据，无则用内建工具」——绝不因 MCP 缺失而中断复盘流程。

## 版本兼容性

| 检查项 | 值 |
|---|---|
| SKILL.md 版本 | 1.0.1 |
| Agent Skills 标准 | 兼容（[agentskills.io](https://agentskills.io) 开放标准，frontmatter: name/description/license/metadata） |
| frontmatter 校验 | 通过 `skills-ref validate`（CI 自动检查，见 [.github/workflows/validate.yml](.github/workflows/validate.yml)） |
| 运行依赖 | 无 Python/Node 脚本；需文件读写工具 + memory 目录约定 |
| MCP 依赖 | 无（可选接入） |
| 联动 skill | [deep-review-loop](https://github.com/1273984347/deep-review-loop)（审查）/ [mem-wrap-up](https://github.com/1273984347/mem-wrap-up)（收尾）——不装也能独立运行 |

**客户端兼容矩阵**：

| 客户端 | 安装方式 | 支持 |
|---|---|---|
| Claude Code | `/plugin marketplace add` 或复制目录 | ✅ |
| Codex / Cursor / OpenCode 等 | 复制目录（Agent Skills 标准客户端） | ✅ |
| WorkBuddy / QwenWork / TRAE | 复制目录到 skills 目录，自动注册 | ✅ |
| 其他 | 需支持 SKILL.md frontmatter + 渐进披露 | 视实现 |

## 环境适配

- 需要文件读写工具 + memory 目录约定（`<memory_root>` 占位符，按你的环境替换）。
- 复盘维度引用上游 skill 的产出：DRL residual risk / mem-wrap-up sediment（未装时不影响本 skill 独立使用）。

## 相关仓库

- [agent-session-loop](https://github.com/1273984347/agent-session-loop)（整合版：审查→收尾→沉淀流水线）
- [deep-review-loop](https://github.com/1273984347/deep-review-loop)（审查：residual risk 喂给问题预防维度）
- [mem-wrap-up](https://github.com/1273984347/mem-wrap-up)（收尾：sediment 喂给经验复用维度）

## 许可证

[Apache-2.0](LICENSE)
