import pandas as pd
sheet1 = "in.xlsx" 
sheet2 = "out.xlsx" 
df = pd.read_excel(sheet1)

df.to_excel(sheet2, index=False)

print(f"\nData copied to '{sheet2}'")
df2=pd.read_excel(sheet2)
print(f"reading data from '{sheet2}':\n {df2}")

