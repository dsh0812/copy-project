/*============================================================
  Title: DID Analysis for Digital Transformation Demo
  Course: 经济与商务实证研究方法 (RMEB)
  Author: 陈志远
  Date: 2026-06-24
  Purpose: 读取企业面板数据 → 描述统计 → DID 回归 → 事件研究图
============================================================*/

clear all
set more off
capture log close

* 工作目录设为项目根目录（运行前请确认）
* cd "/path/to/demo-project"

log using "output/stata_did_analysis.log", replace text

* ============================================================
* 1. 读取数据
* ============================================================

import delimited using "data/raw/digital_transformation_firm_panel.csv", ///
    clear bindquotes(strict) case(preserve)

* 确认变量类型
describe
count

* ============================================================
* 2. 描述统计
* ============================================================

* 关键变量：log_tfp（对数全要素生产率）、digital（数字化转型状态）
summarize log_tfp digital

* 保存描述统计到 CSV
quietly summarize log_tfp, detail
local tfp_mean = r(mean)
local tfp_sd   = r(sd)
local tfp_n    = r(N)

quietly summarize digital, detail
local dig_mean = r(mean)
local dig_sd   = r(sd)
local dig_n    = r(N)

* 输出描述统计表
clear
set obs 2
gen variable = ""
gen mean = .
gen sd = .
gen N = .

replace variable = "log_tfp" in 1
replace mean = `tfp_mean' in 1
replace sd = `tfp_sd' in 1
replace N = `tfp_n' in 1

replace variable = "digital" in 2
replace mean = `dig_mean' in 2
replace sd = `dig_sd' in 2
replace N = `dig_n' in 2

export delimited using "output/stata_descriptives.csv", replace
display "描述统计已保存到 output/stata_descriptives.csv"

* ============================================================
* 3. DID 回归
* ============================================================

* 确保 reghdfe 已安装
capture which reghdfe
if _rc != 0 {
    ssc install reghdfe
}

* 重新读取数据（因为描述统计表覆盖了数据集）
import delimited using "data/raw/digital_transformation_firm_panel.csv", ///
    clear bindquotes(strict) case(preserve)

* DID 基准回归
reghdfe log_tfp digital, absorb(firm_id year) vce(cluster firm_id)

* 保存回归系数
estimates store did_main

* 提取结果并保存到 CSV
* 提取关键统计量
local b_digital = _b[digital]
local se_digital = _se[digital]
local t_digital = _b[digital] / _se[digital]
local p_digital = 2 * ttail(e(df_r), abs(`t_digital'))
local r2 = e(r2)
local r2_within = e(r2_within)
local N = e(N)
local df_r = e(df_r)

* 标注显著性
if `p_digital' < 0.01 {
    local stars "***"
}
else if `p_digital' < 0.05 {
    local stars "**"
}
else if `p_digital' < 0.1 {
    local stars "*"
}
else {
    local stars ""
}

display _newline
display "========================================"
display "DID 主回归结果"
display "========================================"
display "数字转型系数 (digital): " %9.4f `b_digital' " `stars'"
display "聚类标准误:               " %9.4f `se_digital'
display "t 统计量:                 " %9.4f `t_digital'
display "p 值:                     " %9.4f `p_digital'
display "R² (整体):                " %9.4f `r2'
display "R² (组内):                " %9.4f `r2_within'
display "样本量:                    " %9.0f `N'
display "残差自由度:                " %9.0f `df_r'
display "========================================"

* 将回归结果写入 CSV
clear
set obs 1
gen term = "digital"
gen coefficient = `b_digital'
gen se = `se_digital'
gen tstat = `t_digital'
gen pvalue = `p_digital'
gen stars = "`stars'"
gen r2 = `r2'
gen r2_within = `r2_within'
gen N = `N'
gen df_r = `df_r'

export delimited using "output/stata_did_results.csv", replace
display "DID 回归结果已保存到 output/stata_did_results.csv"

* ============================================================
* 4. 事件研究
* ============================================================

