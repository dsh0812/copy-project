# AI Prompts: Install Stata and MATLAB Jupyter Kernels

本文件用于指导 AI Agent 在本机安装和验证 Stata / MATLAB 的 Jupyter kernel。先让 Agent 做环境诊断，再让它执行安装，避免盲目改系统路径。

## Prompt 1: 环境诊断

```text
请检查当前电脑是否已经具备运行 Stata kernel 和 Matlab kernel 的条件。不要修改文件或安装软件，先只做诊断。

请完成：
1. 检查 `python --version`、`pip --version`、`jupyter --version`、`jupyter kernelspec list`。
2. 检查 Stata CLI 是否可用：优先测试 `stata`，其次测试 `stata-mp`，不要打开 GUI。
3. 检查 Matlab CLI 是否可用：测试 `matlab -batch "disp(version)"`。
4. 判断当前 notebooks 的 kernelspec 是否匹配：`digital_stata_did.ipynb` 应使用 name=`stata`，`digital_matlab_model.ipynb` 应使用 name=`matlab`。
5. 给出缺失项清单和建议安装命令。不要请求密码；如果需要管理员权限，停止并说明应由用户手动执行。
```

## Prompt 2: 安装 Stata Kernel

```text
请为当前 Python/Jupyter 环境安装 Stata Jupyter kernel，并验证 VS Code 能识别它。

要求：
1. 先确认 Stata CLI 可用：`stata` 或 `stata-mp` 至少有一个能在命令行运行。
2. 使用当前环境的 Python 安装 kernel 包，优先使用 `python -m pip install stata_kernel`。
3. 如果 `stata_kernel` 要求配置 Stata 可执行文件路径，请根据本机 `which stata` 或 `which stata-mp` 的结果配置，不要猜路径。
4. 安装后运行 `jupyter kernelspec list`，确认出现名为 `stata` 的 kernel。
5. 打开或检查 `notebooks/digital_stata_did.ipynb`，确认它的 kernelspec name 是 `stata`。
6. 如果 kernel 安装失败，不要硬改 notebook；请保留 `scripts/run_stata_did.do` 作为 fallback，并总结失败原因。

验证命令参考：
   python -m pip install stata_kernel
   jupyter kernelspec list
   stata -b do scripts/run_stata_did.do
```

## Prompt 3: 安装 Matlab Kernel

```text
请为当前 Python/Jupyter 环境安装 MATLAB Jupyter kernel，并验证 VS Code 能识别它。

要求：
1. 先确认 Matlab CLI 可用：运行 `matlab -batch "disp(version)"`。
2. 使用当前环境的 Python 安装 kernel 包，优先使用 `python -m pip install matlab_kernel`。
3. 如果需要 MATLAB Engine for Python，请先检测 MATLAB 安装目录和当前 Python 版本是否兼容，再提出命令；不要猜目录。
4. 安装后运行 `jupyter kernelspec list`，确认出现名为 `matlab` 的 kernel。
5. 打开或检查 `notebooks/digital_matlab_model.ipynb`，确认它的 kernelspec name 是 `matlab`。
6. 如果 kernel 安装失败，不要硬改 notebook；请保留 `scripts/matlab_power_simulation.m` 作为 fallback，并总结失败原因。

验证命令参考：
   python -m pip install matlab_kernel
   jupyter kernelspec list
   matlab -batch "run('scripts/matlab_power_simulation.m')"
```

## Prompt 4: 安装后完整验证

```text
请验证 Stata kernel、Matlab kernel 和 fallback 脚本都可用于当前 demo-project。

请完成：
1. 运行 `jupyter kernelspec list`，确认有 `stata` 和 `matlab`。
2. 检查 `notebooks/digital_stata_did.ipynb` 和 `notebooks/digital_matlab_model.ipynb` 的 kernelspec name 是否分别为 `stata` 和 `matlab`。
3. 不执行整本 Stata/Matlab notebook；先运行 fallback：
   - `stata -b do scripts/run_stata_did.do`
   - `matlab -batch "run('scripts/matlab_power_simulation.m')"`
4. 确认输出文件存在：
   - `output/stata_did_results.csv`
   - `output/stata_event_study.csv`
   - `output/stata_placebo_results.csv`
   - `output/matlab_theory_estimates.csv`
   - `output/matlab_theory_model.png`
5. 汇报：kernel 是否可用、fallback 是否可用、现场演示建议使用哪条路径。
```
