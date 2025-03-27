import random

import generate_person

import generate_transaction_model
import generate_transaction
import numpy as np
import pandas as pd

if __name__ == "__main__":

    # 生成交易账户，并为他们随机开卡
    people, persons = generate_person.generate_person_data(100)
    print(persons.head())

    normal_n=generate_transaction.generate_transactions(people,1000)
    normal_n.to_csv('data/normal_n.csv', index=False, encoding='utf-8-sig')

    # abnormal_n=generate_transaction.generate_transactions_illegal(people,1000)
    # abnormal_n.to_csv('data/abnormal_n.csv', index=False, encoding='utf-8-sig')







