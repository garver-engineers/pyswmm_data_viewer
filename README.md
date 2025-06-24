# Main.py

Will run the SWMM Timeseries dataviewer as well as the Comparer. Each will out put plots and csv files

## SWMM Timeseries dataviewer
Give a list of links and nodes along with their respective parameters, and the .out file and let the script go to work

### Output
CSV data and plots of each parameter stacked
![node_total_inflow_plot](https://github.com/user-attachments/assets/16931946-ea1d-46be-8da6-3bcd36e42051)

![link_flow_plot](https://github.com/user-attachments/assets/2fabd797-e43d-49da-97a7-25f2ffdeca06)

## Comparer
Compares the results across multiple .out files processed by SWMM Timeseries dataviewer. 

### Output
Will output a csv file for each node and link with columns for the compariing simulations. Also output plots for each node and link to compare across the simulations. Output is found in the `output/comparisons/` directory

![image](https://github.com/user-attachments/assets/1b893d10-d2bd-4221-982d-b454e2ccc641)


![image](https://github.com/user-attachments/assets/c1db3567-2e4c-4e96-80cb-1ea17aec2427)


