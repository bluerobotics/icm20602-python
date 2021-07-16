#!/usr/bin/python3

import argparse
from datetime import datetime
from fpdf import FPDF
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd

from llogger import LLogReader

WIDTH = 210
HEIGHT = 297

file_path = './tmp/'
if not os.path.exists(file_path):
    os.makedirs(file_path)

# TODO Can I put this into a function?
parser = argparse.ArgumentParser(description='icm20602 test report')
parser.add_argument('--input', action='store', type=str, required=True)
# parser.add_argument('--output', action='store', type=str, required=True)
args = parser.parse_args()


log = LLogReader(args.input)

# log.plot('measurement', ['gx', 'gy', 'gz'], ['ax', 'ay', 'az'])
# log.plot('measurement', ['ax', 'ay', 'az'], ['temperature'])
# log.plot('measurement', ['gx', 'gy', 'gz'], ['temperature'])
# log.plot('measurement', ['gx', 'gy', 'gz'], ['temperature'])
m = log.dataByName('measurement')

log.pplot(m['time'], m[['ax', 'gy']])
plt.show()
# data = pd.read_csv(args.input, header=None, sep=' ')
# data.rename(columns={0: "Timestamp", 1: "Log_Type"}, inplace=True)
# data['Timestamp'] = pd.to_datetime(data['Timestamp'], unit='s')
# print(data.head())

# measurements = pd.DataFrame(data=data.query('Log_Type == 1'))
# # TODO name raw columns
# measurements.rename(columns={2: "Ax", 3: "Ay", 4: "Az", 5: "Gx", 6: "Gy", 7: "Gz", 8: "T"}, inplace=True)

# configuration = pd.DataFrame(data=data.query('Log_Type == 2'))
# configuration.rename(columns={2: 'FSRa', 3: 'FSRg', 4: "LPFa", 4: "LPFg"}, inplace=True)

# errors = pd.DataFrame(data=data.query('Log_Type == 0'))
# errors.rename(columns={2: 'Error Message'}, inplace=True)


# def generate_table():
#     # Calib and errors
#     error_list = None
#     ts_list = None

#     # TODO - based on configuration
#     # if not configuration.empty:
#     #     first_last_config = configuration.iloc[[0, -1]]
#     #     if first_last_config['CTRL Register Byte'].iloc[0] == first_last_config['CTRL Register Byte'].iloc[1]:
#     #         # gain settings unchanged during test
#     #         ctrl_const = True
#     #         ctrl = first_last_config['CTRL Register Byte'].iloc[0]
#     #     if first_last_config['CFG Register Byte'].iloc[0] == first_last_config['CFG Register Byte'].iloc[1]:
#     #         # odr settings unchanged during test
#     #         cfg_const = True
#     #         cfg = first_last_config['CFG Register Byte'].iloc[0]
#     #     else:
#     #         ctrl_const = False
#     #         cfg_const = False

#     if not errors.empty:
#         error_list = errors['Error Message'].tolist()
#         ts_list = errors['Timestamps'].to_list()

#     # Measurement table
#     mean_ax = round(measurements['Ax'].mean(), 3)
#     mean_ay = round(measurements['Ay'].mean(), 3)
#     mean_az = round(measurements['Az'].mean(), 3)
#     mean_gx = round(measurements['Gx'].mean(), 3)
#     mean_gy = round(measurements['Gy'].mean(), 3)
#     mean_gz = round(measurements['Gz'].mean(), 3)
#     mean_t = round(measurements['T'].mean(), 3)
#     mean_list = ['Mean', mean_ax, mean_ay, mean_az, mean_gx, mean_gy, mean_gz, mean_t]

#     min_ax = round(measurements['Ax'].min(), 3)
#     min_ay = round(measurements['Ay'].min(), 3)
#     min_az = round(measurements['Az'].min(), 3)
#     min_gx = round(measurements['Gx'].min(), 3)
#     min_gy = round(measurements['Gy'].min(), 3)
#     min_gz = round(measurements['Gz'].min(), 3)
#     min_t = round(measurements['T'].min(), 3)
#     min_list = ['Min', min_ax, min_ay, min_az, min_gx, min_gy, min_gz, min_t]

#     max_ax = round(measurements['Ax'].max(), 3)
#     max_ay = round(measurements['Ay'].max(), 3)
#     max_az = round(measurements['Az'].max(), 3)
#     max_gx = round(measurements['Gx'].max(), 3)
#     max_gy = round(measurements['Gy'].max(), 3)
#     max_gz = round(measurements['Gz'].max(), 3)
#     max_t = round(measurements['T'].max(), 3)
#     max_list = ['Max', max_ax, max_ay, max_az, max_gx, max_gy, max_gz, max_t]

#     std_ax = round(measurements['Ax'].std(), 3)
#     std_ay = round(measurements['Ay'].std(), 3)
#     std_az = round(measurements['Az'].std(), 3)
#     std_gx = round(measurements['Gx'].std(), 3)
#     std_gy = round(measurements['Gy'].std(), 3)
#     std_gz = round(measurements['Gz'].std(), 3)
#     std_t = round(measurements['T'].std(), 3)
#     std_list = ['Std', std_ax, std_ay, std_az, std_gx, std_gy, std_gz, std_t]

#     return mean_list, min_list, max_list, std_list, error_list, ts_list


