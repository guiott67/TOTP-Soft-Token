from otp import totpToken
from ui import clear_console, menu, print_otp, add_service
import time

# Open file storing seeds
memory = open("keys.secret", "a+")

# Write seed and description in memory file
def store_seed(list):
    memory.write(list[0] + ":" + list[1] + "\n")

# Read memory file and put data in Python array
def read_storage():
    memory.seek(0)
    list = memory.readlines()
    result = []
    for i in range (len(list)):
        service = list[i]
        service = service[:-1]
        result.append (service.split(":"))
    return result

# Display TOTPs from stored seeds
# This function uses ui module to print information
def display_otp():
    clear_console()
    storage = read_storage()
    for i in range(len(storage)):
        print_otp(storage[i][0], str(totpToken(storage[i][1])))

# Call display_otp function in a loop, which ensures that the codes displayed are always valid.
def show_otp_loop():
    display_otp()
    old_time = int(time.time())//30
    while True:
        if old_time != int(time.time())//30:
            old_time = int(time.time())//30
            display_otp()
        else:
            time.sleep(1)

# Initiate app
while True:
    action = menu()
    if action == 1:
        show_otp_loop()
    elif action == 2:
        store_seed(add_service())