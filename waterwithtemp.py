import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt

width, length, depth = 300, 300, 5
water_temp = [12]
water_volume = 400000
volume, surface_area = width * length * depth, width * length
water_level = [water_volume / surface_area]
heat_capacity_water, density_water = 4186, 1000

days = int(input("Enter the number of days to calculate: "))


def get_data(filename_prompt, value_prompt, column_name):
    if input(filename_prompt) == 'y':
        root = tk.Tk()
        root.withdraw()
        path = filedialog.askopenfilename()
        data = pd.read_csv(path, header=None, delimiter=";")
        data.columns = ['Day', f'{column_name}']
    else:
        value = float(input(value_prompt + ": "))
        data = pd.DataFrame({'Day': range(1, days + 1), f'{column_name}': [value] * days})
    return data


inflow_data = get_data("Do you want to supply an inflow CSV file? (y/n): ", "Inflow", "Inflow(m^3)")
outflow_data = get_data("Do you want to supply an outflow CSV file? (y/n): ", "Outflow", "Outflow(m^3)")
solar_radiation_data = get_data("Do you want to supply a solar radiation CSV file? (y/n): ", "Solar radiation (W/m^2)",
                                "Solar Radiation(W/m^2)")
temp_data = get_data("Do you want to supply an outside temperature CSV file? (y/n): ", "Outside Temperature (°C)",
                     "Outside Temp(°C)")

water_level_zero = False
for day in range(1, days + 1):
    inflow = inflow_data.loc[inflow_data['Day'] == day, 'Inflow(m^3)'].values[0]
    outflow = outflow_data.loc[outflow_data['Day'] == day, 'Outflow(m^3)'].values[0]
    solar_radiation = solar_radiation_data.loc[solar_radiation_data['Day'] == day, 'Solar Radiation(W/m^2)'].values[0]
    outside_temp = temp_data.loc[temp_data['Day'] == day, 'Outside Temp(°C)'].values[0]

    water_level_change = (inflow - outflow) / surface_area
    water_level_today, water_temp_prev = water_level[day - 1] + water_level_change, water_temp[day - 1]

    heat_received = solar_radiation * surface_area * 86400
    heat_loss = (water_temp_prev - outside_temp) * surface_area * 86400
    temp_change = (heat_received - heat_loss) / ((water_level_today * surface_area) * density_water *
                                                 heat_capacity_water)
    water_temp_today = water_temp_prev + temp_change

    if water_level_today < 0:
        if not water_level_zero:
            print(f"Water level has dropped to 0 on day {day}!")
            water_level_zero = True
        water_level_today = 0
    water_level.append(water_level_today)
    water_temp.append(water_temp_today)

print(f"Total water amount in the basin after {days} days: {water_level[-1] * surface_area:.2f}m^3")
print(f"Water level after {days} days: {water_level[-1] :.2f}m")
print(f"Water temperature after {days} days: {water_temp[-1] :.2f}\u2103")


def plot_data(data, ylabel, title):
    plt.plot(range(days + 1), data)
    plt.xlabel("Days")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()


plot_data(water_level, "Water level (m)", "Water level in basin over time")
plot_data(water_temp, "Water temperature (°C)", "Water temperature in basin over time")
