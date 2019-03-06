from datetime import datetime
from app.my_secrets import passwords
import os


def init_settings():
    # Grab the production file date label
    # Add these filenames to the app settings dict
    print('running init settings')
    path_to_main_dir = (os.path.join(app['HOME'], app['WORKING_DIR']))
    path_to_update_dir = (os.path.join(app['HOME'], app['WORKING_DIR'], app['UPDATES_DIR']))

    main_files = os.listdir(path_to_main_dir)
    update_files = os.listdir(path_to_update_dir)

    prod_date = [file[-13:-13 + 8] for file in main_files if file.find('Master Bookings') != -1]
    update_date = [file[-13:-13 + 8] for file in update_files if file.find('Master Bookings') != -1]

    app['PROD_DATE'] = prod_date[0]
    app['UPDATE_DATE'] = update_date[0]
    app['XLS_RENEWALS'] = 'TA Renewal Dates as of ' + app['PROD_DATE'] + '.xlsx'
    app['XLS_BOOKINGS'] = 'TA Master Bookings as of ' + app['PROD_DATE'] + '.xlsx'
    app['XLS_CUSTOMER'] = 'tmp_TA Customer List ' + app['PROD_DATE'] + '.xlsx'
    app['XLS_ORDER_DETAIL'] = 'tmp_TA Order Details ' + app['PROD_DATE'] + '.xlsx'
    app['XLS_ORDER_SUMMARY'] = 'tmp_TA Scrubbed Orders ' + app['PROD_DATE'] + '.xlsx'
    app['XLS_BOOKINGS_TRASH'] = 'tmp Bookings Trash ' + app['PROD_DATE'] + '.xlsx'
    app['XLS_DASHBOARD'] = 'tmp_TA Unified Adoption Dashboard ' + app['PROD_DATE'] + '.xlsx'

    print("prod date", app['PROD_DATE'])
    print('update date', app['UPDATE_DATE'])
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
app = dict(
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
    SS_CX='Tetration Engaged Customer Report',
    SS_AS='Tetration Shipping Notification & Invoicing Status',
    SS_COVERAGE='Tetration Coverage Map',
    SS_SKU='Tetration SKUs',
    SS_CUSTOMERS='TA Customer List',
    SS_DASHBOARD='TA Unified Adoption Dashboard',
    SS_WORKSPACE='Tetration Customer Adoption Workspace',
    AS_OF_DATE=datetime.now().strftime('_as_of_%m_%d_%Y')
)

init_settings()


