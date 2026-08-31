# Demo Project: Digital Transformation and Firm Productivity

这个演示项目用于讲座“一站式科研：VS Code 与大模型实操应用”。它使用合成企业面板数据模拟“数字化转型与企业生产率”研究，用来展示 VS Code + AI + Python/Jupyter + Stata-MCP/CLI + Matlab-MCP/CLI + LaTeX Workshop 的科研闭环。

## 环境要求

- Python 3.10 或更高版本
- 建议使用虚拟环境
- Python 依赖见 `requirements.txt`
- 学生课前 VS Code 插件、专业软件和配置文件清单见 `STUDENT_SETUP.md`

## 运行顺序

先进入 demo 项目目录：

```bash
cd InvitedLectures/one-stop-research-vscode-llm/demo-project
```

再运行：

```bash
python scripts/generate_synthetic_did.py
stata -b do scripts/run_stata_did.do
matlab -batch "run('scripts/matlab_power_simulation.m')"
python scripts/analyze_did.py
jupyter nbconvert notebooks/research_memo.ipynb --to html --execute
latexmk -pdf -outdir=paper -interaction=nonstopmode -halt-on-error paper/main.tex
```

## 输出文件

- `data/raw/digital_transformation_firm_panel.csv`
- `output/python_did_results.csv`
- `output/stata_did_results.csv`
- `output/stata_event_study.csv`
- `output/stata_placebo_results.csv`
- `output/digital_parallel_trends.png`
- `output/digital_event_study.png`
- `output/matlab_theory_estimates.csv`
- `output/matlab_productivity_surface.csv`
- `output/matlab_theory_model.png`
- `output/demo_summary.md`
- `notebooks/digital_stata_did.ipynb`
- `notebooks/digital_matlab_model.ipynb`
- `notebooks/research_memo.html`
- `paper/main.tex`

## 现场演示建议

1. 先打开 `prompts/prompt-cards.md`，说明每个 prompt 的风险等级。
2. 运行 Python 数据生成脚本，生成企业层面合成面板数据。
3. 打开 `notebooks/digital_stata_did.ipynb`，展示 Stata kernel 中的 DID、事件研究和平行趋势/安慰剂检验。
4. 运行 `scripts/run_stata_did.do` 作为 Stata-MCP 或 CLI fallback，生成可复用结果文件。
5. 打开 `notebooks/digital_matlab_model.ipynb`，展示 Matlab kernel 中的简单理论模型。
6. 运行 `scripts/matlab_power_simulation.m` 作为 Matlab-MCP 或 CLI fallback。
7. 打开 `notebooks/research_memo.ipynb`，说明 Jupyter 如何汇总实证与理论输出。
8. 打开 `paper/main.tex`，说明 LaTeX Workshop 如何承载论文初稿或学术汇报。
9. 更新 `audit-log.md`，强调 AI 使用记录和人工验证。

Stata 与 Matlab fallback 脚本可以从 `demo-project/`、`demo-project/scripts/` 或讲座包根目录运行；为了减少现场变量，建议仍然先进入 `demo-project/`。

## 学术边界

本项目所有数据均为合成数据，只用于工作流演示。任何估计结果都不能解释为真实企业数字化转型效果。
