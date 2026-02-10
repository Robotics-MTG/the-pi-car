from time import sleep
import RPi.GPIO as GPIO
PWM = GPIO.PWM

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# PWM Frequency
PWM_FREQUENCY = 100

# Setup GPIO for Motor A
MOTOR_A_PWM_PIN = 12
MOTOR_A_DIR_PIN1 = 16
MOTOR_A_DIR_PIN2 = 18

# Setup GPIO for Motor B
MOTOR_B_PWM_PIN = 11
MOTOR_B_DIR_PIN1 = 15
MOTOR_B_DIR_PIN2 = 13

# Motor driver standby/enable pin
MOTOR_ENABLE_PIN = 22

# Setup GPIO pins
GPIO.setup(MOTOR_A_PWM_PIN, GPIO.OUT)
GPIO.setup(MOTOR_A_DIR_PIN1, GPIO.OUT)
GPIO.setup(MOTOR_A_DIR_PIN2, GPIO.OUT)

GPIO.setup(MOTOR_B_PWM_PIN, GPIO.OUT)
GPIO.setup(MOTOR_B_DIR_PIN1, GPIO.OUT)
GPIO.setup(MOTOR_B_DIR_PIN2, GPIO.OUT)

GPIO.setup(MOTOR_ENABLE_PIN, GPIO.OUT)

motor_config = {
    'A': {
        'PWM': PWM(MOTOR_A_PWM_PIN, PWM_FREQUENCY),
        'DIR_PIN1': MOTOR_A_DIR_PIN1,
        'DIR_PIN2': MOTOR_A_DIR_PIN2
    },
    'B': {
        'PWM': PWM(MOTOR_B_PWM_PIN, PWM_FREQUENCY),
        'DIR_PIN1': MOTOR_B_DIR_PIN1,
        'DIR_PIN2': MOTOR_B_DIR_PIN2
    }
}

# Initialize PWM
for motor_data in motor_config.values():
    motor_data['PWM'].start(0)  # Start with 0% duty cycle

# Direction constants
DIRECTION_FORWARD = 0
DIRECTION_REVERSE = 1

def move_motor_forward(motor_id, speed_percent):
    """Move specified motor forward at given speed"""
    run_motor(motor_id, speed_percent, DIRECTION_FORWARD)

def move_motor_reverse(motor_id, speed_percent):
	"""Move specified motor in reverse at given speed"""
	run_motor(motor_id, speed_percent, DIRECTION_REVERSE)
    
def run_motor(motor_id, speed_percent, direction):
    """Run motor with specified speed and direction"""
    # Enable motor driver
    GPIO.output(MOTOR_ENABLE_PIN, GPIO.HIGH)
    
    # Set direction pins based on direction
    if direction == DIRECTION_FORWARD:
        dir_pin1_state = GPIO.HIGH
        dir_pin2_state = GPIO.LOW
    else:  # DIRECTION_REVERSE
        dir_pin1_state = GPIO.LOW
        dir_pin2_state = GPIO.HIGH
        
    GPIO.output(motor_config[motor_id]['DIR_PIN1'], dir_pin1_state)
    GPIO.output(motor_config[motor_id]['DIR_PIN2'], dir_pin2_state)
    motor_config[motor_id]['PWM'].ChangeDutyCycle(speed_percent)

def stop_all_motors():
    """Stop all motors and disable motor driver"""
    for motor_data in motor_config.values():
        motor_data['PWM'].ChangeDutyCycle(0)
    GPIO.output(MOTOR_ENABLE_PIN, GPIO.LOW)

def cleanup_gpio():
    """Clean up GPIO resources"""
    stop_all_motors()
    for motor_data in motor_config.values():
        motor_data['PWM'].stop()
    GPIO.cleanup()

def main(args=None):
    try:
        while True:
            # Move both motors forward
            move_motor_forward('A', 50)
            move_motor_forward('B', 50)
            sleep(2)
            
            # Stop motors
            stop_all_motors()
            sleep(1)  # Add pause between cycles
            
    except KeyboardInterrupt:
        print("Program interrupted")
    finally:
        cleanup_gpio()
        
if __name__ == "__main__":
    main()