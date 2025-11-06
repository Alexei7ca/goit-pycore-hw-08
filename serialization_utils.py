import pickle
from models import AddressBook

FILENAME = "addressbook.pkl"

def save_data(book: AddressBook):
    with open(FILENAME, "wb") as f:
        pickle.dump(book, f)

def load_data() -> AddressBook:
    try:
        with open(FILENAME, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()