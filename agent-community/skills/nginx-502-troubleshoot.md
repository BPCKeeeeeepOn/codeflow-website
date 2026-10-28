---
name: nginx-502-troubleshoot
description: 502/504 三连查：本机端口还听不听 → 上游通不通 → nginx 日志怎么说。先分清"挂了"还是"慢了"，再谈改配置。
alerts: [nginx.*, 探活失败, 502, 业务HTTP]
commands:
  - systemctl status nginx
  - ss -ltnp
  - curl -I http://127.0.0.1:80
  - journalctl -u nginx --since 30 min ago
  - docker ps
rca_priority: 5
---

## 何时用

- 告警里出现 `nginx.*` 指标异常、业务 HTTP 探活失败、或用户报 502/504。
- 排查目标机上有 nginx（systemd 单元或容器二选一，本技能两条路都给）。

## 动作（全部只读）

1. **nginx 还活着吗**：`systemctl status nginx`——注意看是否处于 failed / restarting 循环。
   容器部署用 `docker ps` 先确认容器状态，再看 `docker logs <容器名>`（不带 --tail，先看全量最近的）。
2. **端口还在听吗**：`ss -ltnp`——确认 80/443（或你的监听口）仍在 LISTEN。
   没监听 = nginx 挂了或配置改坏；有监听 = 往上游找。
3. **本机自测**：`curl -I http://127.0.0.1:80`——
   - 返回 200/301 → nginx 自身正常，502 来自上游，跳第 4 步；
   - 卡住超时 → worker 被打满或磁盘/IO 卡，看第 5 步；
   - 连接拒绝 → 回第 1 步，配置丢了或启动失败。
4. **上游三连**（502 的主战场）：
   - 用 `curl -I http://<上游地址>:<端口>` 逐个探 upstream（地址取自 nginx 配置里的 proxy_pass，本技能不读配置文件内容，仅提示路径 `/etc/nginx/conf.d/*.conf`）；
   - `ss -ltnp` 确认上游端口是否在目标机本机监听；
   - 上游是容器时 `docker ps` 看是否重启循环。
5. **日志要说法**：`journalctl -u nginx --since 30 min ago`——
   关键词：`connect() failed`（上游拒绝=端口没听/进程死）、`upstream timed out`（上游慢=看上游机器）、`no live upstreams`（全部上游被摘）。日志里的时间点与告警触发时间对齐。

## 边界

- 本技能**不改任何配置、不重启任何服务**——`nginx -t || 隔离坏配置` 类修复走变更单（动作清单里已有 `nginx-fix-bad-conf`），需人工确认。
- 读配置文件内容用平台的 `read_log_tail`（仅平台自身主机）或技能授权命令 `cat /etc/nginx/conf.d/<文件>.conf`——但不要把配置文件整个贴进报告，摘 proxy_pass 一行即可。
- 上游是数据库/消息队列时，改用对应专项技能（mysql-conn-pool-exhaust / redis-memory-pressure）。
