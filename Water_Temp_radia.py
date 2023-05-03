import numpy as np
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt

# Ask the user for the number of days to calculate
days = int(input("Enter the number of days to calculate: "))

# Constants
rho_w = 1  # Density of water g/cm^3
C_w = 4.18  # Specific heat capacity J/(g*K)
epsilon = 0.96

# Define the dimensions of the basin and the initial water temperature and volume
basin_width = 300  # m
basin_length = 300  # m
basin_depth = 5
# water_temp = [12]
water_volume = 400000
basin_volume = basin_width * basin_length * basin_depth
basin_surface_area = basin_width * basin_length

# Calculate the initial water level based on the volume and surface area of the basin
z_w = np.zeros(days)
z_w[0] = water_volume / basin_surface_area * 100  # cm


# Initialize water surface temperature
t_w = np.zeros(days)
t_w[0] = 25  # Assign starting water temperature of 15 degrees

# Define a function to get data from a CSV file or from user input


def get_data(filename_prompt, value_prompt, column_name):
    if input(filename_prompt) == 'y':
        # If the user wants to supply a CSV file, open a file dialog to select the file
        root = tk.Tk()
        root.withdraw()
        path = filedialog.askopenfilename()
        # Read the data from the CSV file and set the column names
        data = pd.read_csv(path, header=None, delimiter=";")
        data.columns = ['Day', f'{column_name}']
    else:
        # If the user doesn't want to supply a CSV file, ask for a single value and
        # create a DataFrame with that value for each day
        value = float(input(value_prompt + ": "))
        data = pd.DataFrame({'Day': range(1, days + 1), f'{column_name}': [value] * days})
    return data


# Get the inflow, outflow, solar radiation, and outside temperature data
inflow_data = get_data("Do you want to supply an inflow CSV file? (y/n): ", "Inflow", "Inflow(cm)")
outflow_data = get_data("Do you want to supply an outflow CSV file? (y/n): ", "Outflow", "Outflow(cm)")
globrad_data = get_data("Do you want to supply an global radiation CSV file? (y/n): ", "Globrad", "Global radiation (J/cm^2*h)")
T_L_data = get_data("Do you want to supply an Air temperature CSV file? (y/n): ", "T_L", "Air temp (°C)")
E_L_data = get_data("Do you want to supply a Water vapor pressure CSV file? (y/n): ", "E_L", "Water vapor pressure (hPa)")
mu_data = get_data("Do you want to supply a Wind velocity CSV file? (y/n): ", "mu", "Wind velocity (m/s)")
E_w_data = get_data("Do you want to supply a Saturation water vapor pressure CSV file? (y/n): ", "E_w", "Saturation water vapor pressure (hPa)")
e_L_data = get_data("Do you want to supply a Water vapor pressure CSV file? (y/n): ", "e_L", "Water vapor pressure (hPa)")


# Initialize a flag to track if the water level has dropped to zero
water_level_zero = False

# Loop through each day and calculate the water level and temperature
for day in range(1, days):
    # Get the inflow, outflow, solar radiation, and outside temperature for the current day
    inflow = inflow_data.loc[inflow_data['Day'] == day, 'Inflow(cm)'].values[0]
    outflow = outflow_data.loc[outflow_data['Day'] == day, 'Outflow(cm)'].values[0]
    globrad = globrad_data.loc[globrad_data['Day'] == day, 'Global radiation (J/cm^2*h)'].values[0]
    T_L = T_L_data.loc[T_L_data['Day'] == day, 'Air temp (°C)'].values[0]
    E_L = E_L_data.loc[E_L_data['Day'] == day, 'Water vapor pressure (hPa)'].values[0]
    mu = mu_data.loc[mu_data['Day'] == day, 'Wind velocity (m/s)'].values[0]
    E_w = E_w_data.loc[E_w_data['Day'] == day, 'Saturation water vapor pressure (hPa)'].values[0]
    e_L = e_L_data.loc[e_L_data['Day'] == day, 'Water vapor pressure (hPa)'].values[0]

    # Calculate the change in water level based on the inflow and outflow
    water_level_change = (inflow - outflow)
    # Calculate the new water level
    water_depth = z_w[day - 1] + water_level_change

    K_short_wave = 0.85 * globrad
    L_up = epsilon * 2.06e-8 * (t_w[day - 1] + 273) ** 4
    L_down = 2.06e-8 * (0.83 - 0.25 * 10 ** (-0.08 * e_L)) * (T_L + 273) ** 4
    Q_star = K_short_wave - L_up + L_down

    eth_L = 2.05 * mu ** 0.65
    Q_E = 1.52 * eth_L * (E_w - e_L)
    Q_H = eth_L * (t_w[day - 1] - T_L)

    # Calculate current temperature at each day
    Temp_today = t_w[day - 1] - (Q_star - Q_E - Q_H) / (rho_w * C_w * z_w[day - 1])

    # If the water level has dropped to zero, print a message and set the flag to True
    if water_depth < 0:
        if not water_level_zero:
            print(f"Water level has dropped to 0 on day {day}!")
            water_level_zero = True
        water_depth = 0

    # Add the new water level and temperature to the arrays
    z_w[day] = water_depth
    t_w[day] = Temp_today

# Print the final water volume, water level, and water temperature
print(f"Total water amount in the basin after {days} days: {z_w[-1] * basin_surface_area:.2f}m^3")
print(f"Water level after {days} days: {z_w[-1] :.2f}cm")
print(f"Water temperature after {days} days: {t_w[-1] :.2f}\u2103")


# Define a function to plot the data
def plot_data(data, ylabel, title):
    plt.plot(range(days), data)
    plt.xlabel("Days")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()


# Plot the water level and temperature over time
plot_data(z_w, "Water level (cm)", "Water level in basin over time")
plot_data(t_w, "Water temperature (°C)", "Water temperature in basin over time")
