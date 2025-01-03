import RPi.GPIO as GPIO
import time

PWM_PIN1 = 18 
PWM_PIN2 = 19  

GPIO.setmode(GPIO.BCM)
GPIO.setup(PWM_PIN1, GPIO.OUT)
GPIO.setup(PWM_PIN2, GPIO.OUT)

# Initialize PWM
pwm2 = GPIO.PWM(PWM_PIN2, 50) 
pwm1 = GPIO.PWM(PWM_PIN1, 50)  
pwm1.start(0)
pwm2.start(0)  

def set_pwm(pwm, duty_cycle):
    """Set the PWM signal for the given ESC."""
    pwm.ChangeDutyCycle(duty_cycle)

try:
    print("Starting ESC test...")
    print("Calibrating ESC 1 and ESC 2...")
    set_pwm(pwm1, 7.5) 
    set_pwm(pwm2, 7.5)  
    time.sleep(2)
    set_pwm(pwm1, 10)  
    set_pwm(pwm2, 10) 
    time.sleep(2)
    set_pwm(pwm1, 5) 
    set_pwm(pwm2, 5)
    time.sleep(2)

    print("Testing motors...")
    while True:
        # Increase speed
        for duty_cycle in range(5, 11):  # From neutral to full throttle
            print(f"Setting PWM to {duty_cycle * 10}% for both ESCs")
            set_pwm(pwm1, duty_cycle)
            set_pwm(pwm2, duty_cycle)
            time.sleep(1)

        # Decrease speed
        for duty_cycle in range(10, 4, -1):  # From full throttle to neutral
            print(f"Setting PWM to {duty_cycle * 10}% for both ESCs")
            set_pwm(pwm1, duty_cycle)
            set_pwm(pwm2, duty_cycle)
            time.sleep(1)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    pwm1.stop()
    pwm2.stop()
    GPIO.cleanup()
