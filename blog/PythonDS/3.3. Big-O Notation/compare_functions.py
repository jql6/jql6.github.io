# compare_functions.py

from timeit import default_timer as timer
import random
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


from find_min_n import find_min_n
from find_min_n2 import find_min_n2
import csv


def generate_execution_time_csv():
    # Make the same list of random numbers every time
    random.seed(a=100)

    # Create a list of random numbers
    list1 = list(map(lambda x: random.uniform(0, 1), list(range(0, 100000))))
    print(f"Length of list1: {len(list1)}")

    length_of_number_list = [10, 100, 1000, 10000, 100000]
    functions = [find_min_n, find_min_n2]

    dict1 = {
        "length_of_number_list": [],
        "function": [],
        "execution_time": [],
        "minimum_number": [],
    }

    for n in length_of_number_list:
        for func in functions:
            # Get the execution times of the functions
            start_time = timer()
            # Get the minimum number from the number list slice from 0 to n
            min = func(list1[0:n])
            end_time = timer()
            execution_time = end_time - start_time
            # Add values to dictionary
            dict1["length_of_number_list"].append(n)
            dict1["function"].append(func.__name__)
            dict1["execution_time"].append(execution_time)
            dict1["minimum_number"].append(min)

    # Convert dictionary into dataframe
    df1 = pd.DataFrame(dict1)

    df1.to_csv("execution_time.csv", index=False)


# Try loading the data
try:
    df1 = pd.read_csv("execution_time.csv")
# If the data doesn't exist, make it and then load it
except:
    generate_execution_time_csv()
    df1 = pd.read_csv("execution_time.csv")

### print(df1)

# Make plots
# x-axis: length_of_number_list
# y-axis: execution_time
# legend/color: function
plot1 = sns.lineplot(
    data=df1,
    x="length_of_number_list",
    y="execution_time",
    hue="function",
    style="function",
    marker=True,
)
# Use log 10 scale on x-axis
plot1.set(xscale="log")
plot1.set(xlabel="length of number list", ylabel="execution time (seconds)")
# Save plot
plot1.get_figure().savefig("execution_time.png", dpi=300)
