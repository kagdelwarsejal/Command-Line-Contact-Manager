"""
@Author:   MaximilianEdison (MaxianEdison)
@Date:     2023-06-15 06:39:51
"""

import os
import sys
from typing import List

CLEAR_COMMAND = "cls" if sys.platform == "win32" else "clear"


class Contact:
    """Contact class."""

    def __init__(self, name: str, email: str, phone: str):
        self.name = name
        self.email = email
        self.phone = phone

    def get_name(self) -> str:
        return self.name

    def get_email(self) -> str:
        return self.email

    def get_phone(self) -> str:
        return self.phone

    def display(self) -> None:
        print(f"{self.name}, {self.email}, {self.phone}")

    @staticmethod
    def create_from_user_input() -> "Contact":
        """Create a Contact from user input."""
        while True:
            name = input("Enter name: ").strip()
            if name:
                break
            print("Name can't be empty. Please try again.")

        while True:
            email = input("Enter email: ").strip()
            if Contact.is_valid_email(email):
                break
            print("Invalid email format. Please try again.")

        while True:
            phone = input("Enter phone number: ").strip()
            if Contact.is_valid_phone_number(phone):
                break
            print("Invalid phone format. Please try again.")

        return Contact(name, email, phone)

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Validate email format."""
        return bool(email) and "@" in email

    @staticmethod
    def is_valid_phone_number(phone: str) -> bool:
        """Validate phone number format."""
        return bool(phone) and len(phone) >= 10


def clear_screen() -> None:
    """Clear terminal screen based on OS."""
    os.system(CLEAR_COMMAND)


def display_menu() -> None:
    """Display menu for user."""
    print("Contact List Manager")
    print("\nSelect an option:")
    print("1. Add new contact")
    print("2. List all contacts")
    print("3. Search for a contact")
    print("4. Update a contact")
    print("5. Delete a contact")
    print("6. Quit")


def add_contact(contacts: List[Contact]) -> None:
    """Add contact to contacts list."""
    clear_screen()
    print("Add a new Contact")
    contact = Contact.create_from_user_input()
    contacts.append(contact)
    print("\nContact added successfully!")


def list_contacts(contacts: List[Contact]) -> None:
    """List all contacts."""
    clear_screen()
    print("List of all contacts")
    for contact in contacts:
        contact.display()


def search_contact(contacts: List[Contact]) -> None:
    """Search for contacts."""
    clear_screen()
    print("Search for contact")
    search_term = input("Enter search term: ").strip()

    found = False
    print("\nSearch results:")
    for contact in contacts:
        if (search_term in contact.get_name() or
            search_term in contact.get_email() or
            search_term in contact.get_phone()):
            contact.display()
            found = True

    if not found:
        print("No matching contacts found.")


def update_contact(contacts: List[Contact]) -> None:
    """Update info for one contact."""
    clear_screen()
    print("Update contact")
    search_term = input("Enter the name of the contact to update: ").strip()

    found = False
    for i, contact in enumerate(contacts):
        if contact.get_name() == search_term:
            contacts[i] = Contact.create_from_user_input()
            print("\nContact updated successfully!")
            found = True
            break

    if not found:
        print("Contact not found.")


def delete_contact(contacts: List[Contact]) -> None:
    """Delete contact from contacts list."""
    clear_screen()
    print("Delete a contact")
    search_term = input("Enter the name of the contact to delete: ").strip()

    found = False
    for i, contact in enumerate(contacts):
        if contact.get_name() == search_term:
            contacts.pop(i)
            print("\nContact deleted successfully!")
            found = True
            break

    if not found:
        print("Contact not found.")


def save_contacts(contacts: List[Contact], filename: str) -> None:
    """Save contacts to disk."""
    try:
        with open(filename, "w") as file:
            for contact in contacts:
                file.write(f"{contact.get_name()},{contact.get_email()},{contact.get_phone()}\n")
    except IOError:
        print("Error opening file for writing.")


def load_contacts(filename: str) -> List[Contact]:
    """Load contacts from disk."""
    contacts = []

    try:
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()
                parts = line.split(",")
                if len(parts) == 3:
                    contacts.append(Contact(parts[0], parts[1], parts[2]))
    except IOError:
        pass

    return contacts


def main() -> None:
    """Main function."""
    filename = "contacts.csv"
    contacts = load_contacts(filename)

    while True:
        clear_screen()
        display_menu()
        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            add_contact(contacts)
        elif choice == "2":
            list_contacts(contacts)
        elif choice == "3":
            search_contact(contacts)
        elif choice == "4":
            update_contact(contacts)
        elif choice == "5":
            delete_contact(contacts)
        elif choice == "6":
            save_contacts(contacts, filename)
            clear_screen()
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()