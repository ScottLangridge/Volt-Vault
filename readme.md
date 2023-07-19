# Volt Vault
The Volt Vault is a place for storing stats about your drone flights and LiPo batteries. It will allow you to monitor stats such as:
- How many cycles each battery has been run through
- Which batteries have been allowed to dip to dangerous levels in the past
- Which batteries perform best
- How quickly your chargers charge

# Interfaces
## Charge Logger
Set up a charge session, tell the software which batteries you are charging, which charger you are ch

# Tables
## Battery
- id
- code
- cell_count
- capacity

## Drone
- id
- name
- prop_size

## Charger
- id
- name
- min_output_voltage
- max_output_voltage
- min_output_current
- max_output_current

## Power Source
- id
- name

## Flight
- id
- datetime
- drone
- battery
- initial_volts
- final_volts
- min_volts
- armed_time
- total_time

## Charge Session
- id
- batteries
- charger
- power_source

## Charge Value
- id
- charge_session_id
- datetime
- value
