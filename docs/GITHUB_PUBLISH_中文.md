# 把这个项目安全发布到 GitHub（Windows）

本包是准备公开的 **代码版**，不是附带私有教材、视频或 Chroma 索引的本地完整版。发布前请在仓库中保持这种区分。

## 最简方案：GitHub 网页上传

1. 将 GitHub 发布版 ZIP **解压**到一个新的、独立的文件夹。不要从当前含 `.env`、`.venv`、`chroma_db` 的本地开发文件夹上传。
2. 登录 [GitHub 新建仓库](https://github.com/new)。建议仓库名称 `multimodal-rag-verifiable-tutor`；描述：`Evidence-first multimodal RAG tutor research prototype with PDF and temporally grounded video source inspection.`
3. 选择 `Public`（确认准备好公开后），**不要勾选自动创建 README、.gitignore、License**，因为发布包中已经带有前两者，许可证尚未选定。
4. 创建仓库，在仓库页面选择 **Add file → Upload files**。
5. 将解压出来的 `Multimodal_RAG_Tutor_Enhanced` 文件夹**内部的文件和子文件夹**拖入上传区域。不要把 ZIP 当作一个文件上传。检查 `.gitignore`、`.env.example`、`README.md` 与 `screenshots/ui-preview.jpg` 都在待上传文件清单里；不要出现 `.env` 和 `sources.json`。
6. 填写提交信息 `Initial public research prototype` 并完成提交。
7. 打开仓库首页，检查 README 正常渲染出 **UI Preview** 截图，检查 `docs/FEATURE_STATUS.md`、`docs/THIRD_PARTY_MATERIALS.md` 是否存在。

## 另一种方式：Git 命令行

在**干净的解压后项目目录**内、确保没有个人数据的前提下运行：

```powershell
git init
git branch -M main
git add .
git status --short
git diff --cached --name-only
```

确认清单没有 `.env`、`sources.json`、`Agents.pdf`、`Agents.mp4`、`chroma_db/` 或其他版权受限的导出内容，然后运行：

```powershell
git commit -m "Initial public research prototype"
git remote add origin https://github.com/YOUR_USERNAME/multimodal-rag-verifiable-tutor.git
git push -u origin main
```

将 `YOUR_USERNAME` 替换成你的 GitHub 用户名；以上命令**不会**在 GitHub 远程自动创建仓库，需先创建空仓库并配置 Git 身份/认证。

## 公开前安全清单

- `.env`、旧 Gemini Key、新 Key、私人路径、完整终端报错中的可能敏感信息都不得公开。
- 原始 PDF、MP4、PDF 片段、视频帧、由课程资料衍生的文本、Chroma 记录均不包含在此发布包。
- 截图来自本地 UI Preview，清楚标注它不是完整在线 RAG 功能演示。
- GitHub 仓库**没有**可公开再分发的原始课程数据，因此不承诺下载后即能运行完整的多模态证据导航。
- 选择开源许可证（如 MIT）之前先确认代码版权归属；没有许可证不妨碍把代码放在公开仓库，但默认不自动授予别人自由复用许可。
- 不要把整个本地开发目录拖到 GitHub；`.gitignore` 不能保护直接上传的 ZIP 文件或已被提交的敏感文件。

## 第一次对外展示的真实说法

> An evidence-first multimodal RAG research prototype featuring a Streamlit split-pane learning interface, dense vector retrieval integration, and metadata-driven navigation to PDF pages and lecture timestamps. The public repository includes source code and an offline UI preview; the original third-party course materials and vector index are intentionally excluded. End-to-end source navigation remains subject to local media verification.
