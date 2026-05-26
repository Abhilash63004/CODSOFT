def subtract(a, b): return a - b
def multiply(a, b): return a * b
def divide(a, b):
    if b == 0:
        return "Error: Division by zero"
    return a / b
def modulus(a, b):
    if b == 0:
        return "Error: Division by zero"
    return a % b
def power(a, b):    return a ** b
def floor_div(a, b):
    if b == 0:
        return "Error: Division by zero"
    return a // b


def get_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("  ⚠  Please enter a valid number.")


def calculator():
    print("╔══════════════════════════════════════╗")
    print("║      CODSOFT - CALCULATOR            ║")
    print("╚══════════════════════════════════════╝")

    operations = {
        "1": ("+",  "Addition",        add),
        "2": ("-",  "Subtraction",     subtract),
        "3": ("*",  "Multiplication",  multiply),
        "4": ("/",  "Division",        divide),
        "5": ("%",  "Modulus",         modulus),
        "6": ("**", "Power",           power),
        "7": ("//", "Floor Division",  floor_div),
    }

    while True:
        print("\n┌─────────────────────────────────────┐")
        for key, (sym, name, _) in operations.items():
            print(f"│  {key}. {sym:<4}  {name:<28}│")
        print("│  8. Exit                            │")
        print("└─────────────────────────────────────┘")

        choice = input("  Choose operation (1-8): ").strip()

        if choice == "8":
            print("\n  Goodbye! 👋")
            break

        if choice not in operations:
            print("  ⚠  Invalid choice. Please select 1–8.")
            continue

        sym, name, func = operations[choice]

        num1 = get_number(f"\n  Enter first number  : ")
        num2 = get_number(f"  Enter second number : ")

        result = func(num1, num2)

        print(f"\n  ┌─────────────────────────────────┐")
        if isinstance(result, str):
            print(f"  │  {result:<33}│")
        else:
            # Show as int if result is a whole number
            display = int(result) if result == int(result) else result
            print(f"  │  {num1:g} {sym} {num2:g} = {display:<22}│")
        print(f"  └─────────────────────────────────┘")

        again = input("\n  Calculate again? (yes/no): ").strip().lower()
        if again not in ("yes", "y"):
            print("\n  Goodbye! 👋")
            break


if __name__ == "__main__":
    calculator()
