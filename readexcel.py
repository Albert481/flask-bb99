import xlrd

wb = xlrd.open_workbook("99th Coy Nominal Roll.xlsx")
worksheet = wb.sheet_by_index(0)

total_rows = worksheet.nrows
total_cols = worksheet.ncols

table = list()
record = list()

for i in range(total_rows):
    for j in range(total_cols):
        record.append(worksheet.cell(i, j).value)
    table.append(record)
    record = []
    i += 1

print(table)