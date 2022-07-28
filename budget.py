class Category:
    def __init__(self, category):
        self.ledger = []
        self.balance = 0
        self.category = category
        self.spending = 0

    def __repr__(self):
        return self.__get_formatted()

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})
        self.balance += amount

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            self.balance -= amount
            self.spending += amount
            return True
        else:
            return False

    def get_balance(self):
        return self.balance

    def transfer(self, amount, dbc):
        if self.withdraw(amount, description=f"Transfer to {dbc.category}"):
            dbc.deposit(amount, description=f"Transfer from {self.category}")
            return True
        else:
            return False

    def check_funds(self, amount):
        return amount <= self.balance

    def __get_formatted(self):
        string = f"{self.category:*^30}\n"
        for transaction in self.ledger:
            string += f"{transaction['description'][:23]:<23}{transaction['amount']:>7.2f}\n"
        string += f"Total: {self.balance}"

        return string


def create_spend_chart(categories):
    percentage = __get_percentage_spent(categories)
    scale = [[f"{x:>3}|" for x in reversed(range(0, 101, 10))], ]
    names = [[], []]
    k = 0
    for _ in categories:
        data = ["  "] * 11
        for i in range(1, percentage[k] + 2):
            data[-i] = "o "
        scale.append(data)
        names[0].append([x for x in _.category])
        k += 1
    names[1].append(['   '] * len(max(names[0], key=len)))
    for s in names[0]:
        names_data = [' '] * len(max(names[0], key=len))
        for i in range(len(s)):
            names_data[i] = s[i]
        names[1].append(names_data)

    return "Percentage spent by category\n" + " \n".join(map(' '.join, zip(*scale))) + \
           f" \n    -{'---' * len(categories)}\n" + "  \n".join(map('  '.join, zip(*names[1]))) + "  "


def __get_percentage_spent(categories):
    total_spending = 0
    for category in categories:
        total_spending += category.spending
    return [int((x.spending / total_spending) * 10) for x in categories]
