# 参考文献核查日志

**日期：** 2026-06-03
**论文：** `paper/main_zh.tex`
**核查通道：** Crossref DOI API（英文文献，7 条）
**CNKI 通道：** 本文无中文文献，跳过
**执行者：** review-paper skill

---

## 汇总

| 条目 | 引用键 | 状态 |
|------|--------|------|
| Bloom, Sadun & Van Reenen (2012) | `BloomSadunVanReenen2012` | ✅ 核实无误 |
| Bertrand, Duflo & Mullainathan (2004) | `BertrandDufloMullainathan2004` | ✅ 核实无误 |
| Callaway & Sant'Anna (2021) | `CallawaySantAnna2021` | ✅ 核实无误（标题大小写差异，见下） |
| Sun & Abraham (2021) | `SunAbraham2021` | ✅ 核实无误（标题大小写差异，见下） |
| Goodman-Bacon (2021) | `GoodmanBacon2021` | ✅ 核实无误（标题大小写差异，见下） |
| Acemoglu & Restrepo (2019) | `AcemogluRestrepo2019` | ✅ 核实无误 |
| Agrawal, Gans & Goldfarb (2019) | `AgrawalGansGoldfarb2019` | ✅ 核实无误 |

**总计：** 7 条全部通过，0 条实质性错误。

---

## 逐条核查

### 1. BloomSadunVanReenen2012

| 字段 | .bib 录入 | Crossref 返回 | 结论 |
|------|-----------|--------------|------|
| 标题 | Americans Do IT Better: US Multinationals and the Productivity Miracle | Americans Do IT Better: US Multinationals and the Productivity Miracle | ✅ |
| 作者 | Bloom, Nicholas; Sadun, Raffaella; Van Reenen, John | Bloom; Sadun; Reenen | ✅（Van Reenen 全名一致） |
| 期刊 | American Economic Review | American Economic Review | ✅ |
| 年份 | 2012 | 2012 | ✅ |
| 卷/期/页 | 102 / 1 / 167–201 | 102 / 1 / 167–201 | ✅ |
| DOI | 10.1257/aer.102.1.167 | 解析成功 | ✅ |

---

### 2. BertrandDufloMullainathan2004

| 字段 | .bib 录入 | Crossref 返回 | 结论 |
|------|-----------|--------------|------|
| 标题 | How Much Should We Trust Differences-in-Differences Estimates? | How Much Should We Trust Differences-In-Differences Estimates? | ✅（连字符大小写差异属格式非内容，可忽略） |
| 作者 | Bertrand, Marianne; Duflo, Esther; Mullainathan, Sendhil | Bertrand; Duflo; Mullainathan | ✅ |
| 期刊 | The Quarterly Journal of Economics | The Quarterly Journal of Economics | ✅ |
| 年份 | 2004 | 2004 | ✅ |
| 卷/期/页 | 119 / 1 / 249–275 | 119 / 1 / 249–275 | ✅ |
| DOI | 10.1162/003355304772839588 | 解析成功 | ✅ |

**附注：** `audit-log.md` 记录旧 DOI 10.1162/003355303322552328（对应同名文章的早期版本或测试 DOI）未能通过 Crossref 返回元数据，已被正确弃用，改用 10.1162/003355304772839588。此核查印证 audit-log 决策正确。

---

### 3. CallawaySantAnna2021

| 字段 | .bib 录入 | Crossref 返回 | 结论 |
|------|-----------|--------------|------|
| 标题 | Difference-in-Differences with Multiple Time Periods | Difference-in-Differences with multiple time periods | ✅（"multiple" 大写差异属 BibTeX 格式规范，内容一致） |
| 作者 | Callaway, Brantly; Sant'Anna, Pedro H. C. | Callaway; Sant'Anna | ✅ |
| 期刊 | Journal of Econometrics | Journal of Econometrics | ✅ |
| 年份 | 2021 | 2021 | ✅ |
| 卷/期/页 | 225 / 2 / 200–230 | 225 / 2 / 200–230 | ✅ |
| DOI | 10.1016/j.jeconom.2020.12.001 | 解析成功 | ✅ |

---

### 4. SunAbraham2021

