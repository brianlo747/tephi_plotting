import numpy as np

from constants.thermodynamics import CONST_ES0, CONST_GAS_CONST_AIR, CONST_GAS_CONST_VAP, CONST_TO, \
    CONST_LATENT_HEAT_VAP_WATER, \
    CONST_EPSILON, CONST_KELVIN, CONST_CP_AIR

from plots.radiosonde.emagram.emagram_transforms import convert_pressure_theta_to_temperature_theta, \
    convert_temperature_theta_to_temperature_pressure, convert_pressure_mixing_ratio_to_temperature


def isotherm(min_pressure, max_pressure, axes, transform, kwargs, temperature):
    steps = 1000
    pressures = np.linspace(min_pressure, max_pressure, steps)

    # _, thetas = convert_pressure_temperature_to_pressure_theta(pressures, [temperature] * steps)
    (line,) = axes.plot([temperature] * steps, pressures, transform=transform, **kwargs)

    return line


def isentropes(min_temperature, max_temperature, min_pressure, max_pressure, axes, transform, kwargs, theta):
    steps = 1000
    temperature_at_min_pressure, _ = convert_pressure_theta_to_temperature_theta(min_pressure, theta)
    temperature_at_max_pressure, _ = convert_pressure_theta_to_temperature_theta(max_pressure, theta)
    if temperature_at_min_pressure > min_temperature:
        min_temperature = temperature_at_min_pressure
    if temperature_at_max_pressure < max_temperature:
        max_temperature = temperature_at_max_pressure

    temperatures = np.linspace(min_temperature, max_temperature, steps)
    _, pressures = convert_temperature_theta_to_temperature_pressure(temperatures, theta)
    (line,) = axes.plot(temperatures, pressures, transform=transform, **kwargs)

    return line


def isobar(min_temperature, max_temperature, axes, transform, kwargs, pressure):
    steps = 1000
    temperatures = np.linspace(min_temperature, max_temperature, steps)
    (line,) = axes.plot(temperatures, [pressure] * steps, transform=transform, **kwargs)

    return line


def _moist_adiabat_gradient(min_temperature, max_pressure, min_pressure, pressure, temperature, dpressure):
    temperature_kelvin = temperature + CONST_KELVIN
    cc_equation_exp = (CONST_LATENT_HEAT_VAP_WATER / CONST_GAS_CONST_VAP) * (
            (1.0 / CONST_KELVIN) - (1.0 / temperature_kelvin))
    e_s = CONST_ES0 * np.exp(cc_equation_exp)
    r_vs = e_s * CONST_EPSILON / (pressure)
    lrwbt = (CONST_LATENT_HEAT_VAP_WATER * r_vs) / (CONST_GAS_CONST_AIR * temperature_kelvin)
    numerator = ((CONST_GAS_CONST_AIR * temperature_kelvin) / (CONST_CP_AIR * pressure)) * (1.0 + lrwbt)
    denominator = 1.0 + (lrwbt * ((CONST_EPSILON * CONST_LATENT_HEAT_VAP_WATER) / (CONST_CP_AIR * temperature_kelvin)))
    dtemperature_by_dpressure = numerator / denominator
    dtemperature = dpressure * dtemperature_by_dpressure

    # Check if gradient is too long and exceeds min_temperature isotherm.
    # If so, calculate the gradient for a shorter segment.
    if (temperature + dtemperature) < min_temperature:
        dtemperature = min_temperature - temperature
        dpressure = dtemperature / dtemperature_by_dpressure

    if (pressure + dpressure) > max_pressure:
        dpressure = max_pressure - pressure
        dtemperature = dpressure * dtemperature_by_dpressure

    if (pressure + dpressure) < min_pressure:
        dpressure = min_pressure - pressure
        dtemperature = dpressure * dtemperature_by_dpressure

    return dpressure, dtemperature


def moist_adiabat(min_temperature, max_pressure, init_pressure, min_pressure, axes, transform, kwargs, theta_es):
    steps = 1000
    temps_decreasing = [theta_es]
    temps_increasing = [theta_es]
    pressures_decreasing = [init_pressure]
    pressures_increasing = [init_pressure]
    dp = -1.0

    for i in range(steps):
        dp, dt = _moist_adiabat_gradient(
            min_temperature, max_pressure, min_pressure, pressures_decreasing[i], temps_decreasing[i], dp
        )
        temps_decreasing.append(temps_decreasing[i] + dt)
        pressures_decreasing.append(pressures_decreasing[i] + dp)

    dp = 1.0
    for j in range(steps):
        dp, dt = _moist_adiabat_gradient(
            min_temperature, max_pressure, min_pressure, pressures_increasing[j], temps_increasing[j], dp
        )
        temps_increasing.append(temps_increasing[j] + dt)
        pressures_increasing.append(pressures_increasing[j] + dp)

    temps_increasing.reverse()
    pressures_increasing.reverse()
    temps = temps_increasing + temps_decreasing
    pressures = pressures_increasing + pressures_decreasing
    # _, thetas = convert_pressure_temperature_to_pressure_theta(pressures, temps)
    (line,) = axes.plot(temps, pressures, transform=transform, **kwargs)

    return line


def mixing_ratio(min_temperature, min_pressure, max_pressure, axes, transform, kwargs, r_vs):
    steps = 1000
    pressures = np.linspace(min_pressure, max_pressure, steps)
    temps = convert_pressure_mixing_ratio_to_temperature(pressures, r_vs)

    temps_filter = np.where(temps > min_temperature)
    temps = temps[temps_filter]
    pressures = pressures[temps_filter]
    (line,) = axes.plot(temps, pressures, transform=transform, **kwargs)

    return line
