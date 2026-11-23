# Antigravity Guide 交付审核记录

审查日：2026-11-23。项目预期发布到 AIPMAndy/antigravity-guide。

## 已验证

- [x] `docs/index.html` 已构建，12 章、18 条 Prompt、7 天计划都在页面中
- [x] 33 页 A5 PDF 已生成，文本可抽取，封面与课程正文经渲染抽查
- [x] Python `unittest` 6 项通过：文件路径、数量、基础无障碍标记、隐私与来源
- [x] Chromium 页面渲染（HTML/CSS/JS 注入无网络的空白页）：1380px、390px、375px 均无横向溢出和页面脚本异常
- [x] 浏览器交互测试：勾选打卡、进度显示、课程搜索、Prompt 搜索、任务书生成、JSON 导出入口
- [x] 所有资源使用相对路径，无 Google Analytics / 外部 JS / 第三方 CSS 运行依赖
- [x] 清楚标明非 Google 官方、虚构案例与免费/付费边界

## 未验证 / 需要线上确认

- [ ] **仓库创建**：此环境连接只允许读取和修改已有仓库，不支持直接创建新仓库；创建动作需要 GitHub 账号持有人完成
- [ ] **GitHub Pages 设置**：本环境不能代表账号持有人调整 Pages 页面设置
- [ ] **上线后 URL**：未上线前，`https://aipmandy.github.io/antigravity-guide/` 只是预期地址
- [ ] **Antigravity 真实账号操作**：本次依据官方文档编写，并没有以真实 Antigravity 账号全程复现
- [ ] **真实浏览器 HTTPS 复制/本地存储**：浏览器测试采用不联网的 inline 渲染；部署后仍应检查浏览器权限与跨端导入导出
- [ ] **真实客户案例与收入**：没有提供或宣称任何已审计的用户收入效果

## 解决过的问题

1. 初版筛选隐藏卡片的 `hidden` 属性被自定义 CSS 中的 `display:grid` / `display:flex` 覆盖，已添加 `[hidden]{display:none!important}`，并在 Chromium 中验证过滤行为。
2. 首版 PDF 封面溢出至第 2 页，已缩短封面垂直留白并重新生成，封面单页完成。
3. 页面头部开发过程示意状态改为 `WORKFLOW DEMO`，不误导为本机真实 Antigravity 运行截图。

## 源码与持续维护

- 真正的内容源在 `tools/content_source.py`；修改后使用 `python tools/build.py` 更新网页与章节 Markdown，使用 `python tools/build_pdf.py` 同步 PDF。
- 只维护当前可验证的产品事实，随 Google 官方文档变化更新。
- 每次发布前确认部署页面真实可用、PDF 版本与页面版本一致。
