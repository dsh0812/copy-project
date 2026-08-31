# AI Audit Log

## Template

```markdown
## YYYY-MM-DD HH:MM

- 工具：
- 任务：
- 接受的输出：
- 拒绝或修改的输出：
- 验证方式：
- 研究者判断：
```

## 2026-06-03 讲座准备

- 工具：GitHub Copilot / Claude Code
- 任务：创建合成 DID 演示项目、脚本、讲座 slides 和 handout 初稿
- 接受的输出：项目结构、Python 数据生成脚本、Python DID 分析脚本、Stata/Matlab fallback 脚本、Jupyter 研究备忘录、LaTeX 正式写作骨架
- 拒绝或修改的输出：不使用真实数据；不把模拟结果解释为真实政策结论；不把 MCP 配置作为现场必要条件
- 验证方式：运行 Python 脚本，导出 Jupyter notebook，渲染讲座 slides/handout，检查输出是否可从脚本再生成
- 研究者判断：本项目只用于演示科研工作流，不用于实证结论

## 2026-06-03 数字化转型 demo 修订

- 工具：GitHub Copilot / VS Code / Stata CLI / Matlab CLI
- 任务：将原通用 DID demo 改为“数字化转型与企业生产率”的模拟研究项目
- 接受的输出：企业面板数据生成脚本、Stata DID/事件研究/安慰剂检验脚本、Matlab 理论模型脚本、Stata kernel notebook、Matlab kernel notebook、研究备忘录 notebook、LaTeX 初稿
- 拒绝或修改的输出：不再使用泛化政策示例；不把模拟结果解释为真实企业数字化转型效果；不要求现场 MCP 必须可用
- 验证方式：通过 CLI 重跑 Python、Stata、Matlab、LaTeX、Quarto 与 notebook JSON 检查
- 研究者判断：该 demo 更贴近经济学研究学生和教师的完整工作流，但仍然只用于教学展示

## 2026-06-03 双语论文写作示范

- 工具：GitHub Copilot / VS Code / Crossref API / XeLaTeX
- 任务：将 Stata DID notebook、Matlab AI 采用模型 notebook 与 output 结果扩展为中英文经济学论文写作示范，并把对应 prompt 放入 prompt-cards.md
- 输入材料：README.md、notebooks/digital_stata_did.ipynb、notebooks/digital_matlab_model.ipynb、notebooks/research_memo.ipynb、output/stata_did_results.csv、output/stata_event_study.csv、output/stata_placebo_results.csv、output/matlab_theory_estimates.csv、output/matlab_productivity_surface.csv、output/digital_parallel_trends.png、output/stata_event_study_ci.png、output/matlab_theory_model.png、paper/main.tex
- 接受的输出：prompts/prompt-cards.md 第 9 张“双语经济学论文写作”prompt；paper/main_zh.tex；paper/main_en.tex；paper/references.bib
- 拒绝或修改的输出：不引用未能通过 Crossref/DOI 核查的旧 DOI 条目；不把合成数据结果写成真实企业数字化转型证据；不记录隐藏思维链，只记录可审计的决策摘要和验证证据
- 关键写作决策摘要：中文与英文论文分成两个 LaTeX 源文件；两篇论文都保留完整经济学论文结构；真实 output 数值进入结果段落；Matlab 模型定位为机制示范而非结构估计
- 文献核查方式：通过 Crossref API 核查 DOI 元数据。已核查并使用 Bloom, Sadun and Van Reenen (2012)；Bertrand, Duflo and Mullainathan (2004)；Callaway and Sant'Anna (2021)；Sun and Abraham (2021)；Goodman-Bacon (2021)；Acemoglu and Restrepo (2019)；Agrawal, Gans and Goldfarb (2019)。旧 DOI 10.1162/003355303322552328 未能通过 Crossref 返回元数据，未纳入 references.bib
- LaTeX 编译命令：latexmk -xelatex -outdir=paper -interaction=nonstopmode -halt-on-error paper/main_zh.tex；latexmk -xelatex -outdir=paper -interaction=nonstopmode -halt-on-error paper/main_en.tex
- 验证方式：已运行 XeLaTeX 编译命令并确认 paper/main_zh.pdf、paper/main_en.pdf 非空；检查 Markdown/LaTeX 诊断
- 研究者判断：该写作示范适合课堂展示“基于已验证结果写论文”的 AI 工作流，但论文中的实证结论仍仅适用于合成数据演示

## 2026-06-03 Stata 回归表自动化

