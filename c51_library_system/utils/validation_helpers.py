import re


def is_valid_email(self, reader_email):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, reader_email) is not None

def is_valid_phone(self, reader_phone):
    return reader_phone.isdigit() and len(reader_phone) == 8 and reader_phone.startswith("6")