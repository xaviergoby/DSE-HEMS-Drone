"""This file calculates the following flight performance parameters:
Max ascent speed,
Max Descent speed,
Max horizontal flight speed,
Max ascent acceleration,
Max Descent acceleration,
Max horizontal flight acceleration,
Max range,
Hovering endurance,
Cruising endurance,
Wind speed resistance."""
import numpy as np


def value_printer():
    """prints all values based on inputs in a formatted way"""
    print("Max ascent speed = "+ max_ascent_speed() + " m/s")
    print("Max ascent acceleration = " + ascent_acc() + " m/s^2")
    print("Max ascent acceleration = " + descent_acc() + " m/s^2")
    print("Max acceleration = " + acc() + " m/s^2")

velocity_vector = np.array([1.0, 2.0, 3.0])
acc_vector = np.array([0.0,0.0,0.0])
attitude_vector = np.array([0.4,0.20,0.10])
thrust_magnitude = 10
thrust_vector = thrust_magnitude*attitude_vector
dragcoef = 0.3
drag_vector = -1*velocity_vector *dragcoef
dronemass = 10
def add_force(acc_vector, force, mass):
    return acc_vector+ force/mass
print(add_force(acc_vector,thrust_vector,dronemass))
def max_ascent_speed():
    print("this is not yet implemented")

def ascent_acc(thrust, drone_mass, g=9.81, drag = 0.):
    """
    This function uses Newton's second law to generate a maximum ascent acceleration number
    :param thrust: float in Newton
    :param drone_mass: float in kg
    :param g: float specifying gravitational acceleration default value = 9.81 m/s^2
    :param drag: float specifying drag in ascent in Newton
    :return: max ascent acceleration in m/s^2 This should be a positive number
    """
    output = (thrust - drone_mass * g - drag) / drone_mass
    return output

def descent_acc(thrust, drone_mass, g=9.81, drag = 0.):
    """
    This function uses Newton's second law to generate a maximum descent acceleration number
    :param thrust: float in Newton
    :param drone_mass: float in kg
    :param g: float specifying gravitational acceleration default value = 9.81 m/s^2
    :param drag: float specifying drag in descent in Newton
    :return: max descent acceleration in m/s^2 this should be a negative number
    """
    output = (-thrust - drone_mass * g + drag) / drone_mass
    return output

def acc(thrust, attitude_tilt, drone_mass, g=9.81, drag = 0. ):
    """
    2d situation
    :param thrust: float in Newton
    :param attitude_tilt: float in rad
    :param drone_mass: float in kg
    :param g:  float specifying gravitational acceleration default value = 9.81 m/s^2
    :param drag: doesn't even have a  direction this calculation is worthless

    """
    weight = drone_mass*g
    vertical_acc = thrust*np.cos(attitude_tilt)-drag-weight
    horizontal_acc= thrust*np.sin(attitude_tilt)-drag

    return vertical_acc,horizontal_acc


