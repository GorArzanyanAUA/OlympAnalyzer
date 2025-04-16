import os
import pandas as pd
import json

from utils import calculate_statistics

# Example usage
data_csv_base = "/home/student/Desktop/Statistics Project/data/data_csv"
statistics = calculate_statistics(data_csv_base)
print(statistics)
