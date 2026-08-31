---
name: latex-to-word-zh
description: 'Convert Chinese LaTeX academic papers to Word .docx with Chinese journal formatting. Use when asked to 将中文 LaTeX 转 Word, 论文转 docx, 中文期刊格式, 宋体/仿宋/黑体字号调整, 回归表中文化, 参考文献格式, or reproducible python-docx conversion from .tex to .docx.'
argument-hint: 'source .tex path and formatting requirements'
---
# Chinese LaTeX to Word

## What This Skill Produces

Use this skill to convert a Chinese LaTeX academic paper into a Word document that follows Chinese journal-style formatting. The output should include:

- A generated `.docx` file.
- A reusable conversion script, preferably `python-docx`, when strict formatting is required.
- Verification evidence that the Word file is non-empty, readable, and structurally complete.
- A short note of any Word feature limitations, such as simulated footnotes when native Word footnotes are not implemented.

## When To Use

Use this skill when the user asks for any of the following:

- Convert `main_zh.tex` or another Chinese LaTeX paper to Word.
- Apply Chinese journal formatting to `.docx` output.
- Adjust Chinese fonts and sizes such as 宋体五号、黑体小四、仿宋小四.
- Convert LaTeX regression tables into Chinese Word tables.
- Preserve figures, captions, references, abstracts, keywords, and section headings.
- Produce a reproducible conversion workflow rather than a one-off manual file.

Do not use Pandoc as the default for strict journal formatting. Pandoc is acceptable for rough drafts, but direct `python-docx` generation gives better control over Chinese fonts, paragraph spacing, table headers, captions, and references.

## Inputs To Inspect

Before editing or generating output, inspect the relevant source files:

1. The Chinese LaTeX source, usually `paper/main_zh.tex`.
2. Included table fragments, usually under `output/*.tex`.
3. Figures referenced by the paper, usually under `output/*.png` or `figures/`.
4. Bibliography files, usually `paper/references.bib` or project-level `.bib` files.
5. Existing conversion scripts, if any, to avoid duplicating workflows.
6. Existing audit logs, if the project records AI-assisted writing or conversion decisions.

## Formatting Defaults

When the user gives no conflicting requirement, use these defaults for Chinese journal-style output:


| Element                    | Default Format                                                             |
| ---------------------------- | ---------------------------------------------------------------------------- |
| Title                      | 宋体, 16 pt, bold, centered                                                |
| Author                     | 宋体, 10.5 pt, centered; author mark as superscript`*` if needed           |
| Author note                | 宋体, 7.5 pt, footnote-style paragraph                                     |
| Abstract label`内容提要：` | 黑体, 12 pt, bold                                                          |
| Abstract body              | 仿宋, 12 pt                                                                |
| Keywords label`关键词：`   | 黑体, 12 pt, bold                                                          |
| Keywords body              | 仿宋, 12 pt                                                                |
| Section headings           | 宋体, 15 pt, bold, centered                                                |
| Body paragraphs            | 宋体, 10.5 pt, justified, first-line indent about two Chinese characters   |
| Table caption              | 宋体, 9 pt, bold, centered                                                 |
| Table body                 | 仿宋, 9 pt, centered                                                       |
| Table note                 | 宋体, 7.5 pt, no first-line indent                                         |
| Figure caption             | 宋体, 9 pt, centered                                                       |
| References heading         | Same as section heading                                                    |
| References                 | 宋体, 7.5 pt; English and numbers in Times New Roman; journal names italic |

If the user later changes one element, update only that element unless the request implies a global style change.

## Conversion Procedure

### 1. Confirm Scope

Identify whether the task is:

- A direct conversion of one `.tex` file.
- A format revision of an already generated `.docx`.
- A reusable conversion pipeline for future papers.

If the user has already provided a path and format rules, proceed without asking. Ask only if the source file or output destination is ambiguous.

### 2. Choose Implementation Strategy

Prefer this decision order:

1. Use an existing project conversion script if it already matches the target workflow.
2. Use `python-docx` for strict Chinese formatting.
3. Use Pandoc only for rough conversion or as an intermediate diagnostic, not as the final strict-format output.

For `python-docx`, use explicit run-level font settings:

- `run.font.name = "Times New Roman"` for Latin text.
- `run._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")` or another Chinese font for East Asian text.
- `Pt(...)` for exact font sizes.

### 3. Build Document Sections

Create focused helper functions for each part of the paper:

