# UI 优先改造（2026-10-16）

现在运行 `app.py` **默认进入 UI Preview 模式**：不加载模型、不调 Gemini、不创建示例检索结果。若要恢复真实 RAG，请在侧边栏启用 `Enable Live RAG`。优先阅读 [`UI_PREVIEW_使用说明.md`](UI_PREVIEW_使用说明.md)。

# 从这里开始（Windows）

你拿到的是一个**已经修改了真实 Python 源码的版本**，不是静态 Demo。

## 你需要做的四件事

**1. 解压 Local 版。** 这个版本已保留原项目的 `chroma_db/`；千万不要把 Local 压缩包直接上传 GitHub。

**2. 安装依赖（推荐 Python 3.11）：**

在解压目录打开 PowerShell：

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

首次运行会下载 BGE Embedding 模型。确保网络可以访问模型仓库；如需要代理，可在本机自行设置环境变量，项目不会强制改写代理。

**3. 配置全新 Gemini API Key（旧 Key 已在原源码暴露，必须轮换）：**

```powershell
Copy-Item .env.example .env
```

用编辑器打开 `.env`，将 `GOOGLE_API_KEY` 换成**你自己新生成的密钥**。不要把密钥发给我，也不要提交 `.env`。如果暂时没有 Key，可以运行真实检索，但不会生成 AI 回答。

**4. 运行：**

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

### 激活 PDF 与视频跳转（必须匹配原索引）

如果你确认最初建库确实使用了 `Agents.pdf` 和 `Agents.mp4`，那么：

1. 把原始 `Agents.pdf` 放在 `assets/Agents.pdf`。
2. 把原始 `Agents.mp4` 放在 `assets/Agents.mp4`。
3. 运行 `Copy-Item sources.example.json sources.json` 并确认其中 PDF/视频别名映射与原素材确实一致。
4. 刷新网页，提出问题，点击回答下方的 **Textbook p.N / Video mm:ss** 来源按钮。

如果只有其他版本的教材或录屏，**不要直接重命名假装匹配**。需要检查实际素材与索引一致性，必要时重新建立带 `source_id` 的索引。

## 这次真正改了什么

- `app.py`：不再是单栏聊天 + 展开框，改为 Conversation / Evidence Workspace 双栏布局；有完整的检索/生成错误处理、来源选择和会话级证据保存。
- `evidence.py`：**真实检索结果的 provenance 适配层**，验证页码、时间戳、来源 ID 和文件是否存在。不解析 AI 自由文本中的虚构导航位置。
- `rag_core.py`：仍使用原来的 BGE + Chroma/LlamaIndex + Gemini 2.5 Flash。
- `build_index.py`：禁止误删原向量库，建库默认输出新目录。
- `process_pdf_*` / `Process_video.py`：去除硬编码个人路径和密钥，保留文本、图片描述和视频关键帧的处理流程。
- `tests/`：13 项测试，已通过；详见 `docs/FEATURE_STATUS.md`。

## 尚未完成端到端验证

当前生成环境无法安装 Streamlit、Chroma 和 LlamaIndex，也缺少原始教材 PDF 和视频 MP4，因此**没有完成网页真实启动、在线 Gemini 调用、播放器 seek、PDF 页面跳转的现场验证**。这不是测试成功的声明。拿到媒体文件后，按上述步骤逐项验证。

GitHub 请使用单独提供的 **GitHub_Ready** ZIP，并优先阅读 `docs/SECURITY.md`。
