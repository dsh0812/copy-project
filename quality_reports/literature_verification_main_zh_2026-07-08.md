# 参考文献核查日志：main_zh

**日期：** 2026-07-08
**核查工具：** review-paper skill
**核查文件：** `paper/references.bib`
**对应论文：** `paper/main_zh.tex`

## 核查范围说明

本次运行在受限环境中完成，未进行外部 CNKI/Crossref 网络查询。因此，本日志只基于本地 LaTeX 源文件、`references.bib`、`main_zh.bbl` 和编译日志进行一致性核查。需要正式投稿前，应再执行外部元数据核验。

## 核查摘要

- `paper/references.bib` 中共有 7 个 BibTeX 条目。
- `paper/main_zh.tex` 正文中共出现 12 个引用键。
- 已在 BibTeX 中找到：7 个。
- 正文引用但 BibTeX 缺失：5 个。
- 当前编译日志显示全部引用一度为 undefined，且最终因缺失表格文件中断。修复表格路径并重新运行 BibTeX/LaTeX 后，应再次检查 citation 状态。

## 正文引用键与本地 BibTeX 匹配

| 引用键 | 本地 BibTeX 状态 | 备注 |
|--------|------------------|------|
| BloomSadunVanReenen2012 | 已找到 | `paper/references.bib` 第 1-10 行 |
| AcemogluRestrepo2019 | 已找到 | `paper/references.bib` 第 56-65 行 |
| AgrawalGansGoldfarb2019 | 已找到 | `paper/references.bib` 第 67-76 行 |
| BertrandDufloMullainathan2004 | 已找到 | `paper/references.bib` 第 12-21 行 |
| CallawaySantAnna2021 | 已找到 | `paper/references.bib` 第 23-32 行 |
| SunAbraham2021 | 已找到 | `paper/references.bib` 第 34-43 行 |
| GoodmanBacon2021 | 已找到 | `paper/references.bib` 第 45-54 行 |
| BrynjolfssonHitt2000 | 缺失 | 正文第 43 行引用 |
| AutorDorn2013 | 缺失 | 正文第 43 行引用 |
| Bessen2019 | 缺失 | 正文第 43 行引用 |
| Rosenberg1982 | 缺失 | 正文第 43 行引用 |
| Jovanovic1982 | 缺失 | 正文第 43 行引用 |

## 需实质性修正

### BrynjolfssonHitt2000

- **当前问题：** 正文引用但 `references.bib` 无条目。
- **引用上下文：** 数字化转型和生产率的实证研究。
- **建议：** 确认具体文献版本后补充 BibTeX。可能对应 Brynjolfsson and Hitt (2000), "Beyond Computation: Information Technology, Organizational Transformation and Business Performance"。

### AutorDorn2013

- **当前问题：** 正文引用但 `references.bib` 无条目。
- **引用上下文：** 数字化转型和生产率的实证研究。
- **建议：** 确认是否确实需要该文支撑"数字化转型和生产率"论点；该文更常用于劳动市场极化和任务结构讨论。

### Bessen2019

- **当前问题：** 正文引用但 `references.bib` 无条目。
- **引用上下文：** 数字化转型和生产率的实证研究。
- **建议：** 确认正式发表版或工作论文版，避免版本混用。

### Rosenberg1982

- **当前问题：** 正文引用但 `references.bib` 无条目。
- **引用上下文：** 企业技术采用决策理论模型。
- **建议：** 确认是否引用 Rosenberg (1982) 的专著 *Inside the Black Box: Technology and Economics*，并补充书籍型 BibTeX。

### Jovanovic1982

- **当前问题：** 正文引用但 `references.bib` 无条目。
- **引用上下文：** 企业技术采用决策理论模型。
- **建议：** 确认是否引用 Jovanovic (1982), "Selection and the Evolution of Industry"，并补充期刊型 BibTeX。

## 编译日志中的引用问题

`paper/main_zh.log` 显示以下引用警告：

- 第 596-617 行：7 个已存在于 `references.bib` 的引用键被报告为 undefined，可能因为编译流程未完成或 BibTeX 未重新运行。
- 第 620-632 行：5 个缺失引用键被报告为 undefined。
- 第 644 行：编译因 `output/stata_regression_table.tex` 文件不存在而中断。

## 建议的修复顺序

1. 修复 `paper/main_zh.tex` 第 70 行的表格路径，确保 LaTeX 能继续编译到参考文献阶段。
2. 补齐 5 个缺失 BibTeX 条目，或删除正文中的未落实引用。
3. 运行完整编译链：LaTeX -> BibTeX -> LaTeX -> LaTeX。
4. 再次检查 `main_zh.log`，确认没有 undefined citations 和 undefined references。
5. 对 12 条最终参考文献执行外部 CNKI/Crossref 核验。
