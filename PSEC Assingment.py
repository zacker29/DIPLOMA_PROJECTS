import hashlib
import datetime
import os
import msvcrt

# Saved data
services = { 
    1: {'name' : 'Firewall Service', 'price': 1200},
    2: {'name' : 'Security Ops Centre', 'price': 4200},
    3: {'name' : 'Hot Site', 'price': 8500},
    4: {'name' : 'Data Protection', 'price': 10000},
    5: {'name' : 'Premium Support', 'price': 15000},
}
user_data = {} # Add user_data dictionary to store user information
admin_logins = {'superadmin': hashlib.sha256('password123'.encode()).hexdigest()}
premium_users = {'user1': hashlib.sha256('password1'.encode()).hexdigest()}
login_logs = []
discount_codes = {'10': 10, '20': 20, '30': 30}

# Utility to clear the screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n" + "="*60)
    print(" " * 8 + "WELCOME TO ELECTRONIC SERVICES & PROTECTION")
    print("="*60)

# Custom password input to show asterisks
def input_password(prompt):
    print(prompt, end='', flush=True)
    password = ''
    while True:
        ch = msvcrt.getch()
        if ch in {b'\r', b'\n'}:  # Enter key pressed
            print('')
            break
        elif ch == b'\x08':  # Backspace key pressed
            if len(password) > 0:
                password = password[:-1]
                print('\b \b', end='', flush=True)
        else:
            password += ch.decode('utf-8')
            print('*', end='', flush=True)
    return password

# Display Main Menu
def display_main_menu():
    clear_screen()
    print("\n1. Customer Login")
    print("2. Premium Customer Login")
    print("3. Admin Login")
    print("4. Exit")
    print("="*60)
    return input("Enter your choice: ")

# Display Menu
def display_menu():
    clear_screen()
    print("""\n1. Display Services
             \n2. Search Service
             \n3. Add Service to Cart
             \n4. View Cart
             \n5. Modify Cart
             \n6. Apply Discount
             \n7. Payment
             \n0. Logout""")
    return input("Enter your choice: ")

def display_services():
    print("\n" + "-"*60)
    print("Services:")
    for id, service in services.items():
        print(f"NO {id}. {service['name']} : ${service['price']:.2f}k/year")
    print("-"*60 + "\n")
    
# Search Service
def search_service():
    query = input("Search for a service: ").lower()
    for id, service in services.items():
        if query in service['name'].lower():
            print(f"NO {id}. {service['name']} : ${service['price']/1000}k/year")

# Add Service into Cart
def add_to_cart(user):
    while True:
        display_services()
        service_id_input = input("Enter the service ID to add to cart (0 to stop): ")
        if not service_id_input.isdigit():
            print("Please enter a valid service ID (a number).")
            continue
        service_id = int(service_id_input)
        if service_id == 0:
            break
        if service_id in services:
            user_data[user]['cart'].append(services[service_id])
            print(f"Added {services[service_id]['name']} to cart.")
        else:
            print("Invalid service ID.")


# Display Cart
def display_cart(user):
    if user_data[user]['cart']:
        print("\nCart:")
        for idx, service in enumerate(user_data[user]['cart'], start=1):
            print(f"{idx}. {service['name']} : ${service['price']/1000}k/year")
    else:
        print("Your cart is empty.")

# Modify Cart
def modify_cart(user):
    if not user_data[user]['cart']:
        print("Your cart is empty.")
        return
    while True:
        display_cart(user)
        print("""\n1. Remove Item
                 \n2. Clear Cart
                 \n0. Back""")
        choice = input("Enter choice: ")
        if choice == '1':
            index = int(input("Enter item number to remove: ")) - 1
            if 0 <= index < len(user_data[user]['cart']):
                removed = user_data[user]['cart'].pop(index)
                print(f"Removed {removed['name']}")
            else:
                print("Invalid item number.")
        elif choice == '2':
            user_data[user]['cart'].clear()
            print("Cart cleared.")
        elif choice == '0':
            break

# Discount
def apply_discount(user):
    if user_data[user]['discount_applied']:
        print(f"Your services are already in {user_data[user]['discount_applied']}% discount.")
        return user_data[user]['discount_applied']
    
    code = input("Enter discount code: ")
    if code in discount_codes:
        discount = discount_codes[code]
        print(f"Discount code applied: {discount}% off")
        user_data[user]['discount_applied'] = discount
        return discount
    else:
        print("Invalid discount code.")
        return 0

