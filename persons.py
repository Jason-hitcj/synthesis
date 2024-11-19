import random
from datetime import datetime, timedelta
import uuid


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def __repr__(self):
        return f"Person(name={self.name}, age={self.age})"


class BankCard:
    def __init__(self, owner, bank_name, account_number=None):
        self.owner = owner
        self.bank_name = bank_name
        if account_number is None:
            account_number = str(uuid.uuid4())[:8]
            print("卡号："+account_number)
        self.account_number = account_number

    def __repr__(self):
        return f"BankCard(owner={self.owner.name}, bank_name={self.bank_name}, account_number={self.account_number})"


class TransactionGenerator:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    def _generate_timestamp(self):
        time_between_dates = self.end_date - self.start_date
        days_between_dates = time_between_dates.days
        random_days = random.randrange(days_between_dates)
        random_date = self.start_date + timedelta(days=random_days)
        return random_date

    def generate_transactions(self, people, num_transactions=None):
        if num_transactions is None:
            num_transactions = random.randint(20, 50)

        transactions = []
        for _ in range(num_transactions):
            sender = random.choice(people)
            receiver = random.choice(people)
            while receiver == sender:
                receiver = random.choice(people)

            amount = random.uniform(100, 2000)
            timestamp = self._generate_timestamp()
            sender_card = random.choice(sender.cards) if sender.cards else None
            receiver_card = random.choice(receiver.cards) if receiver.cards else None

            transaction = {
                'sender_id': sender_card.account_number if sender_card else None,
                'receiver_id': receiver_card.account_number if receiver_card else None,
                'amount': round(amount, 2),
                'timestamp': timestamp,
                'transaction_type': 'small_transfer',
                'frequency': 'high',
                'risk_level': 'low'
            }
            transactions.append(transaction)

        return transactions


### 3. 生成1000个人并为他们开卡

def generate_people(num_people=10, min_age=18, max_age=60):
    names = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Hannah", "Ivan", "Julia"]
    banks = ["ICBC", "ABC", "CMB", "BOC", "SPDB", "CMBC"]

    people = []
    for i in range(num_people):
        name = random.choice(names) + str(i)  # 确保名字唯一
        age = random.randint(min_age, max_age)
        person = Person(name, age)
        num_cards = random.randint(1, 3)  # 每个人随机开1到3张卡
        for _ in range(num_cards):
            bank_name = random.choice(banks)
            person.add_card(BankCard(owner=person, bank_name=bank_name))
        people.append(person)

    return people


### 4. 生成交易数据

if __name__ == "__main__":
    # 生成1000个用户
    people = generate_people()

    # 创建交易生成器实例
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)
    generator = TransactionGenerator(start_date, end_date)

    # 生成交易
    transactions = generator.generate_transactions(people, num_transactions=10)  # 生成10000笔交易

    # 打印生成的交易
    for transaction in transactions:
        print(transaction)