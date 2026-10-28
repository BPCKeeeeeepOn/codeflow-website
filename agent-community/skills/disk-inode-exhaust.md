---
name: disk-inode-exhaust
description: df 还有空间但写入报错，八成是 inode 耗尽。定位小文件目录，而不是急着重启。
alerts: [disk.*.percent, disk.inode.*, 写入失败]
commands:
  - df -i
  - df -h
  - du -xhd1 /var
  - du -xhd1 /tmp
rca_priority: 5
---

## 何时用

- `disk.inode.<挂载点>.percent` 告警，或 `df -h` 显示有空间但应用写文件报 "No space left on device"。
- 会话大量小文件（session、缓存、邮件队列、容器日志）的机器重点怀疑。

## 动作（全部只读）

1. **确认是 inode 不是块**：`df -i` 与 `df -h` 一起看——
   - IUse% ≈ 100% 而 Use% 不高 → 小文件耗尽 inode，本技能主场；
   - 两者都高 → 是普通空间满，回到磁盘水位类技能。
2. **找小文件聚集地**：`du -xhd1 /var` 与 `du -xhd1 /tmp`——
   常见聚集地（按命中率排序）：`/var/spool`（邮件/任务队列）、`/var/lib/docker`（容器层）、`/var/log`（碎日志）、`/tmp`（临时文件）、session 目录。
   注意 `du -x` 限定同一文件系统，防止跨挂载点把数字看串。
3. **对时间**：把聚集目录的"最近变化"与告警触发时间对齐——磁盘类指标是缓慢增长曲线，异常加速点往往就是新任务上线/新定时任务的起点。

## 边界

- 定位到目录后**不要**直接删：清理动作用变更单（动作清单 `cleanup-tmp` 仅覆盖 `/tmp` 下 mtime>7 天的文件），其余目录必须人工确认。
- `du` 对大目录本身耗时——本技能的命令只到第一层（-d1），更深层次数给人工执行，避免诊断把自己跑成慢查询。
- 容器场景：宿主机看到的路径与容器内不同，报告里注明观察视角。
