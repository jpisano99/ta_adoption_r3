from my_app.settings import app_cfg, init_settings
from my_app.func_lib.open_wb import open_wb
from my_app.func_lib.push_list_to_xls import push_list_to_xls
from my_app.func_lib.build_sku_dict import build_sku_dict
import os
from shutil import copyfile


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

    print(path_to_main_dir)
    print(path_to_updates)
    print(path_to_archives)
    print(app_cfg['PROD_DATE'])
    print(app_cfg['UPDATE_DATE'])

    # Look in the "ta_data_updates" dir
    # this is where we place newly updated sheets to be put into production
    if len(update_files) == 0:
        # NO update files exist so throw an error ?
        print('ERROR: No Update files exist in:', path_to_updates)
        return
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

    # We have now created the bookings list lets write it
    # and rename it to the current as_of_date
    print('New Master Bookings has ', len(bookings), ' line items')
    push_list_to_xls(bookings, 'tmp_working_bookings', 'updates')
    os.rename(os.path.join(path_to_updates, 'tmp_working_bookings'),
              os.path.join(path_to_updates, 'tmp_Master Bookings as of '+as_of_date+'.xlsx'))

    # Create a workbook of filtered AS SKUs only
    as_bookings = get_as_skus(bookings)
    push_list_to_xls(as_bookings, 'tmp_working_as_bookings', 'updates')
    os.rename(os.path.join(path_to_updates, 'tmp_working_as_bookings'),
              os.path.join(path_to_updates, 'tmp_TA AS SKUs as of '+as_of_date+'.xlsx'))

    # Make an archive directory we need to place these update files
    os.mkdir(os.path.join(path_to_archives, as_of_date+" Updates"))
    archive_folder_path = os.path.join(path_to_archives, as_of_date+" Updates")
    print(archive_folder_path)

    # Move a copy to the working directory also
    main_files = os.listdir(path_to_updates)
    for file in main_files:
        copyfile(os.path.join(path_to_updates, file), os.path.join(path_to_main_dir, file))

    # Move the updates to the archive directory
    main_files = os.listdir(path_to_updates)
    for file in main_files:
        print(file)
        os.rename(os.path.join(path_to_updates, file), os.path.join(archive_folder_path, file))
    exit()

    # Move the Renewals file into production from updates director
    renewal_file = 'TA Renewal Dates as of '+as_of_date+'.xlsx'
    os.rename(os.path.join(path_to_updates, renewal_file), os.path.join(path_to_main_dir, renewal_file))

    print('All data files have been refreshed and archived !')

    exit()





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






    # Move the Renewals file into production from updates director
    renewal_file = 'TA Renewal Dates as of '+as_of_date+'.xlsx'
    os.rename(os.path.join(path_to_updates, renewal_file), os.path.join(path_to_main_dir, renewal_file))

    print('All data files have been refreshed and archived !')
    return


def get_as_skus(bookings):
    # Build a SKU dict as a filter
    tmp_dict = build_sku_dict()
    sku_dict = {}
    header_row = bookings[0]

    # Strip out all but Service sku's
    for sku_key, sku_val in tmp_dict.items():
        if sku_val[0] == 'Service':
            sku_dict[sku_key] = sku_val

    sku_col_header = 'Bundle Product ID'
    sku_col_num = 0
    as_bookings = [header_row]

    # Get the col number that has the SKU's
    for idx, val in enumerate(header_row):
        if val == sku_col_header:
            sku_col_num = idx
            break

    # Gather all the rows with AS skus
    for booking in bookings:
        if booking[sku_col_num] in sku_dict:
            as_bookings.append(booking)

    print('All AS SKUs have been extracted from the current data!')
    return as_bookings


if __name__ == "__main__" and __package__ is None:
    print(__package__)
    print('running process bookings')
    refresh_data()
    print('Extracting AS SKUs')


