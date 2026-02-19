import pytest
from unittest.mock import patch
from contact_manager import Contact, save_contacts, load_contacts, add_contact, search_contact, update_contact, delete_contact


class TestContact:
    def test_init(self):
        c = Contact("John Doe", "john@example.com", "1234567890")
        assert c.get_name() == "John Doe"
        assert c.get_email() == "john@example.com"
        assert c.get_phone() == "1234567890"

    def test_display(self, capsys):
        c = Contact("John Doe", "john@example.com", "1234567890")
        c.display()
        captured = capsys.readouterr()
        assert captured.out.strip() == "John Doe, john@example.com, 1234567890"

    def test_is_valid_email(self):
        assert Contact.is_valid_email("test@example.com") == True
        assert Contact.is_valid_email("") == False
        assert Contact.is_valid_email("invalid") == False
        assert Contact.is_valid_email("test@") == True  # Simple check, but according to code, as long as @ is present

    def test_is_valid_phone_number(self):
        assert Contact.is_valid_phone_number("1234567890") == True
        assert Contact.is_valid_phone_number("") == False
        assert Contact.is_valid_phone_number("123") == False  # Less than 10


def test_save_load_contacts(tmp_path):
    contacts = [
        Contact("John Doe", "john@example.com", "1234567890"),
        Contact("Jane Smith", "jane@example.com", "0987654321")
    ]
    filename = tmp_path / "test_contacts.csv"
    save_contacts(contacts, str(filename))
    loaded = load_contacts(str(filename))
    assert len(loaded) == 2
    assert loaded[0].get_name() == "John Doe"
    assert loaded[1].get_name() == "Jane Smith"


def test_add_contact(capsys):
    contacts = []
    with patch('builtins.input', side_effect=['John Doe', 'john@example.com', '1234567890']):
        add_contact(contacts)
    assert len(contacts) == 1
    assert contacts[0].get_name() == 'John Doe'
    captured = capsys.readouterr()
    assert "Contact added successfully!" in captured.out


def test_search_contact_found(capsys):
    contacts = [Contact("John Doe", "john@example.com", "1234567890")]
    with patch('builtins.input', return_value='John'):
        search_contact(contacts)
    captured = capsys.readouterr()
    assert "John Doe, john@example.com, 1234567890" in captured.out


def test_search_contact_not_found(capsys):
    contacts = [Contact("John Doe", "john@example.com", "1234567890")]
    with patch('builtins.input', return_value='Jane'):
        search_contact(contacts)
    captured = capsys.readouterr()
    assert "No matching contacts found." in captured.out


def test_update_contact(capsys):
    contacts = [Contact("John Doe", "john@example.com", "1234567890")]
    with patch('builtins.input', side_effect=['John Doe', 'Jane Smith', 'jane@example.com', '0987654321']):
        update_contact(contacts)
    assert contacts[0].get_name() == 'Jane Smith'
    captured = capsys.readouterr()
    assert "Contact updated successfully!" in captured.out


def test_update_contact_not_found(capsys):
    contacts = [Contact("John Doe", "john@example.com", "1234567890")]
    with patch('builtins.input', return_value='Jane'):
        update_contact(contacts)
    captured = capsys.readouterr()
    assert "Contact not found." in captured.out


def test_delete_contact(capsys):
    contacts = [Contact("John Doe", "john@example.com", "1234567890")]
    with patch('builtins.input', return_value='John Doe'):
        delete_contact(contacts)
    assert len(contacts) == 0
    captured = capsys.readouterr()
    assert "Contact deleted successfully!" in captured.out


def test_delete_contact_not_found(capsys):
    contacts = [Contact("John Doe", "john@example.com", "1234567890")]
    with patch('builtins.input', return_value='Jane'):
        delete_contact(contacts)
    captured = capsys.readouterr()
    assert "Contact not found." in captured.out