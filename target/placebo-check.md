# DID 安慰剂检验（Placebo Test）

## Skill 触发
调用 `did-placebo-check` 这一 Skill，对 `data/raw/digital_transformation_firm_panel.csv` 数据执行 DID 安慰剂检验。

## 检验目的
验证真实处理效应是否只是随机噪音或时间趋势所致，而不是真实政策效应。

## 数据与模型
- 数据：`data/raw/digital_transformation_firm_panel.csv`
- 主回归：`log_tfp ~ digital + capital_intensity + export_share + soe + C(firm_id) + C(year)`
- 标准误：按 `firm_id` 聚类
- 安慰剂设计：保留真实处理组不变，随机指定处理年份为 2017 或 2018，并重复 200 次估计

## 结果摘要
- 真实 DID 系数：0.1209
- 伪处理系数均值：0.0740
- 伪处理系数标准差：0.0032
- |伪估计| >= |真实估计| 的比例：0.0000
- 图片输出：`output/placebo-check.png`

## 判断
Placebo test raises caution: pseudo estimates are sizable or overlap the true DID estimate more than expected.

## 结论
本次安慰剂检验结果为 需谨慎。真实系数与伪处理分布的重叠程度为 较高，说明该 DID 估计的解释需要结合时间趋势、处理选择和未观测冲击进一步审慎评估。
