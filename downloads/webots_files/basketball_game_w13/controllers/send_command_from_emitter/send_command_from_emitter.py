from controller import Supervisor

def run_supervisor():
    # Create the Supervisor instance
    supervisor = Supervisor()

    # Get simulation time step
    timestep = int(supervisor.getBasicTimeStep())

    # Get the emitter for sending commands
    emitter = supervisor.getDevice("emitter")  # Ensure the emitter is defined in your world file
    if emitter is None:
        print("Error: Could not find emitter device")
        return

    # Main control loop
    while supervisor.step(timestep) != -1:

        # Send motor position command to the robot
        motor_position = 38 * 3.14159 / 180  # Motor position in radians
        message = f"SET_POSITION:{motor_position}"  # Construct the command message
        emitter.send(message.encode("utf-8"))  # Send the message via the emitter

if __name__ == "__main__":
    run_supervisor()