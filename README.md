# 🤖 Contact Assistant Bot

A command-line interface (CLI) application built in Python to manage personal contacts, including phone numbers, custom fields, and birthday tracking with persistence across sessions.

---

## ✨ Features

This project implements a robust address book system with the following capabilities:

* **Custom Class Structure:** Uses a hierarchical class structure (`Field`, `Name`, `Phone`, `Birthday`, `Record`, `AddressBook`) to ensure data integrity and object-oriented design.
* **Data Validation:** Phone numbers are strictly validated (10 digits, numeric only), and birthdays require a specific `DD.MM.YYYY` format.
* **Persistence:** Data is automatically **saved to disk** using the **`pickle`** serialization protocol upon exiting the application and automatically **loaded** upon startup.
* **Error Handling:** Robust command parsing and exception handling ensure a stable user experience.
* **Upcoming Birthday Tracking:** Calculates and lists contacts whose birthdays are coming up within the next **7 days**, automatically shifting weekend birthdays to the following Monday.

---

## 🛠️ Project Setup and Installation

Follow these steps to set up and run the project locally on macOS.

1.  **Clone the Repository (or Navigate to Folder):**
    ```bash
    cd [project-directory]
    ```

2.  **Create and Activate Virtual Environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Run the Application:**
    The application will automatically load data from `addressbook.pkl` if it exists, or start with an empty address book otherwise.
    ```bash
    python3 main.py
    ```

---

## 📖 Usage and Commands

When the bot starts, enter `hello` to view the full list of commands.

## 📁 File Structure

The project is divided into three key modules:

| File | Description |
| :--- | :--- |
| `main.py` | Contains the main command loop, command handling logic, and the integration points for persistence (`load_data` and `save_data`). |
| `models.py` | Defines the core data structures: `Field`, `Name`, `Phone`, `Birthday`, `Record`, and the `AddressBook` class (based on `UserDict`). Also includes custom exception classes. |
| `serialization_utils.py` | Contains the helper functions (`save_data`, `load_data`) responsible for serializing and deserializing the `AddressBook` object using the `pickle` protocol. |
| `demo.py` | A utility script used to test the functional correctness of the `models.py` classes and to write initial data to `addressbook.pkl`. |
| `addressbook.pkl` | **(Generated File)** The binary file used to store the serialized `AddressBook` data. |