- 工具：GitHub Copilot / VS Code / Stata CLI / XeLaTeX
- 任务：调整 digital_stata_did.ipynb 的 DID 回归分析部分，生成可被 LaTeX 直接引用的星号显著性回归表，并同步更新中英文论文
- 接受的输出：notebooks/digital_stata_did.ipynb 中新增 LaTeX 表格导出逻辑；scripts/run_stata_did.do 中同步新增 fallback 导出逻辑；output/stata_regression_table.tex；paper/main_zh.tex 与 paper/main_en.tex 中的主结果表改为 \input{} 自动引用
- 拒绝或修改的输出：不再在论文中手写单变量简表，避免论文表格与 Stata 回归结果分叉；不依赖 esttab/estout 等额外用户命令生成最终表格
- 验证方式：运行 python -m json.tool 检查 notebook JSON；运行 stata -b do scripts/run_stata_did.do 生成表格；运行 XeLaTeX 编译中英文论文并确认 PDF 非空
- 研究者判断：该表格适合课堂展示“从 Stata 回归结果到 LaTeX 论文表格”的自动化链条；数值仍仅服务于合成数据教学示范

## 2026-06-03 中文 Word 论文格式转换

- 工具：GitHub Copilot / VS Code / python-docx
- 任务：将 paper/main_zh.tex 转换为符合中文期刊排版要求的 Word 文档
- 接受的输出：scripts/convert_zh_paper_to_word.py；paper/main_zh_word.docx
- 格式处理摘要：标题居中宋体小三；作者信息使用星号脚注式说明；内容提要使用黑体小四标题与仿宋小四正文；节标题居中宋体小三；正文使用仿宋并设置首行缩进；表格变量名改为中文，采用 Panel 行、分组行、变量名行、列号行结构；表格正文使用仿宋小五，备注使用宋体六号；参考文献无编号并按英文期刊格式列出完整作者
- 拒绝或修改的输出：未直接使用 Pandoc 默认转换，因为默认样式难以满足中文字体、字号、表格表头层级和参考文献格式要求；改用 python-docx 直接控制 Word 样式
- 验证方式：运行转换脚本；确认 paper/main_zh_word.docx 非空；使用 unzip -t 检查 docx 压缩包结构；使用 python-docx 读取段落、表格和图片关系数量；检查脚本诊断无错误
- 研究者判断：该 Word 文档适合作为中文期刊格式演示版；由于 python-docx 不原生支持真实 Word 脚注，作者信息采用星号标记加脚注式说明段落呈现

## 2026-06-04 11:10 中文 Word 论文重新导出

- 工具：Codex / python-docx
- 任务：读取 latex-to-word-zh 技能说明，并将 paper/main_zh.tex 重新导出为中文 Word 文档
- 接受的输出：复用 scripts/convert_zh_paper_to_word.py 生成 paper/main_zh_word.docx
- 拒绝或修改的输出：未改动 LaTeX 源文件和转换脚本；继续使用 python-docx 而非 Pandoc，以保留中文字体、字号、表格和图片格式控制
- 验证方式：运行 python scripts/convert_zh_paper_to_word.py；运行 python -m py_compile scripts/convert_zh_paper_to_word.py；确认 paper/main_zh_word.docx 非空；运行 unzip -t paper/main_zh_word.docx；使用 python-docx 确认文档包含 48 个段落、1 个表格和 3 张图片
- 研究者判断：重新导出的 Word 文件可作为 main_zh.tex 的中文期刊格式 Word 版本；作者说明仍采用星号加脚注式段落呈现

## 2026-08-31 Skill 重跑R2安慰剂检验

- 接受的输出：Skill (Part‑B) 版本输出。完整归档基准回归模型元信息；同时校验**尾部概率**与**伪系数分布中心是否趋近于 0**两套安慰剂检验判定准则；输出标准化审计告警标签，给出 “需谨慎” 综合判断；输出分模块结构化，明确给出后续实证改进方向。
- 拒绝或修改的输出：裸 Prompt (Part‑A) 版本输出。①仅关注尾部概率指标，忽视伪系数整体中心显著偏离零点这一核心风险，风险警示力度偏弱；②缺失基准回归方程、固定效应、聚类标准误等可复现元信息；③无标准化检验判定标签；④解读逻辑权重失衡，依赖 prompt 完整度，存在因果解读偏误，需要修订风险判断部分，补全模型设定记录。
- 验证方式：对照 R2 安慰剂检验直方图；比对 DID 安慰剂检验通用识别规范；对比两份输出文档`placebo‑check.md`与`R2.md`文本内容。
- 研究者判断：裸 Prompt 属于**每次提醒**模式，检验规则完全依赖提示词，提示词稍有遗漏就会产生解读缺陷；Skill 属于**制度内置**模式，将安慰剂检验双重判定逻辑、报告规范内置，稳定性、可审计性、可迁移性更强。本项安慰剂检验虽然真实估计落在伪分布尾部，但伪估计系统性偏离零点，基准 DID 因果结果应当审慎解读，需要补充平行趋势、模型设定调试等稳健性检验。
