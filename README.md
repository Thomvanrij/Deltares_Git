## Abiotic factors floodplain Model
This model calculates the water level and temperature in a basin over a specified number of days based on inputs for inflow, outflow, solar radiation, air temperature, and other parameters. The model allows you to specify different scenarios by providing external CSV files for the input parameters.

# Getting Started
To run the model, enter the number of days to calculate when prompted. You will then be prompted to either supply CSV files or enter single values for the inflow, outflow, solar radiation, air temperature, wind speed, and humidity parameters for each day. If you choose to supply CSV files, you will be presented with a file dialog to select the files.

The model will output the final water volume, water level, and water temperature in the basin after the specified number of days. It will also plot the water level and temperature over time.

# Parameters
The model uses the following parameters:

rho_w - Density of water (g/cm^3)
C_w - Specific heat capacity of water (J/(g*K))
epsilon - Surface emissivity
Basin dimensions (width, length, depth)
Initial water temperature
Initial water volume
It requires inputs for the following for each day:

Inflow (cm) - The flow of water into the basin
Outflow (cm) - The flow of water out of the basin
Global radiation (J/cm^2*h) - The solar radiation reaching the water surface
Air temp (°C) - The ambient air temperature
Water vapor pressure (hPa) - The atmospheric water vapor pressure
Wind velocity (m/s) - The wind speed
Saturation water vapor pressure (hPa) - The saturation water vapor pressure at the air temperature

# Output
The model outputs the following:

Total water amount (m^3) - The total volume of water in the basin at the end of the time period
Water level (cm) - The depth of the water in the basin at the end of the time period
Water temperature (°C) - The temperature of the water in the basin at the end of the time period
Two plots showing water level and temperature over time
The model allows you to specify different scenarios by providing external CSV files for the input parameters.
