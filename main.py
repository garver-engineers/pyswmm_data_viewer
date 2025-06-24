from swmm_timeseries_maker import extract_swmm_timeseries
from comparer import compare_timeseries_data
from comparer import plot_comparison
import os

project_name = "DFW Terminal F Design Build"
out_files = [
    r"L:\2022\22A28803 - DFW Terminal F Design Build\Design\Calculations\Drainage\EPASWMM\ex EPASWMM from BUC\Ex_RE_EC_100yr.out",
    r"L:\2022\22A28803 - DFW Terminal F Design Build\Design\Calculations\Drainage\EPASWMM\ex EPASWMM from BUC\Prop_RE_EC_100yr_both_20251906.out"
]

compare_out_files = [
    r"L:\2022\22A28803 - DFW Terminal F Design Build\Design\Calculations\Drainage\EPASWMM\ex EPASWMM from BUC\Ex_RE_EC_100yr.out",
    r"L:\2022\22A28803 - DFW Terminal F Design Build\Design\Calculations\Drainage\EPASWMM\ex EPASWMM from BUC\Prop_RE_EC_100yr_both_20251906.out"
]

node_ids = ["BC-BB-F3-18900", "BC-BB-F3-18890"]
link_ids = ["BC-BB-F3-18100-0101", "BC-BB-F3-17300-0101", "BC-BB-F3-18900", "BC-BB-F3-18890S"]

node_params = ["head", "total_inflow"]
link_params = ["flow"]

output_dir = "output"

for out_file in out_files:
    # Extract timeseries data from the SWMM output file
    # The function will create an output directory if it doesn't exist
    # output csv files will now exist for each node and link parameter
    # and plots will be generated for each parameter across all nodes and links
    extract_swmm_timeseries(
        out_file,
        node_ids,
        link_ids,
        node_params,
        link_params,
        project_name,
        output_dir=output_dir,
        save_csv=True,
        plot=True,
        round_decimals=6,
    )

# Now we want to compare the timeseries data from two different output files
# use the compare_out_files list to know where to find the output files from extract_swmm_timeseries
sim_name_1 = compare_out_files[0].split("\\")[-1].replace(".out", "")
sim_name_2 = compare_out_files[1].split("\\")[-1].replace(".out", "")
compare_dir_1 = f"{output_dir}/{project_name}/{sim_name_1}"
compare_dir_2 = f"{output_dir}/{project_name}/{sim_name_2}"

# check if output files exist

sim1_links_csv = f"{compare_dir_1} - links data.csv"
sim1_nodes_csv = f"{compare_dir_1} - nodes data.csv"
sim2_links_csv = f"{compare_dir_2} - links data.csv"
sim2_nodes_csv = f"{compare_dir_2} - nodes data.csv"
if not (os.path.exists(sim1_links_csv) and os.path.exists(sim1_nodes_csv) and
        os.path.exists(sim2_links_csv) and os.path.exists(sim2_nodes_csv)):
    raise FileNotFoundError("One or more output CSV files do not exist. Please run the extraction first.")

# for each node and link parameter, create a dataframe that contains the timeseries data from both simulations
# output the comparison results to CSV files
comparison_results = compare_timeseries_data(compare_dir_1, compare_dir_2, node_params, link_params)
compare_output_dir = f"{output_dir}/{project_name}/comparisons/{sim_name_1} - VS - {sim_name_2}"
os.makedirs(compare_output_dir, exist_ok=True)
for param, df in comparison_results["nodes"].items():
    df.to_csv(f"{compare_output_dir}/{param} comparison.csv", index=False)
    print(f"Node parameter '{param}' comparison saved to {compare_output_dir}/node {param} comparison.csv")
for param, df in comparison_results["links"].items():
    df.to_csv(f"{compare_output_dir}/{param} comparison.csv", index=False)
    print(f"Link parameter '{param}' comparison saved to {compare_output_dir}/link {param} comparison.csv")

# lets also create plots for each id with both simulations
plot_comparison(comparison_results, output_dir, project_name, sim_name_1, sim_name_2)
