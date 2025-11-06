from typing import Dict, List, Callable, Tuple
from models import AddressBook, Record, InvalidPhoneFormatError, ContactNotFoundError, PhoneNotFoundError, Birthday
from datetime import datetime
from serialization_utils import save_data, load_data

def input_error(func: Callable) -> Callable:
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, IndexError) as e:
            if "not enough values to unpack" in str(e) or "Invalid format" in str(e):
                return "Invalid command format."
            return f"Invalid format or data: {e}"
        except KeyError:
            return "Contact not found."
        except InvalidPhoneFormatError as e:
            return str(e)
        except ContactNotFoundError as e:
            return str(e)
        except PhoneNotFoundError as e:
            return str(e)
    return inner

def parse_input(user_input: str) -> Tuple[str, List[str]]:
    parts = user_input.split()
    
    if not parts:
        return "", []
        
    cmd = parts[0].strip().lower()
    args = parts[1:]
    
    # Handle multi-word commands
    if cmd == "show-birthday" and not args:
        return cmd, args
    elif cmd == "add-birthday" and len(parts) >= 3:
        return cmd, parts[1:]
    elif cmd == "show" and len(parts) >= 2 and parts[1].lower() == "birthday":
        return "show-birthday", parts[2:]
    elif cmd == "add" and len(parts) >= 2 and parts[1].lower() == "birthday":
        return "add-birthday", parts[2:]
    elif cmd == "show" and parts[1].lower() == "all":
        return "all", []
    
    return cmd, args

@input_error
def add_contact(args: List[str], book: AddressBook) -> str:
    if len(args) < 2:
        raise ValueError("Invalid format. Command requires a name and phone number.")

    name, phone, *_ = args
    record = book.find(name)
    message = "Phone added to existing contact."
    
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    
    record.add_phone(phone)
    return message

@input_error
def change_contact(args: List[str], book: AddressBook) -> str:
    if len(args) < 3:
        raise ValueError("Invalid format. Command requires a name, old phone, and new phone.")

    name, old_phone, new_phone, *_ = args
    record = book.find(name)

    if record is None:
        raise ContactNotFoundError(f"Contact '{name}' not found.")

    record.edit_phone(old_phone, new_phone)
    return "Contact updated."

@input_error
def show_phone(args: List[str], book: AddressBook) -> str:
    if len(args) < 1:
        raise ValueError("Invalid format. Command requires a name.")

    name = args[0]
    record = book.find(name)

    if record is None:
        raise ContactNotFoundError(f"Contact '{name}' not found.")
    
    if not record.phones:
        return f"Contact {name} has no phone numbers."

    phones_str = '; '.join(str(p) for p in record.phones)
    return f"{record.name}: {phones_str}"

def show_all(book: AddressBook) -> str:
    if not book.data:
        return "The address book is empty."
        
    result = "All contacts:\n"

    for record in book.data.values():
        result += f"{record}\n"
            
    return result.strip()

@input_error
def add_birthday(args: List[str], book: AddressBook) -> str:
    if len(args) < 2:
        raise ValueError("Invalid format. Command requires a name and birthday (DD.MM.YYYY).")
        
    name, birthday_str, *_ = args
    record = book.find(name)
    
    if record is None:
        raise ContactNotFoundError(f"Contact '{name}' not found. Add the contact first.")
    
    record.add_birthday(birthday_str)
    return "Birthday added."

@input_error
def show_birthday(args: List[str], book: AddressBook) -> str:
    if len(args) < 1:
        raise ValueError("Invalid format. Command requires a name.")
        
    name = args[0]
    record = book.find(name)

    if record is None:
        raise ContactNotFoundError(f"Contact '{name}' not found.")

    if record.birthday:
        return f"{record.name}'s birthday: {record.birthday}"
    else:
        return f"Contact {record.name} has no birthday recorded."

def upcoming_birthdays(book: AddressBook) -> str:
    return book.get_upcoming_birthdays()

def hello_command() -> str:
    manual = """
Hello! How can I help you? Here are the available commands:

| Command | Arguments                  | Example                      | Description                                 |
| :------ | :------------------------- | :--------------------------- | :------------------------------------------ |
| hello   |                            | hello                        | Displays this manual.                       |
| add     | <Name> <Phone>             | add John 1234567890          | Adds contact or phone.                      |
| change  | <Name> <Old Phone> <New P> | change John 1234567890 098.. | Updates existing contact's phone.           |
| phone   | <Name>                     | phone John                   | Shows the contact's phone numbers.          |
| all     |                            | all                          | Lists all saved contacts.                   |
| add-birthday| <Name> <DD.MM.YYYY>    | add-birthday John 01.01.1990 | Adds birthday to contact.                   |
| show-birthday| <Name>                | show-birthday John           | Shows the contact's birthday.               |
| birthdays|                           | birthdays                    | Shows upcoming birthdays next week.         |
| close   |                            | close                        | Exits the chat.                             |
| exit    |                            | exit                         | Exits the chat.                             |
"""
    return manual

def main():
    book = load_data()
    
    print("Welcome to the assistant bot! Enter 'hello' to start")
    
    commands_map = {
        "hello": hello_command,
        "add": add_contact,
        "change": change_contact,
        "phone": show_phone,
        "all": show_all,
        "add-birthday": add_birthday,
        "show-birthday": show_birthday,
        "birthdays": upcoming_birthdays,
    }

    while True:
        try:
            user_input = input("Enter a command: ").strip()
        except EOFError:
            print("\nGood bye!")
            save_data(book)
            break

        if not user_input:
            continue
            
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            save_data(book)
            break
        
        handler = commands_map.get(command)

        if handler:
            if command in ["hello", "all", "birthdays"]:
                # Commands that only take the book (or no args)
                if command == "hello":
                    print(handler())
                elif command == "all" or command == "birthdays":
                    print(handler(book))
            else:
                # Commands that take args and the book
                print(handler(args, book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()