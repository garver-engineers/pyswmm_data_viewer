import pandas as pd
import os
import matplotlib.pyplot as plt
def compare_timeseries_data(sim1_dir, sim2_dir, node_params, link_params):
    # Load the CSV files into dataframes
    sim1_nodes_df = pd.read_csv(f"{sim1_dir} - nodes data.csv")
    sim2_nodes_df = pd.read_csv(f"{sim2_dir} - nodes data.csv")
    sim1_links_df = pd.read_csv(f"{sim1_dir} - links data.csv")
    sim2_links_df = pd.read_csv(f"{sim2_dir} - links data.csv")

    # Create a dictionary to hold the comparison results
    comparison_results = {
        "nodes": {},
        "links": {}
    }

    # Compare node parameters
    for param in node_params:
        merged = pd.merge(
            sim1_nodes_df[["id", "time", param]],
            sim2_nodes_df[["id", "time", param]],
            on=["id", "time"],
            suffixes=('_sim1', '_sim2'),
            how='outer'
        )
        # Drop rows where either simulation's parameter value is missing
        merged = merged.dropna(subset=[f"{param}_sim1", f"{param}_sim2"])
        comparison_results["nodes"][param] = merged

    # Compare link parameters
    for param in link_params:
        merged = pd.merge(
            sim1_links_df[["id", "time", param]],
            sim2_links_df[["id", "time", param]],
            on=["id", "time"],
            suffixes=('_sim1', '_sim2'),
            how='outer'
        )
        merged = merged.dropna(subset=[f"{param}_sim1", f"{param}_sim2"])
        comparison_results["links"][param] = merged
    
    print("Comparison of timeseries data completed.")
    # print the head of each comparison dataframe
    for param, df in comparison_results["nodes"].items():
        print(f"Node parameter '{param}' comparison head:\n{df.head()}\n")

    return comparison_results

import matplotlib.pyplot as plt
def plot_comparison(comparison_results, output_dir, project_name, sim_name_1, sim_name_2):
    compare_output_dir = f"{output_dir}/{project_name}/comparisons/{sim_name_1} - VS - {sim_name_2}"
    os.makedirs(compare_output_dir, exist_ok=True)

    # Plot node comparisons
    for param, df in comparison_results["nodes"].items():
        for nid in df['id'].unique():
            print(f"Plotting comparison for '{param}' on node {nid}...")
            subset = df[df['id'] == nid].reset_index(drop=True)  # <-- reset index here
            plt.figure(figsize=(10, 5), facecolor='white')
            plt.plot(
                subset['time'],
                subset[f'{param}_sim1'],
                label=f'Simulation 1 ({sim_name_1})',
                color='blue',
                linewidth=3,
                linestyle=':'
            )
            plt.plot(
                subset['time'],
                subset[f'{param}_sim2'],
                label=f'Simulation 2 ({sim_name_2})',
                color='orange'
            )
            plt.title(f'Node {nid} - {param} Comparison')
            plt.xlabel('Time')
            plt.ylabel(param)
            plt.legend()
            plt.grid(axis='y')
            # Format x-axis: show every 1 hour
            times = pd.to_datetime(subset['time'])
            # Set x-ticks at a reasonable interval to reduce clutter
            n_points = len(times)
            max_ticks = 8  # Adjust this to control max number of x-ticks
            if n_points > max_ticks:
                tick_indices = list(range(0, n_points, max(1, n_points // max_ticks)))
                plt.xticks(
                    tick_indices,
                    [times.iloc[i].strftime('%Y-%m-%d %H:%M') for i in tick_indices],
                    rotation=45
                )
            else:
                plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(f"{compare_output_dir}/node_{nid}_{param}_comparison.png")
            plt.close()

    # Plot link comparisons
    for param, df in comparison_results["links"].items():
        for lid in df['id'].unique():
            print(f"Plotting comparison for '{param}' on link {lid}...")
            subset = df[df['id'] == lid].reset_index(drop=True)  # <-- reset index here
            plt.figure(figsize=(10, 5), facecolor='white')
            plt.plot(
                subset['time'],
                subset[f'{param}_sim1'],
                label=f'Simulation 1 ({sim_name_1})',
                color='blue',
                linewidth=3,
                linestyle=':'
            )
            plt.plot(
                subset['time'],
                subset[f'{param}_sim2'],
                label=f'Simulation 2 ({sim_name_2})',
                color='orange'
            )
            plt.title(f'Link {lid} - {param} Comparison')
            plt.xlabel('Time')
            plt.ylabel(param)
            plt.legend()
            plt.grid(axis='y')
            # Format x-axis: show every 1 hour
            times = pd.to_datetime(subset['time'])
            # Set x-ticks at a reasonable interval to reduce clutter
            n_points = len(times)
            max_ticks = 8  # Adjust this to control max number of x-ticks
            if n_points > max_ticks:
                tick_indices = list(range(0, n_points, max(1, n_points // max_ticks)))
                plt.xticks(
                    tick_indices,
                    [times.iloc[i].strftime('%Y-%m-%d %H:%M') for i in tick_indices],
                    rotation=45
                )
            else:
                plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(f"{compare_output_dir}/link_{lid}_{param}_comparison.png")
            plt.close()