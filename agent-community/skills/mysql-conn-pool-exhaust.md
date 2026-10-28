---
name: mysql-conn-pool-exhaust
description: 连接数打满不一定是要加 max_connections：先看 processlist 里谁在占、有没有 sleep 堆积，再判断是泄漏还是容量。
alerts: [mysql.*, 连接数, 连接池]
commands:
  - mysql -e "show processlist"
  - mysql -e "show status like 'Threads_connected'"
  - mysql -e "show variables like 'max_connections'"
  - mysql -e "show status like 'Aborted_connects'"
rca_priority: 6
---

## 何时用

- 告警指标 `mysql.*.connections` 或自定义连接数指标越限。
- 应用侧报"too many connections"或连接池获取超时。

## 动作（全部只读）

1. **现在到底占了多少**：`mysql -e "show status like 'Threads_connected'"` 对上 `show variables like 'max_connections'`——
   占用率 ≥90% 才算"打满"；60-80% 是爬坡，先看趋势不要动手。
2. **谁在占**：`mysql -e "show processlist"`——按三列读：
   - `Command=Sleep` 且 `Time` 很大 → 应用侧连接泄漏（借了不还）；
   - `Command=Query` 且 `Time` 很大 → 慢查询堆积（配合 `show processlist` 里的 State 列）；
   - 大量同库同用户的短连接 → 连接池配置太小，风暴式建连。
3. **连接质量**：`mysql -e "show status like 'Aborted_connects'"`——持续增长说明客户端认证/网络层在反复失败，与容量无关。

## 边界

- 本技能**只读库**：SQL 限 select/show/describe/explain（平台只读白名单强制）。
- **不建议**直接调大 max_connections：那只是把 OOM 的位置从 MySQL 挪到主机内存。结论里给出判断（泄漏/慢查/容量），处置交给人工决策。
- 主从架构下先确认连的是哪个节点；只读从库的连接风暴要单独归因。
- 凭据不进技能：连接走主机上已配置好的客户端环境（如 `~/.my.cnf`），技能里不带密码。
