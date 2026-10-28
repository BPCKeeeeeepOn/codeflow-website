# TestHub 智能测试管理平台 · 官网设计文档

> **调研对象**：`https://testhub.aisky.cloud/`（TestHub 官网 / 产品介绍站）
> **调研方式**：静态取证 —— 站点为 Vue3 + Vite 构建的 SPA，首页路由 `/#/` 拉取主 bundle `assets/index-BzJWdXEc.js`（238 KB），全部文案、路由、对比表、Skills 目录与开源项目目录均在该 bundle 内。
> **取证时间**：2026-10-28
> **主体**：杭州智穹云启科技有限公司
> **作者**：大刚（据官网 FAQ：前期作者个人开发，现已组建团队）

---

## 0. 文档定位与证据边界

### 0.1 这份文档是什么

对 TestHub **官网**（营销/产品介绍站）的结构化拆解，覆盖：信息架构、全量功能矩阵、Skills 生态目录、开源项目目录、版本对比模型、商业模式、技术栈披露、合规文本。

### 0.2 证据来源与强度

| 来源 | 强度 | 说明 |
|---|---|---|
| 官网主 bundle 静态字符串 | **强** | 路由表、对比表、Skills 目录、FAQ、隐私政策均为构建产物，逐字可复现 |
| 官网 HTML head | 强 | 标题、meta description、静态资源指纹 |
| 腾讯文档 `docs.qq.com/aio/*`（13 篇） | 中 | 产品内嵌的关联文档；部分为第三方 Skill 介绍，部分为产品自身素材 |
| 伴生部署 `extesthub.aisky.cloud` | **参考** | 同一产品的另一构建，暴露了应用侧模块划分。**仅作旁证**，已在 §9 单独标注 |

### 0.3 明确未覆盖（不臆测）

- **未渲染验证**：官网为客户端渲染，本次调研未做浏览器渲染（ZCode 的 `node_repl` 宿主进程 cwd 失效导致浏览器工具不可用），因此**页面视觉布局、动效、响应式断点、图片素材**均不在本文范围。
- **未做交互**：登录流程、VIP 购买流程、Skills 下载流程未实际执行。
- **未读后端**：`/api` 命名空间虽可从伴生部署的 bundle 观察到，但官网本身不含后端信息。
- **腾讯文档权限**：`manage.search_file` 在本账号的个人空间返回空；`get_content` 读取 `aio/` 类文档返回 `len=0`（AI 笔记格式不支持正文提取）。仅成功读取 3 篇。

---

## 1. 产品定位

### 1.1 一句话

> **以 AI 驱动的全栈测试管理平台**，融合需求分析、用例管理、API 测试、UI/APP 自动化与数据工厂，让测试流程更标准、更高效、更可追溯。

### 1.2 目标客群（官网 FAQ 原文）

> 适合需要"从需求到自动化"的测试团队：互联网 / ToB / 研发效能团队；也适合希望统一管理 API、Web UI、APP 自动化资产的组织。

### 1.3 价值主张（首页四大板块）

| 板块 | 标题 | 副文案 | 具体能力 |
|---|---|---|---|
| 1 | **从需求到用例，从页面到步骤，让"生成"成为默认** | 解析 PDF/Word/TXT 需求文档，自动提取业务需求 | 需求点结构化 · 用例自动生成 · 流式输出 |
| 2 | **API + Web UI + Android APP，全链路覆盖** | — | API 集合/环境变量/套件执行/定时任务/Allure 报告；Web UI 用 Selenium + Playwright 双引擎 + 元素库 + POM；Android 用 Airtest + 设备资源池 + UI Flow 编排；执行记录/截图/视频/统计看板 |
| 3 | **统一身份、权限与团队协作，让平台可在组织内扩展** | — | JWT 双 Token + 自动刷新 + Token 黑名单；项目/版本/成员/角色权限控制；用例评审工作流（模板/检查清单/多层级意见）；企业微信/钉钉 Webhook |
| 4 | **环境检测、驱动管理与模型配置统一入口，降低运维与接入成本** | — | 自动检测系统浏览器与 Playwright 环境；一键安装/更新浏览器驱动；按角色配置模型参数并支持连接测试 |

### 1.4 四大标签

- 测试人最全的 **AI 脚手架平台**
- 一站式搞定：**AI 需求分析、用例管理与评审、API 测试、Web/UI/APP 自动化与数据工厂**
- 支持**个人学习、私有化部署、二次开发**，开箱即用
- 一个平台，覆盖测试全流程 —— 把需求、用例、评审、执行、报告和工具链统一起来

---

## 2. 信息架构

### 2.1 路由表（全部 5 条）

| 路径 | 组件 | 用途 |
|---|---|---|
| `/` | `HomePage` | 首页：Hero + 四大价值主张 + 功能全景 + 开源专区 + VIP 对比 + FAQ + 隐私政策 |
| `/skills` | `SkillsPage` | Skills 专区：全量技能目录 + 分组筛选 |
| `/vip` | `VipPage` | VIP 服务介绍：8 大权益 + 版本对比表 + 会员 FAQ |
| `/docs/:pathMatch(.*)*` | — | 平台内置文档（登录后可见） |
| `/:pathMatch(.*)*` | — | 404 兜底 |

