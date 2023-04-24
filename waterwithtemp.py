import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt

# Set basin properties
width = 300  # m
length = 300  # m
depth = 5  # m
volume = width * length * depth  # m^3
surface_area = width * length  # m^2
water_level = []  # list to store water level values
water_temp = []  # list to store water temperature values

# Set starting value for amount of water
initial_water_amount = 400000  # m^3
initial_water_temp = 15  # deg Celsius
outside_temp = 10  # deg Celsius
solar_radiation = 100  # W/m^2
heat_capacity_water = 4186  # J/(kg*K)
density_water = 1000  # kg/m^3

water_level.append(initial_water_amount / (width * length))
water_temp.append(initial_water_temp)

# Ask for calculation days
days = int(input("Enter the number of days to calculate: "))

# Ask for inflow data
inflow_filename = input("Do you want to supply an inflow CSV file? (y/n): ")
if inflow_filename == 'y':
    # Open file dialog to choose inflow file
    root = tk.Tk()
    root.withdraw()
    inflow_path = filedialog.askopenfilename()
    inflow_data = pd.read_csv(inflow_path, header=None, delimiter=";")
    inflow_data.columns = ['Day', 'Inflow(m^3)']
else:
    # Set constant inflow rate
    inflow_rate = float(input("Enter the inflow rate (m^3/day): "))
    inflow_data = pd.DataFrame({'Day': range(1, days+1), 'Inflow(m^3)': [inflow_rate] * days})

# Ask for outflow data
outflow_filename = input("Do you want to supply an outflow CSV file? (y/n): ")
if outflow_filename == 'y':
    # Open file dialog to choose outflow file
    root = tk.Tk()
    root.withdraw()
    outflow_path = filedialog.askopenfilename()
    outflow_data = pd.read_csv(outflow_path, header=None, delimiter=";")
    outflow_data.columns = ['Day', 'Outflow(m^3)']
else:
    # Set constant outflow rate
    outflow_rate = float(input("Enter the outflow rate (m^3/day): "))
    outflow_data = pd.DataFrame({'Day': range(1, days+1), 'Outflow(m^3)': [outflow_rate] * days})

# Perform calculations
water_level_dropped_to_zero = False  # flag to track whether the water level has dropped to 0
for day in range(1, days + 1):
    inflow = inflow_data.loc[inflow_data['Day'] == day, 'Inflow(m^3)'].values[0]
    outflow = outflow_data.loc[outflow_data['Day'] == day, 'Outflow(m^3)'].values[0]
    water_level_change = (inflow - outflow) / volume
    water_level_today = water_level[day - 1] + water_level_change

    # Calculate water temperature
    heat_received = solar_radiation * surface_area * 86400  # J
    heat_loss = (water_temp[day - 1] - outside_temp) * surface_area * 86400  # J (assuming a simple linear relationship)
    temp_change = (heat_received - heat_loss) / (volume * density_water * heat_capacity_water)
    water_temp_today = water_temp[day - 1] + temp_change

    if water_level_today < 0:
        if not water_level_dropped_to_zero:
            print(f"Water level has dropped to 0 on day {day}!")
            water_level_dropped_to_zero = True
        water_level_today = 0
    water_level.append(water_level_today)
    water_temp.append(water_temp_today)

# Print total water amount
total_water_amount = water_level[-1] * volume
print(f"Total water amount in the basin after {days} days: {total_water_amount:.2f} m^3")

# Create plot of water level over time
plt.plot(range(days + 1), water_level)
plt.xlabel("Days")
plt.ylabel("Water level (m)")
plt.title("Water level in basin over time")
plt.show()

# Create plot of water temperature over time
plt.plot(range(days + 1), water_temp)
plt.xlabel("Days")
plt.ylabel("Water temperature (°C)")
plt.title("Water temperature in basin over time")
plt.show()
