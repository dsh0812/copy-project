# 中文 LaTeX 论文到 Word 转换工具 - 用户指南

**工具版本：** 1.0  
**最后更新：** 2026-07-08  
**适用范围：** 中文学术论文 LaTeX → Word (期刊格式)

---

## 🚀 快速开始

### 1. 查看转换结果

打开生成的 Word 文档：

```
📄 paper/main_zh_word_V2.docx
```

### 2. 了解转换过程

查看两份详细报告：

```
📋 quality_reports/conversion_audit_2026-07-08.md      (技术细节)
📊 quality_reports/conversion_summary_2026-07-08.md    (总体概览)
```

### 3. 重新运行转换

如需更新参考文献或修复内容后重新转换：

```bash
cd "demo-project"
python scripts/convert_zh_paper_to_word_v2.py
```

---

## 📖 详细使用指南

### 转换工具位置

```
scripts/convert_zh_paper_to_word_v2.py
```

### 输入要求

转换工具需要以下文件存在：

| 文件 | 位置 | 必需 | 用途 |
|------|------|------|------|
| main_zh.tex | paper/ | ✅ 是 | LaTeX 源文件 |
| references.bib | paper/ | ✅ 是 | 参考文献库 |
| 图表 PNG | output/ | ✅ 是 | 数据可视化 |
| 回归表 | output/do-test/ | ⏳ 可选 | 统计结果 |

### 输出产物

| 文件 | 大小 | 包含 |
|------|------|------|
| main_zh_word_V2.docx | 206.6 KB | 完整论文 + 图表 |

---

## 🎯 Word 文档质量评估

### 格式要素检查清单

使用此清单在 Microsoft Word 中快速校对：

#### 字体与大小

- [ ] **标题** (第 1 段)：宋体 16 pt, 加粗, 居中
- [ ] **作者** (第 3 段)：宋体 10.5 pt, 居中
- [ ] **摘要标签** "内容提要："：黑体 12 pt, 加粗
- [ ] **摘要正文**：仿宋 12 pt
- [ ] **关键词标签** "关键词："：黑体 12 pt, 加粗
- [ ] **第一个章节标题** "一、引言"：宋体 15 pt, 加粗, 居中
- [ ] **正文段落** (引言第一段)：宋体 10.5 pt, 两端对齐

#### 段落格式

- [ ] **首行缩进**：~21 pt (2 个汉字宽) ✅ 检查前几个正文段落
- [ ] **行间距**：20 pt ✅ 检查正文行间距一致性
- [ ] **对齐方式**：两端对齐 ✅ 检查边界是否整齐

#### 内容完整性

- [ ] **章节数**：12 个 (引言 → 参考文献)
- [ ] **图表**：3 张 (平行趋势、事件研究、理论模型)
- [ ] **参考文献**：7 条 (已按字母顺序排列)

---

## 🔧 常见问题与解决方案

### Q1: 数学公式看起来很奇怪（下标显示不对）

**现象：** 公式如 `TFP_{it}` 显示为 `TFPit` (下标不明显)

**原因：** 当前转换使用简化的 Unicode 格式，而非完整的 OMML

**解决方案：**
1. 选中有问题的公式
2. 使用 Word 公式编辑器：**插入** > **公式** > **编辑**
3. 手工输入正确的下标/上标格式

### Q2: 表格是等宽字体，看起来很丑

**现象：** 表格显示为 LaTeX 源代码，使用 Courier New 等宽字体

**原因：** 当前脚本保留了 LaTeX 原始代码，便于数据完整性

**解决方案（快速）：**
1. 选中表格文本
2. **表格** > **转换** > **文本转表格**
3. 设置分隔符为空格或制表符

**解决方案（精细）：**
1. 手动在 Word 中创建新表格
2. 从 LaTeX 表格源中复制数据
3. 粘贴到 Word 表格

### Q3: 缺少一些参考文献条目

**现象：** 文本中提到 5 篇文献但参考文献列表中没有

**原因：** paper/references.bib 中这 5 条条目缺失

