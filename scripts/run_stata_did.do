/*============================================================
  Title: Digital transformation and productivity DID analysis
  Purpose: Stata-MCP/fallback script for DID, event study, and placebo tests
============================================================*/

clear all
set more off
capture log close

local data_file "data/raw/digital_transformation_firm_panel.csv"
local output_dir "output"
capture confirm file "`data_file'"
if _rc != 0 {
  local data_file "../data/raw/digital_transformation_firm_panel.csv"
  local output_dir "../output"
  capture confirm file "`data_file'"
}
if _rc != 0 {
  local data_file "demo-project/data/raw/digital_transformation_firm_panel.csv"
  local output_dir "demo-project/output"
  capture confirm file "`data_file'"
}
if _rc != 0 {
  display as error "Data file not found. Run scripts/generate_synthetic_did.py first."
  exit 601
}

capture mkdir "`output_dir'"
log using "`output_dir'/stata_did.log", replace text

import delimited "`data_file'", clear
encode industry, gen(industry_id)
encode province, gen(province_id)
xtset firm_id year

label variable log_tfp "Log TFP"
label variable digital "Digital transformation"
label variable capital_intensity "Capital intensity"
label variable export_share "Export share"
label variable soe "State-owned enterprise"

reg log_tfp digital capital_intensity export_share soe i.firm_id i.year, vce(cluster firm_id)
estimates store did_model

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
  else {
    file write table "`label' & Absorbed by firm FE \\" _n
    file write table " & \\" _n
  }
}
local n_obs : display %9.0fc e(N)
local n_obs = strtrim("`n_obs'")
local r_squared : display %6.3f e(r2)
local r_squared = strtrim("`r_squared'")
file write table "\midrule" _n
file write table "Firm fixed effects & Yes \\" _n
file write table "Year fixed effects & Yes \\" _n
file write table "Observations & `n_obs' \\" _n
file write table "R-squared & `r_squared' \\" _n
file write table "\bottomrule" _n
file write table "\end{tabular}" _n
file close table
display as text "LaTeX regression table written to `table_file'"

scalar did_estimate = _b[digital]
scalar did_std_error = _se[digital]
scalar did_t_value = did_estimate / did_std_error
scalar did_p_value = 2 * ttail(e(df_r), abs(did_t_value))
scalar did_n_obs = e(N)
preserve
clear
set obs 1
gen term = "digital"
gen estimate = did_estimate
gen std_error = did_std_error
gen t_value = did_t_value
gen p_value = did_p_value
gen n_obs = did_n_obs
export delimited using "`output_dir'/stata_did_results.csv", replace
restore

forvalues k = -4/4 {
  local suffix = cond(`k' < 0, "m" + string(abs(`k')), "p" + string(`k'))
  gen event_`suffix' = treated == 1 & relative_year == `k'
}
drop event_m1

reg log_tfp event_m4 event_m3 event_m2 event_p0 event_p1 event_p2 event_p3 event_p4 ///
    capital_intensity export_share soe i.firm_id i.year, vce(cluster firm_id)

preserve
tempfile event_results
tempname event_handle
postfile `event_handle' relative_year str12 term estimate std_error t_value p_value using `event_results', replace
foreach event in "-4 event_m4" "-3 event_m3" "-2 event_m2" "0 event_p0" "1 event_p1" "2 event_p2" "3 event_p3" "4 event_p4" {
  local relative_year = word("`event'", 1)
  local coefficient = word("`event'", 2)
  local estimate = _b[`coefficient']
  local std_error = _se[`coefficient']
  local t_value = `estimate' / `std_error'
  local p_value = 2 * ttail(e(df_r), abs(`t_value'))
  post `event_handle' (`relative_year') ("`coefficient'") (`estimate') (`std_error') (`t_value') (`p_value')
}
postclose `event_handle'
use `event_results', clear
export delimited using "`output_dir'/stata_event_study.csv", replace
gen ci_low = estimate - invnormal(0.975) * std_error
gen ci_high = estimate + invnormal(0.975) * std_error
sort relative_year
twoway (rcap ci_high ci_low relative_year, lcolor(navy)) ///
  (connected estimate relative_year, mcolor(navy) lcolor(navy)), ///
  yline(0, lcolor(gs8) lpattern(dash)) ///
  xline(-0.5, lcolor(maroon) lpattern(dash)) ///
  xlabel(-4(1)4) ///
  xtitle("Years relative to digital adoption") ///
  ytitle("Coefficient relative to year -1") ///
  title("Event-study estimates with 95% CI") ///
  legend(off) graphregion(color(white)) bgcolor(white)
graph export "`output_dir'/stata_event_study_ci.png", replace width(2000)
restore

preserve
keep if year < 2020
gen placebo_digital = treated == 1 & year >= 2018
reg log_tfp placebo_digital capital_intensity export_share soe i.firm_id i.year, vce(cluster firm_id)
scalar placebo_estimate = _b[placebo_digital]
scalar placebo_std_error = _se[placebo_digital]
scalar placebo_t_value = placebo_estimate / placebo_std_error
scalar placebo_p_value = 2 * ttail(e(df_r), abs(placebo_t_value))
scalar placebo_n_obs = e(N)
clear
set obs 1
gen term = "placebo_digital_2018"
gen estimate = placebo_estimate
gen std_error = placebo_std_error
gen t_value = placebo_t_value
gen p_value = placebo_p_value
gen n_obs = placebo_n_obs
export delimited using "`output_dir'/stata_placebo_results.csv", replace
restore

log close
