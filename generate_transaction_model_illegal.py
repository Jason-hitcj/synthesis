import random
from datetime import datetime, timedelta


class TransactionGenerator:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    def _generate_timestamp(self):
        """生成随机时间戳"""
        time_between_dates = self.end_date - self.start_date
        return self.start_date + timedelta(days=random.randrange(time_between_dates.days))

    def generate_daily_open_account_and_outflow(self, num_accounts, total_outflow, account_threshold=10,
                                                outflow_threshold=100000):
        """
        模式1: 当天开户数大于X个且当天汇出金额累计大于X元
        """
        is_abnormal = num_accounts > account_threshold and total_outflow > outflow_threshold
        return {
            'new_accounts': num_accounts,
            'total_outflow': total_outflow,
            'is_abnormal': is_abnormal,
            'risk_level': 'high' if is_abnormal else 'low'
        }

    def generate_short_term_private_transactions(self, num_private_accounts, num_days=10, account_threshold=10):
        """
        模式2: 对公账户短期内(如:10天)的交易对手均为对私账户，且累计对私账户数大于X户
        """
        is_abnormal = num_private_accounts > account_threshold
        return {
            'period_days': num_days,
            'private_accounts': num_private_accounts,
            'is_abnormal': is_abnormal,
            'risk_level': 'high' if is_abnormal else 'low'
        }

    def generate_incoming_and_outgoing_transactions(self, num_transactions, last_in_date, out_date,
                                                    transaction_threshold=20, days_threshold=2):
        """
        模式3: 对公账户短期内收到其他对公账户转入交易，统计交易笔数>=X笔，转出日期-最晚转入日期<=Y天
        """
        days_difference = (out_date - last_in_date).days
        is_abnormal = num_transactions >= transaction_threshold and days_difference <= days_threshold
        return {
            'num_transactions': num_transactions,
            'days_difference': days_difference,
            'is_abnormal': is_abnormal,
            'risk_level': 'high' if is_abnormal else 'low'
        }

    def generate_location_mismatch(self, person_location, transaction_location):
        """
        模式4: 对手为个人或公司，交易地区与开户地不一致
        """
        is_abnormal = person_location != transaction_location
        return {
            'person_location': person_location,
            'transaction_location': transaction_location,
            'is_abnormal': is_abnormal,
            'risk_level': 'high' if is_abnormal else 'low'
        }

    def generate_new_account_activity(self, days_since_opening, first_half_transactions, second_half_transactions,
                                      first_half_amount, second_half_amount, transaction_threshold=30,
                                      amount_threshold=500000):
        """
        模式5: 新账户开卡后前后15天的交易对比，后15天交易数量和金额显著增加
        """
        is_abnormal = (second_half_transactions > first_half_transactions and
                       second_half_amount > first_half_amount and
                       second_half_transactions >= transaction_threshold and
                       second_half_amount >= amount_threshold)
        return {
            'days_since_opening': days_since_opening,
            'first_half_transactions': first_half_transactions,
            'second_half_transactions': second_half_transactions,
            'is_abnormal': is_abnormal,
            'risk_level': 'high' if is_abnormal else 'low'
        }

    def generate_online_bank_low_balance(self, online_transfer, account_balance, inflow_amount, outflow_amount,
                                         inflow_outflow_ratio=(0.9, 1.1), inflow_threshold=200000,
                                         counter_rate_threshold=0.8):
        """
        模式6: 低余额账户网上银行转账，流入和流出比例接近，且柜面入账比例高
        """
        inflow_outflow_ratio_valid = inflow_outflow_ratio[0] <= inflow_amount / outflow_amount <= inflow_outflow_ratio[
            1]
        is_abnormal = (account_balance <= 100 and
                       inflow_outflow_ratio_valid and
                       inflow_amount >= inflow_threshold)
        return {
            'online_transfer': online_transfer,
            'account_balance': account_balance,
            'inflow_amount': inflow_amount,
            'outflow_amount': outflow_amount,
            'is_abnormal': is_abnormal,
            'risk_level': 'high' if is_abnormal else 'low'
        }

    def generate_frequent_small_inflows(self, inflow_amount, inflow_frequency, check_interval_days, min_interval,
                                        max_interval, backtracking_period=60):
        """
        模式7: 频繁的小额入账交易，且短期内发生多个类似入账
        """
        is_abnormal = (max_interval - min_interval <= 3 and inflow_amount % 10000 == 0)
        return {
            'inflow_amount': inflow_amount,
            'inflow_frequency': inflow_frequency,
            'min_interval': min_interval,
            'max_interval': max_interval,
            'is_abnormal': is_abnormal,
            'risk_level': 'high' if is_abnormal else 'low'
        }

    def generate_keyword_related_outflows(self, customer_type, keywords, inflow_count, outflow_count, inflow_amount,
                                          outflow_amount, inflow_outflow_ratio=(0.9, 1.1),
                                          inflow_frequency_greater=True, private_count=10):
        """
        模式8: 对公客户带特定关键字的频繁转入转出
        """
        keyword_present = any(kw in customer_type for kw in keywords)
        is_abnormal = (keyword_present and
                       inflow_count / outflow_count >= 5 and
                       inflow_amount >= 500000 and
                       inflow_outflow_ratio[0] <= inflow_amount / outflow_amount <= inflow_outflow_ratio[1] and
                       inflow_frequency_greater and
                       private_count >= 10)
        return {
            'customer_type': customer_type,
            'inflow_count': inflow_count,
            'outflow_count': outflow_count,
            'inflow_amount': inflow_amount,
            'outflow_amount': outflow_amount,
            'is_abnormal': is_abnormal,
            'risk_level': 'high' if is_abnormal else 'low'
        }

    def generate_low_balance_large_inflow_outflow(self, customer_type, keywords, balance, inflow_amount, outflow_amount,
                                                  inflow_outflow_ratio=(0.9, 1.1), transaction_threshold=10):
        """
        模式9: 低余额账户的对私和对公账户频繁大额入账或出账
        """
        keyword_present = any(kw in customer_type for kw in keywords)
        is_abnormal = (keyword_present and
                       balance <= 1000 and
                       inflow_amount >= 200000 and
                       inflow_outflow_ratio[0] <= inflow_amount / outflow_amount <= inflow_outflow_ratio[1] and
                       transaction_threshold >= 10)
        return {
            'customer_type': customer_type,
            'balance': balance,
            'inflow_amount': inflow_amount,
            'outflow_amount': outflow_amount,
            'is_abnormal': is_abnormal,
            'risk_level': 'high' if is_abnormal else 'low'
        }

    def generate_outflow_dominant_transactions(self, customer_type, keywords, inflow_count, outflow_count,
                                               inflow_amount, outflow_amount, inflow_outflow_ratio=(0.9, 1.1),
                                               private_count=10):
        """
        模式10: 对公客户转出占比高且特定关键字的账户
        """
        keyword_present = any(kw in customer_type for kw in keywords)
        is_abnormal = (keyword_present and
                       outflow_count / inflow_count >= 5 and
                       inflow_amount >= 200000 and
                       inflow_outflow_ratio[0] <= inflow_amount / outflow_amount <= inflow_outflow_ratio[1] and
                       private_count >= 10)
        return {
            'customer_type': customer_type,
            'inflow_count': inflow_count,
            'outflow_count': outflow_count,
            'inflow_amount': inflow_amount,
            'outflow_amount': outflow_amount,
            'is_abnormal': is_abnormal,
            'risk_level': 'high' if is_abnormal else 'low'
        }
