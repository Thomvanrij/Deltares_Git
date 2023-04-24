import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt

width, length, depth = 300, 300, 5
outside_temp = 10
solar_radiation = 100
water_temp = [15]
water_volume = 400000
volume, surface_area = width * length * depth, width * length
water_level = [water_volume / surface_area]
heat_capacity_water, density_water = 4186, 1000

days = int(input("Enter the number of days to calculate: "))

def get_flow_data(filename_prompt, flow_rate_prompt):
    if input(filename_prompt) == 'y':
        root = tk.Tk()
        root.withdraw()
        path = filedialog.askopenfilename()
        data = pd.read_csv(path, header=None, delimiter=";")
        data.columns = ['Day', f'{flow_rate_prompt}(m^3)']
    else:
        rate = float(input(flow_rate_prompt))
        data = pd.DataFrame({'Day': range(1, days+1), f'{flow_rate_prompt}(m^3)': [rate] * days})
    return data

inflow_data = get_flow_data("Do you want to supply an inflow CSV file? (y/n): ", "Inflow")
outflow_data = get_flow_data("Do you want to supply an outflow CSV file? (y/n): ", "Outflow")

water_level_zero = False
for day in range(1, days + 1):
    inflow = inflow_data.loc[inflow_data['Day'] == day, 'Inflow(m^3)'].values[0]
    outflow = outflow_data.loc[outflow_data['Day'] == day, 'Outflow(m^3)'].values[0]
    water_level_change = (inflow - outflow) / surface_area
    water_level_today, water_temp_prev = water_level[day - 1] + water_level_change, water_temp[day - 1]

    heat_received = solar_radiation * surface_area * 86400
    heat_loss = (water_temp_prev - outside_temp) * surface_area * 86400
    temp_change = (heat_received - heat_loss) / (volume * density_water * heat_capacity_water)
    water_temp_today = water_temp_prev + temp_change

    if water_level_today < 0:
        if not water_level_zero:
            print(f"Water level has dropped to 0 on day {day}!")
            water_level_zero = True
        water_level_today = 0
    water_level.append(water_level_today)
    water_temp.append(water_temp_today)

print(f"Total water amount in the basin after {days} days: {water_level[-1] * surface_area:.2f} m^3")

def plot_data(data, ylabel, title):
    plt.plot(range(days + 1), data)
    plt.xlabel("Days")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()

plot_data(water_level, "Water level (m)", "Water level in basin over time")
plot_data(water_temp, "Water temperature (°C)", "Water temperature in basin over time")