"""
Lab 2.2 - Contact Manager

Two implementations:
- Array-based (using Python list)
- Linked List-based (custom Node + LinkedList)

Both support:
- add_contact(name, phone)
- search_contact(name)
- delete_contact(name)
- display_contacts()

This file also includes a simple menu-driven CLI
to test both implementations.
"""


class Contact:
    """
    Simple data class to store contact information.
    """

    def __init__(self, name: str, phone: str):
        self.name = name
        self.phone = phone

    def __str__(self) -> str:
        return f"{self.name} - {self.phone}"


class ArrayContactManager:
    """
    Contact manager that stores contacts in a Python list.
    Each contact is an instance of the Contact class.
    """

    def __init__(self):
        # Using a list (array) to store contacts
        self.contacts = []

    def add_contact(self, name: str, phone: str) -> None:
        """
        Add a new contact to the list.
        If a contact with the same name exists, we update the phone.
        """
        for contact in self.contacts:
            if contact.name == name:
                contact.phone = phone
                print(f"Updated existing contact: {contact}")
                return

        new_contact = Contact(name, phone)
        self.contacts.append(new_contact)
        print(f"Added new contact: {new_contact}")

    def search_contact(self, name: str):
        """
        Linear search for a contact by name.
        Returns the Contact object if found, otherwise None.
        """
        for contact in self.contacts:
            if contact.name == name:
                return contact
        return None

    def delete_contact(self, name: str) -> bool:
        """
        Delete a contact by name.
        Returns True if deletion was successful, False otherwise.
        """
        for i, contact in enumerate(self.contacts):
            if contact.name == name:
                del self.contacts[i]
                print(f"Deleted contact: {name}")
                return True

        print(f"Contact not found: {name}")
        return False

    def display_contacts(self) -> None:
        """
        Print all contacts in the list.
        """
        if not self.contacts:
            print("No contacts to display.")
            return

        print("Contacts (Array-based):")
        for contact in self.contacts:
            print(f"- {contact}")

    def get_all_contacts(self):
        """
        Return all contacts as a list of dictionaries.
        Useful for programmatic access (e.g., web APIs).
        """
        return [{"name": contact.name, "phone": contact.phone} for contact in self.contacts]


class Node:
    """
    Node class for the linked list.
    Each node holds a Contact object and a reference to the next node.
    """

    def __init__(self, contact: Contact):
        self.contact = contact
        self.next = None  # Reference to the next node


class LinkedList:
    """
    Singly linked list to store contacts.
    We keep a reference to the head (first node) of the list.
    """

    def __init__(self):
        self.head = None

    def append(self, contact: Contact) -> None:
        """
        Add a new contact node to the end of the list.
        """
        new_node = Node(contact)

        if self.head is None:
            self.head = new_node
            return

        current = self.head
        while current.next is not None:
            current = current.next
        current.next = new_node

    def find(self, name: str):
        """
        Find the node that contains a contact with the given name.
        Returns the node if found, otherwise None.
        """
        current = self.head
        while current is not None:
            if current.contact.name == name:
                return current
            current = current.next
        return None

    def delete(self, name: str) -> bool:
        """
        Delete the first node whose contact has the given name.
        Returns True if deletion was successful, False otherwise.
        """
        current = self.head
        previous = None

        while current is not None:
            if current.contact.name == name:
                if previous is None:
                    self.head = current.next
                else:
                    previous.next = current.next
                return True

            previous = current
            current = current.next

        return False

    def __iter__(self):
        """
        Allow iteration over the contacts in the linked list.
        This makes it easy to use 'for contact in linked_list'.
        """
        current = self.head
        while current is not None:
            yield current.contact
            current = current.next


class LinkedListContactManager:
    """
    Contact manager that uses a custom singly linked list to store contacts.
    """

    def __init__(self):
        self.contacts = LinkedList()

    def add_contact(self, name: str, phone: str) -> None:
        """
        Add a new contact by appending to the end of the linked list.
        If a contact with the same name exists, we update its phone.
        """
        node = self.contacts.find(name)
        if node is not None:
            node.contact.phone = phone
            print(f"Updated existing contact: {node.contact}")
            return

        new_contact = Contact(name, phone)
        self.contacts.append(new_contact)
        print(f"Added new contact: {new_contact}")

    def search_contact(self, name: str):
        """
        Search for a contact by name in the linked list.
        Returns the Contact object if found, otherwise None.
        """
        node = self.contacts.find(name)
        if node is not None:
            return node.contact
        return None

    def delete_contact(self, name: str) -> bool:
        """
        Delete a contact by name from the linked list.
        Returns True if deletion was successful, False otherwise.
        """
        deleted = self.contacts.delete(name)
        if deleted:
            print(f"Deleted contact: {name}")
        else:
            print(f"Contact not found: {name}")
        return deleted

    def display_contacts(self) -> None:
        """
        Print all contacts stored in the linked list.
        """
        contacts_list = list(self.contacts)
        if not contacts_list:
            print("No contacts to display.")
            return

        print("Contacts (Linked List-based):")
        for contact in contacts_list:
            print(f"- {contact}")

    def get_all_contacts(self):
        """
        Return all contacts as a list of dictionaries.
        Useful for programmatic access (e.g., web APIs).
        """
        return [{"name": contact.name, "phone": contact.phone} for contact in self.contacts]


