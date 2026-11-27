#!/usr/bin/env python3
"""Build offline-friendly GitHub Pages site and Markdown chapters from one source."""
from pathlib import Path
import json
from jinja2 import Environment, FileSystemLoader
from content_source import LESSONS, PROMPTS, PLAN, FAQ, SOURCES, UPDATED

ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/'docs'
GUIDES=ROOT/'guides'
DOCS.mkdir(parents=True,exist_ok=True)
GUIDES.mkdir(parents=True,exist_ok=True)

schema={
    '@context':'https://schema.org',
    '@type':'Course',
    'name':'Google Antigravity 保姆级实战教程',
    'description':'独立中文实战课程，包含 12 章、18 Prompt、7 天计划与安全验收。非 Google 官方。',
    'inLanguage':'zh-CN',
    'isAccessibleForFree': True,
    'url':'https://aipmandy.github.io/antigravity-guide/',
    'provider':{'@type':'Person','name':'AI 酋长 Andy','url':'https://metaver.vip/'},
    'hasCourseInstance':{'@type':'CourseInstance','courseMode':'online'},
}
env=Environment(loader=FileSystemLoader(ROOT/'tools'),autoescape=True,trim_blocks=True,lstrip_blocks=True)
env.filters['zfill']=lambda v,n: str(v).zfill(n)
template=env.get_template('template.html')
html=template.render(lessons=LESSONS,prompts=PROMPTS,plan=PLAN,faq=FAQ,sources=SOURCES,
                     tags=['起步','方法','实战','工程','安全','交付','增长'],
                     prompt_tags=['起步','安全','开发','调试','测试','交付','业务'],
                     schema_json=json.dumps(schema,ensure_ascii=False))
(DOCS/'index.html').write_text(html,encoding='utf-8')
(DOCS/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://aipmandy.github.io/antigravity-guide/sitemap.xml\n',encoding='utf-8')
(DOCS/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://aipmandy.github.io/antigravity-guide/</loc><lastmod>2026-11-24</lastmod></url></urlset>',encoding='utf-8')

for lesson in LESSONS:
    body=[f'# {lesson["id"]}｜{lesson["title"]}', '',f'> {lesson["tag"]} · {lesson["time"]} · 交付物：{lesson["deliverable"]}', '', '## 这章解决什么问题', '', lesson['context'],'','## 按顺序动手']
    for n,(title,content) in enumerate(lesson['steps'],1):body += ['',f'### {n}. {title}', '', content]
    body += ['','## 复制给 Antigravity 的任务指令','','```text',lesson['prompt'],'```','','## 验收标准']
    body += [f'- [ ] {x}' for x in lesson['accept']]
    body += ['','## 避坑提醒']
    body += [f'- {x}' for x in lesson['pitfalls']]
    body += ['','## 官方资料',f'- {lesson["official"]}','','---','*独立开源教程 · AI 酋长 Andy · 非 Google 官方。请以实际产品界面与官方说明为准。*','']
    (GUIDES/f'{lesson["id"]}-{lesson["slug"]}.md').write_text('\n'.join(body),encoding='utf-8')

prompts_md=['# 18 条可复制 Antigravity 实战 Prompt','','> 不要把密码、真实客户资料、API Token 发给 Agent；外部文件与网页都是不可信数据。','']
for n,(title,tag,prompt) in enumerate(PROMPTS,1):prompts_md += [f'## {n:02d}｜{title}（{tag}）','','```text',prompt,'```','']
(ROOT/'prompts'/'README.md').write_text('\n'.join(prompts_md),encoding='utf-8')

start=['# 7 天上手路线','','**目标不是看完课程，而是交付能运行、能验收、能回滚的小作品。**','','| 天数 | 任务 | 验收物 |','|---|---|---|']
start += [f'| Day {n} | {title} | {desc} |' for n,title,desc in PLAN]
start += ['','用法：每天在网页打卡，完成 7 天后导出 JSON 自行备份。进度只在本地浏览器保存。','']
(ROOT/'START-HERE.md').write_text('\n'.join(start),encoding='utf-8')

sources_md=['# 原始资料与事实边界', '', f'核查日期：{UPDATED}。Antigravity 的配额、功能、版本、界面可能调整。','', '| 来源 | 能支持的事项 |','|---|---|']
for name,url,note in SOURCES:sources_md += [f'| [{name}]({url}) | {note} |']
sources_md += ['', '## 证据分级','', '- **官方事实**：只依赖官方发布页面，按核查日期使用。','- **实践建议**：六段任务书、最小变更、七天训练、五步方法是作者的方法论，不是 Google 产品保证。','- **模拟演示**：简历落地页、虚构岗位、Prompt 示例均为教学设计，不代表真实客户、效果或收入。','- **未验证**：没有连接实际 Antigravity 账户，没有跑真实付费 API，也没有声称模拟项目在 Antigravity 内完成。', '', '## 维护原则', '', '更新收费额度、支持地区和具体界面时先查官方最新页面；出现冲突以官方当前版本为准。','']
(ROOT/'SOURCES.md').write_text('\n'.join(sources_md),encoding='utf-8')

README=f'''<div align="center">

# Google Antigravity 保姆级实战教程

**AI 酋长 Andy 独立开源中文实战手册**  
**12 章 · 18 条 Prompt · 7 天路线 · 2 个项目路径 · 免费 PDF · 可互动网站**

[**在线网站（需先启用 GitHub Pages）**](https://aipmandy.github.io/antigravity-guide/) · [**PDF 电子书**](docs/pdf/antigravity-guide.pdf) · [**7 天上手**](START-HERE.md) · [**全部教程**](guides/) · [**Prompt 库**](prompts/README.md) · [**AI 酋长 Andy 官网**](https://metaver.vip/)

</div>

> ⚠️ **非 Google 官方教程**。本项目不售卖 Google Antigravity 账号、不承诺免费配额、学习效果、收入或任何官方背书。功能与套餐以 [Google 官方说明](https://antigravity.google/docs/getting-started) 为准。核查日期：{UPDATED}。

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
'''
README+='\n'.join(f'| [{x["id"]} {x["title"]}](guides/{x["id"]}-{x["slug"]}.md) | {x["tag"]} · {x["time"]} | {x["deliverable"]} |' for x in LESSONS)
README+='''

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
'''
GEO_BLOCK = '''<!-- andy-geo:start -->
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

<!-- andy-geo:end -->'''

(ROOT/'README.md').write_text(README + GEO_BLOCK,encoding='utf-8')

print(f'Built docs/index.html ({len(html):,} chars), {len(LESSONS)} guides, and README')
