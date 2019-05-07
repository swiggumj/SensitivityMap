# SensitivityMap
An archive of current pulsar survey coverage and tools for mapping minimum sensitivity as a function of sky position. The package is currently under development and an up-to-date task list can be found in `TASKS.md`. For current usage instructions, see below.

# Usage
* Edit `surv_list` variable in `cov.py` and run it to generate survey coverage files and sky maps.
* Make sure `surv_list` variable is set correctly in `sens_map.py` and set `desired_frequency` to a chosen reference frequency at which to compare the sensitivities of multiple pulsar surveys; run `sens_map.py` to generate `all.dat`, which contains a header with the desired reference frequency, and columns that describe minimum sensitivity, most sensitive survey, and coverage redundancy for each sky position.
* Edit `plot_all.py` and run it to create the desired sky map in Galactic coordinates. 
