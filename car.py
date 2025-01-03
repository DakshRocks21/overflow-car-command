import json
import asyncio
from dotenv import dotenv_values
from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosedError
import RPi.GPIO as GPIO


config = dotenv_values("config.env")
DRIVE_CONTROL_IP = config["DRIVE_CONTROL_IP"]
DRIVE_CONTROL_PORT = int(config["DRIVE_CONTROL_PORT"])

PWM_LEFT = 18 
PWM_RIGHT = 19  

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(PWM_LEFT, GPIO.OUT)
GPIO.setup(PWM_RIGHT, GPIO.OUT)

# Initialize PWM
pwm_left = GPIO.PWM(PWM_LEFT, 50)  
pwm_right = GPIO.PWM(PWM_RIGHT, 50) 
pwm_left.start(0)  
pwm_right.start(0) 

N_SPEED = 7.5
F_SPEED = 10
B_SPEED = 5

def turn_motor(motor, velocity):    
    speed = (velocity / 100 * 2.5) + 7.5
    
    print(motor, speed)
    if motor == "left":
        pwm_left.ChangeDutyCycle(speed)
    elif motor == "right":
        pwm_right.ChangeDutyCycle(speed)

def control_motors(angle, accelerate):
    """
    Control the motors based on angle (-90 to 90) and accelerate (-100 to 100).
    // This function took way too long to fine tune. Let's not change it.
    """
    if accelerate==0:
        turn_motor("left", 0)
        turn_motor("right", 0)
        return
    
    if angle<0:
        l_velocity = (10/9*angle+100)/100 * accelerate
        r_velocity = accelerate
    else:
        l_velocity = accelerate
        r_velocity = (-10/9*angle+100)/100 * accelerate
    
    turn_motor("left", l_velocity)
    turn_motor("right", r_velocity)
    return

async def handle_message(websocket):
    try:
        async for message in websocket:
            message_data = json.loads(message)
            angle = message_data["angle"]
            accelerate = message_data["accelerate"]

            print(f"Angle: {angle} \tAccelerate: {accelerate}")
            control_motors(angle, accelerate)
            

    except ConnectionClosedError:
        print("Connection to command server closed unexpectedly.")
    finally:
        # Stop the motors if the connection is lost
        control_motors(0, 0)

async def main():
    print("Starting server...")
    async with serve(handle_message, DRIVE_CONTROL_IP, DRIVE_CONTROL_PORT):
        await asyncio.Future() 

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        pwm_left.stop()
        pwm_right.stop()
        GPIO.cleanup()