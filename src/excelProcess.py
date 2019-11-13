import xlrd
import xlsxwriter

# Reading from input
locData = 'C:/Users/RedLine/Desktop/Semester 8/FYP/FYP_2/FYP_01/data/Book1.xlsx'

open_wb = xlrd.open_workbook(locData)
sheet = open_wb.sheet_by_index(0)

workbook = xlsxwriter.Workbook('../data/format1.xlsx')
worksheet = workbook.add_worksheet()
locFormat = 'C:/Users/RedLine/Desktop/Semester 8/FYP/FYP_2/FYP_01/data/format1.xlsx'

count = 0

for i in range(sheet.nrows):
    for j in range(sheet.ncols):
        prefix = sheet.cell_value(0, j)
        newText = sheet.cell_value(i, j)
        if newText and i != 0:
            worksheet.write(i, j, prefix + ':' + newText.lower())
            count+=1

workbook.close()

open_wb = xlrd.open_workbook(locFormat)
sheet1 = open_wb.sheet_by_index(0)

print(count)