from smellscapy.databases.DataExample import load_example_data_Eurac, load_example_data_Measure2_Unitn
from smellscapy.surveys import validate
from smellscapy.calculations import calculate_pleasantness, calculate_presence
import pandas as pd
from smellscapy.analysis.descriptive_analysis import descriptive_statistics
from smellscapy.plotting.simple_density import plot_simple_density
from smellscapy.plotting.dynamic import plot_dynamic
from smellscapy.analysis.descriptive_analysis import descriptive_statistics


df = load_example_data_Eurac()





print(df)



df,_ = validate(df)
df = calculate_pleasantness(df)
df = calculate_presence(df)

df = descriptive_statistics (df, group_by_col="Smell source")


#fig = plot_dynamic(df,
    #time_col="How long have you been in your office without leaving?",
    #group_by_col="Smell source",
    #frame_order=[
        #"Less than 3 minutes",
        #"3-30 minutes",
        #"31-60 minutes",
        #"61-120 minutes",
        #"More than 2 hours"
    #]
#)

#fig.write_html("docs/plot_dynamic_example.html", auto_open=False)

#fig.show()