### 2.2 全局组件

| 组件 | 作用 |
|---|---|
| `AppNavbar` | 顶部导航 |
| `AppFooter` | 页脚（FAQ 锚点 / 返回顶部 / 版权） |
| `AuthModal` | 登录注册弹窗（不跳独立页） |
| `PlatformMobileTipModal` | 移动端提示：**"平台暂未适配移动端，请使用 PC 浏览器访问"** |
| `AppToast` | 全局轻提示 |
| `CellDisplay` / `ComparisonTable` | 版本对比表渲染（可展开行，状态三态：`supported` / `unsupported` / `string` / `neutral`） |

### 2.3 路由守卫

```js
router.beforeEach((to) => {
  // 1) 带 hash 的跳转原样放行（锚点）
  if (to.hash) return { path: to.path, query: to.query }
  // 2) 需要鉴权的路径 + /docs/* → 无 token 则重定向到 home，并带 intent
  if (to.meta.requiresAuth || to.path.startsWith(docsPrefix)) {
    if (!localStorage.getItem('access_token') && !localStorage.getItem('testhub_auth')) {
      return { name: 'home', query: { intent: to.fullPath } }
    }
  }
})
```

**关键设计**：鉴权失败不是跳 401 页，而是**回首页 + `?intent=` 记住来源**，首页再弹 `AuthModal`。登录后凭 `intent` 跳回。

### 2.4 首页纵向叙事顺序

```
Hero（"测试人最全的 AI 脚手架平台" + 三行数字 + 部署命令前置）
  → 四大价值主张（feature-reveal 滚动揭示）
  → 8 大功能板块卡片
  → 适合哪些团队 / FAQ（4 问）
  → 企业专属版本·私有化定制
  → 开源专区（5 分类 33 项目）
  → VIP 对比（ComparisonTable）
  → VIP 8 大权益
  → 会员 FAQ（10 问）
  → 隐私政策（8 章）
  → 页脚
```

---

## 3. 全量功能矩阵（8 大板块）

### 3.1 能力总表

| # | 板块 | 核心能力 | 关键实现 |
|---|---|---|---|
| 1 | **AI 用例生成** | 上传需求文档 → 自动提取需求点 → 生成用例草稿 | 需求点结构化 / 用例自动生成 / **流式输出** / 用例单个·批量采纳·弃用 / 异步批量导入 / 导出 Excel / 导出时自定义字段 |
| 2 | **用例评审** | 多人评审、模板与检查清单，提升用例质量与一致性 | 工作流状态 / 多层级意见 / 模板复用 / 评审模板 / 版本管理 |
| 3 | **API 测试** | 从调试到批量执行与报告，形成可复用的接口资产 | 环境变量 / 集合管理 / 请求调试 / 套件执行 / 定时任务 / **Allure 报告** / 历史记录 / cURL 导入导出 / Mock URL |
| 4 | **Web UI 自动化** | 元素库 + POM + 脚本编辑 + 多浏览器执行 | 录制回放 / 元素库 / 脚本编辑 / 套件 / 执行记录 / 截图 / 视频 |
| 5 | **Android APP 自动化** | Airtest 图像识别 + 设备资源池 + UI Flow 编排 | 设备管理 / 组件化编排 / 异步执行 / 设备锁 / ADB 远程连接 |
| 6 | **数据工厂** | 51+ 实用工具，覆盖编码/随机/加密/JSON/Crontab 等 | 标签系统 / 历史记录 / 一键引用 / 分类 / 统计 |
| 7 | **AI 问答助手** | 基于 **Dify 工作流**的知识库 + AI 问答机器人 | 专属知识库 / 工作流编排 / 多模型接入 / 悬浮助手 |
| 8 | **统一配置中心 & 安全** | 驱动/模型/通知统一配置，JWT 与权限体系 | 环境检测 / 模型连接测试 / 权限控制 / 通知配置 / 日志 |

### 3.2 技术栈（官网自述 + 对比表佐证）

| 层 | 开源版 | VIP 版 |
|---|---|---|
| 前端 | Vue 3 + Vite（免构建，与本站同构） | 同 + 全面统一图标 |
| 后端 | **Django 4.2** | **Django 6.0（最新）** |
| 任务队列 | **Celery** | **Redis + Django-Q2（轻量级任务队列）** |
| 调度 | APScheduler | Django-Q2 框架 |
| 配置 | `.env` 管理 | `config.yaml` 配置统一 |
| 认证 | JWT 双 Token + 自动刷新 + Token 黑名单 | 同 |
| 部署 | Docker 镜像，一键部署 | 同 + 远程部署指导 |

> 对比表另有一行「代码行数：VIP 版 50 行 / 开源版 192 行」——指**配置代码行数**（config.yaml vs .env），非产品总代码量。

### 3.3 AI 模型接入

