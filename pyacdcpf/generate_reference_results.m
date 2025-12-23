function generate_reference_results()
% GENERATE_REFERENCE_RESULTS  Generate reference results from MATACDC for comparison testing
%
%   This script runs all MATACDC test cases and saves the results to JSON files
%   that can be used to verify PyACDC produces equivalent results.
%
%   MatACDC
%   Copyright (C) 2012 Jef Beerten
%   University of Leuven (KU Leuven)

%% Setup paths
namedir = cd;
addpath([cd '/Cases/PowerflowAC/']);
addpath([cd '/Cases/PowerflowDC/']);

%% Create output directory
output_dir = 'reference_results';
if ~exist(output_dir, 'dir')
    mkdir(output_dir);
end

%% Define options (no output to console)
mdopt = macdcoption;
mdopt(13) = 0;  % no output info

%% Define test cases
% Format: {ac_case, dc_case, test_name}
test_cases = {
    'case5_stagg', 'case5_stagg_MTDCslack', 'case5_MTDCslack';
    'case5_stagg', 'case5_stagg_MTDCdroop', 'case5_MTDCdroop';
    'case5_stagg', 'case5_stagg_HVDCptp', 'case5_HVDCptp';
    'case24_ieee_rts1996_3zones', 'case24_ieee_rts1996_MTDC', 'case24_MTDC';
};

%% Run all test cases and save results
fprintf('Generating MATACDC reference results...\n');
fprintf('=========================================\n\n');

for i = 1:size(test_cases, 1)
    ac_case = test_cases{i, 1};
    dc_case = test_cases{i, 2};
    test_name = test_cases{i, 3};

    fprintf('Running: %s + %s\n', ac_case, dc_case);

    try
        % Run power flow
        [baseMVA, bus, gen, branch, busdc, convdc, branchdc, converged, timecalc] = ...
            runacdcpf(ac_case, dc_case, mdopt);

        if converged
            fprintf('  -> Converged in %.4f seconds\n', timecalc);
        else
            fprintf('  -> WARNING: Did not converge!\n');
        end

        % Save results to JSON
        results = struct();
        results.test_name = test_name;
        results.ac_case = ac_case;
        results.dc_case = dc_case;
        results.converged = converged;

        % AC results
        results.baseMVA = baseMVA;
        results.bus = bus;
        results.gen = gen;
        results.branch = branch;

        % DC results
        results.busdc = busdc;
        results.convdc = convdc;
        results.branchdc = branchdc;

        % Save to JSON file
        json_file = fullfile(output_dir, [test_name '.json']);
        save_results_json(results, json_file);
        fprintf('  -> Saved to %s\n\n', json_file);

    catch ME
        fprintf('  -> ERROR: %s\n\n', ME.message);
    end
end

fprintf('=========================================\n');
fprintf('Reference results generation complete!\n');
fprintf('Results saved to: %s/\n', output_dir);

end

function save_results_json(results, filename)
% SAVE_RESULTS_JSON  Save results structure to JSON file
%
%   This function converts MATLAB matrices to a JSON-compatible format

    % Create JSON structure
    json_struct = struct();
    json_struct.test_name = results.test_name;
    json_struct.ac_case = results.ac_case;
    json_struct.dc_case = results.dc_case;
    json_struct.converged = results.converged;

    % Convert matrices to cell arrays for JSON compatibility
    json_struct.baseMVA = results.baseMVA;
    json_struct.bus = matrix_to_list(results.bus);
    json_struct.gen = matrix_to_list(results.gen);
    json_struct.branch = matrix_to_list(results.branch);
    json_struct.busdc = matrix_to_list(results.busdc);
    json_struct.convdc = matrix_to_list(results.convdc);
    json_struct.branchdc = matrix_to_list(results.branchdc);

    % Write to JSON file
    json_str = jsonencode(json_struct);

    % Pretty print JSON (add newlines for readability)
    fid = fopen(filename, 'w');
    if fid == -1
        error('Cannot open file for writing: %s', filename);
    end
    fprintf(fid, '%s', json_str);
    fclose(fid);
end

function list = matrix_to_list(mat)
% MATRIX_TO_LIST  Convert matrix to cell array (list of lists) for JSON
    if isempty(mat)
        list = {};
    else
        list = num2cell(mat, 2);
        list = cellfun(@(x) x(:)', list, 'UniformOutput', false);
    end
end