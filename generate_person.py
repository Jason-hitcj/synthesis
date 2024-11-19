import string
import uuid

from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta


class Person:
    def __init__(self, person_id, name, gender, age, occupation, income_level, monthly_income, marital_status, address,
                 education, credit_score):
        self.person_id = person_id
        self.name = name
        self.age = age
        self.gender = gender
        self.occupation = occupation
        self.income_level = income_level
        self.monthly_income = monthly_income
        self.marital_status = marital_status
        self.address = address
        self.education = education
        self.credit_score = credit_score

        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def __repr__(self):
        return f"Person(name={self.name}, age={self.age})"


class BankCard:
    def __init__(self, owner, bank_name, balance, card_type='C', account_number=None):
        self.owner = owner
        self.bank_name = bank_name
        self.card_type = card_type
        self.balance = balance
        if account_number is None:
            account_number = card_type + ''.join(random.choices(string.digits, k=8))  # 生成8位纯数字卡号
        self.account_number = account_number

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        # 使用round()函数确保value保持2位小数
        self._balance = round(float(value), 2)

    def __repr__(self):
        return f"BankCard(owner={self.owner.name}, bank_name={self.bank_name}, account_number={self.account_number}, balance={self.balance})"


class PersonDataGenerator:
    def __init__(self):
        self.fake = Faker(['zh_CN'])

        # 初始化常量数据
        self.occupations = ['学生', '白领', '教师', '医生', '工程师', '销售', '管理人员', '自由职业']
        self.education_levels = ['高中', '专科', '本科', '硕士', '博士']
        self.marital_status = ['未婚', '已婚', '离异']
        self.risk_levels = ['低风险', '中风险', '高风险']
        self.payment_methods = ['支付宝', '微信支付', '银行卡', '现金']
        self.consumption_categories = ['电子产品', '娱乐', '餐饮', '教育培训', '服装', '房租', '车贷', '旅行', '时尚',
                                       '健身', '家电', '装修', '医疗保健', '保险', '投资']
        self.banks = ["ICBC", "ABC", "CMB", "BOC", "SPDB", "CMBC"]

    def generate_person(self, num_records=1):
        """生成个人主体数据"""
        persons = []
        people = []
        for _ in range(num_records):
            age = random.randint(18, 80)
            income_level, occupation, marital_statu = assign_income_level_and_occupation(age)

            person_id = self.fake.unique.ssn()
            name = self.fake.name()
            gender = random.choice(['男', '女'])
            monthly_income = generate_monthly_income(income_level)
            address = self.fake.province()
            education = generate_education_level(income_level)
            credit_score = random.randint(300, 850)

            person = Person(person_id, name, gender, age, occupation, income_level, monthly_income, marital_statu,
                            address, education, credit_score)
            num_cards = random.randint(1, 3)  # 每个人随机开1到3张卡
            for _ in range(num_cards):
                bank_name = random.choice(self.banks)
                person.add_card(BankCard(owner=person, bank_name=bank_name, balance=round(monthly_income * 10, 2)))

            person_table = {
                # 基本信息
                'person_id': person_id,
                'name': name,
                'gender': gender,
                'age': age,
                'occupation': occupation,
                'income_level': income_level,
                'monthly_income': monthly_income,
                'marital_status': marital_statu,
                'address': address,
                'education': education,

                # 补充信息
                'credit_score': credit_score
            }
            people.append(person)
            persons.append(person_table)

        return people, pd.DataFrame(persons) if num_records > 1 else persons[0]


