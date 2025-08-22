from smellscapy.surveys import validate
from smellscapy.databases.DataExample import load_example_data
import pandas as pd
from importlib import resources
from smellscapy.calculations import calculate_pleasantness, calculate_presence
from smellscapy.plotting.scatter import plot_scatter
from smellscapy.plotting.simple_density import plot_50percentile
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


plot_scatter(df, xlim=(-1, 1), ylim=(-1, 1))

plot_joint(df, xlim=(-1, 1), ylim=(-1, 1))

plot_50percentile(df, xlim=(-1, 1), ylim=(-1, 1))
    
print(df)

pass