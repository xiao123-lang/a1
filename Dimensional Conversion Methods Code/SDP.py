import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os


# SDP Transform function
def sdp(wave_data, start_angle, xi, il):
    data_len = len(wave_data)
    x_max = np.max(wave_data)
    x_min = np.min(wave_data)
    polar_list = []
    clockwise_list = []
    anticlockwise_list = []
    xi = np.radians(xi)
    for j in range(6):
        theta = np.radians(start_angle + j * 60)
        polar = []
        clockwise = []
        anticlockwise = []
        for i in range(data_len - il):
            if i < data_len - il:
                x_i = wave_data[i]
                # Calculate the radius in polar coordinates
                polar_radius = (x_i - x_min) / (x_max - x_min)
                # Retrieve the value of x(i + l)
                x_i_l = wave_data[i + il]
                # Calculate the clockwise rotation angle
                clockwise_angle = theta + ((x_i_l - x_min) / (x_max - x_min)) * xi
                # Calculate the counterclockwise angle
                anticlockwise_angle = theta - ((x_i_l - x_min) / (x_max - x_min)) * xi
                polar.append(polar_radius)
                clockwise.append(clockwise_angle)
                anticlockwise.append(anticlockwise_angle)
        polar_list.append(polar)
        clockwise_list.append(clockwise)
        anticlockwise_list.append(anticlockwise)
    return polar_list, clockwise_list, anticlockwise_list


# Read Excel files
file_path = 'DataAverage.xlsx'  # Please replace with the path to your Excel file.
try:
    df = pd.read_excel(file_path)
except FileNotFoundError:
    print(f"ERROR: FILE {file_path} Not found")
except Exception as e:
    print(f"Other errors occurred while reading the file. {e}")

# Create a directory to save images
output_dir = 'images'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

if 'df' in locals():
    for index, column in enumerate(df.columns):
        data = df[column].values
        r, beta, gamma = sdp(data, 0, 50, 9)   #SDP Image Parameters

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={'projection': 'polar'})

        for x, k in enumerate(r):
            ax.plot(beta[x], k, color='blue', linewidth=3)
            ax.plot(gamma[x], k, color='blue', linewidth=3)

        # Hide angle scale labels
        ax.set_thetagrids([])
        # Hide radius scale labels
        ax.set_rgrids([])

        plt.tight_layout()

        image_name = f'{index}.png'
        image_path = os.path.join(output_dir, image_name)
        plt.savefig(image_path)
        plt.close()