**涉及文献：**
- BrynjolfssonHitt2000 (文献综述)
- AutorDorn2013 (文献综述)
- Bessen2019 (文献综述)
- Rosenberg1982 (理论机制)
- Jovanovic1982 (理论机制)

**解决方案：**
1. 查看 quality_reports/literature_verification_2026-07-08.md 中的建议条目
2. 将这 5 条条目添加到 paper/references.bib
3. 重新运行转换脚本

### Q4: 文献综述有"增加一些文献综述..."的编辑标记

**现象：** 文献综述中间有未完成的编辑注释

**原因：** LaTeX 源文件中的批注

**解决方案：**
1. 打开 paper/main_zh.tex
2. 查找并删除行 43 的批注
3. 补充完整的文献综述内容
4. 重新运行转换脚本

### Q5: 怎样修改字体或间距？

**修改源代码：**

1. 打开 `scripts/convert_zh_paper_to_word_v2.py`
2. 找到常量定义部分（第 30-45 行）：

```python
SONG = "宋体"
FANGSONG = "仿宋"
HEITI = "黑体"

SIZES = {
    "body": 10.5,  # 修改此行改变正文大小
    "abstract_body": 12,  # 修改此行改变摘要大小
    # ... 其他大小定义
}
```

3. 修改需要的常量
4. 保存文件
5. 重新运行脚本

---

## 📋 转换脚本结构说明

### 关键函数

| 函数 | 作用 |
|------|------|
| `set_run_font_chinese()` | 为文本段设置中英文混合字体 |
| `add_title()` | 添加标题、作者、日期 |
| `add_abstract()` | 添加摘要和关键词 |
| `add_section_heading()` | 添加章节标题 |
| `add_body_paragraph()` | 添加正文段落 |
| `add_equation_display()` | 添加独立公式 |
| `add_figure()` | 添加图表 |
| `add_references()` | 添加参考文献列表 |
| `build_document()` | 整合所有元素生成完整文档 |

### 扩展转换脚本

若需要添加新功能，可在 `build_document()` 函数中添加：

```python
def build_document():
    # ... 现有代码 ...
    
    # 在这里添加新的元素，例如：
    add_section_heading(doc, "新章节标题")
    add_body_paragraph(doc, "新段落内容")
    add_figure(doc, "path/to/image.png", "图表标题")
```

---

## 🔄 转换工作流完整步骤

### 步骤 1: 准备源文件

确保以下文件完整无误：

```
✅ paper/main_zh.tex           (LaTeX 主文件)
✅ paper/references.bib        (参考文献库)
✅ output/*.png                (所有图表)
✅ output/do-test/*.tex        (表格源代码)
```

### 步骤 2: 运行转换脚本

```bash
cd "/Users/happyhome/Nutstore Files/0.Teaching/01-RMEB/InvitedLectures/one-stop-research-vscode-llm/demo-project"
python scripts/convert_zh_paper_to_word_v2.py
```

### 步骤 3: 验证输出

```bash
# 检查文件是否生成
ls -lh paper/main_zh_word_V2.docx

# 可选：验证文档结构
unzip -t paper/main_zh_word_V2.docx | head -20
```

### 步骤 4: 在 Word 中打开并检查

1. 用 Microsoft Word 打开 `paper/main_zh_word_V2.docx`
2. 使用上面的"格式要素检查清单"
3. 对数学公式、表格等进行手工调整

### 步骤 5: 优化与定稿

1. 修复表格（转换为本机格式）
2. 完善数学公式（OMML 格式）
3. 补充缺失参考文献
4. 根据期刊要求进行最后微调

### 步骤 6: 导出最终版本

1. 另存为最终版：`main_zh_word_final.docx` 或 `main_zh_word_submitted.docx`
2. 备份原始版本
3. 准备提交期刊或审阅

---

## 🎓 技术背景

### 为什么选择 python-docx 而非 Pandoc?

| 工具 | 优势 | 劣势 |
|------|------|------|
| **python-docx** | 精细控制字体/格式；适合中文期刊规范 | 需要编程能力；不支持完整 OMML |
| **Pandoc** | 快速转换；支持多格式 | 字体控制有限；表格处理不精准 |

