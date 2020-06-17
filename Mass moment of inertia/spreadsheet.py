from typing import Optional, Any, Dict, List, Union

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np
from shapely import geometry, ops
import matplotlib.pyplot as plt


def import_spreadsheet(sheetname):
    # the data is stored in list of hashes as a list containing dict(ionarie)s by the import script
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open(sheetname).sheet1
    return sheet


def center_of_gravity(m, x, y, z):
    """
    calculate center of gravity using the weighted average
    :param m: numpy array or list containing floats with masses
    :param x: numpy array or list containing floats with x coordinates
    :param y: numpy array or list containing floats with y coordinates
    :param z: numpy array or list containing floats with z coordinates
    :return:
    """
    cgx = 0.0
    cgy = 0.0
    cgz = 0.0

    for i in range(len(m)):
        cgx = cgx + (m[i] * x[i])
        cgy = cgy + (m[i] * y[i])
        cgz = cgz + (m[i] * z[i])
    # divide by sum of mass
    return float(cgx / sum(m)), float(cgy / sum(m)), float(cgz / sum(m))


def vehicle_to_body_reference_frame(x_v, y_v, z_v, cg):
    """This is the position of the components with respect to the body axis system: origin is the Center of gravity,
    x lies in the symmetry plane and points forward, z lies in the symmetry plane and points downward, y from the
    right handrule

   """
    x_b = cg[0] - y_v
    y_b = cg[1] - x_v
    z_b = cg[2] - z_v
    return x_b, y_b, z_b


def mass_moment_of_inertia_cuboid(mass, width, depth, height):
    """
    This function calculates ths mass moment of inertia for a cuboid. It assumes an equal distribution of mass
    throughout the specified cuboid. It returns an inertia tensor.
     :param float mass: mass
     :param float width: width
     :param float depth: depth
     :param float height: height
     :return: nparray inertia tensor
    """
    return 1. / 12. * np.array([[mass * (height ** 2 + depth ** 2), 0.0, 0.0],
                                [0.0, mass * (width ** 2 + depth ** 2), 0.0],
                                [0.0, 0.0, mass * (width ** 2 + height ** 2)]])


def mass_moment_of_inertia_steiner(mass, x, y, z):
    """

    :param float mass: mass
    :param float x:
    :param float y:
    :param float z:
    :return: nparray inertia tensor
    """
    return np.array(
        [[mass * x * x, mass * x * y, mass * x * z], [mass * y * x, mass * y * y, mass * y * z],
         [mass * z * x, mass * z * y, mass * z * z]])


def width_of_landing_gear_from_tip_over_angle(tip_over_angle, cg_z):
    tip_over_angle_radians = tip_over_angle / 180 * np.pi
    return 2 * np.tan(tip_over_angle_radians) * cg_z


def tip_over_angle_from_width_of_landing_gear(width_of_landing_gear, cg_z):
    tip_over_angle_radians = np.arctan((width_of_landing_gear / 2) / cg_z)
    return tip_over_angle_radians * 180 / np.pi


"""Start of the script"""
# import sheet
sheet = import_spreadsheet("Mass of components for mass moment inertia calculation")
# Extract all of the values into a dictionary
list_of_hashes = sheet.get_all_records()

# print(list_of_hashes)


# convert the columns to floats
m = np.array(sheet.get('B2:B999'), dtype=float)
x = np.array(sheet.get('C2:C999'), dtype=float)
y = np.array(sheet.get('D2:D999'), dtype=float)
z = np.array(sheet.get('E2:E999'), dtype=float)

c_o_g = center_of_gravity(m, x, y, z)
c_o_g_for_cell = [[c_o_g[0]], [c_o_g[1]], [c_o_g[2]]]
# update the corresponding cell G2
sheet.update('L2', c_o_g_for_cell)

# update the positions of components with respect to the center of gravity


cellvalues = []
for column in list_of_hashes:
    Xb, Yb, Zb = vehicle_to_body_reference_frame(column.get("x [m]"), column.get("y [m]"), column.get("z [m]"), c_o_g)
    cellvalues.append([Xb, Yb, Zb])

# update the cells in the sheet
sheet.update('M2', cellvalues)

# re import sheet to get new values # lazy method
sheet = import_spreadsheet("Mass of components for mass moment inertia calculation")
# Extract all of the values into a dictionary
list_of_hashes = sheet.get_all_records()

# Calculate mass moment of inertia for each component
InertiaTensor = np.zeros((3, 3))
for column in list_of_hashes:
    m = column.get('mass [kg]')
    w = column.get('w [m]')
    d = column.get('d [m]')
    h = column.get('h [m]')
    InertiaTensor = InertiaTensor + mass_moment_of_inertia_cuboid(m, w, d, h)

# calculate Steiner term
for column in list_of_hashes:
    m = column.get('mass [kg]')
    x = column.get('Xb [m]')
    y = column.get('Yb [m]')
    z = column.get('Zb [m]')
    InertiaTensor = InertiaTensor + mass_moment_of_inertia_steiner(m, x, y, z)

# update the cells in the sheet
sheet.update('Q5', InertiaTensor.tolist())

# find the frontal area of the drone

# create a Polygon object for each cuboid
rects = []
area = 0.0
for column in list_of_hashes:
    # find bounding points
    left = column.get('Yb [m]') - (column.get('w [m]') / 2.)
    right = column.get('Yb [m]') + (column.get('w [m]') / 2.)
    bottom = column.get('Zb [m]') - (column.get('h [m]') / 2.)
    top = column.get('Zb [m]') + (column.get('h [m]') / 2.)
    top, bottom = bottom, top
    rect = geometry.Polygon([(left, top), (right, top), (right, bottom), (left, bottom)])
    x, y = rect.exterior.xy
    plt.fill(x, y, alpha=0.5, fc='red', ec='black')
    plt.axis('square')
    area = area + rect.area
    rects.append(rect)
plt.axis([-0.45, 0.45, -0.1, 0.32])
plt.gca().invert_yaxis()
plt.gca().invert_xaxis()
plt.title("Drone component distribution front view")
plt.xlabel("y axis in body reference frame")
plt.ylabel("z axis in body reference frame")
plt.savefig('figures/front_view.pdf', format = "pdf")
plt.show()

frontal_area = ops.unary_union(rects)

# find the overlapped area

# update the corresponding cell R2
sheet.update('T2', str(frontal_area.area))
# find the top area of the drone

# create a Polygon object for each cuboid
rects = []
area = 0.0
for column in list_of_hashes:
    # find bounding points
    left = column.get('Yb [m]') - (column.get('w [m]') / 2.)
    right = column.get('Yb [m]') + (column.get('w [m]') / 2.)
    bottom = column.get('Xb [m]') - (column.get('d [m]') / 2.)
    top = column.get('Xb [m]') + (column.get('d [m]') / 2.)
    rect = geometry.Polygon([(left, top), (right, top), (right, bottom), (left, bottom)])
    x, y = rect.exterior.xy
    plt.fill(x, y, alpha=0.5, fc='green', ec='black')
    plt.axis('square')
    area = area + rect.area
    rects.append(rect)
plt.axis([-0.36, 0.36, -0.35, 0.35])
plt.gca().invert_yaxis()
plt.gca().invert_xaxis()
plt.title("Drone component distribution top view")
plt.xlabel("y axis in body reference frame")
plt.ylabel("x axis in body reference frame")
plt.savefig('figures/top_view.pdf', format = "pdf")
plt.show()

top_area = ops.unary_union(rects)

# find the overlapped area

# update the corresponding cell S2
sheet.update('U2', str(top_area.area))
print("The script has finished.")
