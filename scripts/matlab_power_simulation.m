% Digital transformation theory model for Matlab-MCP demonstration
% Firms solve a compact AI adoption problem. Each firm chooses AI intensity x
% in [0, 1], pays convex implementation costs and a fixed adoption cost, then
% adopts AI only when the optimized net benefit is positive. The parameter phi
% is calibrated to match the simulated DID estimate.

script_dir = fileparts(mfilename('fullpath'));
project_root = fileparts(script_dir);
output_dir = fullfile(project_root, 'output');

if ~exist(output_dir, 'dir')
    mkdir(output_dir);
end

did_file = fullfile(output_dir, 'stata_did_results.csv');
if exist(did_file, 'file')
    did_results = readtable(did_file);
    target_effect = did_results.estimate(1);
else
    target_effect = 0.12;
end

rng(2026);
managerial_capability = linspace(-1.5, 1.5, 61)';
psi = 1.8;
lambda = 0.12;
fixed_ai_cost = 0.06;
cost_sensitivity = 0.10;
ai_setup_cost = fixed_ai_cost + cost_sensitivity .* max(-managerial_capability, 0);
baseline_productivity = 1.0;

objective = @(phi) (mean(solve_ai_adoption(phi, lambda, psi, ai_setup_cost, managerial_capability)) - target_effect)^2;
phi_hat = fminbnd(objective, 0, 2);
[productivity_gain, ai_intensity, adopt_ai, net_benefit_if_adopt] = ...
    solve_ai_adoption(phi_hat, lambda, psi, ai_setup_cost, managerial_capability);
productivity_level = baseline_productivity .* exp(productivity_gain);

mean_gain = mean(productivity_gain);
sd_gain = std(productivity_gain);
adoption_share = mean(adopt_ai);
fprintf('Target DID effect: %.3f\n', target_effect);
fprintf('Calibrated phi: %.3f\n', phi_hat);
fprintf('Mean model-implied gain: %.3f\n', mean_gain);
fprintf('AI adoption share: %.3f\n', adoption_share);

estimates = table(target_effect, phi_hat, psi, lambda, fixed_ai_cost, cost_sensitivity, mean_gain, sd_gain, adoption_share);
writetable(estimates, fullfile(output_dir, 'matlab_theory_estimates.csv'));

surface = table(managerial_capability, ai_setup_cost, ai_intensity, adopt_ai, net_benefit_if_adopt, productivity_gain, productivity_level);
writetable(surface, fullfile(output_dir, 'matlab_productivity_surface.csv'));

figure('Visible', 'off');
plot(managerial_capability, productivity_gain, 'LineWidth', 2);
yline(0, '--');
xlabel('Managerial capability');
ylabel('Model-implied productivity gain');
title('AI Adoption Optimization and Productivity Gain');
grid on;
saveas(gcf, fullfile(output_dir, 'matlab_theory_model.png'));
close(gcf);

function [productivity_gain, ai_intensity, adopt_ai, net_benefit_if_adopt] = solve_ai_adoption(phi, lambda, psi, ai_setup_cost, managerial_capability)
    n_firms = numel(managerial_capability);
    ai_intensity = zeros(n_firms, 1);
    adopt_ai = false(n_firms, 1);
    net_benefit_if_adopt = zeros(n_firms, 1);
    productivity_gain = zeros(n_firms, 1);

    for i = 1:n_firms
        capability = managerial_capability(i);
        value = @(x) (phi + lambda * capability) * x - 0.5 * psi * x^2 - ai_setup_cost(i);
        [candidate_intensity, negative_value] = fminbnd(@(x) -value(x), 0, 1);
        candidate_benefit = -negative_value;
        net_benefit_if_adopt(i) = candidate_benefit;
        adopt_ai(i) = candidate_benefit > 0;

        if adopt_ai(i)
            ai_intensity(i) = candidate_intensity;
            productivity_gain(i) = candidate_benefit;
        end
    end
end
