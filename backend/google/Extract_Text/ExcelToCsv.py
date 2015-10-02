__author__ = 'tanmoy'

import xlrd
import csv
import os
import sys

def csv_from_excel(excel_file):
    workbook = xlrd.open_workbook(excel_file)
    all_worksheets = workbook.sheet_names()
    file_name = os.path.basename(excel_file)
    csv_file = open(''.join([file_name.split('.')[0],'.csv']), 'wb')
    csv_file_name = ''.join([file_name.split('.')[0],'.csv'])
    for worksheet_name in all_worksheets:
        worksheet = workbook.sheet_by_name(worksheet_name)
        wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
        wr.writerow([unicode(worksheet_name).encode("utf-8")])
        for rownum in xrange(worksheet.nrows):
            wr.writerow([unicode(entry).encode("utf-8") for entry in worksheet.row_values(rownum)])
    csv_file.close()
    return csv_file_name


if __name__ == "__main__":
    path = raw_input("Enter path of excel file: ")
    csv_from_excel(path)

