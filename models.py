from collections import UserDict
from typing import List, Optional
from datetime import datetime
import calendar

class InvalidPhoneFormatError(Exception):
    pass

class ContactNotFoundError(Exception):
    pass

class PhoneNotFoundError(Exception):
    pass

class Field:
    def __init__(self, value):
        self._value = value

    def __str__(self):
        return str(self._value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

class Name(Field):
    pass

class Phone(Field):
    
    def __init__(self, value):
        self.value = value
        
    @Field.value.setter
    def value(self, new_value: str):
        if not (new_value.isdigit() and len(new_value) == 10):
            raise InvalidPhoneFormatError("Phone number must be 10 digits and contain only numbers.")
        super(Phone, Phone).value.__set__(self, new_value)

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        
    def __str__(self):
        return self.value.strftime("%d.%m.%Y")
    
    @Field.value.setter
    def value(self, new_value):
        if isinstance(new_value, str):
            try:
                self._value = datetime.strptime(new_value, "%d.%m.%Y").date()
            except ValueError:
                raise ValueError("Invalid date format. Use DD.MM.YYYY")
        else:
            self._value = new_value

class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: List['Phone'] = []
        self.birthday: Optional[Birthday] = None

    def __str__(self):
        phones_str = '; '.join(str(p) for p in self.phones)
        birthday_str = f", birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name}, phones: {phones_str}{birthday_str}"

    def add_phone(self, phone_number: str):
        if self.find_phone(phone_number):
            return
        phone = Phone(phone_number)
        self.phones.append(phone)

    def find_phone(self, phone_number: str) -> Optional['Phone']:
        for phone in self.phones:
            if str(phone) == phone_number:
                return phone
        return None

    def edit_phone(self, old_phone: str, new_phone: str):
        found_phone = self.find_phone(old_phone)
        
        if found_phone is None:
            raise PhoneNotFoundError(f"Phone {old_phone} not found in contact {self.name}.")
        
        found_phone.value = new_phone

    def remove_phone(self, phone_number: str):
        found_phone = self.find_phone(phone_number)
        
        if found_phone is None:
            raise PhoneNotFoundError(f"Phone {phone_number} not found in contact {self.name}.")
            
        self.phones.remove(found_phone)

    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)

class AddressBook(UserDict):
    
    def add_record(self, record: Record):
        self.data[str(record.name).lower()] = record

    def find(self, name: str) -> Optional[Record]:
        return self.data.get(name.lower())

    def delete(self, name: str):
        standardized_name = name.lower()
        if standardized_name in self.data:
            del self.data[standardized_name]
        else:
            raise ContactNotFoundError(f"Contact {name} not found in the address book.")

    def get_upcoming_birthdays(self, days: int = 7) -> str:
        upcoming_birthdays = {}
        today = datetime.now().date()
        
        for record in self.data.values():
            if record.birthday is None:
                continue
            
            birthday_date = record.birthday.value
            birthday_this_year = birthday_date.replace(year=today.year)

            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)
            
            delta = birthday_this_year - today
            
            if 0 <= delta.days < days:
                
                # Check for weekend and adjust
                if birthday_this_year.weekday() >= 5: # Saturday (5) or Sunday (6)
                    # Move to Monday (0)
                    days_until_monday = (7 - birthday_this_year.weekday()) % 7
                    birthday_this_year = birthday_this_year.replace(day=birthday_this_year.day + days_until_monday)
                
                day_of_week = birthday_this_year.strftime("%A")
                date_str = birthday_this_year.strftime("%d.%m.%Y")
                
                if day_of_week not in upcoming_birthdays:
                    upcoming_birthdays[day_of_week] = []
                
                upcoming_birthdays[day_of_week].append(f"{record.name} ({date_str})")
        
        if not upcoming_birthdays:
            return "No upcoming birthdays in the next week."

        result = "Upcoming birthdays:\n"
        
        # Define the order of days for sorting (starting from Monday)
        day_order = list(calendar.day_name) 

        # Sort by day of the week
        sorted_birthdays = sorted(
            upcoming_birthdays.items(), 
            key=lambda item: day_order.index(item[0])
        )
        
        for day, names in sorted_birthdays:
            result += f"{day}: {', '.join(names)}\n"
            
        return result.strip()