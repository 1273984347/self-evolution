# Changelog

本文件记录 self-evolution 的版本演进，遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 风格。版本号与 `SKILL.md` 的 `metadata.version` 保持一致。

## [Unreleased]

## [1.0.3] - 2026-09-04

### Fixed
- publish-tessl.yml：TESSL_TOKEN 提升到 job 级 env——step 自身的 env 在它自己的 `if` 求值时尚未应用，原 step 级写法条件恒为 false，配置了 secret 也永远跳过（发布流水线死代码修复）
- GitHub Actions 全部 pin 到 commit SHA（actions/checkout v4/v6、setup-python v5、tesslio/setup-tessl v2），消除可变 tag 的供应链风险
- P0/P1 自动执行边界收窄：「更新 Skill」（Edit 任意 SKILL.md）不再自动执行，一律等用户确认后才执行——skill 自改影响所有后续 session，且本 skill 运行时大量读取仓库文档与 work-log，不允许无人值守通道被可能被污染的内容驱动自改 skill
- verdict 禁词自匹配误报：grep 命中先剔除禁词定义行本身再计数（meta-skill 场景 +「OK」子串误报 TOKEN/BROKEN 等），fragment-lint 新增锚点防漂移

### Changed
- compatibility 字段如实声明：需要文件系统 + 文件读写 + shell（PowerShell/POSIX）路径检查；无 shell 的纯 Web agent 不支持（原文 "Agent-agnostic" 超前）
- CI 加 windows-latest runner（skills-ref 两步在 Windows 跳过：上游 CLI 静默 exit 1）；lint/eval 步骤三平台覆盖
- .gitignore 补 `__pycache__/` 与 `.mimosa/`
- README（中/英）补 token 成本预期；运行依赖行同步 compatibility 修订

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
