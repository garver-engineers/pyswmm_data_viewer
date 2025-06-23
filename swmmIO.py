from pyswmm import Output
from swmm.toolkit.shared_enum import NodeAttribute
import matplotlib.pyplot as plt


#  -------------- Input Variables --------------

# Path to the .out file
out_file = r"\\garverinc.local\gdata\Projects\2022\22A28803 - DFW Terminal F Design Build\Quality Program\QAQC\Reviews\95% EPASWMM  MODEL\Proposed_RE_EC_25yr_v3.out"

# Node and link IDs
node_ids = ["BC-BB-F3-18900", "BC-BB-F3-18890"]
link_ids = ["BC-BB-F3-18100-0101", "BC-BB-F3-17300-0101", "BC-BB-F3-18900", "BC-BB-F3-18890S"]

# Parameters to extract
node_params = ["head", "total_inflow"]
link_params = ["flow"]

# ---------------------------------------------


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

#     ts = out.node_series("BC-BB-F3-18900", "total_inflow")
#     for index in ts:
#         print(index, ts[index])

# Now `data` is a dictionary with time-stamped values for each parameter


# Convert to DataFrame for easier manipulation (optional)
import pandas as pd
# Flatten node data: each node gets its own DataFrame with columns ["time", param]
node_dfs = {}
for nid in node_ids:
    for param in node_params:
        ts = data["nodes"][nid][param]
        df = pd.DataFrame(list(ts.items()), columns=["time", param])
        node_dfs[(nid, param)] = df

# Flatten link data: each link gets its own DataFrame with columns ["time", param]
link_dfs = {}
for lid in link_ids:
    for param in link_params:
        ts = data["links"][lid][param]
        df = pd.DataFrame(list(ts.items()), columns=["time", param])
        link_dfs[(lid, param)] = df

# Example: get DataFrame for a specific node and parameter
df_nodes = node_dfs[(node_ids[0], node_params[0])]  # e.g., first node, first param
df_links = link_dfs[(link_ids[0], link_params[0])]  # 
print("Node Data:") # e.g., first link, first param
# Print the first few rows of the DataFrame
print(df_nodes.head())
print("\nLink Data:")
print(df_links.head())

# # # Plotting for all nodes, one plot per parameter
# Plotting for all nodes, one plot per parameter
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
    plt.savefig(f"node_{param}_plot.png")
    plt.close()
# Plotting for all links, one plot per parameter
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
    plt.savefig(f"link_{param}_plot.png")
    plt.close()

# Save the data to CSV files one for nodes and one for links. paramters should be combined as added columns 
df_nodes_combined = pd.concat(node_dfs.values(), axis=1)
df_links_combined = pd.concat(link_dfs.values(), axis=1)
# drop duplicate columns
df_nodes_combined = df_nodes_combined.loc[:, ~df_nodes_combined.columns.duplicated()]
df_links_combined = df_links_combined.loc[:, ~df_links_combined.columns.duplicated()]
# round values to 6 decimal places
df_nodes_combined = df_nodes_combined.round(6)
# Save to CSV files
df_nodes_combined.to_csv("nodes_data.csv", index=False)
df_links_combined.to_csv("links_data.csv", index=False)


