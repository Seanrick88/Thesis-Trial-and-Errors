import pandas as pd

csv1 = pd.read_csv("testdata.csv")
csv2 = pd.read_csv("traindata.csv")

merged = pd.concat([csv1,csv2], ignore_index=True)

merged.to_csv("merged_file.csv", index = False)

print("CSV file successfully merged")

