---
name: failed-unit-storm
description: 服务反复重启往往不是服务自己的问题。先拉 failed 单元清单，再用 journalctl 找第一现场。
alerts: [服务不可用, 探活失败, 业务端口]
commands:
  - systemctl list-units --failed
  - systemctl status nginx
  - journalctl -u nginx --since 60 min ago
rca_priority: 6
---

## 何时用

- 服务级监控三态（up/degraded/down）反复翻转，或探活呈"通-断-通"锯齿。
- 平台"分级恢复"护栏已对同一服务连续熔断（说明自动恢复在打转，该找根因了）。

## 动作（全部只读）

1. **全景**：`systemctl list-units --failed`——failed 的通常不止一个。多个单元同时 failed 指向**共同依赖**（磁盘满 / 内存压力 / 依赖的 DB 不可达），而不是每个服务各自的 bug。
2. **单点深挖**：`systemctl status <unit>`——
   - 看最近几行日志摘要与 `Main PID` 变化频率（几分钟换一个 PID = 重启风暴）；
   - 看 `CGroup` 里的进程树是否残缺（fork 失败 = 主机资源问题）。
3. **第一现场**：`journalctl -u <unit> --since 60 min ago`——
   找**最早一次**失败记录（不是最新的）：第一现场的错误往往被后续重启日志刷掉。常见根因序：配置语法错（改了配置没 `nginx -t` 就 restart）、依赖端口未就绪（启动顺序）、OOM（journal 里搜 oom-kill）、权限/证书文件变更。

## 边界

- **与自愈护栏的边界**：本技能只取证。平台"分级恢复"的 restart 类动作有自己的护栏（限流/熔断/爆炸半径），诊断期间不要再建议"再重启一次试试"。
- 多单元同时 failed 时，先修共同依赖再谈单个服务——顺序错了会把恢复动作打成风暴。
- journalctl 按单元过滤；跨单元的全机日志用平台的 `fetch_remote_log` 工具（支持时间窗），本技能不负责。
