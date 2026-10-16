# UI-First Redesign — 本次你怎么操作

这次的目标是**先看、先调整界面**，不是运行实验。新版 `app.py` 默认进入 **UI Preview**；不会加载 BGE Embedding，也不会进行 Chroma 检索，更不会调用 Gemini 生成回答。你输入问题只会在本地对话区显示，并明确提示未生成 AI 回答；不会制造虚假 Citation。

## 用补丁更新你现在电脑上的项目（推荐）

1. 在运行 Streamlit 的 VS Code 终端按 **Ctrl+C** 停止旧进程。
2. 解压 `RAG_Tutor_UI_First_Patch.zip`。
3. 将补丁中的 `app.py`、`style.css`、`workspace_mode.py` 复制到你当前的 `Multimodal_RAG_Tutor_Enhanced` 文件夹，覆盖同名文件。**不要删除 `.env`、`.venv`、`chroma_db`。**
4. 在原来的项目目录打开终端，执行：

   ```powershell
   .\.venv\Scripts\python.exe -m streamlit run app.py
   ```

5. 打开 `http://localhost:8501`。页面的标签应为 **UI PREVIEW · No model requests**，此时立刻可以查看界面。

**如果以前设置过 `RAG_UI_MODE=live` 环境变量：** 在当前 PowerShell 终端执行 `$env:RAG_UI_MODE = 'preview'` 再启动。

## 之后需要真实问答时

打开左侧 **Workspace mode**，开启 `Enable Live RAG`。这会加载你已有的向量库和 BGE 模型，提出问题后才会尝试真实检索与 Gemini 回答。你原来的 `.env`、数据库、媒体映射都仍然适用。在线生成可能慢，切回预览不会修复网络问题。

## 这一版真正做了什么

- 新的顶部品牌区、三段式工作流、浅色研究工作台视觉规范。
- Conversation 区有空白引导、问题提示、对话消息和真实证据按钮。
- Evidence Workspace 有更大的阅读容器、PDF / Video 功能区及来源核查原则。
- **UI Preview 不提供伪造的检索结果、回答、PDF 页面或 Video Citation。**
- Live RAG 分支继续复用原有 `rag_core.py`、`evidence.py`、`source_viewer.py`。

## 验证边界

本次完成 Python 静态检查与纯 Python 单元测试。当前执行环境未安装 Streamlit / Chroma / LlamaIndex，**没有完成浏览器真实渲染、在线 Gemini 检索或 PDF / 视频跳转的端到端测试**。你本地查看后，可以把新截图发来再进一步微调。
