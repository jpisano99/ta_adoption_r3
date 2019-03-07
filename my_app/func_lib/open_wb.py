import xlrd
import os
from my_app.settings import app_cfg


def open_wb(excel_file, dir_to_open='working'):
    #
    # Get settings for file locations and names
    #
    home = app_cfg['HOME']
    working_dir = app_cfg['WORKING_DIR']
    path_to_files = ''
    if dir_to_open == 'working':
        path_to_files = os.path.join(home, working_dir)
    elif dir_to_open == 'updates':
        update_dir = app_cfg['UPDATES_DIR']
        path_to_files = os.path.join(home,  working_dir, update_dir)

    path_to_file = os.path.join(path_to_files, excel_file)
    print('OPENING>>>>>>>>>> ', path_to_file)

    #
    # Open up excel workbook
    #
    my_wb = xlrd.open_workbook(path_to_file)
    my_sheet = my_wb.sheet_by_index(0)

    return my_wb, my_sheet


if __name__ == "__main__":
    my_excel = open_wb(app_cfg['BOOKINGS'])
    print('We have: ', my_excel[0], my_excel[1])
