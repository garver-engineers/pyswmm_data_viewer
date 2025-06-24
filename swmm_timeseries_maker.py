# %%
from pyswmm import Output
from swmm.toolkit.shared_enum import NodeAttribute
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Agg') # or 'QtAgg' if you need interactivity

# %%
def extract_swmm_timeseries(
    out_file,
    node_ids,
    link_ids,
    node_params,
    link_params,
    project_name="",
    output_dir="output",
    save_csv=True,
    plot=True,
    round_decimals=6
):
    """
    Extracts SWMM timeseries data for specified nodes and links, saves CSVs, and plots if requested.

    Args:
        out_file (str): Path to SWMM .out file.
        node_ids (list): List of node IDs.
        link_ids (list): List of link IDs.
        node_params (list): List of node parameters.
        link_params (list): List of link parameters.
        project_name (str): Prefix for CSV and plot filenames.
        save_csv (bool): Whether to save CSV files.
        plot (bool): Whether to generate plots.
        round_decimals (int): Number of decimals to round in CSV.
        
    Returns:
        dict: Dictionary with combined DataFrames for nodes and links.
    """
    import pandas as pd
    import matplotlib.pyplot as plt
    from pyswmm import Output

    # get simulation name from the out_file path
    sim_name = out_file.split("\\")[-1].split(".")[0]

    # create output directory if it doesn't exist
    import os
    project_output_dir = f"{output_dir}/{project_name}"
    os.makedirs(project_output_dir, exist_ok=True)

    # Initialize data structure
    data = {
        "nodes": {nid: {param: {} for param in node_params} for nid in node_ids},
        "links": {lid: {param: {} for param in link_params} for lid in link_ids}
    }

    # Extract data from the .out file
    with Output(out_file) as out:
        for nid in node_ids:
            for param in node_params:
                ts = out.node_series(nid, param)
                for timestamp in ts:
                    data["nodes"][nid][param][timestamp] = ts[timestamp]

        for lid in link_ids:
            for param in link_params:
                ts = out.link_series(lid, param)
                for timestamp in ts:
                    data["links"][lid][param][timestamp] = ts[timestamp]

    # Flatten node data: each node gets its own DataFrame with columns ["time", "id", param]
    node_dfs = {}
    for nid in node_ids:
        for param in node_params:
            ts = data["nodes"][nid][param]
            df = pd.DataFrame(list(ts.items()), columns=["time", param])
            df["id"] = nid  # Add node ID column
            node_dfs[(nid, param)] = df

    # Flatten link data: each link gets its own DataFrame with columns ["time", "id", param]
    link_dfs = {}
    for lid in link_ids:
        for param in link_params:
            ts = data["links"][lid][param]
            df = pd.DataFrame(list(ts.items()), columns=["time", param])
            df["id"] = lid  # Add link ID column
            link_dfs[(lid, param)] = df


    # %%
    # Combine node and link DataFrames
    df_nodes_combined = pd.concat(node_dfs.values(), axis=0, ignore_index=True)
    df_links_combined = pd.concat(link_dfs.values(), axis=0, ignore_index=True)
    # Optional: reorder columns for clarity (put 'id' first)
    df_nodes_combined = df_nodes_combined[["id", "time"] + node_params]
    df_links_combined = df_links_combined[["id", "time"] + link_params]
    # round values to specified decimal places
    df_nodes_combined = df_nodes_combined.round(round_decimals)
    df_links_combined = df_links_combined.round(round_decimals)

    # Save to CSV files
    if save_csv:
        df_nodes_combined.to_csv(f"{output_dir}/{project_name}/{sim_name} - nodes data.csv", index=False)
        df_links_combined.to_csv(f"{output_dir}/{project_name}/{sim_name} - links data.csv", index=False)

    # Plotting for all nodes, one plot per parameter
    if plot:
        for param in node_params:
            plt.figure(figsize=(12, 6))
            for nid in node_ids:
                df = node_dfs[(nid, param)]
                plt.plot(df["time"], df[param], label=f"Node {nid} {param.replace('_', ' ').title()}")
            plt.xlabel("Time")
            plt.ylabel(param.replace('_', ' ').title())
            plt.title(f"{param.replace('_', ' ').title()} at Nodes Over Time")
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(f"{output_dir}/{project_name}/{sim_name} - nodes {param} plot.png")
            plt.close()
        for param in link_params:
            plt.figure(figsize=(12, 6))
            for lid in link_ids:
                df = link_dfs[(lid, param)]
                plt.plot(df["time"], df[param], label=f"Link {lid} {param.replace('_', ' ').title()}")
            plt.xlabel("Time")
            plt.ylabel(param.replace('_', ' ').title())
            plt.title(f"{param.replace('_', ' ').title()} at Links Over Time")
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(f"{output_dir}/{project_name}/{sim_name} - links {param} plot.png")
            plt.close()

    return {
        "node_dfs": node_dfs,
        "link_dfs": link_dfs,
        "df_nodes_combined": df_nodes_combined,
        "df_links_combined": df_links_combined
    }
# %%
if __name__ == "__main__":
    # Example usage
    project_name = "DFW Terminal F Design Build"

    # Path to the .out file
    out_file = r"\\garverinc.local\gdata\Projects\2022\22A28803 - DFW Terminal F Design Build\Quality Program\QAQC\Reviews\95% EPASWMM  MODEL\Proposed_RE_EC_25yr_v3.out"

    # Node and link IDs
    node_ids = ["BC-BB-F3-18900", "BC-BB-F3-18890"]
    link_ids = ["BC-BB-F3-18100-0101", "BC-BB-F3-17300-0101", "BC-BB-F3-18900", "BC-BB-F3-18890S"]

    # Parameters to extract
    node_params = ["head", "total_inflow"]
    link_params = ["flow"]



    extract_swmm_timeseries(
        out_file,
        node_ids,
        link_ids,
        node_params,
        link_params,
        project_name,
        output_dir="output",
        save_csv=True,
        plot=True,
        round_decimals=6,
    )


# %%
