import json
from collections import defaultdict, Counter

DATA_FILE = 'library_data.json'

# ---------------------- Data Persistence ----------------------

def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'books': {}, 'borrowed': {}, 'stats': {}}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# ---------------------- Core Functions ----------------------

def add_book(data):
    book_id = input("Enter Book ID: ")
    title = input("Enter Book Title: ")
    author = input("Enter Author: ")
    quantity = int(input("Enter Quantity: "))

    data['books'][book_id] = {
        'title': title,
        'author': author,
        'quantity': quantity,
        'available': quantity
    }
    save_data(data)
    print(f"\nBook '{title}' added.\n")

def remove_book(data):
    book_id = input("Enter Book ID to remove: ")
    if book_id in data['books']:
        del data['books'][book_id]
        save_data(data)
        print("Book removed.\n")
    else:
        print("Book not found.\n")

def issue_book(data):
    user = input("Enter Borrower Name: ")
    book_id = input("Enter Book ID to issue: ")

    if book_id not in data['books']:
        print("Book not found.\n")
        return

    if data['books'][book_id]['available'] <= 0:
        print("No copies available.\n")
        return

    data['books'][book_id]['available'] -= 1
    data['borrowed'].setdefault(user, []).append(book_id)
    data['stats'][book_id] = data['stats'].get(book_id, 0) + 1

    save_data(data)
    print(f"Book issued to {user}.\n")

def return_book(data):
    user = input("Enter Borrower Name: ")
    book_id = input("Enter Book ID to return: ")

    if user in data['borrowed'] and book_id in data['borrowed'][user]:
        data['borrowed'][user].remove(book_id)
        data['books'][book_id]['available'] += 1
        save_data(data)
        print("Book returned.\n")
    else:
        print("Invalid return. Check borrower and book.\n")

def list_books(data):
    print("\n--- Book Inventory ---")
    for book_id, info in data['books'].items():
        print(f"[{book_id}] {info['title']} by {info['author']} - {info['available']}/{info['quantity']} available")
    print()

def list_borrowers(data):
    print("\n--- Borrowers ---")
    for user, books in data['borrowed'].items():
        print(f"{user} -> {books}")
    print()

def view_usage(data):
    print("\n--- Most Borrowed Books ---")
    stats = Counter(data['stats'])
    for book_id, count in stats.most_common():
        title = data['books'].get(book_id, {}).get('title', 'Unknown')
        print(f"{title} (ID: {book_id}) - Borrowed {count} times")
    print()

# ---------------------- Main Menu ----------------------

def main():
    data = load_data()

    menu = """
Library Management System

1. Add Book
2. Remove Book
3. Issue Book
4. Return Book
5. View Book Inventory
6. View Borrowers
7. View Usage Statistics
8. Exit
"""
    while True:
        print(menu)
        choice = input("Enter choice: ")

        if choice == '1':
            add_book(data)
        elif choice == '2':
            remove_book(data)
        elif choice == '3':
            issue_book(data)
        elif choice == '4':
            return_book(data)
        elif choice == '5':
            list_books(data)
        elif choice == '6':
            list_borrowers(data)
        elif choice == '7':
            view_usage(data)
        elif choice == '8':
            print("Exiting...")
            break
        else:
            print("Invalid choice.\n")

if __name__ == "__main__":
    main()