- `add_title()` for title, author, and author note.
- `add_abstract()` for content summary and keywords.
- `add_section_heading()` for numbered section headings.
- `add_body_paragraph()` for正文 paragraphs.
- `add_regression_table()` for Chinese Word tables.
- `add_figure()` for image insertion and captions.
- `add_references()` for formatted references.
- `build_document()` for orchestration and saving.

Keep format decisions centralized in constants such as `SONG`, `FANGSONG`, `HEITI`, and `TIMES`.

### 4. Handle Body Text

For body paragraphs:

- Use 宋体五号 unless the user says otherwise.
- Use `10.5 pt` for 五号.
- Use justified alignment.
- Use first-line indent of about `21 pt` for two Chinese characters.
- Keep line spacing stable, commonly `20 pt` for Chinese journal-like readability.

Do not accidentally change abstract, table, note, or reference fonts when only the body font is requested.

### 5. Convert Regression Tables

When converting LaTeX regression tables:

- Translate variable labels into Chinese.
- Preserve coefficient values, standard errors, stars, observations, and R-squared exactly.
- Use a multi-row journal-style header when needed:
  - Panel title row.
  - Dependent-variable group row.
  - Variable/dependent-variable row.
  - Column-number row.
- Add a Chinese note explaining clustered standard errors, significance stars, fixed effects, and synthetic data status if relevant.
- Explicitly set table note first-line indent to zero.

### 6. Insert Figures

For each figure:

- Check the image exists before insertion.
- Print a warning if a referenced image is missing; do not silently skip it.
- Use stable image width, such as `Inches(5.6)`, unless the document requires another size.
- Add centered Chinese figure captions.

### 7. Format References

For Chinese journal-style English references:

- Use full author names as represented in the source bibliography or verified citation.
- Use `and` in the reference list, not `&`, unless the user explicitly requests otherwise.
- Italicize journal names.
- Use no numbering if the requested style says references should be unnumbered.
- Use Times New Roman for English and numbers, and set East Asian font explicitly to avoid fallback problems.

For in-text English citations, follow the user's requested convention. In the prior workflow, the required convention was:

- Two authors in text: `Author & Author（Year）`.
- Three or more authors in text: `Author et al.（Year）`.
- Reference list: full author list with `and`.

### 8. Convert Mathematical Formulas (CRITICAL)

**This is the most error-prone part of LaTeX-to-Word conversion.** Chinese economics papers typically contain inline math (`$...$`) and display equations (`\begin{equation}...\end{equation}`). The default behavior of converting math to plain text is UNACCEPTABLE for journal-quality output.

#### 8.1 Format Target

Use **OMML (Office Math Markup Language)** — Word's native equation format. OMML equations are:

- Fully editable in Word (unlike images)
- Render correctly with proper subscripts, superscripts, fractions, and Greek letters
- Support both inline and display modes
- Survive `.docx` round-trips without degradation

Do NOT use these approaches for final output:


| Approach                  | Verdict          | Why                                                    |
| --------------------------- | ------------------ | -------------------------------------------------------- |
| Plain text (`log(TFPit)`) | ❌ Banned        | Subscripts lost; looks unprofessional                  |
| Images of equations       | ❌ Avoid         | Not editable; bloat file; blurry at some zoom levels   |
| MathType OLE objects      | ⚠️ Last resort | Requires MathType installed; fragile on cross-platform |
| OMML via`python-docx`     | ✅ Default       | Native Word equations; editable; stable                |

#### 8.2 Implementation Strategy

Use a **LaTeX → OMML pipeline** with these layers:

1. **Pre-process**: Extract all math fragments from body text before paragraph construction.
2. **Parse**: Convert each LaTeX math expression to an OMML XML tree.
3. **Insert**: For inline math, embed OMML inside a `<w:r>` run within the paragraph. For display equations, create a standalone OMML paragraph.

Helper functions to implement:

```
parse_latex_math(latex_str) → OMML XML element
  - Handles: Greek letters, subscripts, superscripts, fractions, operators
  - Input:  "\log(TFP_{it}) = \alpha_i + \beta X_{it}"
  - Output: <m:oMath>...OMML XML...</m:oMath>

add_inline_math(paragraph, latex_str)
  - Embeds OMML inside a run within a text paragraph
  - Font size matches surrounding text (10.5 pt for body, 12 pt for abstract)

add_display_equation(doc, latex_str, label=None)
  - Creates a centered, standalone OMML paragraph
  - Adds equation number in parentheses if label is provided
  - Uses slightly larger font (11 pt) for readability
```

