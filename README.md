# self-evolution

> 复盘沉淀 skill：快速模式 3 问自检（任务完成自动触发）；全面模式 11 维度深度分析 + 知识层升级（experience → pattern → heuristic → policy）+ 行动项 P0/P1/P2/P3 分流。

## 解决什么问题

任务做完了，但「经验」只留在对话里，下一次遇到同样问题重新踩坑。本 skill 把复盘固化为协议：快速模式保证每个任务提交前都过一遍 3 问自检；全面模式用 11 个维度把 session 的发现、踩坑、工具沉淀、流程瓶颈分析透，并升级为可复利的规则。

## 核心能力

- **双模式**：快速（3 问自检 → experience-log）/ 全面（11 维度 → retrospective.md）
- **11 维度**：经验复用 / 技能优化 / 未用技能 / 场景沉淀 / 问题预防（5Why）/ 工作流优化 / 计划制定 / 元认知 / **一次性工具沉淀（必走）** / 工具链反思 / **复盘过程撞坑（必走）**
- **知识层升级链路**：experience → pattern（≥3 次）→ heuristic（成功率 >80%）→ policy（需人工确认），只创建新文件不覆盖
- **行动项分流**：P0/P1 立即执行、P2 等用户确认、P3 只记录
- **单一事实源**：experience-log.md（权威源）→ experience-quickref.md（索引）→ retrospective.md（报告，不重复内容）
- **多件套 sync verify**：报告生成后强制验证 5 件套全部同步，漏任一件 = 复盘未闭环

## 安装

```bash
git clone https://github.com/1273984347/self-evolution.git
cp -r self-evolution <your-skills-dir>/self-evolution
```

## 使用

任务完成（git commit 前自动）→ 快速模式；用户说「全面复盘 / 周汇总 / retro」→ 全面模式。完整 11 维度模板见 [references/11-dimensions-template.md](references/11-dimensions-template.md)（按需加载，不占上下文）。

## 环境适配

- 需要文件读写工具 + memory 目录约定（`<memory_root>` 占位符，按你的环境替换）。
- 复盘维度引用上游 skill 的产出：DRL residual risk / mem-wrap-up sediment（未装时不影响本 skill 独立使用）。

## 相关仓库

- [agent-session-loop](https://github.com/1273984347/agent-session-loop)（整合版：审查→收尾→沉淀流水线）
- [deep-review-loop](https://github.com/1273984347/deep-review-loop)（审查：residual risk 喂给问题预防维度）
- [mem-wrap-up](https://github.com/1273984347/mem-wrap-up)（收尾：sediment 喂给经验复用维度）

## 许可证

[Apache-2.0](LICENSE)