# 依据年龄生成"收入水平"和"职业"
def assign_income_level_and_occupation(age):
    if age <= 25:
        occupations = ["学生", "初入职场人员", "自由职业者"]
        probabilities = [0.8, 0.15, 0.05]
    elif 26 <= age <= 35:
        occupations = ["白领/公司职员", "专业技术人员", "自由职业者", "小企业主"]
        probabilities = [0.4, 0.3, 0.2, 0.1]
    elif 36 <= age <= 45:
        occupations = ["公司高层管理人员", "专业技术人员", "自由职业者", "中小企业主"]
        probabilities = [0.3, 0.4, 0.2, 0.1]
    elif 46 <= age <= 60:
        occupations = ["高层管理人员", "专业人士", "企业主和高收入个体户", "自由职业者"]
        probabilities = [0.3, 0.3, 0.3, 0.1]
    else:
        occupations = ["退休人员", "自由职业者和顾问", "投资人", "企业高层和企业主"]
        probabilities = [0.5, 0.3, 0.1, 0.1]

    occupation = random.choices(occupations, probabilities)[0]

    if occupation == "学生":
        income_level = "低"
        marital_statu = "未婚"
    elif occupation == "初入职场人员":
        income_level = "低"
        marital_statu = random.choices(["未婚", "已婚", "离异"], [0.8, 0.15, 0.05])[0]
    elif occupation == "自由职业者" and age <= 25:
        income_level = random.choices(["低", "中"], [0.7, 0.3])[0]
        marital_statu = random.choices(["未婚", "已婚", "离异"], [0.8, 0.15, 0.05])[0]
    elif occupation == "白领/公司职员":
        income_level = random.choices(["低", "中", "高"], [0.1, 0.7, 0.2])[0]
        marital_statu = random.choices(["未婚", "已婚", "离异"], [0.3, 0.65, 0.05])[0]
    elif occupation == "专业技术人员":
        income_level = random.choices(["低", "中", "高"], [0.1, 0.6, 0.3])[0]
        marital_statu = random.choices(["未婚", "已婚", "离异"], [0.2, 0.75, 0.05])[0]
    elif occupation == "自由职业者" and 26 <= age <= 35:
        income_level = random.choices(["低", "中", "高"], [0.2, 0.5, 0.3])[0]
        marital_statu = random.choices(["未婚", "已婚", "离异"], [0.3, 0.65, 0.05])[0]
    elif occupation == "小企业主":
        income_level = random.choices(["低", "中", "高"], [0.1, 0.5, 0.4])[0]
        marital_statu = random.choices(["未婚", "已婚", "离异"], [0.2, 0.75, 0.05])[0]
    elif occupation == "公司高层管理人员":
        income_level = random.choices(["中", "高"], [0.05, 0.95])[0]
        marital_statu = random.choices(["未婚", "已婚", "离异"], [0.1, 0.85, 0.05])[0]
    elif occupation == "自由职业者" and 36 <= age <= 45:
        income_level = random.choices(["中", "高"], [0.2, 0.8])[0]
        marital_statu = random.choices(["未婚", "已婚", "离异"], [0.2, 0.75, 0.05])[0]
    elif occupation == "中小企业主":
        income_level = random.choices(["中", "高"], [0.05, 0.95])[0]
        marital_statu = random.choices(["未婚", "已婚", "离异"], [0.05, 0.85, 0.1])[0]
    elif occupation == "高层管理人员":
        income_level = "高"
        marital_statu = random.choices(["未婚", "已婚", "离异"], [0.05, 0.85, 0.1])[0]
    elif occupation == "专业人士":
        income_level = random.choices(["中", "高"], [0.2, 0.8])[0]
        marital_statu = random.choices(["未婚", "已婚", "离异"], [0.05, 0.85, 0.1])[0]
    elif occupation == "企业主和高收入个体户":
        income_level = "高"
        marital_statu = random.choices(["未婚", "已婚", "离异"], [0.05, 0.85, 0.1])[0]
    elif occupation == "自由职业者" and 46 <= age <= 60:
        income_level = random.choices(["中", "高"], [0.2, 0.8])[0]
        marital_statu = random.choices(["未婚", "已婚", "离异"], [0.05, 0.85, 0.1])[0]
    elif occupation == "退休人员":
        income_level = "中"
        marital_statu = random.choices(["未婚", "已婚", "离异"], [0.05, 0.85, 0.1])[0]
    elif occupation == "自由职业者和顾问":
        income_level = random.choices(["中", "高"], [0.5, 0.5])[0]
        marital_statu = random.choices(["未婚", "已婚", "离异"], [0.05, 0.85, 0.1])[0]
    elif occupation == "投资人":
        income_level = "高"
        marital_statu = random.choices(["未婚", "已婚", "离异"], [0.05, 0.85, 0.1])[0]
    elif occupation == "企业高层和企业主":
        income_level = "高"
        marital_statu = random.choices(["未婚", "已婚", "离异"], [0.05, 0.85, 0.1])[0]

    return income_level, occupation, marital_statu


def generate_monthly_income(level):
    if level == '低':
        return round(random.uniform(2000, 5000), 2)  # 低收入范围：2000-5000
    elif level == '中':
        return round(random.uniform(5000, 15000), 2)  # 中收入范围：5000-15000
    elif level == '高':
        return round(random.uniform(15000, 50000), 2)  # 高收入范围：15000-50000
    else:
        raise ValueError("收入水平只能为 '低'，'中'，或 '高'")


def generate_education_level(income_level):
    # 定义教育水平和对应的概率分布
    education_levels = ['高中', '专科', '本科', '硕士', '博士']

    if income_level == '低':
        probabilities = [0.4, 0.4, 0.15, 0.04, 0.01]  # 低收入的概率分布，高中文凭占比降低
    elif income_level == '中':
        probabilities = [0.2, 0.4, 0.3, 0.08, 0.02]  # 中等收入的概率分布，高中文凭占比进一步降低
    elif income_level == '高':
        probabilities = [0.05, 0.15, 0.5, 0.2, 0.1]  # 高收入的概率分布，高中比例最低，本科及以上占比更高
    else:
        raise ValueError("收入水平只能为 '低'，'中'，或 '高'")

    # 根据概率分布随机选择教育水平
    education_level = random.choices(education_levels, weights=probabilities, k=1)[0]
    return education_level


# 使用示例
def generate_person_data(num_persons=1000):
    generator = PersonDataGenerator()
    people, persons = generator.generate_person(num_persons)
    persons.to_csv('data/persons.csv', index=False, encoding='utf-8-sig')
    return people, persons


if __name__ == "__main__":
    people, persons = generate_person_data(10)
    print(persons.head())

    person = random.choice(people)
    print(person.name, person.age, person.cards)