#### 8.3 LaTeX Math Primitives → OMML Mapping

Every converter MUST handle these primitives correctly:


| LaTeX                        | OMML Element             | Example             |
| ------------------------------ | -------------------------- | --------------------- |
| `x_{i}`                      | `<m:sSub>`               | $x_i$               |
| `x^{2}`                      | `<m:sSup>`               | $x^2$               |
| `x_{i}^{2}`                  | `<m:sSubSup>`            | $x_i^2$             |
| `\frac{a}{b}`                | `<m:f>`                  | $\frac{a}{b}$       |
| `\alpha, \beta, \gamma...`   | Unicode: α, β, γ...   | $\alpha, \beta$     |
| `\varepsilon, \phi, \psi...` | Unicode: ε, φ, ψ...   | $\varepsilon, \phi$ |
| `\lambda, \tau`              | Unicode: λ, τ          | $\lambda, \tau$     |
| `\log, \exp, \ln`            | `<m:func>` + `<m:fName>` | $\log(x)$           |
| `\in`                        | Unicode: ∈              | $x \in [0,1]$       |
| `\prime` or `'`              | Unicode: ′ (U+2032)     | $X'$                |
| `\sum, \prod`                | `<m:nary>`               | $\sum$              |
| `\sqrt{x}`                   | `<m:rad>`                | $\sqrt{x}$          |
| `\left( ... \right)`         | `<m:d>` with `<m:dPr>`   | $(...)$             |
| `\cdot, \times`              | Unicode: ·, ×          | $a \cdot b$         |
| `\partial`                   | Unicode: ∂              | $\partial$          |
| `\infty`                     | Unicode: ∞              | $\infty$            |
| `\leq, \geq`                 | Unicode: ≤, ≥          | $\leq, \geq$        |
| `\neq`                       | Unicode: ≠              | $\neq$              |
| `\approx`                    | Unicode: ≈              | $\approx$           |

#### 8.4 Inline Math in Body Paragraphs

When body text contains inline math like:

> 核心结果变量为企业对数全要素生产率 $\log(TFP_{it})$。

The converter must:

1. Split the paragraph at `$...$` boundaries into text segments and math segments.
2. For text segments: add a `<w:r>` with 宋体 10.5 pt.
3. For math segments: add an `<w:r>` containing `<m:oMath>` with Latin font 10.5 pt.
4. The OMML must use `Cambria Math` or `Times New Roman` for Latin glyphs within equations.

**Critical detail**: OMML inline equations are wrapped in `<m:oMath>` (not `<m:oMathPara>`). Display equations use `<m:oMathPara>`.

#### 8.5 Display Equations

Display equations like:

```latex
\begin{equation}
\log(TFP_{it}) = \alpha_i + \lambda_t + \tau Digital_{it} + X_{it}'\beta + \varepsilon_{it},
\end{equation}
```

