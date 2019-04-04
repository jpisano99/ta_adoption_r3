import xlsxwriter
import datetime
import os
from my_app.settings import app_cfg


def push_list_to_xls(my_list, xls_file, dir_to_push='working'):
    # def push_list_to_xls(my_list, xls_file, xls_time=app_cfg['PROD_DATE']):
    #
    # Get settings for file locations and names
    #

    home = app_cfg['HOME']
    # working_dir = app_cfg['WORKING_DIR']
    # path_to_files = os.path.join(home, working_dir)

    working_dir = app_cfg['WORKING_DIR']
    path_to_files = ''
    if dir_to_push == 'working':
        path_to_files = os.path.join(home, working_dir)
    elif dir_to_push == 'updates':
        update_dir = app_cfg['UPDATES_DIR']
        path_to_files = os.path.join(home,  working_dir, update_dir)

    wb_file = os.path.join(path_to_files, xls_file)
    # wb_file = os.path.join(path_to_files, xls_file + xls_time + '.xlsx')
    print(wb_file)
    #
    # Write the Excel File
    #
    workbook = xlsxwriter.Workbook(wb_file)
    worksheet = workbook.add_worksheet()

    # cell_format = workbook.add_format()
    # cell_format.set_bold()
    # cell_format.set_bg_color('#B7FFF9')
    #
    # cell_format.set_bg_color('#B7D9FF')
    # cell_format.set_bg_color('#FFFEB7')
    # # cell_format.set_font_color('red')

    xls_money = workbook.add_format({'num_format': '$#,##0'})
    xls_date = workbook.add_format({'num_format': 'mm / dd/ yyyy'})

    for row_num, my_row in enumerate(my_list):
        for col_num, cell_val in enumerate(my_row):
            if type(cell_val) is float:
                worksheet.write(row_num, col_num, cell_val, xls_money)
            elif isinstance(cell_val, datetime.datetime):
                worksheet.write(row_num, col_num, cell_val, xls_date)
            else:
                # worksheet.write(row_num, col_num, cell_val, cell_format)
                worksheet.write(row_num, col_num, cell_val)

    workbook.close()

    return
