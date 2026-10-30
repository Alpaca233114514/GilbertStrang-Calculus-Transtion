# Gilbert Strang《微积分》中文翻译

Gilbert Strang 著 *Calculus*（第三版）的简体中文译稿，基于 MIT OpenCourseWare 提供的英文 PDF，面向微积分学习与自学。

## 开始阅读

- **[中文阅读版 PDF](output/pdf/GilbertStrang-Calculus.pdf)**：834 页，含分层章节书签及可点击目录。
- [分节 Markdown 译稿](translation_draft/)：便于逐节阅读、对照与修订。
- [合并 Markdown 译稿](output/markdown/GilbertStrang-Calculus.md)。
- [英文原书 PDF](mitres_18_001_f17_full_book.pdf) · [MIT OCW 教材页面](https://ocw.mit.edu/courses/res-18-001-calculus-fall-2023/pages/open-textbook/)。

建议下载 PDF 后使用支持书签的阅读器打开。

2026-10-30 完成本轮全书忠实性修订，并直接用当前分节稿重新排版。PDF 覆盖 17 章、91 节，共 571 个分层书签；纸面目录的 108 个条目均可跳转。例如“2.7 连续函数”现指向 PDF 第 162 页。目录中的数字仍为英文原书印刷页码；点击后跳转到中文 PDF 的对应位置。已打开旧文件的阅读器需要重新载入。

导航修复工具及复用方法见 [PDF 导航维护](tools/README.md)。

## 内容与版本

内容涵盖导数、积分及其应用、极坐标与复数、无穷级数、向量与矩阵、曲线运动、偏导数、多重积分和向量微积分，并包含序言、目录、公式表与索引。

当前译稿覆盖本仓库英文源文件的全部 706 页。源文件第 16 章仅含导言，未包含正文提及的第 16.1–16.3 节；译稿遵循该文件的实际内容。

本译稿由 AI 辅助翻译与排版，保留原书习题、公式和插图。本轮逐节对照覆盖全部 100 份译稿，撤去原文没有的解释、条件和译注，不代作者修正原书疑点；疑点只保存在审查记录中。审查范围、证据及原页文字遮挡等局限见 [全书忠实性审查汇总](translation_prep/faithfulness_review_20261030.md)。欢迎提交具体勘误。中文 PDF 的页码与英文原书不同。

## 文件组织

| 路径 | 内容 |
| --- | --- |
| `output/pdf/` | 中文阅读版 PDF |
| `output/markdown/` | 当前合并 Markdown 译稿 |
| `translation_draft/` | 分节译稿、插图及复审记录 |
| `translation_prep/` | 原文提取、术语表、问题记录和处理工具 |
| `deliveries/` | 汇总译稿与交付快照 |
| `archives/` | 阶段归档 |
| `tmp/` | 排版中间文件、依赖和检查图片 |
| `mitres_18_001_f17_full_book.pdf` | 本次翻译使用的英文原书 |

## 参与纠错

可以通过 Issue 或 Pull Request 提交修订。请附上章节、原书页码或译稿文件名，以及问题原文和建议改法；涉及公式时，最好同时给出英文原书中的对应公式。贡献的译文修订遵循下述相同许可。

## 来源与许可证

原著：**Gilbert Strang, Calculus, Third Edition**，Wellesley-Cambridge Press；数字资源由 [MIT OpenCourseWare](https://ocw.mit.edu/courses/res-18-001-calculus-fall-2023/) 提供。原作及插图的权利归其各自权利人所有。

依据 [MIT OCW 使用条款](https://ocw.mit.edu/pages/privacy-and-terms-of-use/)，除另有标注的材料外，本仓库教材内容及中文翻译改编采用 **[Creative Commons 署名—非商业性使用—相同方式共享 4.0 国际许可（CC BY-NC-SA 4.0）](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans)**。

你可以在遵守许可的情况下复制、分享和改编这些内容：保留作者、来源与许可信息，注明所作改动，不用于商业目的，并以相同许可分享改编作品。本项目所作改动包括中文翻译、重新排版和公式转写。

单独标注权利或许可的第三方图片、商标及软件依赖遵循各自条款。本项目是非官方翻译，不代表作者、出版社或 MIT 的认可。详细适用范围见 [LICENSE.md](LICENSE.md)。

推荐署名方式：

> Gilbert Strang《Calculus》第三版，原作由 MIT OpenCourseWare 提供；中文翻译与排版来自 [GilbertStrang-Calculus-Transtion](https://github.com/Alpaca233114514/GilbertStrang-Calculus-Transtion)。除另有标注外，依据 CC BY-NC-SA 4.0 分享。此版本包含中文翻译、重新排版和公式转写。
