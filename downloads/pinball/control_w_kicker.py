# pip install pyzmq cbor keyboard
from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import keyboard

# Connecting to the CoppeliaSim server
client = RemoteAPIClient('localhost', 23000)

print('Program started')
sim = client.getObject('sim')

# Get the handle for the slider (prismatic joint)
#cw= sim.getObject('/cw_joint')
#hccw= sim.getObject('/ccw_joint')
kicker= sim.getObject('/kicker_joint')

# Starting the simulation
sim.startSimulation()
print('Simulation started')

# Main control loop
def main():
    # Keep running until simulation is stopped
    while True:
        if keyboard.is_pressed('p'):  # Move slider to -0.15 position
            print("p is pressed")
            sim.setJointTargetPosition(cw, -0.25)
        
        if keyboard.is_pressed('l'):  # Reset slider to the original position
            print("l is pressed")
            sim.setJointTargetPosition(cw, 0.0)  # Reset to the initial position
            
        if keyboard.is_pressed('w'):  # Move slider to -0.15 position
            print("w is pressed")
            sim.setJointTargetPosition(ccw, -0.28)
        
        if keyboard.is_pressed('s'):  # Reset slider to the original position
            print("s is pressed")
            sim.setJointTargetPosition(ccw, 0.0)  # Reset to the initial position
            
        if keyboard.is_pressed('h'):  # set kicker to shot
            print("h is pressed")
            sim.setJointTargetPosition(kicker, 0.3)
            
        if keyboard.is_pressed('b'):  # set kicker to shot
            print("h is pressed")
            sim.setJointTargetPosition(kicker, 0.0)

        if keyboard.is_pressed('t'):  # Stop the simulation when 'q' is pressed
            print("t is pressed - stopping simulation")
            sim.stopSimulation()
            break

# Start the main control loop
main()
