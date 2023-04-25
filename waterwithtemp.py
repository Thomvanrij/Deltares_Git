import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt

# Define the dimensions of the basin and the initial water temperature and volume
basin_width, basin_length, water_depth = 300, 300, 5
water_temp = [12]
water_volume = 400000
basin_volume, basin_surface_area = basin_width * basin_length * water_depth, basin_width * basin_length

# Calculate the initial water level based on the volume and surface area of the basin
water_level = [water_volume / basin_surface_area]

# Define the heat capacity and density of water
heat_capacity_water, density_water = 4186, 1000

# Ask the user for the number of days to calculate
days = int(input("Enter the number of days to calculate: "))


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
inflow_data = get_data("Do you want to supply an inflow CSV file? (y/n): ", "Inflow", "Inflow(m^3)")
outflow_data = get_data("Do you want to supply an outflow CSV file? (y/n): ", "Outflow", "Outflow(m^3)")
solar_radiation_data = get_data("Do you want to supply a solar radiation CSV file? (y/n): ", "Solar radiation (W/m^2)",
                                "Solar Radiation(W/m^2)")
temp_data = get_data("Do you want to supply an outside temperature CSV file? (y/n): ", "Outside Temperature (°C)",
                     "Outside Temp(°C)")

# Initialize a flag to track if the water level has dropped to zero
water_level_zero = False

# Loop through each day and calculate the water level and temperature
for day in range(1, days + 1):
    # Get the inflow, outflow, solar radiation, and outside temperature for the current day
    inflow = inflow_data.loc[inflow_data['Day'] == day, 'Inflow(m^3)'].values[0]
    outflow = outflow_data.loc[outflow_data['Day'] == day, 'Outflow(m^3)'].values[0]
    solar_radiation = solar_radiation_data.loc[solar_radiation_data['Day'] == day, 'Solar Radiation(W/m^2)'].values[0]
    outside_temp = temp_data.loc[temp_data['Day'] == day, 'Outside Temp(°C)'].values[0]

    # Calculate the change in water level based on the inflow and outflow
    water_level_change = (inflow - outflow) / basin_surface_area
    # Calculate the new water level and the previous water temperature
    water_level_today, water_temp_prev = water_level[day - 1] + water_level_change, water_temp[day - 1]

    # Calculate the heat received from solar radiation and the heat lost to the outside environment
    heat_received = solar_radiation * basin_surface_area * 86400
    heat_loss = (water_temp_prev - outside_temp) * basin_surface_area * 86400
    # Calculate the change in water temperature based on the heat received and lost
    temp_change = (heat_received - heat_loss) / ((water_level_today * basin_surface_area) * density_water *
                                                 heat_capacity_water)
    water_temp_today = water_temp_prev + temp_change

    # If the water level has dropped to zero, print a message and set the flag to True
    if water_level_today < 0:
        if not water_level_zero:
            print(f"Water level has dropped to 0 on day {day}!")
            water_level_zero = True
        water_level_today = 0
    # Add the new water level and temperature to the lists
    water_level.append(water_level_today)
    water_temp.append(water_temp_today)

# Print the final water volume, water level, and water temperature
print(f"Total water amount in the basin after {days} days: {water_level[-1] * basin_surface_area:.2f}m^3")
print(f"Water level after {days} days: {water_level[-1] :.2f}m")
print(f"Water temperature after {days} days: {water_temp[-1] :.2f}\u2103")


# Define a function to plot the data
def plot_data(data, ylabel, title):
    plt.plot(range(days + 1), data)
    plt.xlabel("Days")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()


# Plot the water level and temperature over time
plot_data(water_level, "Water level (m)", "Water level in basin over time")
plot_data(water_temp, "Water temperature (°C)", "Water temperature in basin over time")
