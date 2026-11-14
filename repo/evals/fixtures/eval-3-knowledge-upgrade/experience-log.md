# Experience Log

> 同一类问题已出现 4 次：跨文件改动时漏搜引用。

## 2026-07-20 — pathlib 迁移 | Tags: [migration]
### 踩坑
只搜了调用处，漏了 import 引用。
### 下次怎么做
迁移前 Grep 全部引用。

## 2026-07-28 — axios 迁移 | Tags: [migration]
### 踩坑
同上：漏搜引用。
### 下次怎么做
同上。

## 2026-08-02 — REST 迁移 | Tags: [migration]
### 踩坑
漏旧挂载点。
### 下次怎么做
同上。

## 2026-08-08 — tRPC 迁移 | Tags: [migration]
### 踩坑
漏旧挂载点（第 4 次同类）。
### 下次怎么做
同上。
