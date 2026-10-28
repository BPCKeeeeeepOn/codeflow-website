---
name: cert-chain-checkup
description: 证书告警分两种：快到期和链不完整。排查路径完全不同，别拿续期解决信任链问题。
alerts: [https-cert, 探活失败]
commands:
  - openssl s_client -connect 127.0.0.1:443 -servername example.com
  - curl -vI https://example.com
rca_priority: 6
---

## 何时用

- 探活类型为 `https-cert` 的告警（平台取值为证书剩余天数，`<30` 天类规则）。
- 用户报浏览器证书警告，但平台的证书探活显示天数还够。

## 动作（全部只读）

1. **分清是哪种告警**：
   - 平台证书探活报"剩余天数少" → 到期类，第 2 步；
   - 天数充足但用户侧浏览器报警 → 链完整性类，跳第 3 步。两类处置完全不同。
2. **到期类**：证书探活的 `latency_ms` 字段就是剩余天数（平台约定）。报告里给"还剩 N 天 + 到期日期"，提醒续期走证书管理流程，**不在此展开**。
3. **链完整性类**：`openssl s_client -connect <host>:443 -servername <域名>`——看输出里 `Verify return code`：
   - `unable to get local issuer certificate` → 服务器没发**中间证书**（最常见的链断裂，浏览器缓存了旧链所以平台读数正常、新访客报警）；
   - `certificate has expired` → 实际已过期，平台读数与实际不符要交叉核对；
   - `ok` → 平台探活与外部感知不一致，怀疑域名解析差异（内网 vs 公网解析到不同 VIP）。
4. **外部视角交叉**：`curl -vI https://<域名>`——curl 自带系统信任库，能暴露"平台看正常、外部看异常"的视角差。

## 边界

- 命令里的目标地址/域名是**模板**：AI 执行时按事件里的实际探活目标替换，报告里必须写明实际用了哪个目标。
- 续期是变更动作，本技能只定位到"到期 / 链不完整 / 解析不一致"三选一，处置走对应流程。
- 自签内网证书会显示 verify 失败——先确认这台机器是否本就该用私有 CA，不要把"内网自签"报成"证书故障"。
