---
name: redis-memory-pressure
description: 内存告警先看碎片率与淘汰策略是否匹配，再谈大键。改 maxmemory 之前先回答"内存花在哪了"。
alerts: [redis.*, mem.*]
commands:
  - redis-cli info memory
  - redis-cli info stats
  - redis-cli dbsize
rca_priority: 6
---

## 何时用

- 告警指标 `redis.*.memory` 越限，或主机 `mem.*` 告警且该机跑着 Redis。
- 应用侧报 OOM command not allowed（已触发 maxmemory 淘汰上限）。

## 动作（全部只读）

1. **读 memory 段**：`redis-cli info memory`——按顺序看四个字段：
   - `used_memory_human` vs `maxmemory_human`：到顶没有；
   - `mem_fragmentation_ratio`：>1.5 碎片严重（实际占的比数据多得多），<1 说明 swap 在兜底（更糟）；
   - `maxmemory_policy`：淘汰策略与业务预期是否匹配（allkeys-lru 下被逐出的键会"消失"，表现为缓存命中率下降）；
   - `mem_allocator`：libc 分配器碎片问题常见，jemalloc 相对好。
2. **淘汰有没有在发生**：`redis-cli info stats`——看 `evicted_keys` 是否在增长；增长 = 已经在牺牲键了，命中率类告警的根因多半在这。
3. **规模感**：`redis-cli dbsize`——键数量级变化（骤增）比单键大小更容易解释内存爬坡。

## 边界

- 本技能只读。`info keyspace` / `--bigkeys` 属于额外探测，如需可写进技能 `commands` 的候选，但**不要**在生产高峰跑 `--bigkeys`（会扫全库）。
- 大键定位（memory usage 单键）涉及遍历，交给人工决定何时做，AI 报告里只给路径与代价说明。
- **不建议**在结论里直接给"调大 maxmemory"：先回答内存花在哪（数据增长 / 碎片 / 淘汰策略错配），三个答案对应三种处置。
