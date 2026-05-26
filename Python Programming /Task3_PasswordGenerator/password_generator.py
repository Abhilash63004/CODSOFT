# CodSoft Python Internship - Task 3
# Password Generator
# Generates strong random passwords with customizable length & complexity

import random
import string


def generate_password(length, use_upper=True, use_digits=True, use_symbols=True):
    """
    Generates a random password of the given length.
    Guarantees at least one character from each selected category.
    """
    # Build character pool
    pool = list(string.ascii_lowercase)  # always include lowercase
    guaranteed = [random.choice(string.ascii_lowercase)]

    if use_upper:
        pool += list(string.ascii_uppercase)
        guaranteed.append(random.choice(string.ascii_uppercase))

    if use_digits:
        pool += list(string.digits)
        guaranteed.append(random.choice(string.digits))

    if use_symbols:
        pool += list(string.punctuation)
        guaranteed.append(random.choice(string.punctuation))

    # Fill remaining length from pool
    remaining_length = length - len(guaranteed)
    if remaining_length < 0:
        remaining_length = 0

    password_chars = guaranteed + random.choices(pool, k=remaining_length)
    random.shuffle(password_chars)
    return "".join(password_chars)


def get_int(prompt, min_val, max_val):
    while True:
        try:
            val = int(input(prompt))
            if min_val <= val <= max_val:
                return val
            print(f"  ⚠  Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("  ⚠  Invalid input. Enter a whole number.")


def yes_no(prompt):
    while True:
        ans = input(prompt).strip().lower()
        if ans in ("yes", "y", ""):
            return True
        if ans in ("no", "n"):
            return False
        print("  ⚠  Please enter yes or no.")


def strength_label(length, use_upper, use_digits, use_symbols):
    score = sum([length >= 12, use_upper, use_digits, use_symbols])
    if score == 4 and length >= 16:
        return "🔒 Very Strong"
    elif score >= 3:
        return "🟢 Strong"
    elif score == 2:
        return "🟡 Moderate"
    else:
        return "🔴 Weak"


def main():
    print("╔══════════════════════════════════════╗")
    print("║    CODSOFT - PASSWORD GENERATOR      ║")
    print("╚══════════════════════════════════════╝\n")

    while True:
        # Get settings
        length = get_int("  Password length (8–64): ", 8, 64)
        print()
        use_upper   = yes_no("  Include UPPERCASE letters? (yes/no) [yes]: ")
        use_digits  = yes_no("  Include digits (0-9)?       (yes/no) [yes]: ")
        use_symbols = yes_no("  Include symbols (!@#...)?   (yes/no) [yes]: ")

        how_many = get_int("\n  How many passwords to generate? (1–10): ", 1, 10)

        strength = strength_label(length, use_upper, use_digits, use_symbols)

        print(f"\n  ┌──────────────────────────────────────────┐")
        print(f"  │  Length   : {length:<31}│")
        print(f"  │  Strength : {strength:<31}│")
        print(f"  ├──────────────────────────────────────────┤")

        for i in range(how_many):
            pwd = generate_password(length, use_upper, use_digits, use_symbols)
            print(f"  │  {i+1:>2}. {pwd:<38}│")

        print(f"  └──────────────────────────────────────────┘")

        again = yes_no("\n  Generate more passwords? (yes/no): ")
        if not again:
            print("\n  Stay secure! Goodbye 👋")
            break
        print()


if __name__ == "__main__":
    main()