Must be converted to a **centered paragraph** containing `<m:oMathPara>` with the equation. If the equation has a `\label{...}`, do not include it in the Word output (Word equations don't use LaTeX-style labels).

The paragraph formatting:

- Center alignment
- 6 pt space before and after
- Font size 11 pt for readability
- No first-line indent

#### 8.6 Multi-Character Subscripts and Superscripts

A very common bug: `$X_{it}$` becomes $X_i t$ instead of $X_{it}$.

The parser MUST treat `{...}` groups as single units. For `X_{it}`:

- Base: `X`
- Subscript: `it` (both characters inside the `{...}` group)

Regex-based parsers must be greedy within braces. Test with:

- `\log(TFP_{it})` — subscript is `it`, not just `i`
- `X_{it}'\beta` — subscript `it`, then prime, then `\beta`
- `V_i(x_i^*)` — nested: subscript `i`, then `(`, then `x_i^*` (nested sub + sup)

#### 8.7 Greek Letter Lookup Table

The converter must map ALL common LaTeX Greek commands to Unicode:

```python
GREEK = {
    "alpha": "α", "beta": "β", "gamma": "γ", "delta": "δ",
    "epsilon": "ε", "varepsilon": "ε", "zeta": "ζ", "eta": "η",
    "theta": "θ", "iota": "ι", "kappa": "κ", "lambda": "λ",
    "mu": "μ", "nu": "ν", "xi": "ξ", "pi": "π",
    "rho": "ρ", "sigma": "σ", "tau": "τ", "upsilon": "υ",
    "phi": "φ", "varphi": "ϕ", "chi": "χ", "psi": "ψ",
    "omega": "ω",
    "Alpha": "Α", "Beta": "Β", "Gamma": "Γ", "Delta": "Δ",
    "Theta": "Θ", "Lambda": "Λ", "Xi": "Ξ", "Pi": "Π",
    "Sigma": "Σ", "Upsilon": "Υ", "Phi": "Φ", "Psi": "Ψ",
    "Omega": "Ω",
}
```

#### 8.8 Verification Checklist for Math

After conversion, verify:

- [ ]  All inline `$...$` are rendered as OMML, not plain text
- [ ]  Subscripts use `<m:sSub>`, not separate small-font runs
- [ ]  Superscripts use `<m:sSup>`, not separate raised runs
- [ ]  Greek letters appear as actual Unicode Greek (α, β, λ), not Latin equivalents (a, b, L)
- [ ]  Display equations are centered, standalone paragraphs
- [ ]  Fractions use `<m:f>` with numerator/denominator, not `a/b` text
- [ ]  Multi-character subscripts (e.g., `_{it}`) are fully subscripted
- [ ]  Equation font is Cambria Math or consistent with document Latin font

#### 8.9 Handling Edge Cases

**Nested braces**: `V_i(x_i^*)` has `x_i^*` inside parentheses. The parser must handle recursive subscript/superscript within nested groups.

**Prime symbol**: LaTeX `'` should become Unicode U+2032 (′), not an ASCII apostrophe.

**Text within math**: `\text{...}` should render as plain text within the OMML using `<m:t>` without italic styling.

**Empty subscripts**: `X_{}` is invalid LaTeX but should not crash the parser.

**Escaped characters**: `\%`, `\$`, `\&` should render as literal `%`, `$`, `&`.

### 9. Record Limitations

If using `python-docx`, note that native Word footnotes are not directly supported by the public API. If real footnotes are not implemented with lower-level XML, use:

- Superscript `*` after the author.
- A short footnote-style paragraph immediately below the author line.

Mention this clearly in the final summary or audit log.

### 10. Regenerate And Verify

After editing the conversion script, always regenerate the `.docx` and verify it.

Recommended checks:

```bash
python scripts/convert_zh_paper_to_word.py
test -s paper/main_zh_word.docx
unzip -t paper/main_zh_word.docx
```

Use `python-docx` to inspect structure:

```python
from docx import Document
from docx.oxml.ns import qn
from pathlib import Path

path = Path("paper/main_zh_word.docx")
doc = Document(path)
image_rels = [rel for rel in doc.part.rels.values() if "image" in rel.reltype]
print(len(doc.paragraphs), len(doc.tables), len(image_rels), path.stat().st_size)
```

For font-specific revisions, inspect the relevant run directly:

```python
for paragraph in doc.paragraphs:
    if paragraph.text.startswith("目标正文开头"):
        run = paragraph.runs[0]
        east_asia = run._element.rPr.rFonts.get(qn("w:eastAsia"))
        size_pt = run.font.size.pt if run.font.size else None
        assert east_asia == "宋体"
        assert abs(size_pt - 10.5) < 0.01
        break
```

Also run editor diagnostics on the conversion script when available.

### 11. Update Audit Log When Relevant

If the project maintains an audit log, record:

- Source `.tex` file.
- Output `.docx` path.
- Conversion method and why it was chosen.
- Key formatting rules applied.
- Verification checks performed.
- Known limitations such as simulated footnotes.

## Quality Criteria

The task is complete only when:

- The `.docx` exists and is non-empty.
- The document package passes `unzip -t`.
- The document can be opened by `python-docx`.
- Expected paragraphs, tables, and images are present.
- User-specified fonts and sizes are verified on representative runs.
- The conversion script has no unresolved diagnostics or runtime failures.
- The final response links to both the generated `.docx` and the reusable script.

## Example Prompts

- `使用 latex-to-word-zh 将 paper/main_zh.tex 转成中文期刊格式 Word。`
- `把 main_zh.tex 转成 docx，正文宋体五号，摘要仿宋小四，参考文献无编号。`
- `检查 main_zh_word.docx 的正文是否为宋体五号，并重新生成。`
- `把 Stata 输出的 LaTeX 回归表转成中文 Word 表格并插入论文。`
