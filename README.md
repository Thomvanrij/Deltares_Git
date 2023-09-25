Here is a draft GitHub readme for the project:

# Floodplain Rewetting Modeling

This repository contains code to model floodplain rewetting dynamics using Google Earth Engine (GEE) and Python.

## GEE Scripts

The GEE scripts are written in Javascript and can be used to analyze any water area.

`inundation_area.js` - Calculates the inundation area and extent over time for a specified region.

`water_temperature.js` - Estimates water temperature for an inundated area based on thermal data.

## Python Scripts 

The Python scripts model nutrient-phytoplankton-zooplankton (NPZ) dynamics based on abiotic factors like evaporation and radiation.

`wilt.py` - Uses water vapor, global radiation, air temperature etc. to simulate water temperature and level decrease over time in a basin.

`npzaf.py` - Takes output from wilt.py and models NPZ concentrations based on initial values. 

## Usage

The GEE scripts can be run in the GEE Code Editor after authenticating. The Python scripts require the packages listed in requirements.txt and input data as specified in the scripts.


Please contact Thom van Rij at thomvanrij@gmail.com with any questions!