# def generate_figures(filename=args.output):
#     accel_list = ['Ax', 'Ay', 'Az']
#     rotation_list = ['Gx', 'Gy', 'Gz']
#     color1 = ["#FFA630", "#4DA1A9", "#611C35", "#2E5077"]
#     color2 = ["#D7E8BA"]

#     measurements.plot(kind='line', x='Timestamp', y=accel_list, color=color1)
#     label_fig('Timestamp', 'Acceleration Magnitude', 'IMU Acceleration over time')
#     plt.savefig(fname=file_path+'icm_0.png')
#     plt.close()

#     measurements.plot(kind='line', x='Timestamp', y=accel_list, color=color1)
#     label_fig('Timestamp', 'Acceleration Magnitude', 'IMU Acceleration and Temperature')
#     ax2 = plt.twinx()
#     measurements.plot(kind='line', x='Timestamp', y='T', color=color2, ax=ax2)
#     ax2.legend(loc='upper left')
#     ax2.set_ylabel('Temperature')
#     plt.savefig(fname=file_path+'icm_1.png')
#     plt.close()

#     measurements.plot(kind='line', x='Timestamp', y=rotation_list, color=color1)
#     label_fig('Timestamp', 'Rotation Magnitude', 'IMU Rotation over time')
#     plt.savefig(fname=file_path+'icm_2.png')
#     plt.close()

#     measurements.plot(kind='line', x='Timestamp', y=rotation_list, color=color1)
#     label_fig('Timestamp', 'Rotation Magnitude', 'IMU Rotation and Temperature')
#     ax2 = plt.twinx()
#     measurements.plot(kind='line', x='Timestamp', y='T', color=color2, ax=ax2)
#     ax2.legend(loc='upper left')
#     ax2.set_ylabel('Temperature')
#     plt.savefig(fname=file_path+'icm_3.png')
#     plt.close()

#     measurements.plot(kind='line', x='Timestamp', y='T', color=color2)
#     label_fig('Timestamp', 'Temperature', 'IMU Temperature VS Time')
#     plt.savefig(fname=file_path+'icm_4.png')
#     plt.close()



# def label_fig(x, y, title):
#     # TODO - create dict for columns to X and Y axis labels
#     plt.title(f"{title}")
#     plt.ylabel(f"{y}")
#     plt.xlabel(f"{x}")


# def table_helper(pdf, epw, th, table_data, col_num):
#     for row in table_data:
#         for datum in row:
#             # Enter data in columns
#             pdf.cell(epw/col_num, 2 * th, str(datum), border=1)
#         pdf.ln(2 * th)


# def init_report(filename=args.output):
#     mean_list, min_list, max_list, std_list, error_list, ts_list = generate_table()

#     config_data = [None]
#     error_data = [ts_list, error_list]

#     table_data = [['Value', 'Ax', 'Ay', 'Az', 'Gx', 'Gy', 'Gz', 'T'], mean_list, min_list, max_list, std_list]

#     result_data = [[None]] # TODO add the required pass/fails for 9.6 in nav
#     pdf = FPDF()
#     epw = pdf.w - 2*pdf.l_margin
#     pdf.add_page()

#     pdf.set_font('Helvetica', '', 10.0)
#     th = pdf.font_size

#     if None not in result_data:
#         pdf.set_font('Helvetica', '', 14.0)
#         pdf.cell(WIDTH, 0.0, 'Summary of ICM Test', align='C')
#         pdf.set_font('Helvetica', '', 10.0)
#         pdf.ln(5)
#         table_helper(pdf, epw, th, result_data, 3)
#         pdf.ln(5)

#     if None not in config_data:
#         pdf.set_font('Helvetica', '', 12.0)
#         pdf.cell(WIDTH, 0.0, 'Summary of ICM Test Configurations', align='C')
#         pdf.set_font('Helvetica', '', 10.0)
#         pdf.ln(5)
#         table_helper(pdf, epw, th, config_data, 3)
#         pdf.ln(5)

#     if None not in error_data:
#         pdf.set_font('Helvetica', '', 12.0)
#         pdf.cell(WIDTH, 0.0, 'Summary of ICM Test Errors', align='C')
#         pdf.set_font('Helvetica', '', 10.0)
#         pdf.ln(5)
#         table_helper(pdf, epw, th, error_data, len(error_list))
#         pdf.ln(5)

#     if None not in table_data:
#         pdf.set_font('Helvetica', '', 12.0)
#         pdf.cell(WIDTH, 0.0, 'Summary of ICM Test Measurements', align='C')
#         pdf.set_font('Helvetica', '', 10.0)
#         pdf.ln(5)
#         table_helper(pdf, epw, th, table_data, 8)
#         pdf.ln(5)

#     # Add images
#     pdf.image("./tmp/icm_0.png", 5, 85, WIDTH/2-10)
#     pdf.image("./tmp/icm_1.png", WIDTH/2, 85, WIDTH/2-10)
#     pdf.image("./tmp/icm_2.png", 5, 150, WIDTH/2 - 10)
#     pdf.image("./tmp/icm_3.png", WIDTH/2, 150, WIDTH/2 - 10)
#     pdf.image("./tmp/icm_4.png", 5, 225, WIDTH/2 - 10)

#     pdf.output(filename, 'F')