- **多模型可选**：DeepSeek / 通义千问 / 硅基流动 等（伴生部署的模型配置页还列出了 `openai` / `azure_openai` / `anthropic` / `google_gemini` / `deepseek` / `siliconflow` / `zhipu` / `other` 八类 provider）
- **按角色配置模型参数** + **连接测试**（便于替换与成本控制）
- **Dify 工作流**作为 AI 问答与知识库的编排底座

### 3.4 部署与交付形态

| 形态 | 说明 |
|---|---|
| SaaS | `testhub.aisky.cloud`，登录后即可用 |
| 私有化部署 | **支持**。后端 Django + 前端 Vue3/Vite，可部署到内网，并扩展组织级权限、通知与审计 |
| 二次开发 | 提供基建底座，官方称"支持二次开发" |
| 桌面浏览器 | **移动端未适配**，仅 PC 浏览器 |

---

## 4. Skills 生态（全量目录 · 15 分类 36 项）

> Skills = 可复用的 AI 工作流单元。官网分两套目录：**Skills 专区**（TestHub 自研/精选，带描述、标签、飞书/百度网盘下载链接、VIP 标记）与**开源专区**（GitHub 项目，带 star 数）。

### 4.1 Skills 专区（按测试流程阶段划分）

#### ① 需求分析评审（5 项）

| Skill | VIP | 描述 | 标签 |
|---|:--:|---|---|
| `requirements-analysis` | | 专业需求分析师，多轮对话将简短想法转化为详细需求文档，支持 EPIC 分解/优先级排序 | 想法转需求文档 |
| `test-requirement-analysis` | ✓ | 测试需求分析，从 PRD/用户故事/原型图输出结构化测试需求分析报告 | 结构化需求分析 |
| `requirement-decomposition` | ✓ | 需求结构化拆解，**12 维度**识别关键信息（功能目标/业务规则/状态流转/数据逻辑等） | 多维度需求分析 |
| `requirement-reviewer` | | 需求文档/PRD 逻辑审查 + 完整性评估 + **100 分制打分，低于 60 分标记不通过** | 需求评审打分 |
| `lanhu-to-prd Skill` | ✓ | 蓝湖专用 PRD 生成器，**MCP 直连蓝湖**，一键拉取全部页面/标注/交互/评论 | 设计稿转需求文档 |
| `requirement-annotator` | ✓ | 需求理解 Skill 自动批注、矛盾校验，直接生成评审提问清单 | — |

#### ② 测试方案设计（1 项）

| Skill | VIP | 描述 |
|---|:--:|---|
| `test-plan-designer` | ✓ | 测试方案/计划设计专家，**11 节可执行测试方案**（目标/范围/策略/环境/数据/依赖/风险/准入准出） |

#### ③ 测试用例生成（4 项）

| Skill | VIP | 描述 |
|---|:--:|---|
| `test-point-generator` | | 测试点生成专家，从需求/PRD 按 **14 个测试维度**生成测试点清单，支持飞书/XMind 导出 |
| `universal-testcase-generator` | ✓ | 全能测试用例生成器，支持 PRD/接口文档/设计截图/在线文档，输出 Markdown/飞书思维导图/XMind |
| `prd-to-xmind-testcases` | ✓ | PRD/接口文档转飞书兼容的 Markdown 格式测试用例思维导图 |
| `generator-testcase` | | 基于 TestHub 平台内置提示词制作，生成详细测试用例并自动进行质量审查、评审打分 |
| `testcase-writer` | ✓ | 从需求/PRD/测试点清单生成可执行正式用例，**覆盖 13 种用例类型**，输出 11 字段标准化表格 + 待确认问题 + 覆盖自检 + 遗漏风险；支持极简需求（追问模式）与详细需求（直接生成模式）；对金额/算法/AI 交互场景强制补充专项用例 |

#### ④ 测试用例评审（1 项）

| Skill | VIP | 描述 |
|---|:--:|---|
| `testcase-quality-reviewer` | | 批量用例质量审核，**五维评分表 + 逐条问题定位 + 覆盖分析，60 分及格线** |
| `testcase-reviewer` | ✓ | 测试用例评审专家，反向检查覆盖度 + **8 部分**结构化评审报告，聚焦"是否足以支撑测试完成结论" |

#### ⑤ 接口测试（5 项）

| Skill | VIP | 描述 |
|---|:--:|---|
| `api-testcase-generator` | ✓ | 接口测试用例生成器，支持 **Postman/Apipost/Swagger/OpenAPI**，覆盖正常/边界/错误/认证场景 |
| `api-testcase-writer` | ✓ | 一键生成测试用例 + 自动化脚本（把上游参数矩阵/断言矩阵/依赖契约合成为可评审、可追溯、可导入的标准用例条目，产出 JSON 可直接喂给脚本生成器） |
| `api-dependency-analyzer` | ✓ | 接口依赖分析器，生成接口依赖图 |
| `api-assertion-designer` | ✓ | 输入接口定义和测试场景，输出 **7 个维度**的断言矩阵和可直接执行的脚本 |
| `api-param-combiner` | ✓ | 自动生成参数搭配矩阵，搞定隐藏漏测 |

