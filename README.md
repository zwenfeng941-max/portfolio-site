# 郑文凤 · 个人作品集网站

纯静态网站，无构建依赖，双击 `index.html` 即可预览。

## 当前结构

封面（含电话与邮箱）

1. 策划能力页按独立条目展示 8 个项目与策划案例，默认收起，点击单个项目后再展开
   - 苏州阳澄半岛乐园 921 焕新一周年
   - 海合安「自世代」计划
   - 晋城 2026 暑期营销方案
   - 王莽岭暑期营销方案
   - 正佳动漫节活动方案
   - 正佳帽峰湾董事长汇报版
   - 中国主题公园战略营销峰会
   - 钙世英雄，甜伴三十（独立竞赛策划案板块，保留完整 28 页入口）
2. 其余项目：`project-dossiers.html` 只收纳未在策划能力页展开的 5 个项目，避免重复
3. 能力展示：策划、运营、摄影剪辑、商务与嘉宾对接
4. 个人简介 → `about.html`
5. 专业技能 → `skills.html`

案例详情页：

- `work-hahean.html` 海合安自媒体节
- `work-maofengwan.html` 正佳帽峰湾文旅度假区
- `work-jincheng.html` 晋城暑期营销与融媒孵化
- `work-ip.html` 熊晓杰说文旅 IP 运营
- `work-cattery.html` Trendy Cattery 潮猫舍
- `work-summit.html` 中国主题公园战略营销峰会（含商务对接能力、脱敏工作照片、嘉宾手册与主持台本样例）
- `work-calcium.html` 大广赛「钙世英雄，甜伴三十」28 页策划案

## 交互说明

策划能力页使用项目手风琴：默认全部收起，点击单个标题展开，并自动关闭其他项目；桌面端职责卡会随项目滚动，移动端自动改为单栏。其余项目从策划能力页底部或 `project-dossiers.html` 直接进入。

能力浏览顺序统一为：策划能力 → 运营能力 → 摄影剪辑 → 商务与嘉宾对接 → 专业技能。
策划能力页内含“方案呈现 / PPT”模块，用 3 张项目代表页说明汇报逻辑、信息层级和版式呈现；专业技能页另有 PPT 能力拆解。其余项目档案页补充 3 套研究型汇报封面。

## 内容边界

- 策划能力页 6 个项目与档案页 5 个项目不重复。
- 「独立」与「合作」分类依据本人提供的项目清单。
- 「个人 IP 账号孵化建议」与「融媒账号孵化落实建议案」为同一合作项目，已删除独立条目，仅保留合作条目。
- 合作项目只写本人参与的工作包，不把团队成果写成个人独立成果。
- 已删除项目档案中的「熊晓杰说文旅自媒体账号 12 月汇报」，该内容只在运营能力页展示。
- 运营页已移除原始账号后台截图、平台明细看板和内部汇报页，改为描述实际工作过程；IP、猫舍及项目层面的结果数据仍保留。
- 页面已去除预算、联络方式和未公开组织细节；方案截图统一标注为脱敏展示。

## 常改内容

- 电话与邮箱：搜索 `17281068521` 与 `zhengzhangfl@163.com`，首页封面、联系区和各页脚都有。
- 生活照轮播：`about.html` 中的 `.life-carousel`，已使用 `assets/img/life-01.jpg` 至 `life-05.jpg` 五张图片。
- 方案呈现：`capability-planning.html#presentation` 展示 3 张不重复的项目 PPT 代表页，图片位于 `assets/img/presentation/`；`skills.html#presentation` 只列 PPT 能力拆解，不重复项目图。
- 研究型汇报：`project-dossiers.html#research-presentations` 展示 3 套研究型材料封面，不提供原始 PPTX 或演讲备注下载。
- 账号链接：`capability-operations.html` 的「账号矩阵」表格。目前列出账号名、平台、角色与结果，拿到主页链接后可把账号名改成 `<a href="..." target="_blank">账号名 ↗</a>`。
- 账号运营汇报：`capability-operations.html#account-report`，展示熊晓杰说文旅在小红书、B站、视频号与小宇宙的周/月数据、内容表现和下一轮优化方向。
- 视频作品：`capability-visual.html`，学院奖、大广赛广告短片与物理竞赛视频文件在 `assets/video/`，封面在 `assets/img/video-*`。
- 音频作品：`capability-visual.html` 的「音频作品」板块，3 支大广赛音频在 `assets/audio/`。
- 计算机设计大赛：2023、2024 两个独立板块；2023 原始视频找到后，将文件补入 `assets/video/` 并替换 2023 板块中的「原片待补充」。
- 大广赛策划案：`work-calcium.html`，28 张页面图位于 `assets/img/calcium/`。
- 简历文件：`assets/郑文凤-简历.pdf`。
- 峰会对接样例：`assets/docs/summit-liaison-sample.pdf`，由 `scripts/generate_summit_sample.py` 生成；现场照片在 `assets/img/summit-liaison/`，所有人物与资料信息均已二次遮挡。

## 部署

1. Vercel / Cloudflare Pages：上传整个 `portfolio-site` 文件夹，免费自动 HTTPS。
2. 腾讯云 COS / 阿里云 OSS + CDN：国内访问更稳，绑定域名需备案。
3. GitHub Pages：免费，国内访问速度一般。

上线前检查：

- 手机端逐页打开，确认没有横向滚动
- 物理竞赛视频已压缩为约 113MB 的 360p 网页版本；若正式上线且访问量较大，建议再压码率或改用 B 站 / 视频号外链
- 账号链接、个人照片、微信二维码补齐
- 客户项目名称与数据确认可公开
