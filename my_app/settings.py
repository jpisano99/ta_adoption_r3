from datetime import datetime
from my_app.my_secrets import passwords
import os


def init_settings():
    # Grab the production file date label
    # Add these filenames to the app_cfg settings dict
    print('running init settings')
    path_to_main_dir = (os.path.join(app_cfg['HOME'], app_cfg['WORKING_DIR']))
    path_to_update_dir = (os.path.join(app_cfg['HOME'], app_cfg['WORKING_DIR'], app_cfg['UPDATES_DIR']))

    main_files = os.listdir(path_to_main_dir)
    update_files = os.listdir(path_to_update_dir)

    prod_date = [file[-13:-13 + 8] for file in main_files if file.find('Master Bookings') != -1]
    update_date = [file[-13:-13 + 8] for file in update_files if file.find('Master Bookings') != -1]
    if len(update_date) == 0:
        print("No Updates Found")
        update_date.append('None Found')

    prod_date = update_date
    # if len(prod_date) == 0:
    #     print("No Production Files Found")
    #     prod_date.append('No Production Files Found')

    app_cfg['PROD_DATE'] = prod_date[0]
    app_cfg['UPDATE_DATE'] = update_date[0]
    app_cfg['XLS_RENEWALS'] = 'TA Master Renewals as of ' + app_cfg['PROD_DATE'] + '.xlsx'
    app_cfg['XLS_BOOKINGS'] = 'tmp_Master Bookings as of ' + app_cfg['PROD_DATE'] + '.xlsx'
    app_cfg['XLS_CUSTOMER'] = 'tmp_TA Customer List ' + app_cfg['PROD_DATE'] + '.xlsx'
    app_cfg['XLS_ORDER_DETAIL'] = 'tmp_TA Order Details ' + app_cfg['PROD_DATE'] + '.xlsx'
    app_cfg['XLS_ORDER_SUMMARY'] = 'tmp_TA Scrubbed Orders ' + app_cfg['PROD_DATE'] + '.xlsx'
    app_cfg['XLS_BOOKINGS_TRASH'] = 'tmp_Bookings Trash ' + app_cfg['PROD_DATE'] + '.xlsx'
    app_cfg['XLS_DASHBOARD'] = 'tmp_TA Unified Adoption Dashboard ' + app_cfg['PROD_DATE'] + '.xlsx'

    print("prod date", app_cfg['PROD_DATE'])
    print('update date', app_cfg['UPDATE_DATE'])
    return


# database configuration settings
database = dict(
    DATABASE="cust_ref_db",
    USER="root",
    PASSWORD=passwords["DB_PASSWORD"],
    HOST="localhost"
)

# Smart sheet Config settings
ss_token = dict(
    SS_TOKEN=passwords["SS_TOKEN"]
)

# application predefined constants
app_cfg = dict(
    VERSION=1.0,
    GITHUB="{url}",
    HOME=os.path.expanduser("~"),
    WORKING_DIR='ta_adoption_data',
    UPDATES_DIR='ta_data_updates',
    ARCHIVES_DIR='archives',
    PROD_DATE='',
    UPDATE_DATE='',
    XLS_RENEWALS='',
    XLS_BOOKINGS='',
    XLS_CUSTOMER='',
    XLS_ORDER_DETAIL='',
    XLS_ORDER_SUMMARY='',
    XLS_BOOKINGS_TRASH='',
    XLS_DASHBOARD='tmp_TA Unified Adoption Dashboard ',
    SS_SAAS='SaaS customer tracking',
    SS_CX='CX Tetration Customer Comments v3.0',
    # SS_CX='Tetration Engaged Customer Report',
    SS_AS='Tetration Shipping Notification & Invoicing Status',
    SS_COVERAGE='Tetration Coverage Map',
    SS_SKU='Tetration SKUs',
    SS_CUSTOMERS='TA Customer List',
    SS_DASHBOARD='TA Unified Adoption Dashboard',
    SS_WORKSPACE='Tetration Customer Adoption Workspace',
    AS_OF_DATE=datetime.now().strftime('_as_of_%m_%d_%Y')
)

init_settings()