# Compute Payment
def compute_payment(user, discount=0):
    if not user_data[user]['cart']:
        print("No services added.")
        return
    total = sum(y['price'] for y in user_data[user]['cart'])
    if discount:
        discounted_total = total - total * discount / 100
        print(f"Original Total: ${total/1000}k/year")
        print(f"Discounted Total: ${discounted_total/1000}k/year after {discount}% discount")
        print("\nServices in Cart with Discount:")
        for service in user_data[user]['cart']:
            discounted_price = service['price'] - service['price'] * discount / 100
            print(f"{service['name']} : Original ${service['price']/1000}k/year, Discounted ${discounted_price/1000}k/year")
    else:
        print(f"Total: ${total/1000}k/year")
        print("\nServices in Cart:")
        for service in user_data[user]['cart']:
            print(f"{service['name']} : ${service['price']/1000}k/year")

# Normal User Login
def normal_login():
    clear_screen()
    user = input("Enter username: ")
    if user:
        login_logs.append((user, "login", datetime.datetime.now()))
        normal_panel(user)
    else:
        print("Invalid credentials.")

def normal_panel(user):
    clear_screen()
    print(f"Welcome, {user}.")
    if user not in user_data:
        user_data[user] = {'cart': [], 'discount_applied': 0}
    while True:
        print("""\n1. Display Services
                 \n2. Search Service
                 \n3. Add Service to Cart 
                 \n4. View Cart 
                 \n5. Modify Cart
                 \n6. Apply Discount
                 \n7. Payment
                 \n0. Logout""")
        choice = input("Enter choice: ")
        clear_screen()
        if choice == '1':
            display_services()
        elif choice == '2':
            search_service()
        elif choice == '3':
            add_to_cart(user
    )
        elif choice == '4':
            display_cart(user)
        elif choice == '5':
            modify_cart(user)
        elif choice == '6':
            discount = apply_discount(user)
            compute_payment(user, discount)
        elif choice == '7':
            compute_payment(user)
        elif choice == '0':
            login_logs.append((user, "logout", datetime.datetime.now()))
            break

# Premium User Login
def premium_login():
    clear_screen()
    user = input("Enter username: ")
    if user in premium_users:
        password = input_password("Enter password: ")
        if premium_users[user] == hashlib.sha256(password.encode()).hexdigest():
            login_logs.append((user, "login", datetime.datetime.now()))
            premium_panel(user)
        else:
            print("Wrong username or password.")
            input("Press any key to continue...")
    else:
        print("Wrong username or password.")
        input("Press any key to continue...")

def premium_panel(user):
    clear_screen()
    print(f"Welcome, {user}. Services at 50% discount.")
    if user not in user_data:
        user_data[user] = {'cart': [], 'discount_applied': 50}
    while True:
        print("""\n1. Display Services
                 \n2. Search Service
                 \n3. Add Service to Cart 
                 \n4. View Cart 
                 \n5. Modify Cart
                 \n6. Payment (50% Off) 
                 \n0. Logout""")
        choice = input("Enter choice: ")
        clear_screen()
        if choice == '1':
            display_services()
        elif choice == '2':
            search_service()
        elif choice == '3':
            add_to_cart(user)
        elif choice == '4':
            display_cart(user)
        elif choice == '5':
            modify_cart(user)
        elif choice == '6':
            compute_payment(user, 50)
        elif choice == '0':
            login_logs.append((user, "logout", datetime.datetime.now()))
            break

# Admin Functions
def admin_login():
    clear_screen()
    user = input("Enter username: ")
    password = input_password("Enter password: ")
    if user == 'superadmin' and admin_logins.get(user) == hashlib.sha256(password.encode()).hexdigest():
        admin_panel()
    else:
        print("Wrong username or password.")
        input("Press any key to continue...")

def admin_panel():
    clear_screen()
    while True:
        print("""\n1. Add Service
                 \n2. View Logs 
                 \n3. Clear Logs
                 \n0. Logout""")
        choice = input("Enter choice: ")
        clear_screen()
        if choice == '1':
            add_service()
        elif choice == '2':
            view_logs()
        elif choice == '3':
            clear_logs()
        elif choice == '0':
            break
def add_service():
    name = input("Enter service name: ")
    while True:
        price_input = input("Enter price: ")
        try:
            price = float(price_input)
            break
        except ValueError:
            print("Please enter a valid price (a number).")
    id = max(services.keys()) + 1
    services[id] = {'name': name, 'price': price}
    print(f"Service '{name}' added with price ${price:.2f}.")

def view_logs():
    for log in login_logs:
        print(f"{log[0]}, {log[1]}, {log[2].strftime('%H:%M %Y-%m-%d')}")
    input("Press any key to continue...")

def clear_logs():
    login_logs.clear()
    print("Logs cleared.")

# Main function
def main():
    while True:
        choice = display_main_menu()
        if choice == '1':
            # Normal User Login
            normal_login()
        elif choice == '2':
            # Premium Customer Login
            premium_login()
        elif choice == '3':
            # Admin Login
            admin_login()
        elif choice == '4':
            break

main()