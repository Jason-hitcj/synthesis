# from faker import Faker
# import pandas as pd
# import random
# from datetime import datetime, timedelta
# import numpy as np
#
#
# class TransactionDataGenerator:
#     def __init__(self):
#         self.fake = Faker(['zh_CN'])
#         # 初始化常量数据
#         self.company_types = ['有限责任公司', '股份有限公司', '国有企业', '外商投资企业', '合资企业']
#         self.industries = ['制造业', '信息技术', '金融业', '房地产', '教育', '零售业', '医疗卫生', '物流运输']
#         self.transaction_types = ['转账', '支付', '投资', '融资', '退款']
#         self.transaction_status = ['成功', '处理中', '失败', '冻结']
#         self.risk_levels = ['低风险', '中风险', '高风险']
#         self.occupations = ['工人', '白领', '教师', '医生', '工程师', '销售', '管理人员', '自由职业']
#         self.education_levels = ['高中', '专科', '本科', '硕士', '博士']
#         self.consumption_categories = ['日常购物', '餐饮', '娱乐', '教育', '医疗', '旅游', '投资理财']
#
#     def generate_company(self, num_records=1):
#         """生成公司主体数据"""
#         companies = []
#         for _ in range(num_records):
#             company = {
#                 # 基本信息
#                 'company_id': self.fake.unique.credit_card_number(),  # 模拟统一社会信用代码
#                 'company_name': self.fake.company(),
#                 'company_type': random.choice(self.company_types),
#                 'registered_capital': round(random.uniform(100, 10000) * 10000, 2),
#                 'industry': random.choice(self.industries),
#                 'address': self.fake.address(),
#                 'establishment_date': self.fake.date_between(start_date='-30y', end_date='today'),
#                 'legal_representative': self.fake.name(),
#                 'tax_id': self.fake.unique.random_number(digits=15, fix_len=True),
#
#                 # 账户信息
#                 'account_id': self.fake.unique.random_number(digits=16, fix_len=True),
#                 'risk_level': random.choice(self.risk_levels),
#
#                 # 补充信息
#                 'employee_count': random.randint(5, 1000),
#                 'is_listed': random.choice([True, False]),
#                 'business_scope': self.fake.text(max_nb_chars=200)
#             }
#             companies.append(company)
#
#         return pd.DataFrame(companies) if num_records > 1 else companies[0]
#
#     def generate_person(self, num_records=1):
#         """生成个人主体数据"""
#         persons = []
#         for _ in range(num_records):
#             age = random.randint(18, 80)
#             income_level = random.choice(['低', '中', '高'])
#             # 根据年龄和收入水平设置合理的月收入范围
#             if income_level == '低':
#                 monthly_income = random.uniform(3000, 8000)
#             elif income_level == '中':
#                 monthly_income = random.uniform(8000, 25000)
#             else:
#                 monthly_income = random.uniform(25000, 100000)
#
#             person = {
#                 # 基本信息
#                 'person_id': self.fake.unique.ssn(),
#                 'name': self.fake.name(),
#                 'gender': random.choice(['男', '女']),
#                 'age': age,
#                 'occupation': random.choice(self.occupations),
#                 'monthly_income': round(monthly_income, 2),
#                 'income_level': income_level,
#                 'marital_status': random.choice(['未婚', '已婚', '离异']),
#                 'address': self.fake.address(),
#                 'education': random.choice(self.education_levels),
#
#                 # 账户信息
#                 'account_id': self.fake.unique.random_number(digits=16, fix_len=True),
#                 'risk_level': random.choice(self.risk_levels),
#
#                 # 补充信息
#                 'phone_number': self.fake.phone_number(),
#                 'email': self.fake.email(),
#                 'preferred_payment_method': random.choice(['支付宝', '微信支付', '银行卡', '现金']),
#                 'credit_score': random.randint(300, 850)
#             }
#             persons.append(person)
#
#         return pd.DataFrame(persons) if num_records > 1 else persons[0]
#
#     def generate_company_transaction(self, companies_df, num_records=1):
#         """生成公司交易数据"""
#         transactions = []
#         company_ids = companies_df['company_id'].tolist()
#
#         for _ in range(num_records):
#             # 随机选择交易双方
#             party_a = random.choice(company_ids)
#             party_b = random.choice(company_ids)
#             while party_b == party_a:  # 避免自己和自己交易
#                 party_b = random.choice(company_ids)
#
#             transaction = {
#                 'transaction_id': self.fake.unique.uuid4(),
#                 'transaction_time': self.fake.date_time_between(start_date='-1y', end_date='now'),
#                 'amount': round(random.uniform(1000, 1000000), 2),
#                 'transaction_type': random.choice(self.transaction_types),
#                 'party_a': party_a,
#                 'party_b': party_b,
#                 'direction': random.choice(['流入', '流出']),
#                 'status': random.choice(self.transaction_status),
#                 'risk_level': random.choice(self.risk_levels),
#                 'remarks': self.fake.text(max_nb_chars=100)
#             }
#             transactions.append(transaction)
#
#         return pd.DataFrame(transactions) if num_records > 1 else transactions[0]
#
#     def generate_person_transaction(self, persons_df, companies_df, num_records=1):
#         """生成个人交易数据"""
#         transactions = []
#         person_ids = persons_df['person_id'].tolist()
#         company_ids = companies_df['company_id'].tolist()
#
#         for _ in range(num_records):
#             # 随机选择个人
#             person_id = random.choice(person_ids)
#             # 大部分交易是个人对公司
#             if random.random() < 0.8:
#                 counterparty = random.choice(company_ids)
#                 transaction_type = random.choice(self.consumption_categories)
#             else:
#                 counterparty = random.choice(person_ids)
#                 while counterparty == person_id:  # 避免自己和自己交易
#                     counterparty = random.choice(person_ids)
#                 transaction_type = random.choice(['转账', '还款', '借款'])
#
#             transaction = {
#                 'transaction_id': self.fake.unique.uuid4(),
#                 'transaction_time': self.fake.date_time_between(start_date='-1y', end_date='now'),
#                 'amount': round(random.uniform(10, 50000), 2),
#                 'transaction_type': transaction_type,
#                 'person_id': person_id,
#                 'counterparty_id': counterparty,
#                 'direction': random.choice(['流入', '流出']),
#                 'status': random.choice(self.transaction_status),
#                 'payment_method': random.choice(['支付宝', '微信支付', '银行卡', '现金']),
#                 'remarks': self.fake.text(max_nb_chars=100)
#             }
#             transactions.append(transaction)
#
#         return pd.DataFrame(transactions) if num_records > 1 else transactions[0]
#
#
# # 使用示例
# def generate_sample_data(num_companies=100, num_persons=1000, num_transactions=5000):
#     generator = TransactionDataGenerator()
#
#     # 生成公司和个人数据
#     companies = generator.generate_company(num_companies)
#     persons = generator.generate_person(num_persons)
#
#     # 生成交易数据
#     company_transactions = generator.generate_company_transaction(companies, num_transactions // 2)
#     person_transactions = generator.generate_person_transaction(persons, companies, num_transactions // 2)
#
#     # 保存数据
#     companies.to_csv('companies.csv', index=False, encoding='utf-8-sig')
#     persons.to_csv('persons.csv', index=False, encoding='utf-8-sig')
#     company_transactions.to_csv('company_transactions.csv', index=False, encoding='utf-8-sig')
#     person_transactions.to_csv('person_transactions.csv', index=False, encoding='utf-8-sig')
#
#     return {
#         'companies': companies,
#         'persons': persons,
#         'company_transactions': company_transactions,
#         'person_transactions': person_transactions
#     }
#
#
# if __name__ == "__main__":
#     data = generate_sample_data()
#     print("数据生成完成！")
#     for name, df in data.items():
#         print(f"\n{name} 数据样例:")
#         print(df.head())
#         print(f"总记录数: {len(df)}")