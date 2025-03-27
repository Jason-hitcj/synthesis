import random
from datetime import datetime

import pandas as pd

from generate_transaction_model import TransactionGeneratorLegal
from generate_transaction_model_illegal_2 import TransactionGeneratorIllegal

def generate_transactions(people, num):
    """
    Args:
        :param people: （Person）类 交易人员
        :param num: 循环次数
    """
    patterns = ["small", "medium", "large", "investment", "frequent_large", "aa_payment"]
    weights = [0.54, 0.3, 0.07, 0.03, 0.01, 0.05]



    # 创建交易生成器实例
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)
    generator = TransactionGeneratorLegal(start_date, end_date)

    all_transactions = pd.DataFrame(columns=[
        "sender_id", "sender_card_bank", "sender_card_number", "sender_card_balance_old", "sender_card_balance_new",
        "receiver_id", "receiver_card_bank", "receiver_card_number", "receiver_card_balance_old",
        "receiver_card_balance_new", "amount", "timestamp", "transaction_type", "risk_level"
    ])
    new_transactions = pd.DataFrame(columns=[
        "sender_id", "sender_card_bank", "sender_card_number", "sender_card_balance_old", "sender_card_balance_new",
        "receiver_id", "receiver_card_bank", "receiver_card_number", "receiver_card_balance_old",
        "receiver_card_balance_new", "amount", "timestamp", "transaction_type", "risk_level"
    ])
    for _ in range(num):
        sender = random.choice(people)
        receiver = random.choice(people)
        pattern = random.choices(patterns, weights)[0]

        while receiver == sender:
            receiver = random.choice(people)

        if pattern == "small":
            new_transactions = generator.generate_small_transfers(sender, receiver)
        if pattern == "medium":
            new_transactions = generator.generate_medium_transfers(sender, receiver)
        if pattern == "large":
            new_transactions = generator.generate_large_transfers(sender, receiver)
        if pattern == "investment":
            new_transactions = generator.generate_investment_transfers(sender, receiver)
        if pattern == "frequent_large":
            new_transactions = generator.generate_frequent_large_transfers(sender, receiver)
        if pattern == "aa_payment":
            num_to_select = random.randint(3, 10)
            selected_people = random.sample(people, num_to_select)
            random_float = round(random.uniform(60, 2000), 2)
            new_transactions = generator.generate_aa_payments(selected_people, random_float)

        all_transactions = pd.concat([all_transactions, new_transactions], ignore_index=True)
    return all_transactions

def generate_transactions_illegal(people, num):
    """
    Args:
        :param people: （Person）类 交易人员
        :param num: 循环次数
    """
    patterns = []
    weights = [0.54, 0.3, 0.07, 0.03, 0.01, 0.05]



    # 创建交易生成器实例
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)
    generator = TransactionGeneratorIllegal(start_date, end_date)

    all_transactions = pd.DataFrame(columns=[
        "sender_id", "sender_card_bank", "sender_card_number", "sender_card_balance_old", "sender_card_balance_new",
        "receiver_id", "receiver_card_bank", "receiver_card_number", "receiver_card_balance_old",
        "receiver_card_balance_new", "amount", "timestamp", "transaction_type", "risk_level"
    ])
    new_transactions = pd.DataFrame(columns=[
        "sender_id", "sender_card_bank", "sender_card_number", "sender_card_balance_old", "sender_card_balance_new",
        "receiver_id", "receiver_card_bank", "receiver_card_number", "receiver_card_balance_old",
        "receiver_card_balance_new", "amount", "timestamp", "transaction_type", "risk_level"
    ])

    for _ in range(num):
        sender = random.choice(people)
        receiver = random.choice(people)
        # pattern = random.choices(patterns, weights)[0]


        new_transactions = generator.generate_regular_pattern_transfers(sender, receiver)
        all_transactions = pd.concat([all_transactions, new_transactions], ignore_index=True)
    return all_transactions











