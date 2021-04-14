
import os
import csv
import json
import numpy as np
import matplotlib.pyplot as plt

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# %% Global variables
TEST_DATE = "2021-04-13 "

# %% Load Files from Grafana

with open("./data/g_force_x.csv") as fp:
    reader = csv.reader(fp, delimiter=",")
    next(reader, None)
    g_force_x = [row for row in reader if row != []]
    
with open("./data/g_force_y.csv") as fp:
    reader = csv.reader(fp, delimiter=",")
    next(reader, None)
    g_force_y = [row for row in reader if row != []]

with open("./data/g_force_z.csv") as fp:
    reader = csv.reader(fp, delimiter=",")
    next(reader, None)
    g_force_z = [row for row in reader if row != []]

# %% Load timestamps

with open("./timestamps.json", encoding='utf-8') as fp:
    experiment_timestamps = json.load(fp)

# %% Get accelerometer data for each experiment

def get_seconds_between_timestamps(t1, t2):
    h1, m1, s1 = t1.split(":")
    h2, m2, s2 = t2.split(":")
    
    h_diff = int(h2) - int(h1)
    m_diff = int(m2) - int(m1)
    s_diff = int(s2) - int(s1)
    
    return h_diff*3600 + m_diff*60 + s_diff

def get_force_between_timestamps(force_list, time_start, time_end):
    
    t1 = TEST_DATE + time_start
    t2 = TEST_DATE + time_end
    
    start_index = -1
    end_index = -1
    
    for i in range(len(force_list)):
        if force_list[i][0] == t1:
            if i == 0:
                start_index = i
            elif force_list[i-1][0] != t1:
                start_index = i

        if force_list[i][0] == t2:
            if i == len(force_list) - 1:
                end_index = i
            elif force_list[i+1][0] != t2:
                end_index = i
    
    if start_index == -1 or end_index == -1:
        print("Timestamp(s) not found")
        return None
    
    requested_entries = force_list[start_index:end_index+1]
    
    res = [float(entry[1][:-6]) for entry in requested_entries] # -6 to remove " Force" postfix
    
    return np.array(res, dtype=float)

experiment_data = {}

for experiment in experiment_timestamps.keys():
    
    data = {}
    for experiment_run in experiment_timestamps[experiment].keys():
        experiment_run_data = {}
        start = experiment_timestamps[experiment][experiment_run]["start"]
        end = experiment_timestamps[experiment][experiment_run]["slutt"]
        experiment_run_data["duration"] = get_seconds_between_timestamps(start, end)
        experiment_run_data["x"] = get_force_between_timestamps(g_force_x, start, end)
        experiment_run_data["y"] = get_force_between_timestamps(g_force_y, start, end)
        experiment_run_data["z"] = get_force_between_timestamps(g_force_z, start, end)
        data[experiment_run] = experiment_run_data
        
    experiment_data[experiment] = data

# %% Plotting

for experiment, data in experiment_data.items():
    
    for run, run_data in data.items():
        
        duration = run_data["duration"]
        x = run_data["x"]
        y = run_data["y"]
        z = run_data["z"]
        t = np.linspace(0, duration, np.size(x))
        
        x_abs_max = max(np.amax(x+1), np.amin(x+1), key=abs) # offset for gravity
        x_abs_line = [x_abs_max - 1 for i in range(np.size(x))] # offset for gravity
        y_abs_max = max(np.amax(y), np.amin(y), key=abs)
        y_abs_line = [y_abs_max for i in range(np.size(y))]
        z_abs_max = max(np.amax(z), np.amin(z), key=abs)
        z_abs_line = [z_abs_max for i in range(np.size(z))]
        
        plt.figure()
        plt.title(f"Akselerasjon for {experiment} {run}")
        plt.plot(t, x, color="red", linewidth=1)
        plt.plot(t, y, color="green", linewidth=1)
        plt.plot(t, z, color="blue", linewidth=1)
        
        plt.plot(t, x_abs_line, color="red", linestyle="dashed", linewidth=1, label=f"Maks vertikal akselerasjon: {x_abs_max:.2f}g")
        plt.plot(t, y_abs_line, color="green", linestyle="dashed", linewidth=1, label=f"Maks horisontal akselerasjon: {y_abs_max:.2f}g")
        plt.plot(t, z_abs_line, color="blue", linestyle="dashed", linewidth=1, label=f"Maks akselerasjon inn/ut av veggen: {z_abs_max:.2f}g")
        
        plt.legend(loc="best")
        plt.grid()
        plt.ylabel("Akselerasjon (g)")
        plt.xlabel("Tid (sekunder)")
        
        filename = "-".join(experiment.split(" ")) + "-" + run
        
        plt.savefig(f"./results/{filename}.png", dpi=300, bbox_inches='tight')
        
    
    
    
    
    
    
    
    
    
    
    
    
    