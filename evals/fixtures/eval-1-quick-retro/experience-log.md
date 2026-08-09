# Experience Log

## 2026-08-08 — tRPC 迁移 | Tags: [migration, trpc]

### 新发现
迁移后请求体校验用 zod schema 直接推导类型，少写一层 interface。

### 下次怎么做
新 API 优先用 zod 推断类型。

> 本次任务（缓存层接入）有新发现：LRU 缓存 key 设计模式。应追加新条目而非覆盖本条。
