# 每日中文简报：免费云端部署包

当前状态：程序和定时配置已准备，尚未部署到 GitHub，未进行真实模型生成和微信推送。

无需安装本地模型。GitHub Actions 在云端每天北京时间 09:00 触发，采集最近48小时的免费RSS摘要，调用 Groq，分别推送科技简报和5个小团队创业商机。GitHub 调度可能延迟，不保证整点送达。

## 上线步骤

1. 登录 https://github.com/login 。创建一个私有仓库，例如 daily-chinese-briefs。
2. 上传本目录内容到仓库根目录，保留 `.github/workflows/daily.yml` 的目录结构。不要上传旧的本地方案目录或任何密钥文件。
3. 登录 https://console.groq.com ，确认账号为 **Free**，不要升级 Developer、绑定付费结算或购买额度。在 API Keys 页面自行生成密钥。
4. 在 GitHub 仓库 Settings → Secrets and variables → Actions → New repository secret 中自行保存以下两个密钥，勿贴在对话中或代码里：
   - `GROQ_API_KEY`：Groq 的 API Key。
   - `SERVERCHAN_SENDKEY`：Server酱 SCT 开头的 SendKey。
5. 在 Actions 中选择“每日中文简报”→ Run workflow，进行第一次真实测试。成功会显示两个“Server酱已接受”，微信应收到两份简报。
6. 若模型不可用或触发免费额度限制，任务报错，不会自动改用付费提供方。部署前以账号后台实际免费模型与限额为准。

## 免费边界

- GitHub Free 私有仓库每月含2,000运行分钟，与账号其他任务共享。单次任务上限12分钟，每日一次，按31天上限372分钟，额外手动运行另计。保持超额付费禁用；若账号有其他付费配置，需检查预算设置。
- Groq Free 有模型和调用速率限制。默认 `openai/gpt-oss-120b`，需实际测试账号是否可用。程序仅调用固定 Groq 端点，不调用付费搜索。
- Server酱 Turbo 免费版每天5条，两份简报占2条；其他推送与测试也会占用额度。免费版内容展示以通道实际限制为准。
- 免费政策可能变化，无法承诺永久免费或永久可用。

## 内容和可靠性

- 仅使用带有效日期的近48小时RSS条目，按链接去重；允许时间窗口交叠，新闻可能跨日重复。
- 依据RSS标题与摘要生成，不声称阅读全文。源不可用会在运行日志标记。当前环境实测：IT之家、少数派、TechCrunch可用；36氪解析失败、虎嗅超时。
- 创业简报至少3个非科技方向由生成指令约束；每条校验商业模式、收益方式、运作流程、启动、成本、获客、风险、验证字段。模型判断仍需人工评估。
- 没有可靠需求信号的创业点子明确标为“待验证的经营假设，非今日新闻”。所有成本收益只是估算。
- 校验引用编号，链接由程序从原始来源附加，拒绝模型生成链接。不能自动保证每一句事实都被原文支持。
- 同日发送记录保存到 GitHub 缓存，重复运行默认跳过已经尝试发送的简报。网络超时可能已经送达，因此不自动重发。缓存若丢失或保存失败仍可能重复，不能承诺严格仅一次。
- 每份简报生成成功后保存到 Actions 的运行附件，保留7天；日志不打印密钥或完整推送URL。
- 停止自动推送：Actions → 每日中文简报 → Disable workflow。

## 已完成验证

- 实际RSS抓取：87条近期内容，33条匹配科技主题（2026-09-18本机网络环境）。
- 5项测试通过：旧/未来/无日期信息过滤、无效链接过滤、虚构引用拦截、推送超时不重试且不泄露URL、API失败不误报成功。
- 尚待验证：真实模型输出质量、GitHub执行、两份微信消息实际到达。

官方资料：
- https://docs.github.com/en/billing/reference/product-usage-included
- https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows
- https://console.groq.com/docs/billing-faqs
- https://console.groq.com/docs/models
- https://sct.ftqq.com/docs/getting-started/faq/