#### ⑥ 知识图谱（1 项）

| Skill | VIP | 描述 |
|---|:--:|---|
| `knowledge-graph-builder` | | 通用知识图谱构建器。检查环境 → 分析文档 → 构建知识图谱 → 生成交互式 HTML 页面。支持任意目录的 Markdown/代码/PDF/图片文档，自动适配 LLM API 配置 |

#### ⑦ 缺陷管理（4 项）

| Skill | VIP | 描述 |
|---|:--:|---|
| `bug-report-writer` | | AI Bug 提单助手，截图/日志/描述自动生成标准化 Bug 报告，支持**飞书/禅道/TAPD/Markdown** |
| `bug-report-writer-tapd` | | TAPD 专用 Bug 报告生成器，支持 TAPD 格式导出和一键提交（**MCP + API**） |
| `bug-stats-reporter` | | 从禅道/TAPD 导出的 Bug 表自动生成统计报告，支持周报/迭代回顾/可视化看板 |
| `bug-fix-verifier` | ✓ | Bug 修复验证专家，**7 检查点**验证闭环：已复现 + 失败测试 + 最小修复 + 通过测试 + 边界验证 + 回归范围 + 关闭证据 |
| `defect-analyzer` | ✓ | 系统化缺陷根因分析专家，**11 部分**结构化输出，严格区分事实和假设 |

#### ⑧ 性能测试（7 项，全部 VIP）

| Skill | 描述 |
|---|---|
| `perf-requirement-clarifier` | 性能测试需求澄清，明确压测目标/范围/SLA 指标/负载模型/验收标准 |
| `perf-test-planner` | 性能测试计划生成，场景分层/算力估算/流量模型/施压模式/风险预案 |
| `perf-data-builder` | 压测数据构造助手，支持 **DDL 建表**和**接口调用**两种方式生成测试数据 |
| `perf-jmx-generator` | JMeter JMX 脚本生成，全链路联动 + 分布式适配 + 长稳防 OOM |
| `perf-readiness-checker` | 压测就绪检查，**9 大维度 60+ 检查项** |
| `perf-report-analyzer` | 压测报告分析，解析 JMeter CSV/HTML/JSON + 多维度监控数据，定位瓶颈 |
| `perf-report-writer` | 性能测试报告生成，4 类受众视图/数据一致性校验/5 种格式导出 |

#### ⑨ 测试报告（1 项）

| Skill | VIP | 描述 |
|---|:--:|---|
| `test-report-writer` | ✓ | 测试报告生成，**3 类报告 × 4 类受众视图**，自动计算 **9 项指标**，5 种格式导出 |

#### ⑩ APP 自动化测试（2 项）

| Skill | VIP | 描述 |
|---|:--:|---|
| `mobile-app-testing` | | 手机 APP 测试 Skill，覆盖单元测试、UI 自动化与性能测试 |
| `android-device-automation` | | 使用 **Midscene** 实现视觉驱动的 Android 设备自动化。完全基于屏幕截图操作——**无需依赖 DOM 树或无障碍标签** |

#### ⑪ Web 自动化测试（4 项）

| Skill | VIP | 描述 |
|---|:--:|---|
| `Playwright Skill` | | Playwright 技能库，包含 Playwright 的全部功能 |
| `browser-use` | | 自动化处理浏览器交互，适用于 Web 测试、表单填写、网页截图及数据提取 |
| `dev-browser` | | 支持保持页面状态的浏览器自动化 |
| `browserwing` | ✓ | 通过 **HTTP API** 控制浏览器自动化的技能，支持页面导航、元素交互、数据提取、无障碍快照分析、截图及批量操作 |

#### ⑫ 开发工具（3 项）

| Skill | 描述 |
|---|---|
| `Anthropics Skills` | Anthropics 官方出品的技能库 |
| `GLM Skills` | 智谱出品的 GLM 技能库合集 |
| `Awesome Claude Skills` | 精选的 Claude 技能、资源和工具列表 |

#### ⑬ 设计（1 项）

| Skill | 描述 |
|---|---|
| `frontend-design` | 前端开发设计 Skill，辅助前端页面构建 |

> 其余分类（办公 / 其他）在官网当前构建中为空壳占位。

---

## 5. 开源生态（全量目录 · 5 分类 33 项目）

> 定位："精选测试与开发领域的优秀开源项目，助力提升研发效能"。

### 5.1 AI 测试框架/智能体（8 项）

