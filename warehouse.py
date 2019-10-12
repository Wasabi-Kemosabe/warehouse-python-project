from menu import print_menu
from Item import Item
import datetime
import pickle
import os

"""
Program: Warehouse Inventory Control System
Functionality:
    - Register new items
        - ID (auto generated)
        - Title
        - Category
        - Price
        - Stock
    - Print all the items
    - Update the stock of a selected item
    - Print items with no stock
    - Remove items
    - Print different categories
    - Print stock value (sum(price * stock))
    - Register purchase
    - Register sale
    - Log of events
        Time  |  Action  |  ID
        - Generate log string inside important functions
        - Add that string to logs array
        - Save logs array
        - Load logs array when system starts
"""

items = []
logs = []
id_count = 0
items_file = "item.data"
logs_file = "logs.data"


def clear():
    return os.system("clear")


def get_time():
    current_date = datetime.datetime.now()
    time = current_date.strftime("%X")
    return time


def save_items():
    # open creates/opens a file
    # wb = write binary info
    writer = open(items_file, "wb")
    # Converts the object into binary and writes it on the file
    pickle.dump(items, writer)
    writer.close()  # Closes the file stream (to release the file)
    print("Data saved")


def save_logs():
    # open creates/opens a file
    # wb = write binary info
    writer = open(logs_file, "wb")
    # Converts the object into binary and writes it on the file
    pickle.dump(logs, writer)
    writer.close()  # Closes the file stream (to release the file)
    print("Log saved")


def read_items():
    # Import variable into fn scope
    global id_count

    try:
        # rb = open the file and read the binary
        reader = open(items_file, "rb")
        # Read the binary and convert it to the original object
        temp_list = pickle.load(reader)

        for item in temp_list:
            items.append(item)

        last = items[-1]  # Indexed at the last item in an array
        id_count = last.id + 1
        print("Loaded: " + str(len(temp_list)) + " items")
    except:
        # You get here only if try block crashes
        print("Error: data could not be loaded")


def read_logs():
    try:
        # rb = open the file and read the binary
        reader = open(logs_file, "rb")
        # Read the binary and convert it to the original object
        temp_list = pickle.load(reader)

        for item in temp_list:
            logs.append(item)

        print("Loaded: " + str(len(temp_list)) + " log events")
    except:
        # You get here only if try block crashes
        print("Error: data could not be loaded")


def print_header(text):
    print('*' * 40)
    print(text)
    print('*' * 40)


def register_item():
    global id_count  # Here you are importing the global variable into the function scope

    print("\n\n\n")
    print_header('Register new item')
    title = input('Please type the title: ')
    category = input('Please type the category: ')
    price = float(input('Please type the price: '))
    stock = int(input('Please type the number of stock: '))

    # Validations

    new_item = Item()
    new_item.id = id_count
    new_item.title = title
    new_item.category = category
    new_item.price = price
    new_item.stock = stock

    id_count += 1
    items.append(new_item)
    log_line = get_time().ljust(11) + "| Register Item".ljust(23) + "| " + str(id_count)
    logs.append(log_line)
    save_logs()
    print('Item created')


def list_all(header_text):
    print("\n\n\n")
    print_header(header_text)
    print('-' * 90)
    print(
        'ID  | Item Title                | Category        | Price     | Stock')
    print('-' * 90)
    for item in items:
        print(str(item.id).ljust(3) + ' | ' + item.title.ljust(25) + ' | ' + item.category.ljust(15) + ' | ' +
              str(item.price).rjust(9) + ' | ' + str(item.stock).rjust(5))


def print_log():
    print("\n\n\n")
    print_header("Data Log")
    print('-' * 90)
    print(
        'Time       | Action               | ID     ')
    print('-' * 90)
    for item in logs:
        print(item)


def update_stock():
    # Show the user all the items
    list_all('Choose an item from the list')
    # Ask for the desired id
    id = input('\nSelect an ID to update stock: ')
    # Get the element from the array with that id
    found = False
    for item in items:
        if item.id == int(id):
            # Ask for the new stock
            stock = input('Please update the stock: ')
            # Update the stock of the element
            item.stock = stock
            found = True
            # Add registry to the log
            log_line = get_time().ljust(11) + "| Update Item".ljust(23) + "| " + id
            logs.append(log_line)
            save_logs()
    if not found:
        print("Error: ID doesn't exist")


def remove_item():
    # Show the user all the items
    list_all('Choose an item to remove from the list')
    # Ask for the desired id
    id = input('\nSelect an ID to remove stock: ')

    for item in items:
        if item.id == int(id):
            items.remove(item)
            print("Item has been removed")
            log_line = get_time().ljust(11) + "| Remove Item".ljust(23) + "| " + id
            logs.append(log_line)
            save_logs()


def no_stock():
    print("\n\n\n")
    print_header("Out of Stock Items")
    print('-' * 90)
    print(
        'ID  | Item Title                | Category        | Price     | Stock')
    print('-' * 90)
    for item in items:
        if item.stock == 0:
            print(str(item.id).ljust(3) + ' | ' + item.title.ljust(25) + ' | ' + item.category.ljust(15) + ' | ' +
                  str(item.price).rjust(9) + ' | ' + str(item.stock).rjust(5))
        else:
            print("******* Items are fully stocked *******".rjust(65))
            break


def print_categories():
    print("\n\n\n")
    print_header("Categories")
    list_of_categories = []
    for item in items:
        list_of_categories.append(item.category)
    categories = list(dict.fromkeys(list_of_categories))
    for category in categories:
        print(category + "\n")


def print_stock_value():
    total = 0.0
    for item in items:
        total += (item.price * float(item.stock))
    print("\n\n\n")
    print_header("Total Stock Value")
    print("$" + str(round(total, 2)))


def register_purchase():
    """
    Show the items
    Ask the user to select one
    Ask for the quantity in the order (purchase)
    Update the stock of the selected item
    """
    list_all('Choose an item for purchase to stock')
    id = input("Please select an ID: ")
    found = False
    for item in items:
        if item.id == int(id):
            order_qty = input("Please type how many to order: ")
            item.stock += int(order_qty)
            found = True
            log_line = get_time().ljust(11) + "| Purchase Item".ljust(23) + "| " + id
            logs.append(log_line)
            save_logs()
    if not found:
        print("Error: ID doesn't exist")


def register_sale():
    list_all('Scan ID for sale')
    id = input("Please scan an ID: ")
    found = False
    for item in items:
        if item.id == int(id):
            order_qty = input("Quantity sold: ")
            item.stock -= int(order_qty)
            found = True
            log_line = get_time().ljust(11) + "| Sold Item".ljust(23) + "| " + id
            logs.append(log_line)
            save_logs()
    if not found:
        print("Error: ID doesn't exist")


# Read previous data from the file to items array
read_items()
read_logs()

opc = ''

while opc != 'x':
    print_menu()

    opc = input('Please select an option: ')

    # Actions based on selected opc
    if opc == '1':
        register_item()
        save_items()
    elif opc == '2':
        list_all('List of all items')
    elif opc == '3':
        update_stock()
        save_items()
    elif opc == '4':
        no_stock()
    elif opc == '5':
        remove_item()
        save_items()
    elif opc == '6':
        print_categories()
    elif opc == '7':
        print_stock_value()
    elif opc == '8':
        register_purchase()
        save_items()
    elif opc == '9':
        register_sale()
        save_items()
    elif opc == '10':
        print_log()
    elif opc != 'x':
        input('\n\nPress enter to continue')
        clear()