def print_menu() -> None:
    """
    Print the main menu options.
    """
    print("\n--- Contact Manager ---")
    print("1. Add contact")
    print("2. Search contact")
    print("3. Delete contact")
    print("4. Display contacts")
    print("5. Switch implementation")
    print("0. Exit")


def choose_implementation():
    """
    Let the user choose which implementation to use:
    1. Array-based
    2. Linked List-based
    """
    while True:
        print("\nChoose implementation:")
        print("1. Array-based (Python list)")
        print("2. Linked List-based (custom Node + LinkedList)")
        choice = input("Enter choice (1 or 2): ").strip()

        if choice == "1":
            print("Using Array-based Contact Manager.")
            return ArrayContactManager()
        elif choice == "2":
            print("Using Linked List-based Contact Manager.")
            return LinkedListContactManager()
        else:
            print("Invalid choice. Please enter 1 or 2.")


def main():
    """
    Main loop for the menu-driven CLI.
    Allows the user to interact with the chosen implementation.
    """
    manager = choose_implementation()

    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            name = input("Enter name: ").strip()
            phone = input("Enter phone: ").strip()
            manager.add_contact(name, phone)

        elif choice == "2":
            name = input("Enter name to search: ").strip()
            contact = manager.search_contact(name)
            if contact is not None:
                print(f"Contact found: {contact}")
            else:
                print("Contact not found.")

        elif choice == "3":
            name = input("Enter name to delete: ").strip()
            manager.delete_contact(name)

        elif choice == "4":
            manager.display_contacts()

        elif choice == "5":
            manager = choose_implementation()

        elif choice == "0":
            print("Exiting Contact Manager. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number from 0 to 5.")


if __name__ == "__main__":
    main()


# ============================================================
# Comparison between Array-based and Linked List-based versions
# ============================================================

# 1. Insertion efficiency
#    - Array-based version:
#        * add_contact() uses list.append(), which is O(1) on average when
#          adding at the end of the list.
#        * However, we also do a linear search first to check if the contact
#          already exists, which is O(n).
#        * Overall: O(n) due to the search step.
#
#    - Linked List-based version:
#        * add_contact() also has to search the list to see if the contact
#          already exists (O(n)).
#        * Appending to the end of a singly linked list is O(n) in this simple
#          implementation because we traverse to the end before inserting.
#        * Overall: O(n) for insertion as well.
#
# 2. Deletion efficiency
#    - Array-based version:
#        * We first do a linear search over the list to find the index (O(n)).
#        * Removing an element from the middle of a Python list requires
#          shifting later elements one position to the left, which is O(n).
#        * Overall: O(n) for deletion.
#
#    - Linked List-based version:
#        * We traverse the list to find the node to delete and keep track of
#          the previous node (O(n)).
#        * Once found, we simply change one pointer (previous.next), which is
#          O(1); no shifting of elements is required.
#        * Overall: O(n) due to the search, but the actual removal step is
#          cheaper conceptually (no shifting, just pointer change).
#
# 3. Memory usage differences
#    - Array-based version:
#        * Stores Contact objects in a contiguous Python list.
#        * Each list element is just a reference to a Contact object.
#        * Lists may over-allocate extra space internally to allow efficient
#          append operations, which can use a bit more memory than the exact
#          number of elements.
#
#    - Linked List-based version:
#        * Each contact is wrapped in a Node object that stores:
#             - A reference to the Contact
#             - A reference (pointer) to the next Node
#        * This means extra memory is used per element for the Node objects
#          and their 'next' references.
#        * However, linked lists can grow one node at a time without needing
#          to reallocate a large contiguous block, which can be helpful when
#          memory is very fragmented.
#
# Summary:
#    - For this small contact manager, both implementations are O(n) for
#      search, insertion (with search), and deletion.
#    - The array-based version is simpler and typically faster in practice
#      for small to medium datasets because of good cache locality and
#      Python's optimized list operations.
#    - The linked list version uses more memory per element but can illustrate
#      how pointer-based data structures work and how insert/delete operations
#      can avoid shifting large blocks of data.

