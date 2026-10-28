---
name: tcp-timewait-storm
description: TIME_WAIT 堆积是高频短连接的信号。先数清楚分布，再看是哪个调用方在疯狂建连。
alerts: [net.tcp.*, 连接异常]
commands:
  - ss -s
  - ss -tan state time-wait
  - ss -tlnp
rca_priority: 7
---

## 何时用

- `net.tcp.time_wait`（Agent 扩展指标）持续高位，或 `net.tcp.total` 曲线锯齿状剧烈波动。
- 应用侧偶发 "Cannot assign requested address"（本地端口耗尽的前兆）。

## 动作（全部只读）

1. **总量与分布**：`ss -s`——看 TIMED 状态计数与端口使用概况。TIME_WAIT 高不是病本身，是**症状**：说明有调用方在用短连接高频打某个服务。
2. **谁在对谁**：`ss -tan state time-wait`——看对端地址分布：
   - 全部指向同一个 `IP:端口` → 那个服务的客户端没开连接复用（keep-alive/连接池）；
   - 分散在大量远端 → 本机是爬虫/网关类角色，属业务形态，风险等级调低。
3. **本机监听健康**：`ss -tlnp`——确认没有意外新增的监听端口（和告警时间对不上的新监听 = 最近变更线索）。

## 边界

- **不建议**直接调 `net.ipv4.tcp_max_tw_buckets` 或开 tw_reuse：先回答"谁的短连接"。内核参数是最后手段，且要评估对 NAT 场景的副作用。
- 只看 state=time-wait 这一个过滤即可；不要一次抓全量连接表（几万行的输出会被工具预算截断，反而丢信息）。
- TIME_WAIT 是 TCP 正常状态（主动关闭方），0 才奇怪——报告里别把它写成"异常连接"。
