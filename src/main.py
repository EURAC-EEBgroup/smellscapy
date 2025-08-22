from smellscapy.surveys import validate
from smellscapy.databases.DataExample import load_example_data
import pandas as pd
from importlib import resources
from smellscapy.calculations import calculate_pleasantness, calculate_presence
from smellscapy.plotting.scatter import plot_scatter
from smellscapy.plotting.simple_density import plot_simple_density
from smellscapy.plotting.joint import plot_joint


df = load_example_data()
df, excl_df = validate(df)

# for i in range(6):
#     filename = f"DataExample copy {i}.csv"
#     data_resource = resources.files("smellscapy.data").joinpath(filename)
#     with resources.as_file(data_resource) as f:
#         df = pd.read_csv(f)
#     try:
#      df, excl_df = validate(df)
#     except Exception as e:
#        print(str(e))
#        print(filename)

# pass

calculate_pleasantness(df)

calculate_presence(df)


plot_scatter(df)

#plot_scatter(df, group_col = "LocationID")

plot_simple_density(df)

#plot_simple_density(df, group_col = "LocationID")

plot_joint(df)

#plot_joint(df, group_col = "How long have you been in your office without leaving? (e.g., since taking a break or going to the bathroom) ")
    
    
print(df)

pass