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

# Set column pins as input and pulled up high by default
GPIO.setup(COL_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(COL_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(COL_3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(COL_4, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# Function to read each row and each column
def readRow(line, characters, sum_value, output):
    GPIO.output(line, GPIO.LOW)

    if GPIO.input(COL_1) == GPIO.LOW:
        sum_value = sum_value * 10 + try_int(characters[0], sum_value)
        time.sleep(0.4)
        return sum_value, output

    elif GPIO.input(COL_2) == GPIO.LOW:
        sum_value = sum_value * 10 + try_int(characters[1], sum_value)
        time.sleep(0.4)
        return sum_value, output

    elif GPIO.input(COL_3) == GPIO.LOW:
        if characters[2] == "#":
            output = 1
            time.sleep(0.4)
            return sum_value, output
        else:
            sum_value = sum_value * 10 + try_int(characters[2], sum_value)
            time.sleep(0.4)
            return sum_value, output

    elif GPIO.input(COL_4) == GPIO.LOW:
        sum_value = sum_value * 10 + try_int(characters[3], sum_value)
        time.sleep(0.4)
        return sum_value, output

    GPIO.output(line, GPIO.HIGH)
    return sum_value, output


def try_int(value, default):
    try:
        return int(value)
    except ValueError:
        return default


# Endless loop by checking each row
def get_pin():
    try:
        sum_value = 0
        output = 0
        while True:
            sum_value, output = readRow(ROW_1, ["1", "2", "3", "A"], sum_value, output)
            sum_value, output = readRow(ROW_2, ["4", "5", "6", "B"], sum_value, output)
            sum_value, output = readRow(ROW_3, ["7", "8", "9", "C"], sum_value, output)
            sum_value, output = readRow(ROW_4, ["*", "0", "#", "D"], sum_value, output)
            if output == 1:
                temp = sum_value
                sum_value = 0
                output = 0
                return temp
            time.sleep(0.2)  # adjust this per your own setup
    except KeyboardInterrupt:
        print("\nKeypad Application Interrupted!")
        GPIO.cleanup()