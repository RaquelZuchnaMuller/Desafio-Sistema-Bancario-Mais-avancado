import textwrap

def show_menu():
    menu = """\

    [d] Deposit 
    [w] Withdraw
    [s] Statement
    [na] New Account
    [la] List Accounts
    [nu] New User
    [q] Quit
    """
    return input(textwrap.dedent(menu))

def deposit(amount, balance, statement, /):
    if amount > 0:
        balance += amount
        statement += f"Deposit:\t$ {amount:.2f}\n"
    else:
        print("Invalid amount for deposit.")
    return balance, statement

def withdraw(*, balance, amount, statement, limit, num_withdrawals, max_withdrawals):
    exceeded_balance = amount > balance
    exceeded_limit = amount > limit
    exceeded_withdrawals = num_withdrawals >= max_withdrawals

    if exceeded_balance:
        print("Withdrawal failed. Insufficient balance.")
    elif exceeded_limit:
        print("Withdrawal failed. Amount exceeds the limit.")
    elif exceeded_withdrawals:
        print("Withdrawal failed. Daily withdrawal limit reached.")
    elif amount > 0:
        balance -= amount
        statement += f"Withdrawal:\t$ {amount:.2f}\n"
        num_withdrawals += 1
        print(f"Withdrawal successful! Current balance: $ {balance:.2f}")
    else:
        print("Withdrawal failed. Invalid amount.")
    return balance, statement, num_withdrawals

def show_statement(balance, /, *, statement):
    print("\n********** Statement ***********")
    print(statement if statement else "No transactions made.")
    print(f"\nBalance:\t$ {balance:.2f}")
    print("********************************\n")

def create_user(users):
    cpf = input("Enter CPF (numbers only): ")
    user = find_user(cpf, users)

    if user:
        print("\nUser with this CPF already exists.")
        return

    name = input("Enter full name: ")
    birth_date = input("Enter birth date (dd/mm/yyyy): ")
    address = input("Enter address (street, number - neighborhood - city/state): ")

    users.append({
        "name": name,
        "birth_date": birth_date,
        "cpf": cpf,
        "address": address
    })
    print("User created successfully!")

def find_user(cpf, users):
    filtered_users = [user for user in users if user["cpf"] == cpf]
    return filtered_users[0] if filtered_users else None

def create_account(agency, account_number, users):
    cpf = input("Enter user's CPF: ")
    user = find_user(cpf, users)

    if user:
        print("Account created successfully!")
        return {"agency": agency, "account_number": account_number, "user": user}
    else:
        print("User not found. Account creation aborted.")
        return None

def list_accounts(accounts):
    for account in accounts:
        line = f"""
        Agency: {account["agency"]}
        Account:\t{account["account_number"]}
        Holder: {account["user"]["name"]}
        """
        print("-" * 50)
        print(textwrap.dedent(line))

def main():
    MAX_WITHDRAWALS = 3
    AGENCY = "0001"

    balance = 0
    limit = 500
    statement = ""
    num_withdrawals = 0
    users = []
    accounts = []

    while True:
        option = show_menu()

        if option == "d":
            amount = float(input("Enter deposit amount: "))
            balance, statement = deposit(amount, balance, statement)

        elif option == "w":
            amount = float(input("Enter withdrawal amount: "))
            balance, statement, num_withdrawals = withdraw(
                balance=balance,
                amount=amount,
                statement=statement,
                limit=limit,
                num_withdrawals=num_withdrawals,
                max_withdrawals=MAX_WITHDRAWALS
            )

        elif option == "s":
            show_statement(balance, statement=statement)

        elif option == "nu":
            create_user(users)

        elif option == "na":
            account_number = len(accounts) + 1
            account = create_account(AGENCY, account_number, users)
            if account:
                accounts.append(account)

        elif option == "la":
            list_accounts(accounts)

        elif option == "q":
            print("System exiting. Goodbye!")
            break

        else:
            print("Invalid option. Please select a valid operation.")

main()