| 字段 | .bib 录入 | Crossref 返回 | 结论 |
|------|-----------|--------------|------|
| 标题 | Estimating Dynamic Treatment Effects in Event Studies with Heterogeneous Treatment Effects | Estimating dynamic treatment effects in event studies with heterogeneous treatment effects | ✅（首字母大写差异属格式，内容一致） |
| 作者 | Sun, Liyang; Abraham, Sarah | Sun; Abraham | ✅ |
| 期刊 | Journal of Econometrics | Journal of Econometrics | ✅ |
| 年份 | 2021 | 2021 | ✅ |
| 卷/期/页 | 225 / 2 / 175–199 | 225 / 2 / 175–199 | ✅ |
| DOI | 10.1016/j.jeconom.2020.09.006 | 解析成功 | ✅ |

---

### 5. GoodmanBacon2021

| 字段 | .bib 录入 | Crossref 返回 | 结论 |
|------|-----------|--------------|------|
| 标题 | Difference-in-Differences with Variation in Treatment Timing | Difference-in-differences with variation in treatment timing | ✅（大小写差异属格式，内容一致） |
| 作者 | Goodman-Bacon, Andrew | Goodman-Bacon | ✅ |
| 期刊 | Journal of Econometrics | Journal of Econometrics | ✅ |
| 年份 | 2021 | 2021 | ✅ |
| 卷/期/页 | 225 / 2 / 254–277 | 225 / 2 / 254–277 | ✅ |
| DOI | 10.1016/j.jeconom.2021.03.014 | 解析成功 | ✅ |

---

### 6. AcemogluRestrepo2019

| 字段 | .bib 录入 | Crossref 返回 | 结论 |
|------|-----------|--------------|------|
| 标题 | Automation and New Tasks: How Technology Displaces and Reinstates Labor | Automation and New Tasks: How Technology Displaces and Reinstates Labor | ✅ |
| 作者 | Acemoglu, Daron; Restrepo, Pascual | Acemoglu; Restrepo | ✅ |
| 期刊 | Journal of Economic Perspectives | Journal of Economic Perspectives | ✅ |
| 年份 | 2019 | 2019 | ✅ |
| 卷/期/页 | 33 / 2 / 3–30 | 33 / 2 / 3–30 | ✅ |
| DOI | 10.1257/jep.33.2.3 | 解析成功 | ✅ |

---

### 7. AgrawalGansGoldfarb2019

| 字段 | .bib 录入 | Crossref 返回 | 结论 |
|------|-----------|--------------|------|
| 标题 | Artificial Intelligence: The Ambiguous Labor Market Impact of Automating Prediction | Artificial Intelligence: The Ambiguous Labor Market Impact of Automating Prediction | ✅ |
| 作者 | Agrawal, Ajay; Gans, Joshua S.; Goldfarb, Avi | Agrawal; Gans; Goldfarb | ✅ |
| 期刊 | Journal of Economic Perspectives | Journal of Economic Perspectives | ✅ |
| 年份 | 2019 | 2019 | ✅ |
| 卷/期/页 | 33 / 2 / 31–50 | 33 / 2 / 31–50 | ✅ |
| DOI | 10.1257/jep.33.2.31 | 解析成功 | ✅ |

---

## 特别记录：已剔除的旧 DOI

根据 `audit-log.md` 的记录（2026-06-03 双语论文写作示范条目）：

> 旧 DOI 10.1162/003355303322552328 未能通过 Crossref 返回元数据，未纳入 references.bib

本次核查验证：DOI 10.1162/003355304772839588 可正常解析，指向同一文章（Bertrand, Duflo & Mullainathan 2004），确认替换决策正确。

---

## 结论

- **7 条文献，7 条通过，0 条实质性错误。**
- 3 条 Journal of Econometrics 文献（Callaway-Sant'Anna、Sun-Abraham、Goodman-Bacon）标题存在大小写差异，均属 Crossref API 返回的非标题大写（sentence case）与 BibTeX 录入的标题大写（title case）之间的格式差异，不影响文献可识别性，**无需修正**。
- 参考文献部分可视为 **✅ 已核实无误**，可作为 Crossref 双通道核查的教学示范。
