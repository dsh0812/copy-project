# Notebooks

本目录用于现场展示和快速研究备忘录。现场可以先运行脚本生成稳定输出，再打开 notebook 解释表格、图形和下一步检查。

- `digital_stata_did.ipynb`：Stata kernel 版本，展示 DID、事件研究和安慰剂检验
- `digital_matlab_model.ipynb`：Matlab kernel 版本，展示数字化转型理论模型和数值校准
- `research_memo.ipynb`：Python 汇总备忘录，读取 DID、平行趋势、安慰剂检验和 Matlab 理论输出
- 可导出 HTML 作为便携备忘录
- 可导出 slides 用于组会快速汇报

```bash
jupyter nbconvert notebooks/research_memo.ipynb --to html --execute
jupyter nbconvert notebooks/research_memo.ipynb --to slides --execute
```

## Kernel 安装说明

这两份 notebook 需要本机已经安装对应软件，并且命令行能找到可执行入口：

- Stata notebook：需要安装Stata 本体程序、Python/Jupyter、以及 Stata kernel。当前 notebook 的 kernel 名称是 `stata`。
- Matlab notebook：需要 MATLAB 本体、Python/Jupyter、以及 MATLAB kernel。当前 notebook 的 kernel 名称是 `matlab`。

优先用 CLI 验证软件入口是否可用：

```bash
stata -q -e "display c(stata_version)"
matlab -batch "disp(version)"
jupyter kernelspec list
```

如果 kernel 尚未安装，可以先让 AI Agent 按 `kernel-install-prompts.md` 中的 prompt 检查环境、提出安装方案，再执行安装。现场演示时不必强依赖 kernel：Stata 和 Matlab 都有 fallback 脚本。

```bash
stata -b do scripts/run_stata_did.do
matlab -batch "run('scripts/matlab_power_simulation.m')"
```

## 事件研究图调试记录

`digital_stata_did.ipynb` 中的事件研究图应当直接来自上一条事件研究回归的系数和标准误，而不是对原始变量再做描述性置信区间图。此前使用 `ciplot` 容易把图形逻辑混成变量均值展示，不能严格对应回归结果。

当前 notebook 的处理方式是：

1. 先运行事件研究回归，基准期为处理前一年 `relative_year = -1`。
2. 从回归结果中读取每个事件期虚拟变量的 `_b[]` 和 `_se[]`。
3. 计算 `estimate ± invnormal(0.975) * std_error` 得到 95% 置信区间。
4. 使用 `twoway rcap` 绘制置信区间，并用 `connected` 连接事件研究估计值。
5. 导出图形到 `../output/stata_event_study_ci.png`。

命令行 fallback 脚本也已经同步：运行 Stata 脚本会同时生成事件研究结果表和置信区间图。

```bash
stata -b do scripts/run_stata_did.do
```

相关输出文件：

- `output/stata_event_study.csv`：事件研究回归结果，包含相对年份、系数、标准误、t 值和 p 值
- `output/stata_event_study_ci.png`：Stata 生成的事件研究图，包含 95% 置信区间
- `output/digital_event_study.png`：Python 读取 `stata_event_study.csv` 后生成的展示版事件研究图

如果需要重新生成 Python 展示版图形，运行：

```bash
python scripts/analyze_did.py
```

## Matlab 优化模型补充记录

`digital_matlab_model.ipynb` 已从单纯展示生产率收益曲线，扩展为一个简单的企业 AI 采用优化问题。这个补充用于现场展示 Matlab 如何求解“企业是否采用 AI、采用多少 AI 强度，以及采用后生产率水平如何变化”。

当前模型设定为：企业管理能力为 `m`，选择 AI 使用强度 `x`，其中 `x` 被限制在 `[0, 1]`。企业需要支付基础 AI 采用成本；管理能力较低的企业还会面临额外实施成本，因此模型会产生“部分企业采用、部分企业不采用”的成本-收益边界。采用 AI 的净收益为：

```text
V(x) = (phi + lambda * m) * x - 0.5 * psi * x^2 - ai_setup_cost
```

Notebook 中的展示顺序是：

1. 对一个代表性企业，用 `fminbnd` 在 `[0, 1]` 上求解最优 AI 强度。
2. 根据最优净收益是否大于 0，判断企业是否采用 AI。
3. 用有界优化 `fminbnd` 校准 `phi`，使模型平均生产率收益贴近 Stata DID 估计。
4. 对不同管理能力的企业计算 AI 采用决策、AI 强度、生产率收益和生产率水平。
5. 绘制“AI 采用选择与生产率收益”图。

命令行 fallback 脚本 `scripts/matlab_power_simulation.m` 也已同步为同一套优化模型。运行后会更新：

- `output/matlab_theory_estimates.csv`：目标 DID、校准后的 `phi`、成本参数、平均收益和 AI 采用率
- `output/matlab_productivity_surface.csv`：不同管理能力企业的 AI 采用成本、AI 强度、采用决策、净收益和生产率水平
- `output/matlab_theory_model.png`：优化模型下的生产率收益图

重新生成 Matlab 输出：

```bash
matlab -batch "run('scripts/matlab_power_simulation.m')"
```