### 字体映射实现

使用 python-docx 的低级 XML API 实现 CJK + Latin 混合：

```python
# Low-level XML manipulation for font control
rFonts.set(qn("w:eastAsia"), "宋体")  # Chinese
rFonts.set(qn("w:ascii"), "Times New Roman")  # English/Numbers
```

### OMML 数学公式

Office Math Markup Language (OMML) 是 Word 原生的数学公式格式。当前脚本使用简化的 Unicode 格式，可通过直接 XML 操作升级为完整 OMML 支持。

---

## 📚 相关文档

| 文档 | 内容 | 用途 |
|------|------|------|
| conversion_audit_2026-07-08.md | 详细技术实现记录 | 理解转换细节 |
| conversion_summary_2026-07-08.md | 项目总结与成果 | 快速了解转换结果 |
| literature_verification_2026-07-08.md | 参考文献核查 | 检查文献完整性 |
| paper_review_数字化转型与企业生产率.md | 论文综合评审 | 改进论文内容 |

---

## 🚨 故障排查

### 问题：脚本运行错误

**错误信息：** `ModuleNotFoundError: No module named 'docx'`

**解决方案：**
```bash
pip install python-docx
```

### 问题：文件路径错误

**错误信息：** `FileNotFoundError: [Errno 2] No such file or directory: '...'`

**原因：** 脚本假设工作目录为项目根目录

**解决方案：**
```bash
# 确保在正确的目录运行
cd "/Users/happyhome/Nutstore Files/0.Teaching/01-RMEB/InvitedLectures/one-stop-research-vscode-llm/demo-project"
python scripts/convert_zh_paper_to_word_v2.py
```

### 问题：中文字符显示为方框

**原因：** Word 中未正确安装 CJK 字体

**解决方案：**
1. 在 Word 中手动选择中文字体（宋体/仿宋/黑体）
2. 或在系统中安装更多中文字体

---

## 💡 最佳实践建议

### 1. 版本控制

保持多个版本以便对比：
```
main_zh_word_V0.docx        (初始版本)
main_zh_word_V1.docx        (第一次修改后)
main_zh_word_V2.docx        (当前版本)
main_zh_word_final.docx     (定稿版本)
```

### 2. 定期验证

每次运行脚本后：
1. 检查文件大小合理性
2. 验证段落数量一致
3. 检查关键格式元素

### 3. 备份原始文件

转换前创建备份：
```bash
cp paper/main_zh.tex paper/main_zh.tex.backup
cp paper/references.bib paper/references.bib.backup
```

### 4. 增量改进

- 一次只修改一个问题
- 修改后重新转换
- 对比新旧版本的差异

---

## 📞 支持与反馈

### 如何报告问题

1. 检查上面的"常见问题"部分
2. 查阅转换审计报告获取技术细节
3. 检查 LaTeX 源文件是否有特殊字符或格式

### 如何改进脚本

欢迎贡献改进，特别是：
- 完整 OMML 数学公式支持
- LaTeX 表格自动解析
- 更多的字体和格式选项

---

## ✅ 总检查清单

转换完成前的最终验证：

- [ ] 文件已生成：`paper/main_zh_word_V2.docx`
- [ ] 文件大小合理 (>100 KB)
- [ ] 能用 Word 打开
- [ ] 包含所有章节（11-12 个）
- [ ] 包含所有图表（3 张）
- [ ] 参考文献列表完整
- [ ] 中文字体应用正确
- [ ] 审计报告已阅读
- [ ] 已知问题已记录
- [ ] 改进方案已理解

---

**用户指南版本：** 1.0  
**最后更新：** 2026-07-08  
**适用工具：** convert_zh_paper_to_word_v2.py  
**兼容性：** Microsoft Word 2016+ / Office 365 / Mac Word

---

*本指南为中文学术论文 LaTeX → Word 转换工具的使用说明。更多技术细节请参考 conversion_audit_2026-07-08.md。*
