import pdfplumber
import pandas as pd

pdf_path = "input2.pdf"
output_excel = "output2.xlsx"

writer = pd.ExcelWriter(output_excel, engine="openpyxl")

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        table = page.extract_table()

        df = pd.DataFrame(table[1:], columns=table[0])
        df.to_excel(writer)

writer.close()
print(f"table saved to '{output_excel}'")
