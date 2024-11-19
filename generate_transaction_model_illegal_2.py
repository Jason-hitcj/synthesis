import random
from datetime import timedelta, datetime

class TransactionGenerator:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    def _generate_timestamp(self):
        """生成随机时间戳"""
        time_between_dates = self.end_date - self.start_date
        return self.start_date + timedelta(days=random.randrange(time_between_dates.days))

    def generate_daily_open_account_and_outflow(self, num_accounts, total_outflow, account_threshold=10, outflow_threshold=100000):
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

    def detect_private_to_public_account_transfers(self, private_to_public_transfers, private_account_count, private_to_public_threshold=10):
        """
        模式2: 对公账户短期内（如：10天）的交易对手均为对私账户;且该时间段内（如：10天） 累计对私账户数大于 X 户
        """
        is_abnormal = private_to_public_transfers > 0 and private_account_count > private_to_public_threshold
        return {
            'private_to_public_transfers': private_to_public_transfers,
            'private_account_count': private_account_count,
            'is_abnormal': is_abnormal,
            'risk_level': 'high' if is_abnormal else 'low'
        }

    def detect_public_account_rapid_transfers(self, public_account_transfers, latest_transfer_date, transfer_count_threshold=20, transfer_duration_threshold=2):
        """
        模式3: 对公账户短期内（如：10天）收到其他对公账户转入交易，并获得最晚转入日期 2.统计交易笔数>=X 笔 （如：20笔） 3.转出日期-最晚转入日期<= Y 天 （如：2天）
        """
        transfer_count = len(public_account_transfers)
        transfer_duration = (self._generate_timestamp() - latest_transfer_date).days
        is_abnormal = transfer_count >= transfer_count_threshold and transfer_duration <= transfer_duration_threshold
        return {
            'public_account_transfers': public_account_transfers,
            'latest_transfer_date': latest_transfer_date,
            'transfer_count': transfer_count,
            'transfer_duration': transfer_duration,
            'is_abnormal': is_abnormal,
            'risk_level': 'high' if is_abnormal else 'low'
        }

    def detect_location_mismatch(self, account_type, account_location, transaction_location):
        """
        模式4: 1.若对手为个人，取得交易对手账户的开户地，与交易地区不一致即预警（按省比较） 2.若对手为公司，取得公司客户的所在地（截取营业执照前2位），与交易地区不一致即预警（按省比较）
        """
        is_abnormal = account_location != transaction_location
        return {
            'account_type': account_type,
            'account_location': account_location,
            'transaction_location': transaction_location,
            'is_abnormal': is_abnormal,
            'risk_level': 'high' if is_abnormal else 'low'
        }

    def detect_short_term_high_activity(self, early_period_count, early_period_amount, late_period_count, late_period_amount, total_count_threshold=30, total_amount_threshold=500000):
        """
        模式5: 1.查询30天前开卡的账户 2.统计开卡后，头15天的交易笔数、交易金额 3.统计开卡后，第16-30天（后15天）的交易笔数、交易金额 4.后15天交易笔数、交易金额大于头15天交易笔数、交易金额 且总交易笔数>=X笔（如：30笔），总交易金额>=Y元（如：50万元）
        """
        total_count = early_period_count + late_period_count
        total_amount = early_period_amount + late_period_amount
        is_abnormal = total_count >= total_count_threshold and total_amount >= total_amount_threshold and late_period_count > early_period_count and late_period_amount > early_period_amount
        return {
            'early_period_count': early_period_count,
            'early_period_amount': early_period_amount,
            'late_period_count': late_period_count,
            'late_period_amount': late_period_amount,
            'total_count': total_count,
            'total_amount': total_amount,
            'is_abnormal': is_abnormal,
            'risk_level': 'high' if is_abnormal else 'low'
        }

    def detect_short_term_balanced_transfers(self, inflow_amount, outflow_amount, inflow_outflow_ratio_min=0.9, inflow_outflow_ratio_max=1.1, total_amount_threshold=200000):
        """
        模式6: 1. 当日发生网上银行、电话银行、手机银行转出交易,且账户余额<= X 元 （如 ：100元） 2. 统计短期内（3天）借、贷方累计交易金额 0.9<=贷方（流入）累计金额/借方（流出）累计金额<=1.1 且 借方（或贷方）累计金额>= Y 元 （如：20万元） 3. 统计柜面入账交易笔数/入账交易笔数 >= Z% （如：80%）
        """
        inflow_outflow_ratio = inflow_amount / outflow_amount if outflow_amount != 0 else 0
        is_abnormal = inflow_outflow_ratio >= inflow_outflow_ratio_min and inflow_outflow_ratio <= inflow_outflow_ratio_max and max(inflow_amount, outflow_amount) >= total_amount_threshold
        return {
            'inflow_amount': inflow_amount,
            'outflow_amount': outflow_amount,
            'inflow_outflow_ratio': inflow_outflow_ratio,
            'is_abnormal': is_abnormal,
            'risk_level': 'high' if is_abnormal else 'low'
        }

    def detect_repeated_small_inflows(self, inflow_amount, inflow_date, previous_inflows, inflow_amount_threshold=3000, time_delta_threshold=3):
        """
        模式7: 1. 当天个人账户发生转账入账交易，金额<= X 元 （如：3000元） 2. 查询半年内（180天）该账户的转账入账交易，金额与该笔金额相同 3 .根据步骤2中查询的交易 ，计算两次相近交易的时间间隔。 4. 最大时间间隔-最小时间间隔<= Y天 （如：3天） 5. 查询最早一次入账交易之前回顾2个月发生过资金转出交易，转出金额为万元的整数倍
        """
        is_abnormal = inflow_amount <= inflow_amount_threshold and any(abs((inflow_date - prev_inflow_date).days) <= time_delta_threshold for prev_inflow_date in previous_inflows)
        return {
            'inflow_amount': inflow_amount,
            'inflow_date': inflow_date,
            'previous_inflows': previous_inflows,
            'is_abnormal': is_abnormal,
            'risk_level': 'high' if is_abnormal else 'low'
        }

    def detect_public_account_inflow_patterns(self, inflow_count, inflow_amount, inflow_outflow_ratio_min=0.9, inflow_outflow_ratio_max=1.1, inflow_amount_threshold=500000, inflow_count_threshold=10, inflow_account_count_threshold=10):
        """
        模式8: 1. 计算当天有转出交易的账户（对公/对私），如为对公客户，则客户名称要含有设定的关键字（如：投资咨询、财富管理、资产管理、生态发展、科技发展、生物科技、咨询服务、养老保险、交易所、基金管理、股权投资、金融服务、金融信息、网络科技、电子商务等） 2. 查询账户在短期内（如：10天）的所有交易 3. 统计并比较 累计流入笔数/累计流出笔数>=X 倍 （如：5倍） 累计流入金额>=Y 元 （如：50万元） 累计流入金额/累计流出金额在[M%,N%]范围内 （如：90%-110%内，基本上市进多少出多少的） 流入时间均值>流出时间均值 转入的对私对手账户数量>= Z 户 （如：10户）
        """
        inflow_outflow_ratio = inflow_amount / (inflow_amount + 1) # Avoid division by 0
        is_abnormal = inflow_count / 1 >= inflow_count_threshold and inflow_amount >= inflow_amount_threshold and inflow_outflow_ratio >= inflow_outflow_ratio_min and inflow_outflow_ratio <= inflow_outflow_ratio_max and inflow_account_count_threshold >= 10
        return {
            'inflow_count': inflow_count,
            'inflow_amount': inflow_amount,
            'inflow_outflow_ratio': inflow_outflow_ratio,
            'is_abnormal': is_abnormal,
            'risk_level': 'high' if is_abnormal else 'low'
        }

    def detect_low_balance_transfers(self, account_type, account_balance, inflow_amount, inflow_outflow_ratio_min=0.9, inflow_outflow_ratio_max=1.1, inflow_amount_threshold=200000, transaction_count_threshold=10, private_account_balance_threshold=1000, public_account_balance_threshold=10000):
        """
        模式9: 1、当日账户交易，对私账户余额<=X 元 （如：1000元） 或对公账户余额<=Y元 （如：10000元），如客户为对公客户，则客户名称要含有设 定的关键字（如：投资咨询、财富管理、资产管理、生态发展、科技发展、生物科技、咨询服务、养老保险、交易所、基金管理、股权投资、金融服务、金融信息、网络科技、电子商务等） 2、查询该账户在短期内（如：3天）的的所有交易 3、统计并比较 累计流入（或流出）金额>= Z 元（ 如：20万元） 累计流入金额/累计流出金额在[M%,N%]范围内 （如：90%-110%内） 交易总笔数>= K 笔 （如：10笔）
        """
        inflow_outflow_ratio = inflow_amount / (inflow_amount + 1) # Avoid division by 0
        account_balance_threshold = private_account_balance_threshold if account_type == 'private' else public_account_balance_threshold
        is_abnormal = account_balance <= account_balance_threshold and inflow_amount >= inflow_amount_threshold and inflow_outflow_ratio >= inflow_outflow_ratio_min and inflow_outflow_ratio <= inflow_outflow_ratio_max and transaction_count_threshold >= 10
        return {
            'account_type': account_type,
            'account_balance': account_balance,
            'inflow_amount': inflow_amount,
            'inflow_outflow_ratio': inflow_outflow_ratio,
            'is_abnormal': is_abnormal,
            'risk_level': 'high' if is_abnormal else 'low'
        }

    def detect_public_account_outflow_patterns(self, outflow_count, outflow_amount, outflow_inflow_ratio_min=5, outflow_inflow_ratio_max=None, outflow_amount_threshold=200000, outflow_account_count_threshold=10):
        """
        模式10: 1、计算当天有转出交易的账户（对公/对私），如客户为对公客户，则客户名称要含有定的关键字（如：投资咨询、财富管理、资产管理、生态发展、科技发展、生物科技、咨询服务、养老保险、交易所、基金管理、股权投资、金融服务、金融信息、网络科技、电子商务等） 2、查询账户在短期内（如：10天）的所有交易 3、统计并比较 累计流出笔数/累计流入笔数>=X 倍 （如：5倍） 累计流入金额>= Y 元 （ 如：20万元） 累计流入金额/累计流出金额在[M%,N%]范围内 （如：90%-110%内） 流入时间均值<流出时间均值 转出的对私对手账户数量>=Z 户 （如：10户）
        """
        outflow_inflow_ratio = outflow_count / (outflow_count + 1) # Avoid division by 0
        is_abnormal = outflow_inflow_ratio >= outflow_inflow_ratio_min and (outflow_inflow_ratio_max is None or outflow_inflow_ratio <= outflow_inflow_ratio_max) and outflow_amount >= outflow_amount_threshold and outflow_account_count_threshold >= 10
        return {
            'outflow_count': outflow_count,
            'outflow_amount': outflow_amount,
            'outflow_inflow_ratio': outflow_inflow_ratio,
            'is_abnormal': is_abnormal,
            'risk_level': 'high' if is_abnormal else 'low'
        }