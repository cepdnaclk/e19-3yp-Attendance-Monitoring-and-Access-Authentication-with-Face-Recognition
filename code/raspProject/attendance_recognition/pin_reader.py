import RPi.GPIO as GPIO
import time

# Set the Row Pins
ROW_1 = 17
ROW_2 = 27
ROW_3 = 22
ROW_4 = 5

# Set the Column Pins
COL_1 = 23
COL_2 = 24
COL_3 = 25
COL_4 = 16

GPIO.setwarnings(False)
# BCM numbering
GPIO.setmode(GPIO.BCM)

# Set Row pins as output
GPIO.setup(ROW_1, GPIO.OUT)
GPIO.setup(ROW_2, GPIO.OUT)
GPIO.setup(ROW_3, GPIO.OUT)
GPIO.setup(ROW_4, GPIO.OUT)

# Set column pins as input and Pulled up high by default
GPIO.setup(COL_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(COL_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(COL_3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(COL_4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Function to read each row and each column
def read_row(line, characters):
    GPIO.output(line, GPIO.LOW)
    pressed_keys = [GPIO.input(col) == GPIO.LOW for col in [COL_1, COL_2, COL_3, COL_4]]
    GPIO.output(line, GPIO.HIGH)
    return [char for char, pressed in zip(characters, pressed_keys) if pressed]

# Function to get a 4-digit PIN from the keypad
def get_pin_from_keypad():
    pin = []
    try:
        while len(pin) < 4:
            pin += read_row(ROW_1, ["1", "2", "3", "A"]) + read_row(ROW_2, ["4", "5", "6", "B"]) + \
                   read_row(ROW_3, ["7", "8", "9", "C"]) + read_row(ROW_4, ["*", "0", "#", "D"])
            time.sleep(0.2)  # Adjust this per your own setup
    except KeyboardInterrupt:
        print("\nKeypad Application Interrupted!")
    finally:
        GPIO.cleanup()
    return ''.join(pin[:4])
