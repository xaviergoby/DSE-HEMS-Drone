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
#print(list_of_hashes)

#the data is stored in list of hashes as a list containing dict(ionarie)s by the import script

#calculate center of gravity using the weighted average
cgx = 0.0
cgy = 0.0
cgz = 0.0
mass = 0.0

for column in list_of_hashes:
    cgx = cgx + (column.get('mass [kg]')*column.get('x [m]'))
    cgy = cgy + (column.get('mass [kg]')*column.get('y [m]'))
    cgz = cgz + (column.get('mass [kg]')*column.get('z [m]'))
    mass = mass + column.get('mass [kg]')

center_of_gravity = (cgx/mass, cgy/mass, cgz/mass)

#update the corresponding cell Row 2 Column G
sheet.update_cell(2, 7, str(center_of_gravity[0])+","+str(center_of_gravity[1])+","+str(center_of_gravity[2]))

