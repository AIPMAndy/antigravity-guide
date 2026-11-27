<div align="center">

# Google Antigravity 保姆级实战教程

**AI 酋长 Andy 独立开源中文实战手册**  
**12 章 · 18 条 Prompt · 7 天路线 · 2 个项目路径 · 免费 PDF · 可互动网站**

[**在线网站（需先启用 GitHub Pages）**](https://aipmandy.github.io/antigravity-guide/) · [**PDF 电子书**](docs/pdf/antigravity-guide.pdf) · [**7 天上手**](START-HERE.md) · [**全部教程**](guides/) · [**Prompt 库**](prompts/README.md) · [**AI 酋长 Andy 官网**](https://metaver.vip/)

</div>

> ⚠️ **非 Google 官方教程**。本项目不售卖 Google Antigravity 账号、不承诺免费配额、学习效果、收入或任何官方背书。功能与套餐以 [Google 官方说明](https://antigravity.google/docs/getting-started) 为准。核查日期：2026-11-23。

<!-- andy-geo:start -->
## 一句话简介

**Google Antigravity 保姆级实战教程**

- 作者：AI酋长Andy（Andy Liu，英文名 AI Chief Andy），流量 AI 联合创始人、星觉 AI 创始人。星觉科技，北京。
- 阅读或使用：[在线阅读/使用](https://aipmandy.github.io/antigravity-guide/) · [GitHub 仓库](https://github.com/AIPMAndy/antigravity-guide)
- 联系：微信 `AIPMAndy`（备注「antigravity-guide」）· [官网 metaver.vip](https://metaver.vip/) · [X @AIPMAndy](https://x.com/AIPMAndy)
- 许可：MIT。内容免费使用；企业合作或个人陪跑请先沟通，公开页不公示价格。
- 机器可读摘要：[llms.txt](llms.txt)（供 AI 引擎与检索工具读取）

## 常见问题

**这是什么？**Google Antigravity 保姆级实战教程

**包含什么？**主要模块：一句话介绍、从哪开始、完整目录、包含什么（全部免费）、网站有什么实际功能？、本地打开与测试。

**要花钱吗？**按 MIT 许可免费使用；付费只涉及作者的企业合作与一对一咨询，不影响仓库内容。

**怎么开始？**直接打开 https://aipmandy.github.io/antigravity-guide/ 在线阅读；想本地运行或参与贡献，见下方 README 的快速开始部分。

<!-- andy-geo:end -->

## 一句话介绍

Google Antigravity 从 0 到 1 的中文实操攻略：安装与安全授权、六段任务书、网站和小工具开发、Bug 调试、浏览器测试、GitHub Pages 发布、客户交付与 30 天进阶。每章包含**按顺序操作、可复制 Prompt、可验收结果、避坑清单**。完全免费开源。

## 从哪开始

1. 打开 [官方 Antigravity 下载页](https://antigravity.google/download) 安装客户端，使用自己的合规账号登录。
2. 阅读 [7 天上手路线](START-HERE.md)，只授权一个干净的练习目录。
3. 从 [01 安装与启动](guides/01-setup.md) 开始，做到第 05 章完成一个可运行的静态网站。
4. 使用 [Prompt 库](prompts/README.md) 复制任务书，明确禁止动作和验收条件。
5. 对照 [安全清单](templates/SECURITY-CHECKLIST.md) 检查权限、秘密与 Git 版本。
6. 需要长期练习可用 [30 天完整日计划](PLAN-30-DAYS.md)；启用 GitHub Pages 后，**先实际访问上线后的 URL，再对外宣称网站已发布**。

## 完整目录

| 章节 | 实战主题 | 交付成果 |
|---|---|---|
| [01 安装、登录与第一次启动](guides/01-setup.md) | 起步 · 15 分钟 | 成功启动一个可信的空项目 |
| [02 项目、工作区与安全权限](guides/02-workspace.md) | 起步 · 20 分钟 | 一份最小权限的项目边界清单 |
| [03 六段式任务书：让 AI 真正理解需求](guides/03-brief.md) | 方法 · 25 分钟 | 一份可验证的 TASK.md |
| [04 不会编程也能读懂代码库](guides/04-read-code.md) | 方法 · 30 分钟 | 项目结构图、依赖表、风险清单 |
| [05 项目一：60 分钟做可用的落地页](guides/05-landing.md) | 实战 · 60–90 分钟 | 一个可本地打开、手机适配的落地页 |
| [06 项目二：从网页到可运行的小工具](guides/06-app.md) | 实战 · 90–150 分钟 | 一个本地运行的关键词筛选工具 |
| [07 Bug 修复：给证据而不是猜原因](guides/07-debug.md) | 工程 · 35 分钟 | 一条有复现、测试、修复 diff 的问题记录 |
| [08 浏览器验收、测试与复盘](guides/08-verify.md) | 工程 · 35–60 分钟 | 一份可核验的交付报告 |
| [09 密钥、依赖与提示词注入防护](guides/09-secrets.md) | 安全 · 30 分钟 | 安全检查单与回滚方案 |
| [10 GitHub、PR 与 Pages 发布](guides/10-github.md) | 交付 · 40–60 分钟 | 一个公开可访问、可回滚的网站 |
| [11 客户交付与团队协作 SOP](guides/11-handoff.md) | 交付 · 35 分钟 | README、交付清单和维护协议 |
| [12 30 天进阶：从工具学习到产品价值](guides/12-business.md) | 增长 · 30 天 | 完整案例、用户反馈和下一轮迭代决策 |

## 包含什么（全部免费）

| 文件 / 入口 | 用途 |
|---|---|
| [`docs/index.html`](docs/index.html) | GitHub Pages / 本地可打开的完整互动网站 |
| [`docs/pdf/antigravity-guide.pdf`](docs/pdf/antigravity-guide.pdf) | 离线 PDF 实战手册 |
| [`guides/`](guides/) | 12 章完整 Markdown，可供版本控制与二次编辑 |
| [`prompts/README.md`](prompts/README.md) | 18 条可复制指令 |
| [`PLAN-30-DAYS.md`](PLAN-30-DAYS.md) | 完整 30 天每日任务与验收物 |
| [`templates/`](templates/) | 任务书、验收矩阵、安全清单与交付清单 |
| [`SOURCES.md`](SOURCES.md) | 官方来源、核查日期与事实边界 |
| [`tests/`](tests/) | 网站文件、内容、隐私与导航自检 |

## 网站有什么实际功能？

课程按标签筛选、关键词搜索、教程详情展开、18 条指令复制、七天和十二章进度打卡、JSON 导入导出、本地任务书生成器、手机响应式布局、PDF 下载、作者与官网入口。**没有后端、第三方跟踪脚本或用户数据上传功能。** 本地进度可能在浏览器清理缓存后消失。

## 本地打开与测试

```bash
python3 -m pip install -r requirements-dev.txt # 仅重新生成网站/PDF 时需要
python3 tools/build.py
python3 -m unittest discover -s tests -v
python3 -m http.server 8000 --directory docs
# 打开 http://localhost:8000/
```

亦可直接打开 `docs/index.html` 离线阅读；下载 PDF 不需要后端。

## GitHub Pages 部署

1. 使用账号 [@AIPMAndy](https://github.com/AIPMAndy) 创建公开仓库 `antigravity-guide`。
2. 把该项目文件全部上传 `main`，保证 `docs/index.html` 存在。
3. 打开 **Settings → Pages**，Source 选 **Deploy from a branch**，Branch 选 **main**，Folder 选 **/docs**，点击 **Save**。
4. 等 GitHub Pages 报告部署成功，再打开 `https://aipmandy.github.io/antigravity-guide/` 实测 375px 手机页面、搜索、复制与 PDF。

详细说明：[DEPLOY.md](DEPLOY.md)。**仓库未创建时，页面链接只是计划地址，不表示已上线。**

## 安全、事实与服务说明

- 原始产品：Google Antigravity。官网：https://antigravity.google/ 。本课程是独立编辑内容，不是 Google 官方服务或培训。
- 教程中的“简历诊断落地页”与“岗位技能筛选器”均使用虚构数据，未声称有真实客户结果。
- 不推荐购买第三方账号、不教绕过地区/平台规则、不允许在公开仓库上传密码、Tokens、客户敏感信息。
- 个人版免费额度、具体模型与支持地区随产品更新变化，请以官方定价与账号实际界面为准。
- 代码使用 MIT License，Google 与 GitHub 的商标归各自权利人。
- **服务说明（广告）**：AI 酋长 Andy 自愿提供 AI 产品咨询、AI 陪跑与增长相关服务；使用免费教程不需要购买服务。个人微信 **`AIPMAndy`** · [官网](https://metaver.vip/) · [服务](https://metaver.vip/services)。

## 社区反馈

欢迎在 GitHub Issue 提交明确的问题、复现步骤、截图（脱敏后）与更正来源。不要公开账号、API Key、聊天记录中的个人资料。贡献规范见 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

**作者：AI 酋长 Andy** · [官网](https://metaver.vip/) · 微信 `AIPMAndy` · [GitHub](https://github.com/AIPMAndy)
