/*============================================================
  Title: 数字化转型与企业生产率 — DID 分析
  Course: 一站式科研：VS Code 与大模型实操应用
  Author: 陈志远
  Date: 2026-06-10
  Purpose: 合成企业面板数据的 DID 估计、事前平行趋势展示和安慰剂检验
  Source: Exported from digital_stata_did.ipynb
============================================================*/

clear all
set more off
capture log close

* ============================================================
* 0. 路径与数据加载
* ============================================================
local data_file "../data/raw/digital_transformation_firm_panel.csv"
local output_dir "../output"

* 确保 output 目录存在
capture mkdir "`output_dir'"

import delimited "`data_file'", clear
xtset firm_id year
summarize log_tfp digital firm_size capital_intensity export_share

* ============================================================
* 1. DID 估计（简约形式）
* ============================================================
// 估计双重差分模型
xtreg log_tfp digital firm_size capital_intensity export_share i.year, fe

* ============================================================
* 2. DID 估计（完整形式 + LaTeX 表格输出）
* ============================================================
label variable log_tfp "Log TFP"
label variable digital "Digital transformation"
label variable capital_intensity "Capital intensity"
label variable export_share "Export share"
label variable soe "State-owned enterprise"

qui reg log_tfp digital capital_intensity export_share soe i.firm_id i.year, vce(cluster firm_id)
qui estimates store did_model

local n_obs = e(N)
local r_squared : display %6.3f e(r2)
local r_squared = strtrim("`r_squared'")

local table_file "`output_dir'/stata_regression_table.tex"
local variables digital capital_intensity export_share soe

file open table using "`table_file'", write replace text
file write table "\begin{tabular}{lc}" _n
file write table "\toprule" _n
file write table " & Dependent variable: log TFP \\" _n
file write table "\midrule" _n

foreach var of local variables {
    local label : variable label `var'
    if "`label'" == "" local label "`var'"
    if _se[`var'] > 0 & _se[`var'] < . {
        local estimate : display %6.4f _b[`var']
        local estimate = strtrim("`estimate'")
        local std_error : display %6.4f _se[`var']
        local std_error = strtrim("`std_error'")
        local p_value = 2 * ttail(e(df_r), abs(_b[`var'] / _se[`var']))
        local stars ""
        if `p_value' < 0.01 local stars "***"
        else if `p_value' < 0.05 local stars "**"
        else if `p_value' < 0.10 local stars "*"
        file write table "`label' & `estimate'`stars' \\" _n
        file write table " & (`std_error') \\" _n
    }
}

file write table "\midrule" _n
file write table "Firm fixed effects & Yes \\" _n
file write table "Year fixed effects & Yes \\" _n
file write table "Observations & `n_obs' \\" _n
file write table "R-squared & `r_squared' \\" _n
file write table "\bottomrule" _n
file write table "\end{tabular}" _n
file close table

display as text "LaTeX regression table written to `table_file'"
type "`table_file'"

* ============================================================
* 3. 事前平行趋势与动态效应
* ============================================================
forvalues k = -4/4 {
    local suffix = cond(`k' < 0, "m" + string(abs(`k')), "p" + string(`k'))
    capture drop event_`suffix'
    gen event_`suffix' = treated == 1 & relative_year == `k'
}
drop event_m1

reg log_tfp event_m4 event_m3 event_m2 event_p0 event_p1 event_p2 event_p3 event_p4 ///
    capital_intensity export_share soe i.firm_id i.year, vce(cluster firm_id)

* ============================================================
* 4. 事件研究数据导出为 CSV
* ============================================================
local event_table_file "`output_dir'/stata_event_study_data.csv"
file open event_table using "`event_table_file'", write replace text
file write event_table "relative_year,estimate,std_error,p_value" _n

local event_terms event_m4 event_m3 event_m2 event_p0 event_p1 event_p2 event_p3 event_p4
local event_years -4 -3 -2 0 1 2 3 4
local row = 1

foreach term of local event_terms {
    local event_year : word `row' of `event_years'
    local estimate : display %6.4f _b[`term']
    local estimate = strtrim("`estimate'")
    local std_error : display %6.4f _se[`term']
    local std_error = strtrim("`std_error'")
    local p_value = 2 * ttail(e(df_r), abs(_b[`term'] / _se[`term']))
    local p_value_display : display %12.6g `p_value'
    local p_value_display = strtrim("`p_value_display'")
    file write event_table "`event_year',`estimate',`std_error',`p_value_display'" _n
    local row = `row' + 1
}

file close event_table
display as text "Event study data written to `event_table_file'"
type "`event_table_file'"

* ============================================================
* 5. 事件研究图（95% CI）
* ============================================================
local event_terms event_m4 event_m3 event_m2 event_p0 event_p1 event_p2 event_p3 event_p4
local event_years -4 -3 -2 0 1 2 3 4

tempfile event_results
tempname event_post
postfile `event_post' relative_year estimate std_error using `event_results', replace
local row = 1
foreach term of local event_terms {
    local event_year : word `row' of `event_years'
    post `event_post' (`event_year') (_b[`term']) (_se[`term'])
    local row = `row' + 1
}
postclose `event_post'

preserve
use `event_results', clear
gen ci_low = estimate - invnormal(0.975) * std_error
gen ci_high = estimate + invnormal(0.975) * std_error

twoway (rcap ci_high ci_low relative_year, lcolor(navy)) ///
       (connected estimate relative_year, mcolor(navy) lcolor(navy)), ///
       yline(0, lcolor(gs8) lpattern(dash)) ///
       xline(-0.5, lcolor(maroon) lpattern(dash)) ///
       xlabel(-4(1)4) ///
       xtitle("Years relative to digital adoption") ///
       ytitle("Coefficient relative to year -1") ///
       title("Event-study estimates with 95% CI") ///
       legend(off) graphregion(color(white)) bgcolor(white)
graph export "../output/stata_event_study_ci.png", replace width(2000)
restore

* ============================================================
* 6. 安慰剂检验
* ============================================================
preserve
keep if year < 2020
gen placebo_digital = treated == 1 & year >= 2018
reg log_tfp placebo_digital capital_intensity export_share soe i.firm_id i.year, vce(cluster firm_id)
restore

* ============================================================
* 完成
* ============================================================
display as text _n "========================================"
display as text "所有分析完成。"
display as text "输出文件："
display as text "  - `output_dir'/stata_regression_table.tex"
display as text "  - `output_dir'/stata_event_study_data.csv"
display as text "  - ../output/stata_event_study_ci.png"
display as text "========================================" _n
