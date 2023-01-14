import os

def clear_console():
    os.system("clear")

def menu():
    clear_console()
    print("Welcome to this TOTP generator.\nPlease choose an action\n\n1. Display OTP\n2. Set up new account\n")
    option = input()

    if option == "1":
        return 1
    elif option == "2":
        return 2
    else:
        menu()

def print_otp(service, otp):
    print("Account name: " + service)
    print("Current OTP: " + otp + "\n\n")

def add_service():
    clear_console()
    print("On this page you can add a new service to this app. Please enter the required information.\n\n")
    service = input("What is the name of the service (e.g. Facebook...)? ")
    seed = input("What is the secret given by the service? ")
    return [service, seed]