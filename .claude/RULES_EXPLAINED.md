# 权限规则说明 / How the Rules File Works

本目录的 `settings.json` 是 Claude Code 的**权限规则文件**（rules file）。它决定了在本项目里，哪些工具调用可以**自动放行**、哪些需要**先询问**、哪些被**直接拒绝**——无需每次手动点"允许"。

这份文档解释它如何为 `review-paper`（论文全稿审查）技能服务。JSON 本身不支持注释，所以讲解放在这里。

---

## 三个规则桶：allow / ask / deny

`settings.json` 的 `permissions` 字段下有三个数组，优先级为 **deny > ask > allow**：

| 桶 | 含义 | 行为 |
|----|------|------|
| `deny` | 禁止 | 即使匹配 allow 也会被拦截，最高优先级 |
| `ask` | 询问 | 每次调用前暂停，等用户确认 |
| `allow` | 放行 | 匹配则自动执行，不打断 |

未被任何规则匹配的工具，回落到 Claude Code 的默认权限模式。

---

## 规则语法：`Tool(matcher)`

- 裸工具名 `Read`、`Grep`、`Glob` —— 放行该工具的**全部**调用。
- `Edit(quality_reports/**)` —— 仅当路径匹配 glob 时放行。`**` 递归匹配子目录。
- `WebFetch(domain:api.crossref.org)` —— 仅放行指定域名。
- `Bash(ls:*)` —— 仅放行 `ls` 开头的 Bash 命令；`:*` 表示后续参数任意。

---

## 本文件为审查工作流配置了什么

审稿是**只读 + 写报告**的工作：要能自由读取论文、检索引用，但绝不能改动论文原稿或原始数据。

### 放行（allow）—— 审稿的日常动作

- **`Read` / `Grep` / `Glob`** —— 通读论文、在正文里 grep `\cite{...}`、glob 定位 `paper/main_zh.tex`、`references.bib`。这是审查的核心动作，全部自动放行。
- **`Edit/Write(quality_reports/**)`** —— 审查报告与文献核查日志写到这里（`quality_reports/paper_review_*.md`、`quality_reports/literature_verification_*.md`）。只有这个目录可写。
- **`WebFetch(domain:...)`** —— 参考文献双通道验证：Crossref（英文文献）+ CNKI（中文文献），外加 NBER 工作论文兜底。仅白名单域名免询问。
- **`Bash(ls/find/rg/cat/head/wc/pdftotext:*)`** —— 只读检索命令，含 `pdftotext`（把 `main.pdf` 转文本分块阅读）。

### 拒绝（deny）—— 守住技能的只读本性

- **`Edit/Write(paper/**)`** —— 论文原稿（`main.tex`、`references.bib` 等）**禁止改动**。这把 SKILL.md 中"此技能为只读，不直接编辑论文"的承诺，从口头约定变成硬约束。直接修改属于 `revise-paper` 技能。
- **`Edit/Write(data/**)`** —— 原始数据不可变。
- **`Bash(rm:*)` / `Bash(git push:*)`** —— 禁止删除文件、禁止推送，防止审查动作产生不可逆的外部副作用。

### 询问（ask）

- **`WebFetch`** —— 白名单之外的任何抓取都先问一声，避免技能在审稿名义下访问任意网站。

---

## 优先级如何生效（关键示例）

`Read` 在 allow 桶里放行了全部读取，但 `paper/**` 在 deny 桶里只挡 `Edit`/`Write`——所以**论文可读不可改**，正是审稿人应有的权限。

```
读 paper/main_zh.tex   → Read 命中 allow      → ✅ 放行
改 paper/main_zh.tex   → Edit 命中 deny       → ⛔ 拒绝
写 quality_reports/... → Write 命中 allow     → ✅ 放行
抓 api.crossref.org    → WebFetch 命中 allow  → ✅ 放行
抓 example.com         → 仅命中 ask           → ⏸ 询问
rm anything            → Bash(rm) 命中 deny   → ⛔ 拒绝
```

---

## 自己动手改规则

- 想让审查报告写到别处：改 `Edit/Write` 的 glob，例如 `Write(reports/**)`。
- 想新增一个文献验证源：往 allow 里加 `WebFetch(domain:你的域名)`。
- 想彻底锁死论文目录的读取也不行：把 `Read(paper/**)` 加进 deny（一般不需要）。
- 改完用 `python3 -m json.tool .claude/settings.json` 验证 JSON 合法。

> 注：本仓库的 `protect-files.sh` 钩子会拦截对 `settings.json` 的 Edit/Write 工具调用。
> 这是另一层防护（hook），与权限规则（permissions）独立——修改本文件需手动编辑或经钩子放行。
