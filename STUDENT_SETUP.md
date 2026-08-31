# 学生课前准备：VS Code 插件与配置清单

本项目用于讲座“一站式科研：VS Code 与大模型实操应用”。课前建议至少完成“基础必备”；Stata、Matlab、LaTeX 属于增强项，未配置成功也可以跟随现场 fallback 脚本。

## 基础必备

| 类别 | 准备内容 | 用途 |
| :--- | :--- | :--- |
| VS Code | 安装最新版 VS Code | 统一管理项目、代码、Notebook、终端、Git 和 AI 工具 |
| Git | 能运行 `git --version` | 版本控制、回滚 AI 修改、记录研究过程 |
| GitHub 账号 | 能登录 GitHub | 远程备份、协作、Issue/PR 记录 |
| Python | Python 3.10 或更高版本 | 运行数据生成、DID 分析和图表脚本 |
| Jupyter | 安装在当前 Python 环境中 | 打开和执行 `.ipynb` 研究备忘录 |

安装 Python 依赖：

```bash
python -m pip install -r requirements.txt
```

## 推荐 VS Code 插件

| 插件 | Extension ID | 优先级 | 用途 |
| :--- | :--- | :--- | :--- |
| Python | `ms-python.python` | 必装 | Python 脚本、环境识别、语法检查 |
| Jupyter | `ms-toolsai.jupyter` | 必装 | Notebook 打开、运行和导出 |
| Quarto | `quarto.quarto` | 必装 | `.qmd` 报告和 slides 编辑 |
| GitLens | `eamodio.gitlens` | 必装 | 查看修改历史、比较版本 |
| GitHub Pull Requests | `GitHub.vscode-pull-request-github` | 必装 | 在 VS Code 中处理 Issue/PR |
| GitHub Copilot | `GitHub.copilot` | 推荐 | 行内补全、低风险代码生成 |
| GitHub Copilot Chat | `GitHub.copilot-chat` | 推荐 | 解释文件、生成局部修改 |
| Stata Enhanced | `kylebarron.stata-enhanced` | 增强 | Stata do-file 编辑 |
| MATLAB | `MathWorks.language-matlab` | 增强 | Matlab `.m` 文件编辑 |
| LaTeX Workshop | `James-Yu.latex-workshop` | 增强 | LaTeX 编译、预览和错误定位 |

如果已配置 VS Code 的 `code` 命令，可以一次性安装：

```bash
code --install-extension ms-python.python
code --install-extension ms-toolsai.jupyter
code --install-extension quarto.quarto
code --install-extension eamodio.gitlens
code --install-extension GitHub.vscode-pull-request-github
code --install-extension GitHub.copilot
code --install-extension GitHub.copilot-chat
code --install-extension kylebarron.stata-enhanced
code --install-extension MathWorks.language-matlab
code --install-extension James-Yu.latex-workshop
```

## 专业工具自检

| 工具 | 自检命令 | 说明 |
| :--- | :--- | :--- |
| Git | `git --version` | 必备 |
| Python | `python --version` | 必备；必要时试 `python3 --version` |
| Jupyter | `jupyter --version` | 推荐 |
| Stata CLI | `stata -q -e "display c(stata_version)"` | 增强；失败时使用现场演示结果或 fallback |
| Matlab CLI | `matlab -batch "disp(version)"` | 增强；失败时使用现场演示结果或 fallback |
| LaTeX | `latexmk -v` | 增强；用于编译 `paper/main.tex` |
| Quarto | `quarto --version` | 增强；用于渲染 `.qmd` 报告和 slides |

## Notebook Kernel

| Notebook | Kernel | 准备要求 |
| :--- | :--- | :--- |
| `notebooks/research_memo.ipynb` | Python | Python + Jupyter + `requirements.txt` |
| `notebooks/digital_stata_did.ipynb` | `stata` | Stata 本体、Stata CLI、`stata_kernel` |
| `notebooks/digital_matlab_model.ipynb` | `matlab` | MATLAB 本体、MATLAB CLI、`matlab_kernel` |

Kernel 自检：

```bash
jupyter kernelspec list
```

如果没有 Stata 或 Matlab kernel，可以运行 CLI fallback：

```bash
stata -b do scripts/run_stata_did.do
matlab -batch "run('scripts/matlab_power_simulation.m')"
```

更细的安装提示见 `notebooks/kernel-install-prompts.md`。

## 项目配置文件

| 文件 | 用途 | 是否需要修改 |
| :--- | :--- | :--- |
| `.vscode/extensions.json` | VS Code 推荐插件列表，打开项目时提示安装 | 通常不用 |
| `.vscode/settings.json` | 共享工作区设置：Stata/Matlab/Quarto 文件识别、Notebook 根目录、LaTeX 预览 | 通常不用 |
| `requirements.txt` | Python 依赖清单 | 不用，按文件安装 |
| `.gitignore` | 排除虚拟环境、缓存、本地设置和 LaTeX 中间文件 | 通常不用 |
| `notebooks/kernel-install-prompts.md` | 让 AI Agent 检查和安装 Stata/Matlab kernel 的提示词 | 需要 kernel 时使用 |
| `audit-log.md` | 记录 AI 参与、人工修改和验证方式 | 练习时可以追加 |
| `prompts/prompt-cards.md` | 可复用 AI 提问模板 | 练习时可以复制修改 |

## 课前最小验证

```bash
git --version
python --version
python -m pip install -r requirements.txt
jupyter kernelspec list
python scripts/generate_synthetic_did.py
python scripts/analyze_did.py
```

## 使用 AI 工具前的版本控制习惯

1. 先提交当前可运行版本：`git status`、`git add .`、`git commit -m "checkpoint before ai edits"`
2. 让 AI 修改后先看差异：`git diff`
3. 验证通过再提交：`git commit -m "describe verified change"`

核心原则：AI 可以加速生成，Git/GitHub 要负责留下证据、提供回滚点，并让合作者知道每一次研究修改的来龙去脉。
