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
    """prints all values based on inputs in a formatted way"""#todo: add all wanted items
    print("Max ascent speed = "+ max_ascent_speed() + " m/s")
    print("Max ascent acceleration = " + ascent_acc() + " m/s^2")
    print("Max ascent acceleration = " + descent_acc() + " m/s^2")
    print("Max acceleration = " + acc() + " m/s^2")

velocity_vector = np.array([1.0, 2.0, 3.0])
acc_vector = np.array([3.0,0.0,0.0])
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
    #todo: find a relation for max ascent speed
    print("this is not yet implemented")

def max_descent_speed():
    #todo: find a relation for max descent speed
    print("this is not yet implemented")

def max_horizontal_speed():
    # todo: find a relation for max horizontal speed
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

def max_acc(thrust,drone_mass, g=9.81, drag):
    #assuming g is positive
    acc = np.array([0.0,0.0,0.0])
    weight  =  np.array([0.0,0.0,-1*drone_mass*g])#assuming [x,y,z) Z pointing up

    #add weight thrust and drag to the accelerationacc
    acc = acc + thrust + weight + drag
    return acc


def powerusage(thrust_needed_to_hover):
    somerelation=1
    powerusage_at_this_thrust = thrust_needed_to_hover*somerelation#TODO: find relation between powerusage and thrust
    return powerusage_at_this_thrust


def endurance_hover(drone_mass, g=9.81, battery_size):
    weight = drone_mass*g
    thrust_needed_to_hover = weight
    powerusage_at_this_thrust = powerusage(thrust_needed_to_hover)
    endurance = battery_size/powerusage_at_this_thrust
    return endurance

def endurance_cruise(drone_mass, g=9.81, battery_size)
    weight = drone_mass * g
    thrust_needed_to_cruise = #TODO: add thrust_needed_to_cruise
    powerusage_at_this_thrust = powerusage(thrust_needed_to_cruise)
    endurance = battery_size / powerusage_at_this_thrust
    return endurance

def max_range(cruise_speed, drone_mass, g=9.81, battery_size):
    """

    :param cruise_speed:
    :param drone_mass:
    :param g:
    :param battery_size:
    :return:
    """
    return cruise_speed*(drone_mass, g=9.81, battery_size)


def max_wind_speed_resistance():
    # todo: find a relation for max wind speed resistance
    print("this is not yet implemented")
