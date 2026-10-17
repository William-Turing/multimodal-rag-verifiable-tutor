# Zenodo 已正式发表：GitHub DOI 回链说明

## 已完成的学术存档

- 修订版论文：**Designing Temporally Grounded Multimodal Learning Interfaces for Verifiable Interaction**。
- 作者：Rongyu Wang。
- 发布机构/类型：Zenodo / Publication–Preprint。
- 发布时间：2026-10-16。
- **版本 DOI：** https://doi.org/10.5281/zenodo.23418230
- **所有版本概念 DOI：** https://doi.org/10.5281/zenodo.23418229
- 程序代码：https://github.com/William-Turing/multimodal-rag-verifiable-tutor
- Workshop 原始节目：https://extendedhorizon.com/aied2026ws-ai-hci-ls/program/

**重要区别：** 此 DOI 是 Zenodo 独立修订版预印本的稳定标识，不代表新获得 Springer LNCS 或 AIED 主会的正式论文录用。此前版本列入 Workshop Spotlight II；这次 October 2026 修订版不应标为该 Workshop 重新审稿录用。

## 如何更新 GitHub

1. 下载本补丁包，解压后进入 `GitHub_Overlay`。
2. 将其中**所有内容**复制到之前 `git init` 的本地代码仓库根目录（包含 `README.md`、`app.py` 的那个文件夹）。允许合并 `paper/`、`docs/`，并覆盖同名 README / CITATION.cff / paper 引用文件。**不要**把 `GitHub_Overlay` 这个外层目录整个作为子目录上传。
3. `paper/` 内的 PDF 与 Zenodo 上实际发布的 PDF 字节一致（MD5 `a3d365b0430afc300e88dcb990032588`）。LaTeX 源保留了上传时内容；**不要只为了印上 DOI 改写 PDF 并用其覆盖此次 Zenodo 发布的文件**。
4. 运行：

```powershell
git status --short
git add README.md CITATION.cff paper docs/PREPRINT_PUBLICATION_GUIDE_中文.md
git commit -m "Link published Zenodo preprint DOI"
git push origin main
```

如需要此前有效的本地代理：

```powershell
git -c http.proxy=http://127.0.0.1:7890 push origin main
```

5. 检查 GitHub README 的论文 DOI 是否打开 Zenodo 页面，仓库右上角是否出现 `Cite this repository`（依 GitHub UI）。

## 学术引用建议

Wang, R. (2026). *Designing Temporally Grounded Multimodal Learning Interfaces for Verifiable Interaction* (October 2026 revision). Zenodo. https://doi.org/10.5281/zenodo.23418230

CV 中可分别列出 *AIED 2026 Workshop Spotlight Presentations II* 公开记录与 *Revised preprint (Zenodo)*，不要将两者合并为一个未经证实的 Springer Proceedings 引用。

## 其他说明

- GitHub `CITATION.cff` 的软件记录标题与 `preferred-citation` 的论文 DOI 不同，这是有意区分“代码仓库”和“研究预印本”。
- 论文的 CC BY 4.0 不会自动成为代码的开源软件许可证；代码仍应按仓库自己的 LICENSE 文件（如有）判断。
- 此 DOI 目前已经由 Zenodo 公开发布。日后有新的实质性论文修改，应使用 Zenodo 的 `New version` 功能，而非默默替换本版文件。
