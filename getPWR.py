# this is gonna get the mass estimate assuming the battery type
# dry mass of the spacecraft is 30 kg without batteries, including pld

import math

dryMass = 10
mass_per_unit = 2.2 # kg
cap = 12 # Ahr
V = 12 # V
A = 400 # Amps
time = 10 # sec

pwr = V*A
