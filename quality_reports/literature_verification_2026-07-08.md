# 参考文献核查日志

**日期：** 2026-07-08
**核查工具：** review-paper skill（CNKI + Crossref 双通道）
**核查文件：** paper/references.bib
**对应论文：** paper/main_zh.tex

---

## 核查摘要

- 参考文献文件中共 7 条记录
- 正文中引用 12 篇文献
- ✅ 核实无误：7 条
- ⚠️ 需实质性修正：0 条
- 🔴 引用但缺失条目：5 条
- ℹ️ 仅需引用键清理：0 条
- 🔍 需人工核实：0 条

---

## 逐条核查

### ✅ BloomSadunVanReenen2012

- **当前条目：** Bloom, Nicholas and Sadun, Raffaella and Van Reenen, John (2012). "Americans Do IT Better: US Multinationals and the Productivity Miracle." *American Economic Review*, 102(1), 167–201. DOI: 10.1257/aer.102.1.167
- **Crossref 官方元数据：** 标题、作者、期刊名、卷期页码、DOI 均一致。
- **状态：** ✅ 核实无误

### ✅ BertrandDufloMullainathan2004

- **当前条目：** Bertrand, Marianne and Duflo, Esther and Mullainathan, Sendhil (2004). "How Much Should We Trust Differences-in-Differences Estimates?" *The Quarterly Journal of Economics*, 119(1), 249–275. DOI: 10.1162/003355304772839588
- **Crossref 官方元数据：** 标题、作者、期刊名、卷期页码、DOI 均一致。注意：该文先以 NBER Working Paper (w8841, 2002) 形式流传，后发表于 QJE 2004。当前引用的是正式发表版，正确。
- **状态：** ✅ 核实无误

### ✅ CallawaySantAnna2021

- **当前条目：** Callaway, Brantly and Sant'Anna, Pedro H. C. (2021). "Difference-in-Differences with Multiple Time Periods." *Journal of Econometrics*, 225(2), 200–230. DOI: 10.1016/j.jeconom.2020.12.001
- **Crossref 官方元数据：** 标题、作者、期刊名、卷期页码、DOI 均一致。
- **状态：** ✅ 核实无误

### ✅ SunAbraham2021

- **当前条目：** Sun, Liyang and Abraham, Sarah (2021). "Estimating Dynamic Treatment Effects in Event Studies with Heterogeneous Treatment Effects." *Journal of Econometrics*, 225(2), 175–199. DOI: 10.1016/j.jeconom.2020.09.006
- **Crossref 官方元数据：** 正式发表标题为 sentence case: "Estimating dynamic treatment effects in event studies with heterogeneous treatment effects"。当前条目使用 Title Case，为 BibTeX 常规做法，不影响引用准确性。作者、期刊名、卷期页码、DOI 均一致。
- **状态：** ✅ 核实无误

### ✅ GoodmanBacon2021

- **当前条目：** Goodman-Bacon, Andrew (2021). "Difference-in-Differences with Variation in Treatment Timing." *Journal of Econometrics*, 225(2), 254–277. DOI: 10.1016/j.jeconom.2021.03.014
- **Crossref 官方元数据：** 正式发表标题为 sentence case: "Difference-in-differences with variation in treatment timing"。Title Case 用法不影响引用准确性。作者、期刊名、卷期页码、DOI 均一致。
- **状态：** ✅ 核实无误

### ✅ AcemogluRestrepo2019

- **当前条目：** Acemoglu, Daron and Restrepo, Pascual (2019). "Automation and New Tasks: How Technology Displaces and Reinstates Labor." *Journal of Economic Perspectives*, 33(2), 3–30. DOI: 10.1257/jep.33.2.3
- **Crossref 官方元数据：** 标题、作者、期刊名、卷期页码、DOI 均一致。注意：该文同时存在 NBER Working Paper (w25684, 2019.3) 和 SSRN 预印本 (3390283)。当前引用的是正式发表版，正确。
- **状态：** ✅ 核实无误

### ✅ AgrawalGansGoldfarb2019

- **当前条目：** Agrawal, Ajay and Gans, Joshua S. and Goldfarb, Avi (2019). "Artificial Intelligence: The Ambiguous Labor Market Impact of Automating Prediction." *Journal of Economic Perspectives*, 33(2), 31–50. DOI: 10.1257/jep.33.2.31
- **Crossref 官方元数据：** 标题、作者、期刊名、卷期页码、DOI 均一致。注意：该文同时存在 NBER Working Paper (w25619, 2019.2) 和 SSRN 预印本 (3341456)。当前引用的是正式发表版，正确。
- **状态：** ✅ 核实无误

---

## 🔴 引用但缺失条目的文献

以下 5 篇文献在正文中被 `\citet{}` 引用，但 `paper/references.bib` 中无对应条目：

| 引用键 | 引用上下文 | 建议 |
|--------|-----------|------|
| BrynjolfssonHitt2000 | "关于数字化转型和生产率的实证研究" | 需补充 BibTeX 条目。可能指向 Brynjolfsson & Hitt (2000), "Beyond Computation: Information Technology, Organizational Transformation and Business Performance," JEP 14(4), 23-48 (DOI: 10.1257/jep.14.4.23) |
| AutorDorn2013 | 同上 | 需补充 BibTeX 条目。可能指向 Autor & Dorn (2013), "The Growth of Low-Skill Service Jobs and the Polarization of the US Labor Market," AER 103(5), 1553-1597 (DOI: 10.1257/aer.103.5.1553) |
| Bessen2019 | 同上 | 需补充 BibTeX 条目。可能指向 Bessen (2019), "AI and Jobs: The Role of Demand," NBER WP w24235 (DOI: 10.3386/w24235) |
| Rosenberg1982 | "关于企业技术采用决策的理论模型" | 需补充 BibTeX 条目。可能指向 Rosenberg (1982), *Inside the Black Box: Technology and Economics*, Cambridge University Press |
| Jovanovic1982 | 同上 | 需补充 BibTeX 条目。可能指向 Jovanovic (1982), "Selection and the Evolution of Industry," Econometrica 50(3), 649-670 (DOI: 10.2307/1912606) |

---

## 总结

已核实的 7 个参考文献条目均准确无误，DOI、作者、期刊名、卷期页码与 Crossref 官方记录一致。所有引用均为正式发表版（非工作论文版），不存在版本混合问题。

**核心问题：** 5 篇引用文献缺少参考文献条目，必须补充后方可编译。建议作者确认上述 5 篇文献的具体版本后，在 `references.bib` 中添加对应条目。
