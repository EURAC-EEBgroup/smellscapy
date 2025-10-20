from smellscapy.surveys import validate
from smellscapy.databases.DataExample import load_example_data
import pandas as pd
from importlib import resources
from smellscapy.calculations import calculate_pleasantness, calculate_presence
from smellscapy.plotting.scatter import plot_scatter
from smellscapy.plotting.simple_density import plot_simple_density
from smellscapy.plotting.density import plot_density


df = load_example_data()
df, excl_df = validate(df)


df = calculate_pleasantness(df)

df = calculate_presence(df)



print(df.columns)
#plot_scatter(df)

#plot_scatter(df, group_col = "Smell source")

#plot_simple_density(df, show_marginals = False)

#plot_simple_density(df, show_marginals = False, show_points = False)

#plot_simple_density(df)

#plot_simple_density(df, group_col = "Smell source",  palette="tab20")

#plot_simple_density(df, group_col = "Smell source",  show_points= False, palette="tab20")

plot_density(df, filled=True)

plot_density(df, group_col = "Smell source")



#print(df)

pass