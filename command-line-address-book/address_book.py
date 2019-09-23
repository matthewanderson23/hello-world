## This is a command line address book program used to browse, add, modify, delete, or search
#  for contacts such as friends, family and colleagues and their information such as email
#  address and/or phone number. Details must be restored for later retrieval.

# HINT:
# class for person's information
# dictionary for storing person objects
# dictionary methods to add, delete, modify
# pickle module to store objects persistently

# Credits:
# https://stackoverflow.com/questions/28077573/python-appending-to-a-pickled-list/48217112

import pickle
import sys
import os

address_book_file = 'address_book.data'
addr_book = [] # create empty list that we will fill with dict for each member


class ContactMember():
    '''Class for each contact member.

    Can be added, deleted, modified, searched for, or browsed.'''
    def __init__(self, name, email=None, phone=None):
        self.name = name
        self.email = email
        self.phone = phone

        # Check that file exists before overwriting data
        if os.path.exists(address_book_file):
            with open(address_book_file, 'rb') as f:
                addr_book = pickle.load(f)
        self.addr_book = addr_book


    def add(self):
        '''Add a new contact.'''

        contact_info = {'name': self.name,
                        'email': self.email,
                        'phone': self.phone
                        }
        self.addr_book.append(contact_info)
        print(self.addr_book)

        # Write new data to the address book and save it
        if os.path.exists(address_book_file):
            with open(address_book_file, 'wb') as f:
                pickle.dump(self.addr_book, f)

    def delete(self):
        '''Delete existing contact.'''

        contact = self.search()
        if contact == None:
            return None
        else:
            self.addr_book.remove(contact)

            # Write new data to the address book and save it
            if os.path.exists(address_book_file):
                with open(address_book_file, 'wb') as f:
                    pickle.dump(self.addr_book, f)

            return self.name

    def modify(self):
        '''Modify a contact. Must include all details such as name, email, phone.'''

        contact = self.search()
        if contact == None:
            return None
        else:
            self.addr_book.remove(contact)
            self.add()
            return self.name, self.email, self.phone

    def search(self):
        '''Search for a contact by name.'''

        return next((item for item in self.addr_book if item['name'] == self.name), None)

    def browse(self):
        '''Show all contacts.'''

        return self.addr_book if len(self.addr_book) > 0 else None


def main(args):

    if len(args) > 5:
        print("Too many args. Try again with OPTION NAME EMAIL(optional) PHONE(optional).")

    else:
        if args[1] == 'add':
            if len(args) == 5:
                member = ContactMember(args[2], args[3], args[4]).add()
            else:
                print("Not enough args. Try again with 'add NAME EMAIL PHONE'")

        elif args[1] == 'delete':
            if len(args) == 3:
                # delete by name only
                member = ContactMember(args[2]).delete()
                if member != None:
                    print("{} has been removed from the address book.".format(member))
                else:
                    print("Contact does not exist.")
            else:
                print("Not enough args. Try again with 'delete NAME'")

        elif args[1] == 'modify':
            # Must enter entire contact to modify
            if len(args) == 5:
                member = ContactMember(args[2], args[3], args[4]).modify()
                if member != None:
                    print("{}'s new contact is {}; {}.".format(member[0], member[1], member[2]))
                else:
                    print("Contact does not exist.")
            else:
                print("Not enough args. Try again with 'modify NAME EMAIL PHONE'")

        elif args[1] == 'search':
            if len(args) == 3:
                # search by name only
                member = ContactMember(args[2]).search()
                print(member)
            else:
                print("Not enough args. Try again with 'search NAME'")

        elif args[1] == 'browse':
            all_contacts = ContactMember(None).browse()
            print(all_contacts)

        else: # Will never reach here because of sys.argv IndexError exception
            pass


if __name__ == "__main__":
    try:
        main(sys.argv)
    except IndexError:
        print("No option selected. Retry with command-line argument: 'add', 'delete', 'modify', 'search', 'browse'")
        print("Bye!")
