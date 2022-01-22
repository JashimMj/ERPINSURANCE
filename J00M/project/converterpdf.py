from pdf2docx import Converter
pdf_with_path='D:\myproject\J00M\project\Marine Tariff.pdf'
docx_with_path='demo.docx'
cv=Converter(pdf_with_path)
cv.convert(docx_with_path,start=0, end=5)
cv.close()