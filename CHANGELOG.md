# Changelog

本文件记录 self-evolution 的版本演进，遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 风格。版本号与 `SKILL.md` 的 `metadata.version` 保持一致。

## [Unreleased]

## [1.0.2] - 2026-08-31

### Fixed
- 路径预检 + Grep 空结果判别：占位符使用前强制 `test -e`，预检失败中断问用户（漏洞 7/9/15）
- 快速模式全否强制留痕：写「本次无新经验（3 问全否）」，不允许跳过不写文件（漏洞 14）
- 知识层升级复核标记：pattern/heuristic 自动创建标 `review_status: pending`，reviewed 前不作权威规则（漏洞 13）
- 5Why 未知标注：上下文无法支撑的层级标注 `[未知]`，不强制凑满 5 层（漏洞 12）

### Added
- LLM 行为 eval（evals/run_behavior_llm.py，发布前手动门禁）
- fragment-lint 交叉引用校验；version-lint 内容漂移软告警
- README badge 改动态 release badge；CI 加 macos-latest runner + skills-ref pin
- trigger-eval 统一到 12 条（与其余仓库对齐，删除低区分度负例）

## [1.0.1] - 2026-08-31

### Fixed
- 快速模式补「与 agent-session-loop 整合版并用时」的触发/裁剪协调声明
- `<skills_root>` 占位符补路径约定定义

### Added
- references/experience-capture-format.md：经验写入格式规范（质量标准 / 边界纪律 / 手动触发 / 通用编号），从 vault 版 experience-capture skill 蒸馏
- description 触发词扩展：记住这个 / capture / 经验沉淀（同步 trigger-eval 3 条查询）
- scripts/fragment-lint.py 共享片段一致性 lint + CI 接入

### Changed
- 跨平台清理：NEEDS_CONTEXT 信号通用化（去掉 TRAE 平台绑定）
- 新增「无子代理平台说明」（本 skill 正文本就不依赖子代理，无需降级标注）
- 四源版本同步（SKILL.md / README / CHANGELOG / marketplace.json）

## [1.0.0] - 2026-08-10 初始发布

### Added
- 快速 3 问自检 / 全面 11 维度复盘双模式
- 知识层升级链路 experience → pattern → heuristic → policy
- 单一事实源（experience-log → quickref → retrospective）+ 多件套 sync verify
- evals 评估体系：4 个行为场景 fixtures + trigger-eval 12 条触发查询 + 双层 CI
- 双语 README + 自然语言安装 + 叙事升级
- GitHub Release v1.0.0、Discussions、项目文档（CONTRIBUTING/CoC/SECURITY/CHANGELOG）
