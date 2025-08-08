import pandas as pd
from sk.learn.model_selection import train_test_split

#================DATA SELECTION ============================#

data = pd.read_csv("ratings_csv")
print(data.head(10))
print()

data_label = data["rating"]