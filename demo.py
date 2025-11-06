from models import (
    AddressBook, Record, Phone, Birthday,
    InvalidPhoneFormatError, PhoneNotFoundError, ContactNotFoundError
)
from datetime import date
from serialization_utils import save_data, load_data

if __name__ == "__main__":
    try:
        # Load the book (will be empty on first run)
        book = load_data() 
        print("--- 1. Додавання записів та Дня народження ---")
        
        # John with a birthday in the past and multiple phones
        john_record = Record("John")
        john_record.add_phone("1234567890")
        john_record.add_phone("5555555555")
        john_record.add_birthday("29.10.1985") # Day that requires shift from Sat/Sun if today is Oct 30th
        book.add_record(john_record)
        
        # Jane with upcoming birthday
        jane_record = Record("Jane")
        # Assuming current year is 2025 (October 30th)
        # Birthday on 01.11.2025 (Saturday), should shift to Monday 03.11.2025
        future_bday = date.today().replace(day=1, month=11)
        jane_record.add_birthday(future_bday.strftime("%d.%m.%Y"))
        jane_record.add_phone("9876543210")
        book.add_record(jane_record)
        
        # Bob with a phone only
        bob_record = Record("Bob")
        bob_record.add_phone("4444444444")
        book.add_record(bob_record)
        
        # Alice with an upcoming birthday not on weekend
        alice_bday = date.today().replace(day=3, month=11) # Monday
        alice_record = Record("Alice")
        alice_record.add_birthday(alice_bday.strftime("%d.%m.%Y"))
        book.add_record(alice_record)
        
        print("Всі контакти:")
        for name, record in book.data.items():
            print(record)
        print("-" * 30)

        print("--- 2. Редагування та Пошук Телефону ---")
        
        john = book.find("John")
        if john:
            john.edit_phone("1234567890", "1112223333")
            print(f"John updated: {john}")

            found_phone = john.find_phone("5555555555")
            print(f"John's found phone: {found_phone}")

            john.remove_phone("5555555555")
            print(f"John after removing phone: {john}")
        
        print("-" * 30)
        
        print("--- 3. Дні Народження на наступний тиждень ---")
        print(book.get_upcoming_birthdays())
        print("-" * 30)
        
        print("--- 4. Видалення ---")
        
        book.delete("Bob")
        print("Запис Bob видалено.")
        
        print("Всі контакти після видалення Bob:")
        for name, record in book.data.items():
            print(record)
        
        print("-" * 30)
        
        print("--- 5. Перевірка Винятків ---")
        try:
            # Invalid phone format
            john.add_phone("123")
        except InvalidPhoneFormatError as e:
            print(f"Успішно спіймано (Телефон): {e}")

        try:
            # Invalid birthday format
            john.add_birthday("30-01-2000")
        except ValueError as e:
            print(f"Успішно спіймано (Дата народження): {e}")

        try:
            # Non-existent phone
            john.remove_phone("0000000000")
        except PhoneNotFoundError as e:
            print(f"Успішно спіймано (Телефон не знайдено): {e}")
            
        try:
            # Non-existent contact
            book.delete("NonExisting")
        except ContactNotFoundError as e:
            print(f"Успішно спіймано (Контакт не знайдено): {e}")
            
    except Exception as e:
        print(f"Загальна помибка: {e}")
        
    finally:
        # Save the final state after all tests are done
        save_data(book)