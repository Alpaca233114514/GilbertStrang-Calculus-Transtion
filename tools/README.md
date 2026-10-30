# PDF 排版与导航维护

## 当前忠实性修订稿

2026-10-30 版本直接读取 `translation_draft/` 中的当前分节稿，不读取旧交付快照或旧译注备份。它保留作者脚注，移除来源与审校状态元信息；图片替代文本不重复作为图注，原图注与图片共同分页。填空下划线、引用块中的显示公式和多行习题分别按相应结构处理。

使用已配置的 Node.js、Playwright、KaTeX、Edge 与 Python 依赖执行：

```powershell
node tools/build_reading_pdf.cjs --check-only
node tools/build_reading_pdf.cjs
& 'C:/Users/Logan/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' tools/merge_reading_pdf.py
```

中间文件和待验 PDF 写入 `tmp/pdfs/faithfulness-20261029/build/`。`manifest.json` 记录分节、公式和图片检查结果；`pdf_report.json` 记录页码、571 个分层书签及 108 条目录目标。标题和目录在排版时带有定位标记，合并器用实际页面与坐标转换成内部跳转，不复用旧版页号。合并器先加入全部页面，再创建书签。

全书成功排版后同时导出 `output/markdown/GilbertStrang-Calculus.md`，其中图片路径指向当前分节稿的原图。仅更新合并稿时可运行 `node tools/build_reading_pdf.cjs --export-only`。

正式输出为 `output/pdf/GilbertStrang-Calculus.pdf`。替换正式文件前须检查新 PDF 的实际渲染、目录与书签，并在 `tmp/pdfs/` 保留旧文件备份。当前成品为 834 页；检查范围和限制记录在 `translation_prep/faithfulness_review_20261030.json`。

2026-10-30 补修阅读器自动目录：生成器按分节文件编号将章标题统一为 H1、节标题统一为 H2，并保持内部标题的相对层级；合并 Markdown 使用同一规则。排版时，普通文本节点开头的单层编号 `4.` 改为 `4)`，避免讲座和步骤编号干扰章节识别；章节号、小数与 KaTeX 公式不参与替换，分节源稿保持原样。

本次重新生成后，用已安装 Google 学术阅读器 0.5.2 的同款分析器做离线检查：91 节（0.4 上下两部分合计 92 个节入口）全部在正确的起始页检出，第二章 2.1–2.7 均归在第二章下。自动目录仍会把 0.2–0.5 提升到顶层，并将 11.4、11.5 挂在前面的内部标题下；PDF 内置书签的全部章节归属正确。离线分析结果不等同于阅读器界面点击实测。备份、章节首页渲染及检查结果位于 `tmp/pdfs/navigation-fix-20261030/`。

## 旧版平铺书签修复

`repair_pdf_navigation.py` 用于修复本项目旧合并流程生成的平铺书签 PDF。它使用分节译稿的结构，逐项在实际 PDF 中查找大号粗体标题，重建“章 → 节”书签，并为书面目录的每一行添加内部跳转链接。0.4 节保留上下两部分的子书签。

脚本不重排正文，保留原书页码；目标使用 PDF 页面对象引用和标题坐标。合并时应先加入全部页面，再创建书签，避免目标页尚不存在而写入数字页号。当前 pypdf 的内部 Link 注释也需显式替换为页面对象引用，脚本已包含此处理。

依赖：`pypdf`、`pdfplumber`。在仓库根目录执行：

```powershell
python tools/repair_pdf_navigation.py
```

默认读取并更新 `output/pdf/GilbertStrang-Calculus.pdf`，先在 `tmp/pdfs/navigation/` 保存带时间戳的原文件备份。该工具针对旧版平铺书签输入；已修复的分层 PDF 会被拒绝。需要重做时，用保存的旧版备份作为输入：

```powershell
python tools/repair_pdf_navigation.py --source "tmp/pdfs/navigation/<旧版备份文件名>.pdf" --output "output/pdf/GilbertStrang-Calculus.pdf"
```

脚本在替换输出前核对全部书签目标、目录行的覆盖情况、页面数、页面尺寸及每一页的内容流，确认正文未被改动。定位明细、目录链接矩形与备份路径写入 `tmp/pdfs/navigation/report.json`。每次正文重新排版后，须以新合并的 PDF 重新定位，不能复用旧文件的页号或坐标。

## 补齐正文小标题

已有章、节书签后，运行：

```powershell
python tools/expand_pdf_outline.py --scan-only
python tools/expand_pdf_outline.py
```

依赖现有的 `pypdfium2` 和 `pypdf`。工具读取 PDF 实际渲染的字体、文字矩阵和坐标，识别正文标题并按页面上的阅读顺序排列公式与中文，将内部小标题挂到所属章、节下面。它自动以“译注汇总”的起始页为边界，排除书末同名译注。原有页面内容及目录链接保持不变，输出替换前保存原文件备份，并检查文件未被其他进程同时修改。

本次从正文识别到 565 处标题，新增 449 个内部标题书签，总数为 568。完整定位明细见 `tmp/pdfs/navigation/expanded-outline-report.json`；检查结果见 `tmp/pdfs/navigation/subheading-verification.json`。其中“连续函数”定义直接指向 PDF 第 159 页，作为第 158 页“2.7 连续函数”的子书签。

Google 学术阅读器另有自行计算的目录。仅修复 PDF 内置书签不能证明其自动目录正确。本次还已检查其同款分析器的离线输出；普通列表编号与章节编号冲突的处理保留在 `normalize_pdf_headings.py`。该处理会调整列表编号标点和译注标题样式，不应当作仅改书签的操作重复运行。直接在阅读器界面的点击实测仍应与 PDF 结构检查区分。
