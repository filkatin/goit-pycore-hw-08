import pickle
from functools import wraps
from book import AddressBook, Record

CONTACTS_FILE = "address_book.pkl"

def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ").strip().lower()
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            response = add_contact(args, book)
            print(response)

        elif command == "change":
            response = change_contact(args, book)
            print(response)

        elif command == "phone":
            response = show_phone(args, book)
            print(response)

        elif command == "all":
            response = show_all_contacts(book)
            print(response)

        elif command == "add-birthday":
            response = add_birthday(args, book)
            print(response)

        elif command == "show-birthday":
            response = show_birthday(args, book)
            print(response)

        elif command == "birthdays":
            response = birthdays(book)
            print(response)

        else:
            print("Invalid command.")

def input_error(handler):
    @wraps(handler)
    def wrapper(*args, **kwargs):
        try:
            return handler(*args, **kwargs)
        except KeyError as e:
            return f"Error: {e} not found."
        except ValueError as e:
            return f"Error: {e}"
        except IndexError:
            return "Error: Missing required arguments."
        except Exception as e:
            return f"Unexpected error: {e}"
    return wrapper

@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    return cmd, *args

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    if record:
        if record.phones:
            record.edit_phone(record.phones[0].value, phone)
            message = "Contact changed."
        else:
            record.add_phone(phone)
            message = "Phone added to contact."
    else:
        message = "Contact not found."
    return message

@input_error
def show_phone(args, book):
    name, *_ = args
    record = book.find(name)
    if record:
        phones = ', '.join(phone.value for phone in record.phones)
        return f"{record.name.value}: {phones}"
    return "Contact not found."

@input_error
def show_all_contacts(book):
    if not book:
        return "No contacts found."
    return "\n".join(f"{name}: {phone}" for name, phone in book.items())

@input_error
def add_birthday(args, book):
    name, birthday, *_ = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    return "Contact not found."

@input_error
def show_birthday(args, book):
    name, *_ = args
    record = book.find(name)
    if record and record.birthday:
        return f"{record.name.value}'s birthday \
            is on {record.birthday.value.strftime('%d.%m.%Y')}"
    return "Contact or birthday not found."

@input_error
def birthdays(book):
    upcoming_birthdays = book.get_upcoming_birthdays(7)
    if upcoming_birthdays:
        return "\n".join([record.name.value + " " \
            + record.birthday.value.strftime('%d.%m.%Y') for record in upcoming_birthdays])
    else:
        return "No upcoming birthdays."

def save_data(book, filename=CONTACTS_FILE):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename=CONTACTS_FILE):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()

if __name__ == "__main__":
    main()