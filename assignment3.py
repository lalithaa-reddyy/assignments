import PyPDF2
from openpyxl import Workbook

class Reader:
    def __init__(self, file_path):
        self.file_path = file_path
    def extract_data(self):
        pass



class Writer:
    def __init__(self, file_path):
        self.file_path = file_path
        
    def write_data(self, data):
        pass

class PDFReader(Reader):
    def extract_data(self):
        with open(self.file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            page = reader.pages[0]
            text = page.extract_text() 
            return text

class ExcelWriter(Writer):
    def write_data(self, data):
        wb = Workbook()
        ws = wb.active
        ws.cell(row=1, column=1, value=data)

        wb.save(self.file_path)
        print(f"Data written to {self.file_path}")


if __name__ == "__main__":
    pdf_reader = PDFReader("input3.pdf")
    data_extrac = pdf_reader.extract_data()
    excel_writer = ExcelWriter("output3.xlsx")
    excel_writer.write_data(data_extrac)
