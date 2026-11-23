# 10｜GitHub、PR 与 Pages 发布

> 交付 · 40–60 分钟 · 交付物：一个公开可访问、可回滚的网站

## 这章解决什么问题

先发布静态成果，再考虑复杂部署链路。GitHub Pages 适合不需要服务器或机密数据的纯静态网站。

## 按顺序动手

### 1. 创建仓库与主分支

在 github.com/new 新建 public 仓库，默认分支 main，README 写清用途、维护者、非官方声明。

### 2. 审查提交

用 git status 和 git diff --stat 核对没有敏感资料、生成垃圾或不必要的大文件。

### 3. 上传 docs 静态网站

把 index.html、样式、脚本和 PDF 放入 docs 目录；使用相对路径，避免项目路径部署失效。

### 4. 开启 GitHub Pages

Settings → Pages → Source: Deploy from a branch → main /docs → Save，等待 GitHub 显示部署结果。

### 5. 线上验收与回滚

实际打开 GitHub Pages 链接，验证手机/电脑、PDF、按钮和资源文件；失败时检查 Pages 状态和构建日志。

## 复制给 Antigravity 的任务指令

```text
请准备 GitHub Pages 发布审查：1 检查 docs/index.html 是否存在；2 所有内部资源使用相对路径；3 没有敏感值、真实个人数据、密钥或需要服务端的功能；4 输出部署步骤、线上烟测清单与回滚提交。只生成部署说明和待我确认的提交计划，不自动公开或发布。
```

## 验收标准
- [ ] GitHub 仓库公开且文件完整
- [ ] Pages 显示真实 URL 与成功状态
- [ ] 线上 URL 已实际访问并完成冒烟测试

## 避坑提醒
- 仓库有文件不代表 Pages 已开启
- 静态网页不能安全存储 API secret
- 不要把预估网址说成已经上线

## 官方资料
- https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

---
*独立开源教程 · AI 酋长 Andy · 非 Google 官方。请以实际产品界面与官方说明为准。*