| 项目 | Star | 说明 | 链接 |
|---|---:|---|---|
| Midscene | 233k+ | 字节官方出品的 AI 测试框架，支持浏览器、Android 手机、电脑桌面端 | [web-infra-dev/midscene-example](https://github.com/web-infra-dev/midscene-example) |
| Browser Use | 94.6k+ | 基于自然语言的 Web 端 AI 测试框架 | [browser-use/browser-use](https://github.com/browser-use/browser-use) |
| Scrapling | 64.7k+ | Playwright 的浏览器能力 + Scrapy 的工程框架 + 自研自适应算法 | [D4Vinci/Scrapling](https://github.com/D4Vinci/Scrapling) |
| HackingTools | 75.5k+ | 一个集合了多个安全测试工具的项目 | [Z4nzu/hackingtool](https://github.com/Z4nzu/hackingtool) |
| UI TARS Desktop | 34.7k+ | 字节跳动官方出品的 UI-TARS 桌面端智能体应用程序 | [bytedance/UI-TARS-desktop](https://github.com/bytedance/UI-TARS-desktop) |
| Open-AutoGLM | 25.3k+ | 智谱出品的手机端开源测试框架 | [zai-org/Open-AutoGLM](https://github.com/zai-org/Open-AutoGLM) |
| MobileAgent | 8.7k+ | 阿里巴巴通义实验室出品的手机测试智能体 | [X-PLUG/MobileAgent](https://github.com/X-PLUG/MobileAgent) |
| Computer Use Preview | 2.9k+ | 谷歌 Gemini 官方出品的 AI 测试框架 | [google-gemini/computer-use-preview](https://github.com/google-gemini/computer-use-preview) |
| QA Use | 560+ | browser-use 官方出品的 AI 原生 E2E 测试平台，自然语言一键跑通用例 | [browser-use/qa-use](https://github.com/browser-use/qa-use) |

### 5.2 Skills 专区（7 项）

| 项目 | Star | 说明 | 链接 |
|---|---:|---|---|
| Anthropics Skills | 138k+ | Anthropics 官方出品的技能库 | [anthropics/skills](https://github.com/anthropics/skills) |
| Awesome Claude Skills | 60.6k+ | 精选 Claude 技能/资源/工具列表 | [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) |
| Product Manager Skills | 6k+ | 精选的产品管理技能库 | [deanpeters/Product-Manager-Skills](https://github.com/deanpeters/Product-Manager-Skills/tree/main) |
| Playwright Skill | 2.6k+ | Playwright 技能库，包含全部功能 | [lackeyjb/playwright-skill](https://github.com/lackeyjb/playwright-skill) |
| GLM Skills | – | 智谱出品的 GLM 技能库合集 | [modelscope 集合](https://www.modelscope.cn/collections/ZhipuAI/GLM-skills) |
| frontend-design | – | 前端开发设计 Skill | [anthropics/claude-code](https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design/skills/frontend-design) |
| mobile-app-testing | – | 手机 APP 测试 Skill | [lobehub](https://lobehub.com/zh/skills/secondsky-claude-skills-mobile-app-testing?activeTab=installation) |

### 5.3 Agent 专区（10 项）

| 项目 | Star | 说明 | 链接 |
|---|---:|---|---|
| Superpowers | 198k+ | 提供一整套完整且有效的软件开发方法论 | [obra/superpowers](https://github.com/obra/superpowers) |
| Hermes Agent | 158k+ | 智能体界的"爱马仕" | [nousresearch/hermes-agent](https://github.com/nousresearch/hermes-agent) |
| LobeHub | 77.3k+ | 7×24 小时的代理运营商 | [lobehub/lobehub](https://github.com/lobehub/lobehub) |
| rtk | 63.4k+ | 帮助 AI Coding 节约 Token 的神器 | [rtk-ai/rtk](https://github.com/rtk-ai/rtk) |
| CodeWhale | 38.6k+ | DeepSeek V4 的御用驾驶舱 | [Hmbown/CodeWhale](https://github.com/Hmbown/CodeWhale) |
| Archon | 22.4k+ | AI 编码工作流引擎，让 AI Coding 不再抛硬币 | [coleam00/Archon](https://github.com/coleam00/Archon) |
| OpenHuman | 20.4k+ | 您的个人 AI 超级智能 | [tinyhumansai/openhuman](https://github.com/tinyhumansai/openhuman) |
| QwenPaw | 16.8k+ | 千问版开源"龙虾" | [agentscope-ai/QwenPaw](https://github.com/agentscope-ai/QwenPaw/tree/main) |
| joyagent-jdgenie | 11.8k+ | 来自京东的开源端到端产品级通用智能体 | [jd-opensource/joyagent-jdgenie](https://github.com/jd-opensource/joyagent-jdgenie) |
| Hermes Desktop | – | 专为 Hermes 量身打造的桌面端 | [dodo-reach/hermes-desktop](https://github.com/dodo-reach/hermes-desktop) |

### 5.4 RAG 专区（4 项）

| 项目 | Star | 说明 | 链接 |
|---|---:|---|---|
| CodeGraph | 51.3k+ | 建立本地代码知识图谱索引 | [colbymchenry/codegraph](https://github.com/colbymchenry/codegraph) |
| Graphify | 49.5k+ | Karpathy 知识库工作流终极进化 | [safishamsi/graphify](https://github.com/safishamsi/graphify) |
| Understand Anything | 15.2k+ | 用知识图谱搞懂代码库 | [Lum1104/Understand-Anything](https://github.com/Lum1104/Understand-Anything) |
| LLM Wiki | 8.2k+ | 基于 Andrej Karpathy 提出的 LLM Wiki 方法论 | [nashsu/llm_wiki](https://github.com/nashsu/llm_wiki) |

### 5.5 其他 AI 工具（6 项）

| 项目 | Star | 说明 | 链接 |
|---|---:|---|---|
| Warp | 59.1k+ | 自带 AI 的终端神器 | [warpdotdev/Warp](https://github.com/warpdotdev/Warp) |
| career-ops | 54.5k+ | AI 求职系统 | [santifer/career-ops](https://github.com/santifer/career-ops) |
| Ruflo | 53.1k+ | 让 Claude Code 变身"AI 军团指挥中心" | [ruvnet/ruflo](https://github.com/ruvnet/ruflo) |
| CloakBrowser | 26.5k+ | 强反检测浏览器方案 | [CloakHQ/CloakBrowser](https://github.com/CloakHQ/CloakBrowser) |
| PPT Master | 18.6k+ | AI PPT 工具 | [hugohe3/ppt-master](https://github.com/hugohe3/ppt-master) |
| multica | – | 一款可以托管 AI 智能体的平台 | — |

---

## 6. 商业模式：VIP vs 开源

### 6.1 版本对比（13 项，官网 ComparisonTable 原文）

| 维度 | VIP 版 | 开源版 |
|---|---|---|
| **源码** | VIP 版源码，持续更新，一键拉取 | GitHub 开源版 |
| **Skills** | 测试全流程 Skills，配套图文教程 | 自行开发收集 |
| **社群** | 专属 VIP 群聊 | 免费群，自由讨论 |
| **答疑** | 问题 1V1 解答 | 酌情回复 |
| **教程** | 专属图文或视频类使用教程 | 项目内置文档 |
| **任务队列** | Redis + Django-Q2 | Celery 队列 |
| **调度框架** | Django-Q2 框架 | 内置 APScheduler |
| **配置** | config.yaml 配置统一 | .env 管理 |
| **后端版本** | Django 最新 6.0 | Django 4.2 |
| **图标** | 全面统一图标 | 原始图标 |
| **项目打通** | 统一项目打通，自由关联各个模块 | 各个模块单独创建项目 |
| **配置代码行数** | 50 行 | 192 行 |
| **部署** | Docker 镜像，一键部署 | 不支持 |

### 6.2 VIP 8 大专属权益

| # | 权益 | 说明 |
|---|---|---|
| 1 | **VIP 专属版本** | 增强功能，含源码，持续更新 |
| 2 | **Skills 商店 VIP 下载** | 解锁 VIP 专属全链路测试提效 Skills |
| 3 | **专属 VIP 社群** | 专属群聊 |
| 4 | **线上体验环境访问试用** | VIP 版线上体验环境 |
| 5 | **专属图文/视频教程** | 专属图文或视频类使用教程 |
| 6 | **远程部署指导** | 安装部署可远程指导 |
| 7 | **代码拆解分析** | 代码关键点拆解分析 |
| 8 | **需求优先响应** | 需求评估可优先响应 |

### 6.3 商业条款（FAQ 原文要点）

| 议题 | 答复 |
|---|---|
| 是否年费 | **年费制，有效期一年**；续费有大额折扣 |
| 到期后代码还能用吗 | **可以**。已拉取的代码可继续使用，只是不能拉取新代码、不再享受 VIP 服务 |
| 发版节奏 | 每月 **1-2 次**发版，每月一个大版本 |
| 私有化部署 | 支持，部署到自己电脑或公司服务器 |
| 二次开发 | 提供完善基建底座，支持二次开发 |
| 开发团队 | 前期作者（大刚）一人，后续组建团队 |
| 共创激励 | 优秀功能设计可合作（有分成）；自媒体推广有分成；体验类文章有稿费 |
| 开通方式 | 微信扫码或搜索 `cloud288` 添加 |

---

## 7. 首页与内容设计

### 7.1 Hero 区

- 主标题：**测试人最全的 AI 脚手架平台**
- 副标题两行：
  - 一站式搞定：AI 需求分析、用例管理与评审、API 测试、Web/UI/APP 自动化与数据工厂
  - 支持个人学习、私有化部署、二次开发，开箱即用
- 三个"实测数字"行（从 bundle 的文案模板可见存在该结构）
- **部署命令前置**到首屏
- 登录后可见完整功能介绍、技术细节与最佳实践（`/docs/*` 受 `requiresAuth` 保护）

### 7.2 FAQ（首页 4 问）

| 问题 | 答 |
|---|---|
| TestHub 适合哪些团队？ | 互联网/ToB/研发效能团队；统一管理 API/Web UI/APP 自动化资产的组织 |
| 能否私有化部署？ | 可以。后端 Django，前端 Vue3/Vite，可部署内网并扩展组织级权限、通知与审计 |
| AI 能力需要绑定某家模型吗？ | 不需要。支持多模型配置，可按角色设置不同模型与参数，提供连接测试，便于替换与成本控制 |
| 自动化报告如何查看？ | 支持生成 Allure 报告，平台侧保留执行记录与关键产物（日志、截图、视频） |

### 7.3 合规文本：隐私政策（8 章）

- **版本**：更新日期 / 生效日期 均为 **2026 年 5 月 3 日**
- 收集信息：用户名（账号标识）、密码（加密存储，不存明文）、验证码（即时失效）、登录时间与 IP（仅用于安全审计与异常登录检测）
- 使用目的：验证身份 / 平台功能服务（测试管理、自动化执行、报告生成）/ 检测防范安全威胁 / 遵守法规
- 共享边界：法律法规要求 / 关联方共享（限服务必需范围，受本协议约束）/ 授权合作伙伴（短信服务商仅发验证码，**不存手机号**）
- 存储与传输：境内存储，**不跨境传输**；仅在服务必需期间保留，注销后删除或匿名化
- 权利：查看修改、注销账户、撤回同意、获取副本
- Cookie：仅用 localStorage 存 Token 维持登录态，**不使用追踪型 Cookie**
- 未成年人：主要面向专业测试人员；未满 18 周岁需监护人陪同
- 联系方式：`support@testhub.local`，周一至周五 09:30-19:00，**15 个工作日内**回复

---

## 8. 关联的腾讯文档（13 篇）

官网 bundle 内嵌 13 个 `docs.qq.com` 链接，其中 12 个为 `aio/`（AI 笔记）、1 个为 `space/`。已成功读取 3 篇，内容为**第三方 Skill 介绍**（非产品自身设计文档）：

| 文档 | 内容摘要 |
|---|---|
| `aio/DRU9PdktjUWZKUHBV` | **api-testcase-writer** 详解：把 api-param-combiner 的参数矩阵、api-assertion-designer 的断言矩阵、api-dependency-analyzer 的编排契约合成为可评审、可追溯、可导入的标准用例条目；"不编造"红线（无契约背书一律标 `PENDING-XX`）；产出 JSON 可直喂 api-script-generator 生成 pytest 脚本；约 30% 为待人工确认项 |
| `aio/DRVR4bEFndXdmTUV6` | **testers.ai** 介绍：31 个专业 AI 测试代理、三大模式（Bug Detection / Persona Feedback / Test Case Generation）；文档内含**用 testers.ai 测试 TestHub 自身的实战案例**，默认账号 `testadmin/admin123456`，本地地址 `http://127.0.0.1:3000` |
| `aio/DRU9PdktjUWZKUHBV` 外另一篇 | 未能读取（`get_content` 对 `aio` 类返回空或无权限） |

**结论**：这些是生态内的第三方技能介绍，**不是 TestHub 的产品设计文档**。TestHub 自身的产品设计文档位于站内 `/docs/*`（需登录）。

---

## 9. 应用侧模块划分（旁证，非官网内容）

> ⚠️ **本节来自伴生部署 `extesthub.aisky.cloud` 的前端 bundle**，标题为 "TestHub - AI一体化测试平台"，与官网是同一产品的不同构建。列入本节仅为**佐证官网功能描述的落地形态**，不作为官网设计的一部分。

前端路由共 **81 条**，四大业务命名空间：

| 命名空间 | 前端模块 | 后端 API 前缀 |
|---|---|---|
| **接口测试** | Dashboard / Projects / Interfaces / Automation / History / Environments / Reports / ScheduledTasks / AIServiceConfig / NotificationLogs | `/api/api-testing/*` |
| **UI 自动化** | Dashboard / Projects / ElementsEnhanced / TestCases / ScriptsEnhanced / ScriptEditor / Suites / Executions / Reports / ScheduledTasks | `/api/ui-automation/*` |
| **APP 自动化** | Dashboard / ProjectList / DeviceList / PackageList / ElementList / SceneBuilder / TestCaseList / TestSuiteList / Executions / Reports | `/api/app-automation/*` |
| **数据工厂** | DataFactory | `/api/data-factory/*` |
| AI 智能模式 | AITesting / AICaseList / AIExecutionRecords | — |
| 配置中心 | AIModel / PromptConfig / GenerationConfig / UIEnv / AppEnv / AIMode / ScheduledTask / Dify | — |

**应用侧能力细节**（从 chunk 中文文案提取）：

- **APP 自动化元素采集三种类型**：坐标元素（`x,y`）、区域元素（左上/右下角坐标）、**图片元素**（从设备截图创建，OCR 定位 + 匹配阈值，彩色/彩色界面）
- **场景编排（SceneBuilder）**：拖拽式组件编排，含"先检测图片 A → 再点击 B"的条件分支、"保存为变量"（变量名/类型/值/作用域）、自定义组件、组件包导入导出
- **设备管理**：本地模拟器 / 远程设备（IP+端口，**网络 ADB（adb tcpip 5555）**）、设备锁定与解锁、刷新重连
- **定时任务**：Cron 表达式（分/时/日/月/周）、固定间隔、单次执行、失败时通知、成功时通知；示例「每周一9点」「每天0点」「每小时」「每月1号0点」
- **报告**：Allure 报告 + 平台侧统计（套件总数/用例总数/步骤总数、平均通过率、执行耗时、失败步骤定位）
- **执行记录**：实时状态（等待中/执行中/已完成/已停止/执行异常）、步骤统计、WebSocket 状态轮询、停止执行、批量删除
- **需求分析**：**SSE 流式**推送用例生成结果，失败自动降级到轮询模式

---

## 10. 关键设计决策与观察

### 10.1 做对了什么

| 决策 | 价值 |
|---|---|
| **Skills 是一等公民** | 36 项技能按测试流程阶段（需求→方案→用例→评审→接口→缺陷→性能→报告）编排，而非按功能菜单编排。技能有明确输入/输出契约（如 api-testcase-writer 产出的 JSON 可直接喂 api-script-generator） |
| **"不编造"作为硬红线** | `PENDING-XX` 编号机制（Markdown 与 JSON 双格式同源同号）——宁可给待确认清单，不给假的全绿。这与 AI 运维领域"证据链强制引用"是同一类设计 |
| **评分 + 及格线量化评审** | 需求 100 分制 <60 不通过；用例五维评分 60 分及格；压测就绪 9 维度 60+ 检查项。把"评审"从主观变可度量 |
| **VIP 差异定位在运维成本** | 差异不落在功能多寡（Django 6.0 vs 4.2、Celery vs Django-Q2、config.yaml vs .env、图标统一），而落在**"少踩坑"**（统一项目打通、源码持续更新、1V1、远程指导）——对测试团队是真实痛点 |
| **开源区做流量入口** | 33 个高质量开源项目带 star 数，是 SEO + 信任背书双重作用 |
| **移动端明确不支持** | 不做半吊子响应式，直接弹提示要求 PC 浏览器 |

### 10.2 值得注意的取舍

| 取舍 | 分析 |
|---|---|
| **官网 = 产品介绍 + 目录 + 付费转化** | 5 条路由里 3 条是转化向（/ /vip /skills），深度文档藏在登录后 `/docs/*`。这与"开源/商业双轨"的商业模型一致 |
| **开源版各模块独立建项目** | 开源版降低了"统一项目打通"的实现复杂度，但也让跨模块资产关联断裂——这正是 VIP 版的核心卖点之一。**开源版不是功能阉割版，是架构阉割版** |
| **Celery → Django-Q2** | VIP 换掉 Celery 上 Redis，说明官方认为 Celery 对单机部署过重。开源版保留 Celery 可能是历史包袱，也可能是给"要上生产"的团队留选择 |
| **8 大 VIP 权益里有 6 项是"服务"而非"功能"** | 社群、1V1、教程、远程指导、优先响应、拆解分析——本质是**用服务换源码**，与 AGPL 类项目的常见变现路径一致 |

### 10.3 待验证 / 存疑

| 项 | 状态 |
|---|---|
| 官网视觉设计与响应式断点 | **未验证**（浏览器工具不可用，未渲染） |
| 登录后 `/docs/*` 的完整文档体系 | **未读**（需账号） |
| 应用侧 81 条路由与官网 8 大板块的对应关系 | **部分对应**，但应用侧有官网未提的「AI 智能模式」「配置中心」两大独立模块 |
| 官网提到的「51+ 实用工具」具体清单 | 未逐项取证（仅确认分类/统计/历史/标签/引用五个能力项） |
| Star 数为静态快照 | 官网 bundle 硬编码，非实时拉取；**已过期风险** |
| 第三方文档提到的默认账号 `testadmin/admin123456` | 来自第三方 Skill 介绍文档，非官网披露；**未验证** |

---

## 11. 复现命令

```bash
# 官网入口
curl -sS https://testhub.aisky.cloud/            # 708 字节 SPA 空壳
curl -sS https://testhub.aisky.cloud/assets/index-BzJWdXEc.js -o /tmp/testhub.js   # 238KB 主 bundle

# 提取路由（注意：反引号字符串，不是双引号）
grep -oE 'path:`[^`]{1,80}`' /tmp/testhub.js

# 提取 Skills 目录（分类 + 技能条目，含 VIP 标记）
grep -oE '\{name:`[^`]{1,30}`,icon:`[A-Za-z0-9]+`,skills:\[' /tmp/testhub.js

# 提取版本对比表
grep -oE '\{feature:`[^`]{1,60}`,planet:`[^`]{0,40}`,openSource:`[^`]{0,60}`\}' /tmp/testhub.js

# 提取腾讯文档关联链接
grep -oE 'https://docs\.qq\.com/(aio|space)/[A-Za-z0-9]+' /tmp/testhub.js | sort -u
```

> **踩坑记录**：用 `path:"..."`（双引号）匹配路由会**得到 0 条**——Vite 压缩后字符串统一为反引号。同理 Skills 条目字段顺序不固定（`vip` 可能出现在 `linkUrl` 之前），正则必须逐字段独立提取，不能假设固定顺序。

---

## 12. 变更记录

| 日期 | 版本 | 变更 |
|---|---|---|
| 2026-10-28 | v1.0 | 首版：官网静态取证，信息架构 / 8 大功能板块 / 36 项 Skills / 33 个开源项目 / 13 项版本对比 / 8 大 VIP 权益 / 技术栈 / 合规文本 / 会员 FAQ / 应用侧旁证 |
