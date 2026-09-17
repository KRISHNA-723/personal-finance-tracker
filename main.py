import csv, re, datetime
from rich.console import Console
from rich.table import Table
from rich.rule import Rule


def read_transactions(filename: str) -> list[dict]:
    """Read transactions from a CSV file and return them as dictionaries."""
    transactions: list[dict] = []

    try:
        with open(filename, "r") as file:
            content = csv.DictReader(file)
            for line in content:
                transactions.append(line)
    except FileNotFoundError:
        print("File not found")

    return transactions


def view_transactions(filename: str) -> None:
    """Display all transactions in a formatted Rich table."""
    transactions = read_transactions(filename)
    table = Table()
    headers = ["ID", "Date", "Description", "Category", "Amount"]
    date_pattern = r"^\d{4}-\d{2}-\d{2}$"

    for header in headers:
        table.add_column(header)

    for i, line in enumerate(transactions, start=1):
        date = line["date"]

        # Regex checks the expected date structure before displaying it.
        if not re.fullmatch(date_pattern, date):
            date = "Invalid Date"

        description = line["description"] if line["description"] != "" else "None"
        category = line["category"] if line["category"] != "" else "None"

        # Invalid amounts are displayed as £0.00 rather than crashing the table.
        try:
            amount = float(line["amount"].strip("$£"))
        except ValueError:
            amount = 0

        amount_str = f"+£{amount:.2f}" if amount >= 0 else f"-£{abs(amount):.2f}"

        table.add_row(str(i), date, description, category, amount_str)

    Console().print(table)


def add_transaction(filename: str,
                    date: str,
                    description: str,
                    category: str,
                    amount: float) -> None:

    """Append a new transaction to the CSV file."""
    try:
        with open(filename, "a", newline="") as file:
            writer = csv.DictWriter(
                file,
                delimiter=",",
                fieldnames=["date", "description", "category", "amount"]
            )
            writer.writerow({
                "date": date,
                "description": description,
                "category": category,
                "amount": amount
            })
    except FileNotFoundError:
        print("File not found")


def delete_transaction(filename: str, transaction_id: int) -> None:
    """Remove a transaction from the CSV file using its displayed ID."""
    transactions = read_transactions(filename)

    transaction_to_remove = transactions[transaction_id - 1]
    transactions.remove(transaction_to_remove)

    write_transaction(filename, transactions)


def write_transaction(filename: str, transactions: list[dict]) -> None:
    # Rewrite the CSV with the remaining transactions.
    try:
        with open(filename, "w", newline="") as file:
            writer = csv.DictWriter(
                file,
                delimiter=",",
                fieldnames=["date", "description", "category", "amount"]
            )
            writer.writeheader()

            for line in transactions:
                date = line["date"]
                description = line["description"] if line["description"] != "" else "None"
                category = line["category"] if line["category"] != "" else "None"
                amount = line["amount"]

                writer.writerow({
                    "date": date,
                    "description": description,
                    "category": category,
                    "amount": amount
                })
    except FileNotFoundError:
        print("File not found")

def modify_transaction(filename: str, transaction_id: int) -> None:
    """Modify an existing transaction."""
    transactions = read_transactions(filename)
    transaction_to_change = transactions[transaction_id - 1]
    isDone = False
    while not isDone:
        transaction_choice = input("Enter which transaction you would like to change (date/description/category/amount/exit):\n ").lower()
        if transaction_choice == "date":
            date = get_valid_date()
            transaction_to_change["date"] = date
        elif transaction_choice == "description":
            description = get_valid_description()
            transaction_to_change["description"] = description
        elif transaction_choice == "category":
            category = get_valid_category()
            transaction_to_change["category"] = category
        elif transaction_choice == "amount":
            amount = get_valid_amount()
            transaction_to_change["amount"] = amount
        elif transaction_choice == "exit":
            isDone = True


    write_transaction(filename, transactions)




def view_summary(filename: str) -> None:
    """Display summary statistics for all transactions."""
    pass


def get_valid_date() -> str:
    """Prompt for a date and return it once it matches the required format."""
    while True:
        date: str = input("Enter your date:\n")

        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
            return date
        except ValueError:
            print("Invalid Date")


def get_valid_description() -> str:
    """Prompt for a non-empty transaction description."""
    while True:
        description: str = input("Enter your description:\n")

        if description.strip() == "":
            print("Description cannot be empty")
        else:
            return description


def get_valid_category() -> str:
    """Prompt for a non-empty transaction category."""
    while True:
        category: str = input("Enter your category:\n")

        if category.strip() == "":
            print("Category cannot be empty")
        else:
            return category


def get_valid_amount() -> float:
    """Prompt for a valid integer transaction amount."""
    while True:
        try:
            amount: int = int(input("Enter your amount:\n"))
            return amount
        except ValueError:
            print("Invalid amount")


def get_valid_id(filename: str) -> int:
    """Prompt for a valid transaction id."""
    transactions = read_transactions(filename)
    maxLen = len(transactions)

    while True:
        try:
            transaction_id = int(input("Enter your Transaction ID:\n"))
            if 1 <= transaction_id <= maxLen:
                return transaction_id
            else:
                print("Transaction does not exist")
        except ValueError:
            print("Not a valid ID")




def main() -> None:
    """Run the finance tracker menu and handle user input."""
    console = Console()

    flag = False
    while not flag:
        try:
            console.print(Rule("Finance Tracker"))

            choice = int(input(
                "Enter your choice:\n"
                "1. Add\n"
                "2. Delete\n"
                "3. View\n"
                "4. Modify\n"
                "5. Summary Stats\n"
                "6. Exit\n"
                "Choice: "
            ))

            console.print(Rule())

            if choice == 1:
                date = get_valid_date()
                description = get_valid_description()
                category = get_valid_category()
                amount = get_valid_amount()

                add_transaction(filename, date, description, category, amount)

            elif choice == 2:
                transaction_id = get_valid_id(filename)
                delete_transaction(filename,transaction_id)

            elif choice == 3:
                view_transactions(filename)

            elif choice == 4:
                transaction_id = get_valid_id(filename)
                modify_transaction(filename, transaction_id)


            elif choice == 5:
                view_summary(filename)

            elif choice == 6:
                flag = True

            else:
                print("Invalid choice")

        except ValueError:
            print("Try Again (Menu)")


filename = "transactions_1_basic.csv"
main()

