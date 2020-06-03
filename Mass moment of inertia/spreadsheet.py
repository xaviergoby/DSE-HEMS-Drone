import gspread
from oauth2client.service_account import ServiceAccountCredentials

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("Mass of components for mass moment inertia calculation").sheet1

# Extract and print all of the values
list_of_hashes = sheet.get_all_records()
# print(list_of_hashes)

# the data is stored in list of hashes as a list containing dict(ionarie)s by the import script

# calculate center of gravity using the weighted average
cgx = 0.0
cgy = 0.0
cgz = 0.0
mass = 0.0

for column in list_of_hashes:
    cgx = cgx + (column.get('mass [kg]') * column.get('x [m]'))
    cgy = cgy + (column.get('mass [kg]') * column.get('y [m]'))
    cgz = cgz + (column.get('mass [kg]') * column.get('z [m]'))
    mass = mass + column.get('mass [kg]')
# divide by sum of mass
cgx, cgy, cgz = cgx / mass, cgy / mass, cgz / mass
# format the center of gravity into a dict
center_of_gravity = {'x': cgx,
                     'y': cgy,
                     'z': cgz}
# update the corresponding cell G2
sheet.update('G2', str(center_of_gravity))

# update the positions of components with respect to the center of gravity

# This is the position of the components with respect to the body axis system: origin is the Center of gravity,
# x lies in the symmetry plane and points forward, z lies in the symmetry plane and points downward, y from the right
# handrule
cellvalues = []
for column in list_of_hashes:
    column['Xb [m]'] = center_of_gravity.get('x') - column.get('y [m]')
    column['Yb [m]'] = center_of_gravity.get('y') - column.get('x [m]')
    column['Zb [m]'] = center_of_gravity.get('z') + column.get('z [m]')
    # format for cellupdate
    cellvalues.append([column['Xb [m]'], column['Yb [m]'], column['Zb [m]']])

# update the cells in the sheet
sheet.update('H2', cellvalues)
