from faker import Faker
import pandas as pd
import random
from datetime import datetime


class CompanyDataGenerator:
    def __init__(self):
        self.fake = Faker(['zh_CN'])

        # 初始化常量数据
        self.company_types = ['有限责任公司', '股份有限公司', '国有企业', '外商投资企业', '合资企业']
        self.industries = ['制造业', '信息技术', '金融业', '房地产', '教育', '零售业', '医疗卫生', '物流运输']
        self.risk_levels = ['低风险', '中风险', '高风险']

    def generate_company(self, num_records=1):
        """生成公司主体数据"""
        companies = []
        for _ in range(num_records):
            company = {
                # 基本信息
                'company_id': self.fake.unique.credit_card_number(),  # 模拟统一社会信用代码
                'company_name': self.fake.company(),
                'company_type': random.choice(self.company_types),
                'registered_capital': round(random.uniform(100, 10000) * 10000, 2),
                'industry': random.choice(self.industries),
                'address': self.fake.province(),
                'establishment_date': self.fake.date_between(start_date='-30y', end_date='today'),
                'legal_representative': self.fake.name(),
                'tax_id': self.fake.unique.random_number(digits=15, fix_len=True),

                # 账户信息
                'account_id': self.fake.unique.random_number(digits=16, fix_len=True),
                'risk_level': random.choice(self.risk_levels)
            }
            companies.append(company)

        return pd.DataFrame(companies) if num_records > 1 else companies[0]


# 使用示例
def generate_company_data(num_companies=100):
    generator = CompanyDataGenerator()
    companies = generator.generate_company(num_companies)
    companies.to_csv('companies.csv', index=False, encoding='utf-8-sig')
    return companies


if __name__ == "__main__":
    companies = generate_company_data(100)
    print(companies.head())