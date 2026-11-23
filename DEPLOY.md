# GitHub Pages 最短部署路径

## 1. 创建公开仓库

打开：<https://github.com/new?owner=AIPMAndy&name=antigravity-guide&visibility=public>

Owner 选择 `AIPMAndy`，名称填 `antigravity-guide`，Visibility 选 `Public`。可以先不初始化 README，避免与本地源码冲突。网页表单需要账号持有人点击 `Create repository`。

## 2. 上传完整项目文件

在自己的电脑将本文件夹解压并进入：

```bash
git init
git branch -M main
git add .
git commit -m "feat: publish Antigravity Chinese field guide"
git remote add origin https://github.com/AIPMAndy/antigravity-guide.git
git push -u origin main
```

前提：已经配置 Git 用户身份与 HTTPS/SSH 认证。仓库若通过网页初始化 README，请先克隆仓库再拷入文件并提交，避免强推覆盖旧提交。

## 3. 设置 Pages

打开：<https://github.com/AIPMAndy/antigravity-guide/settings/pages>

- Build and deployment → Source：**Deploy from a branch**
- Branch：`main`
- Folder：`/docs`
- Save

`docs/.nojekyll` 已就绪；这是纯静态站点，不需要构建、密钥、依赖安装或 Github Actions 自动部署配置。

## 4. 验证真实上线状态

预期项目站点：<https://aipmandy.github.io/antigravity-guide/>

请先在 GitHub Pages 设置里看见部署成功消息，再执行：

- 网站首页能打开，导航可到各模块
- `/style.css`、`/app.js` 在网站路径下没有 404（注意带项目目录前缀）
- 12 章展开、筛选、搜索实际能用
- 18 条 Prompt 的复制实际成功
- 导出/导入进度 JSON 能恢复打卡
- PDF 链接返回可打开的文件
- 手机端 375px 不横向滚动
- 公司、官网与微信入口文案准确，隐私提示清楚

## 5. 出错时如何排查

- `404`：仓库可能没有开启 Pages、`docs/index.html` 不存在、路径大小写不一致或发布尚未完成。
- 样式失效：检查资源链接是否是 `./style.css` 这种相对路径；不要写 `/style.css` 指向用户主页根目录。
- PDF 404：核对 `docs/pdf/antigravity-guide.pdf` 是否已提交。
- 设置界面没有 Pages：检查仓库管理员权限及账号计划支持。
- 发布构建报错：看 Actions / Pages deployment 运行日志，不要把失败当成功。

官方文档：<https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site>
