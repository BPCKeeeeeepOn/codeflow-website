# TestOps 官网

**告警响了，AI 已经查完，证据链摆在你面前。**

TestOps Platform 的官方网站项目——双层定位：**产品层**（转化）+ **知识层**（留存）。设计、调研、原型、内容资产全部在本仓沉淀。

## 当前状态

**P0~P4 已交付**（2026-10-29）：15 站竞品调研 → 15 屏设计稿 → **39 个可发布产物**（18 主页面 + 21 正文壳页）→ Agent 评测平台全量嵌入（EvalDeck iframe）→ 技能集市 8 技能 → VIP 定时任务权益页 → 文档中心站内渲染。

| 验证 | 结果 |
|---|---|
| 需求项 | **FR 33 / 33** 达成（`docs/engineering/05-交付核对表.md` 逐条核对） |
| 机械守卫 | **21 / 21** 全绿（`python3 tools/check_all.py`） |
| 响应式 | 19 页 × 4 档（1440/1024/768/390）**零横向溢出** |
| 可访问性 | 双主题 12 组对比度全部 ≥4.5:1 |
| 性能 | 单页最大 90KB（限 150KB），零 CDN / 零第三方脚本 |

打开预览：

```bash
# 方式一：静态服务（最快）
cd site && python3 -m http.server 8899

# 方式二：FastAPI 站点服务（与生产同形态，含 /api/health 探活）
pip install -r requirements-website.txt
python3 server.py            # → http://127.0.0.1:8899
```

## 开发流程

```bash
python3 tools/build_pages.py         # 改 site/src/ 后重建全部产物
python3 tools/build_pages.py --check # 校验产物与源一致（CI gate）
python3 tools/check_all.py           # 17 项机械守卫

## 目录

| 路径 | 内容 |
|---|---|
| [PLAN.md](PLAN.md) | **开发计划**（P1-P6 里程碑 · 验收标准 · 风险红线） |
| `server.py` | FastAPI 站点服务（静态托管 + `/api/health` + 404 兜底） |
| `tools/` | `build_pages.py`（生成器）· `check_all.py`（守卫）· `og_template.html`（OG 图模板） |
| `site/` | 产物：18 主页面 + 21 正文壳页 + `assets/`；`site/src/` 是源 |
| `docs/官网设计稿.md` | 设计稿 v1.3：逐屏设计 + 视觉系统 + 数字来源表 + 禁用词表 |
| `docs/开源产品官网设计研究.md` | 15 个开源产品官网调研（六范式 + 信任层级 + 12 个可复用装置） |
| `docs/TestHub-官网设计文档.md` | TestHub 拆解（Skills 目录 / 版本对比 / VIP 模型） |
| `agent-community/` | 8 个种子 SKILL.md（已过只读命令白名单自查）+ 贡献指南；技能卡渲染到首页 `#skills-market` |
| `assets/screenshots/` | 15 张设计过程截图（深浅主题） |
| `docs/engineering/` | 工程文档四件套 + **05-交付核对表**（FR 33/33 逐条核对 + 缺陷台账） |

## 设计原则（红线）

1. **数字全部可追溯**：官网上每一个数字（82 秒 / 720 测试 / 163 端点…）都能追到设计稿 §6.1 来源表
2. **禁用词**：不承诺准确率 / 不承诺无人值守 / 不出现竞品名 / 不放无授权 logo
3. **诚实边界**：未上线功能必须带"即将上线"标识（VIP 定时任务当前状态）
4. **零 CDN 零构建**：与产品免构建纪律同构
5. **视觉同源**：设计令牌直接沿用产品 `static/ops.css`（D50 收敛口径）

## 开发纪律

- 开发计划看 `PLAN.md`，按里程碑推进，每步有验收标准
- 发布前必须过敏感扫描（`tools/sensitive_scan.py`，P1 落地）
- 不在产品仓（`aiops-platform`）或开源仓（`aiops-platform-oss`）内开发本站
