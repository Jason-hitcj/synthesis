import random

import generate_person

import generate_transaction_model
import generate_transaction
import numpy as np
import pandas as pd

if __name__ == "__main__":

    # 生成不同类型人员，并为他们随机开卡
    people, persons = generate_person.generate_person_data(1000)
    print(persons.head())

    generate_transaction.generate_transactions(people,1)