* 重新读取数据
import delimited using "data/raw/digital_transformation_firm_panel.csv", ///
    clear bindquotes(strict) case(preserve)

* 生成相对年份虚拟变量（以 relative_year = -1 即处理前一年为基准）
tabulate relative_year, gen(rel_yr_)

* 基准组为 relative_year = -1（处理前一年）
* 注意：rel_yr_1 对应 relative_year = -4，数字按升序排列
* 需要找出 -1 对应的是第几个虚拟变量

* 先看一下 relative_year 的取值
quietly tabulate relative_year
local n_cats = r(r)

* 确定基准组：relative_year == -1 对应哪个虚拟变量
levelsof relative_year, local(rel_values)
local base_idx = 1
local i = 1
foreach val of local rel_values {
    if `val' == -1 {
        local base_idx = `i'
    }
    local i = `i' + 1
}
display "基准组 relative_year=-1 对应虚拟变量 rel_yr_`base_idx'"

* 去掉基准组，生成交互项（treated × 各期虚拟变量）
* 先生成 treated × relative_year 各期交互项
forvalues j = 1/`n_cats' {
    if `j' != `base_idx' {
        gen treat_x_rel`j' = treated * rel_yr_`j'
    }
}

* 事件研究回归：用交互项替换 digital
local event_vars ""
forvalues j = 1/`n_cats' {
    if `j' != `base_idx' {
        local event_vars "`event_vars' treat_x_rel`j'"
    }
}

display "事件研究回归变量：`event_vars'"
reghdfe log_tfp `event_vars', absorb(firm_id year) vce(cluster firm_id)
estimates store event_study

* 收集事件研究系数和置信区间
clear
* 计算事件研究系数的数量
local n_events = `n_cats' - 1
set obs `n_events'

gen relative_period = .
gen coefficient = .
gen ci_lower = .
gen ci_upper = .

* 遍历各期，收集系数
local obs_idx = 1
local var_idx = 1
foreach val of local rel_values {
    if `val' != -1 {
        local coef = _b[treat_x_rel`var_idx']
        local se_val = _se[treat_x_rel`var_idx']
        local ci_l = `coef' - 1.96 * `se_val'
        local ci_u = `coef' + 1.96 * `se_val'

        replace relative_period = `val' in `obs_idx'
        replace coefficient = `coef' in `obs_idx'
        replace ci_lower = `ci_l' in `obs_idx'
        replace ci_upper = `ci_u' in `obs_idx'

        local obs_idx = `obs_idx' + 1
    }
    local var_idx = `var_idx' + 1
}

* 保存事件研究结果（先去掉 -99 对照组占位值）
drop if relative_period == -99
export delimited using "output/stata_event_study.csv", replace
display "事件研究结果已保存到 output/stata_event_study.csv"

* ============================================================
* 5. 事件研究图
* ============================================================

* 绘制事件研究图
twoway ///
    (scatter coefficient relative_period, mcolor(blue) msymbol(O) msize(medium)) ///
    (rcap ci_lower ci_upper relative_period, lcolor(blue) lwidth(medium)) ///
    (lfit coefficient relative_period, lcolor(red) lpattern(dash) lwidth(thin)), ///
    yline(0, lcolor(black) lpattern(solid) lwidth(thin)) ///
    xline(-0.5, lcolor(gray) lpattern(dash) lwidth(thin)) ///
    xlabel(-4(1)4, labsize(medium)) ///
    title("数字化转型对全要素生产率的事件研究估计") ///
    subtitle("事件研究系数与 95% 置信区间") ///
    xtitle("相对处理年份") ///
    ytitle("估计系数") ///
    legend(order(1 "估计系数" 2 "95% CI" 3 "线性拟合") ///
        position(6) rows(1)) ///
    graphregion(color(white)) ///
    bgcolor(white) ///
    note("基准组：处理前一年 (relative_year = -1)" "置信区间基于聚类到企业层面的标准误", size(small))

graph export "output/digital_event_study.png", replace width(1600) height(1200)

display _newline
display "事件研究图已保存到 output/digital_event_study.png"

log close
