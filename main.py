import pandas as pd
from xlsx2csv import Xlsx2csv
import os

files_folder = "C:\\Users\\dmitry.ershov\\OneDriveBS\\Desktop\\work\\Dev\\benefitscape\\Atlanta Public School\\APSData_2024\data"
files_read_count = 1
convert_hr_data_to_csv = False


def read_data():
    files = get_all_files_recursive(files_folder)
    hr_data = read_hr_data(files).astype(str)
    shbp = read_shbp(files).astype(str)
    move_file_basenames_to_first_column(hr_data, shbp)
    return hr_data, shbp


def move_file_basenames_to_first_column(hr_data, shbp):
    hr_data.insert(0, 'file_basename', hr_data.pop('file_basename'))
    shbp.insert(0, 'file_basename', shbp.pop('file_basename'))


def get_all_files_recursive(folder):
    files_dict = {
        'SHBP': [],
        'HRData': []
    }
    for root, dirs, file_list in os.walk(folder):
        for file in file_list:
            if 'SHBP' in file and file.endswith('.csv'):
                files_dict['SHBP'].append(os.path.join(root, file))
            if 'HRData' in file and file.endswith('.xlsx'):
                files_dict['HRData'].append(os.path.join(root, file))

    return files_dict


def read_hr_data(files):
    global files_read_count
    hr_data = pd.DataFrame()
    for file in files['HRData']:
        file = file.replace('.xlsx', '.csv')
        print(str(files_read_count) + ' - Reading file: ' + file)
        current_hr_data = pd.read_csv(file)
        add_file_basenames(current_hr_data, file)
        hr_data = pd.concat([hr_data, current_hr_data], ignore_index=True)
        files_read_count += 1
    return hr_data


def conver_xlsx_to_csv(files):
    for file in files:
        Xlsx2csv(file, outputencoding="utf-8").convert(file.replace('.xlsx', '.csv'))


def read_shbp(files):
    global files_read_count
    shbp = pd.DataFrame()
    for file in files['SHBP']:
        print(str(files_read_count) + ' - Reading file: ' + file)
        current_shbp = pd.read_csv(file)
        add_file_basenames(current_shbp, file)
        shbp = pd.concat([shbp, current_shbp], ignore_index=True)
        files_read_count += 1
    return shbp


def add_file_basenames(data, file):
    data['file_basename'] = file.split('\\')[-1]


def convert_HRData_to_csv():
    files = collect_files()
    conver_xlsx_to_csv(files)


if convert_hr_data_to_csv:
    convert_HRData_to_csv()


def collect_files():
    files = []
    for root, dirs, file_list in os.walk(files_folder):
        for file in file_list:
            if 'HRData' in file and file.endswith('.xlsx') and not is_already_converted_to_csv(file):
                files.append(os.path.join(root, file))
    print('Files to convert: ' + str(len(files)))
    return files


def is_already_converted_to_csv(file):
    return os.path.exists(file.replace('.xlsx', '.csv'))


def get_employee_by_id(hr_data, shbp_data, employee_id):
    ee_from_ht = hr_data[hr_data['Employee_ID'] == employee_id]
    ssn = ee_from_ht['SocialSecurityNumber'].values[0]
    ee_from_shbp = shbp_data[shbp_data['SHBP.1'] == ssn]
    return ee_from_ht, ee_from_shbp


hr_data, shbp_data = read_data()
employee_id = '136178'
ee_from_ht, ee_from_shbp = get_employee_by_id(hr_data, shbp_data, employee_id)
q = 0
