import json
import asyncio
from dotenv import dotenv_values
from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosedError
import RPi.GPIO as GPIO

# Load configuration
config = dotenv_values("config.env")
DRIVE_CONTROL_IP = config["DRIVE_CONTROL_IP"]
DRIVE_CONTROL_PORT = int(config["DRIVE_CONTROL_PORT"])

# GPIO pin definitions
PWM_RIGHT = 18  # Left motor PWM control
PWM_LEFT = 12  # Right motor PWM control

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(PWM_LEFT, GPIO.OUT)
GPIO.setup(PWM_RIGHT, GPIO.OUT)

# Initialize PWM
pwm_left = GPIO.PWM(PWM_LEFT, 50)  # 50 Hz for ESC
pwm_right = GPIO.PWM(PWM_RIGHT, 50)  # 50 Hz for ESC
pwm_left.start(0)  # Start with 0% duty cycle
pwm_right.start(0)  # Start with 0% duty cycle


N_SPEED = 7.5
MAX_SPEED_DIFF = 2.5
F_SPEED = N_SPEED + MAX_SPEED_DIFF
B_SPEED = N_SPEED - MAX_SPEED_DIFF

def turn_motor(motor, velocity):    
    speed = (velocity / 100 * MAX_SPEED_DIFF) + N_SPEED
    
    print(motor, velocity, speed)
    
    if motor == "left":
        pwm_left.ChangeDutyCycle(speed)
    elif motor == "right":
        pwm_right.ChangeDutyCycle(speed * -1 + 15) # Correct reversed motor


def control_motors(angle, accelerate):
    """
    Control the motors based on angle (-90 to 90) and accelerate (-100 to 100).
    This version applies a non-linear curve for more sensitive turning.
    """
    if accelerate == 0:
        turn_motor("left", 0)
        turn_motor("right", 0)
        return

    # Normalize angle to a range of -1 to 1
    normalized_angle = angle / 90.0

    # Apply a cubic function for non-linear sensitivity
    curve_factor = normalized_angle ** 3

    if normalized_angle > 0:
        # For positive angles (right turns)
        l_velocity = accelerate
        r_velocity = accelerate * (1 - abs(curve_factor)) * 1.1
    elif normalized_angle < 0:
        # For negative angles (left turns)
        l_velocity = accelerate * (1 - abs(curve_factor))
        r_velocity = accelerate * 1.1
    else:
        # For straight motion
        l_velocity = accelerate
        r_velocity = accelerate * 1.3

    # Ensure velocities remain within bounds
    l_velocity = max(-100, min(100, l_velocity))
    r_velocity = max(-100, min(100, r_velocity))

    turn_motor("left", l_velocity)
    turn_motor("right", r_velocity)
    return

async def handle_message(websocket):
    try:
        async for message in websocket:
            message_data = json.loads(message)
            angle = message_data["angle"]
            accelerate = message_data["accelerate"]

            #print(f"Angle: {angle} \tAccelerate: {accelerate}")
            control_motors(angle, accelerate)
            

    except ConnectionClosedError:
        print("Connection to command server closed unexpectedly.")
    finally:
        # Stop the motors if the connection is lost
        control_motors(0, 0)

async def main():
    print("Starting server...")
    async with serve(handle_message, DRIVE_CONTROL_IP, DRIVE_CONTROL_PORT):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        pwm_left.stop()
        pwm_right.stop()
        GPIO.cleanup()
