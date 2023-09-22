import re
from zxcvbn import zxcvbn

class PasswordStrengthChecker:
    def __init__(self, min_length=8, special_chars="!@#$%^&*()-_=+[]{}|;:,.<>?/", dict_file=None):
        self.min_length = min_length
        self.special_chars = special_chars
        self.dictionary = set()
        
        if dict_file:
            with open(dict_file, 'r') as f:
                self.dictionary = set(word.strip().lower() for word in f.readlines())

    def contains_dictionary_word(self, password):
        for word in self.dictionary:
            if word in password.lower():
                return True
        return False

    def contains_easy_pattern(self, password):
        patterns = ["abcd", "1234", "qwer", "asdf"]
        for pattern in patterns:
            if pattern in password.lower():
                return True
        return False

    def check_password_strength(self, password):
        if len(password) < self.min_length:
            return False, f"Password too short. It should be at least {self.min_length} characters."

        if not any(char.islower() for char in password):
            return False, "Password should have at least one lowercase letter."

        if not any(char.isupper() for char in password):
            return False, "Password should have at least one uppercase letter."

        if not any(char.isdigit() for char in password):
            return False, "Password should have at least one number."

        if not any(char in self.special_chars for char in password):
            return False, f"Password should have at least one of the special characters: {self.special_chars}."

        if re.search(r"(.)\1\1", password):
            return False, "Password shouldn't have characters repeated consecutively more than twice."

        if self.contains_dictionary_word(password):
            return False, "Password contains a common dictionary word."

        if self.contains_easy_pattern(password):
            return False, "Password contains an easily guessable pattern."

        zxcvbn_result = zxcvbn(password)
        if zxcvbn_result['score'] < 3:  # zxcvbn scores range from 0 (weak) to 4 (strong)
            return False, "Password is too predictable based on common patterns and behaviors."

        return True, "Password is strong."

# Usage
checker = PasswordStrengthChecker(dict_file="path_to_dictionary.txt")  # Use a dictionary file of your choice
password = input("Enter your password: ")
is_strong, message = checker.check_password_strength(password)
if is_strong:
    print(message)
else:
    print("Weak password! Reason:", message)
