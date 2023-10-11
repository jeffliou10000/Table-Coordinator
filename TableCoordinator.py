# Table Coordinator

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from tkinter import Tk, filedialog


def get_file_path():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    root.destroy()
    return file_path

print('Please select the file with table signal: ')
table_path = get_file_path()
table_data = pd.read_excel(table_path)
df_table = pd.DataFrame(table_data)
timeT = df_table['Time']
table = df_table['Table']
plt.plot(timeT, table)
plt.grid()
plt.show()
x1 = float(input('please type in the first cut point: '))
x2 = float(input('please type in the secend cut point: '))
# x1 = 0.75
# x2 = 1.25
mask = (timeT < x1) | (timeT > x2)
df_table.loc[mask, 'Table'] = 0

number = int(input('How many signal file do you need to process? '))
for i in range(number):
    print('Please select the signal file: ')
    target_path = get_file_path()
    target_data = pd.read_excel(target_path)
    df_target = pd.DataFrame(target_data)
    target_name = input('Please type in the signal name which positioned most close to the table: (usually chassis base)')
    target = df_target[target_name]
    time = df_target['Time']

    table_peak_x = timeT.loc[table.idxmax()]
    target_peak_x = time.loc[target.idxmax()]
    gap = target_peak_x - table_peak_x
    t = timeT + gap
    plt.plot(time, target)
    plt.plot(t, table)
    plt.legend([target_name, 'Table'])
# plt.xlim(x1, x2)
    plt.grid()
    plt.show()
    df_target['Time_Table'] = t
    df_target['Table'] = table
    file_name = f'output_{i+1}.xlsx'
    output_path = os.path.join(os.path.dirname(target_path), file_name)
    df_target.to_excel(output_path, index=False)
print('Job done!')
print('Please check out the new excel in the directory where your selected file is located')