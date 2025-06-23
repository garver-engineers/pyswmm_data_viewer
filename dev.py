# %%
from pyswmm import Simulation, Nodes, Links
import matplotlib.pyplot as plt

# %%
inp_path = r"\\garverinc.local\gdata\Projects\2022\22A28803 - DFW Terminal F Design Build\Quality Program\QAQC\Reviews\95% EPASWMM  MODEL\Proposed_RE_EC_25yr_v3.inp"

# List of node IDs (Head in ft and Total Inflow in CFS)
node_ids = [
    "BC-BB-F3-18900",
    "BC-BB-F3-18890"
]

# List of link IDs (Flow in CFS)
link_ids = [
    "BC-BB-F3-18100-0101",
    "BC-BB-F3-17300-0101",
    "BC-BB-F3-18900",
    "BC-BB-F3-18890S"
]

# Node Attribute Reference:
# -------------------------
# Attribute           Description
# ---------           ------------------------------------------
# nodeid              Node ID
# depth               Water depth at the node
# head                Hydraulic head at the node
# volume              Water volume stored at the node
# total_inflow        Total inflow into the node
# overflow            Overflow rate from the node
# lat_flow            Lateral inflow rate
# invert_elevation    Elevation of the node invert


# parameters to extract
node_params = [
    "head",
    "total_inflow"
]
link_params = [
    "flow"
]


# initialize stor data structure which will look like:
"""
{
    "nodes": {
        "BC-BB-F3-18900": {
            "head": [...],
            "total_inflow": [...],
            "time": [...]
        },
        "BC-BB-F3-18890": {
            "head": [...],
            "total_inflow": [...],
            "time": [...]
        }
    },
    "links": {
        "BC-BB-F3-18100-0101": {
            "flow": [...],
            "time": [...]
        },
        "BC-BB-F3-17300-0101": {
            "flow": [...],
            "time": [...]
        },
        "BC-BB-F3-18900": {
            "flow": [...],
            "time": [...]
        },
        "BC-BB-F3-18890S": {
            "flow": [...],
            "time": [...]
        }
    }
}
"""
data_dict = {"nodes": {}, "links": {}}


# %%
# with Simulation(inp_path) as sim:
#     for node_id in node_ids:
#         # Access the node by its ID
#         node = Nodes(sim)[node_id]
#         # Lists to store param data
#         for param in node_params:
#             data_dict["nodes"].setdefault(node_id, {}).setdefault(param.lower(), [])
#             # Store the time for each step
#             data_dict["nodes"][node_id].setdefault("time", [])
#             for step in sim:
#                 data_dict["nodes"][node_id][param.lower()].append(getattr(node, param))
#                 data_dict["nodes"][node_id]["time"].append(sim.current_time)
#     for link_id in link_ids:
#         # Access the link by its ID
#         link = Nodes(sim)[link_id]
#         # Lists to store param data
#         for param in link_params:
#             data_dict["links"].setdefault(link_id, {}).setdefault(param.lower(), [])
#             # Store the time for each step
#             data_dict["links"][link_id].setdefault("time", [])
#             for step in sim:
#                 data_dict["links"][link_id][param.lower()].append(getattr(link, param))
#                 data_dict["links"][link_id]["time"].append(sim.current_time)

# %%
with Simulation(inp_path) as sim:
    nodes = Nodes(sim)
    links = Links(sim)

    # Initialize data structures
    for node_id in node_ids:
        for param in node_params:
            data_dict["nodes"].setdefault(node_id, {}).setdefault(param, [])
        data_dict["nodes"][node_id].setdefault("time", [])

    for link_id in link_ids:
        for param in link_params:
            data_dict["links"].setdefault(link_id, {}).setdefault(param, [])
        data_dict["links"][link_id].setdefault("time", [])

    # Step through the simulation once
    for step in sim:
        current_time = sim.current_time

        for node_id in node_ids:
            node = nodes[node_id]
            data_dict["nodes"][node_id]["time"].append(current_time)
            for param in node_params:
                data_dict["nodes"][node_id][param].append(getattr(node, param))

        for link_id in link_ids:
            link = links[link_id]
            data_dict["links"][link_id]["time"].append(current_time)
            for param in link_params:
                data_dict["links"][link_id][param].append(getattr(link, param))

            
# %%
data_dict

# %%
# convert dict to a pandas dataframe
import pandas as pd
nodes_df = pd.DataFrame.from_dict(
    {node_id: data_dict["nodes"][node_id] for node_id in node_ids},
    orient='index'
)
links_df = pd.DataFrame.from_dict(
    {link_id: data_dict["links"][link_id] for link_id in link_ids},
    orient='index'
)

#%%
links_df.head()

# %%
# plot the first node head and total inflow
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(nodes_df["time"].iloc[0], nodes_df["head"].iloc[0], label=node_ids[0])
plt.title(f"Node {node_ids[0]} Head Over Time")
plt.xlabel("Time")
plt.ylabel("Head (ft)")
plt.legend()
plt.subplot(2, 1, 2)
plt.plot(nodes_df["time"].iloc[0], nodes_df["total_inflow"].iloc[0], label=node_ids[0])
plt.title(f"Node {node_ids[0]} Total Inflow Over Time")
plt.xlabel("Time")
plt.ylabel("Total Inflow (CFS)")
plt.legend()
plt.tight_layout()
plt.show()

# %%
# export nodes_df and links_df to csv
nodes_df.to_csv("nodes_data.csv", index=False)
links_df.to_csv("links_data.csv", index=False)
# %%
