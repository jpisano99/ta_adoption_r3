from my_app.settings import app_cfg, init_settings
from my_app.func_lib.open_wb import open_wb
from my_app.func_lib.push_list_to_xls import push_list_to_xls
from my_app.func_lib.build_sku_dict import build_sku_dict
import os


def refresh_data():
    # This function retrieves data from the update_dir
    # It looks for a file(s) in the format of:
    #   'FY17 TA Master Bookings as of 02-25-19.xlsx'
    #   'TA Renewal Dates as of 02-25-19.xlsx'
    # It will prep them and then place them in the working_dir
    # It will also take the previously used working files and move them to the archive_dir

    home = app_cfg['HOME']
    working_dir = app_cfg['WORKING_DIR']
    update_dir = app_cfg['UPDATES_DIR']
    archive_dir = app_cfg['ARCHIVES_DIR']

    path_to_main_dir = (os.path.join(home, working_dir))
    path_to_updates = (os.path.join(home, working_dir, update_dir))
    path_to_archives = (os.path.join(home, working_dir, archive_dir))

    update_files = os.listdir(path_to_updates)
    bookings = []
    start_row = 0
    as_of_date = ''

    # Look in the "ta_data_updates" dir
    # this is where we place newly updated sheets to be put into production
    if len(update_files) == 0:
        # NO update files exist so throw an error ?
        print('ERROR: No Update files exist in:', path_to_updates)
        exit()
    else:
        for file in update_files:
            # When we find a "Master Bookings" file
            # Add the rows to the "bookings" list
            if file.find('Master Bookings') != -1:
                wb, ws = open_wb(file, 'updates')
                as_of_date = file[-13:-13+8]

                if start_row == 0:
                    # For the first workbook include the header row
                    start_row = 2
                elif start_row == 2:
                    # For subsequent workbooks skip the header
                    start_row = 3

                for row in range(start_row, ws.nrows):
                    bookings.append(ws.row_values(row))

    # Look in the main working directory for current production files
    # and move to a dated archive folder in the 'archives' directory

    # Get the as_of_date from the current production files
    # so we can create the properly named archive folder
    main_files = os.listdir(path_to_main_dir)
    archive_date = ''
    for file in main_files:
        if file.find('Master Bookings') != -1:
            archive_date = file[-13:-13 + 8]

    # Make the archive directory we need
    os.mkdir(os.path.join(path_to_archives, archive_date+" Updates"))
    archive_folder_path = os.path.join(path_to_archives, archive_date+" Updates")

    for file in main_files:
        if file.find('Master Bookings') != -1:
            os.rename(os.path.join(path_to_main_dir, file), os.path.join(archive_folder_path, file))
        elif file.find('Renewal') != -1:
            os.rename(os.path.join(path_to_main_dir, file), os.path.join(archive_folder_path, file))
        elif file.find('AS SKUs') != -1:
            os.rename(os.path.join(path_to_main_dir, file), os.path.join(archive_folder_path, file))

    # We have now created the bookings list lets write it
    print('New Master Bookings has ', len(bookings), ' line items')
    push_list_to_xls(bookings, 'TA Master Bookings as of ')

    # Move the Renewals file into production from updates director
    renewal_file = 'TA Renewal Dates as of '+as_of_date+'.xlsx'
    os.rename(os.path.join(path_to_updates, renewal_file), os.path.join(path_to_main_dir, renewal_file))

    print('All data files have been refreshed and archived !')
    return


def get_as_skus():
    init_settings()
    print('is this right', app_cfg['PROD_DATE'])

    tmp_dict = build_sku_dict()
    sku_dict = {}
    wb, ws = open_wb(app_cfg['XLS_BOOKINGS'])
    header_row = ws.row_values(0)

    for sku_key, sku_val in tmp_dict.items():
        if sku_val[0] == 'Service':
            sku_dict[sku_key] = sku_val

    sku_col_header = 'Bundle Product ID'
    sku_col_num = 0
    as_skus = [header_row]

    # Get the col number that has the SKU's
    for col in range(ws.ncols):
        if ws.cell_value(0, col) == sku_col_header:
            sku_col_num = col
            break

    # Gather all the rows with AS skus
    for row in range(1, ws.nrows):
        if ws.cell_value(row, sku_col_num) in sku_dict:
            as_skus.append(ws.row_values(row))

    push_list_to_xls(as_skus, 'TA AS SKUs as of ')

    print('All AS SKUs have been extracted from the current data!')
    return
