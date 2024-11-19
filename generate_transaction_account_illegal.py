class AccountAnomalyDetector:
    def __init__(self, corporate_data):
        """
        初始化账户异常检测器

        Args:
            corporate_data (dict): 企业和客户信息数据，包含法人、联系电话、地址、代办人等信息
        """
        self.corporate_data = corporate_data

    def check_account_data_anomaly(self, person_id, x, y, m, n):
        """
        检测账户资料异常
        异常条件：
        1. 同一法人对应的对公账户数量 >= X
        2. 统一联系电话对应的对公账户数量 >= Y
        3. 联系地址对应的客户数量 >= M
        4. 同一代办人对应的客户数量 >= N

        Args:
            person_id (str): 目标客户ID
            x (int): 对公账户数量阈值
            y (int): 联系电话对应账户数量阈值
            m (int): 地址对应客户数量阈值
            n (int): 代办人对应客户数量阈值

        Returns:
            bool: 是否符合异常条件
        """
        legal_representative = self.corporate_data[person_id].get('legal_representative')
        contact_number = self.corporate_data[person_id].get('contact_number')
        address = self.corporate_data[person_id].get('address')
        agent = self.corporate_data[person_id].get('agent')

        # 查询同一法人对应的对公账户数量
        accounts_with_same_legal_rep = sum(
            1 for p in self.corporate_data.values() if p.get('legal_representative') == legal_representative)
        # 查询统一联系电话对应的对公账户数量
        accounts_with_same_contact = sum(
            1 for p in self.corporate_data.values() if p.get('contact_number') == contact_number)
        # 查询同一地址对应的客户数量
        accounts_with_same_address = sum(1 for p in self.corporate_data.values() if p.get('address') == address)
        # 查询同一代办人对应的客户数量
        accounts_with_same_agent = sum(1 for p in self.corporate_data.values() if p.get('agent') == agent)

        return (accounts_with_same_legal_rep >= x and
                accounts_with_same_contact >= y and
                accounts_with_same_address >= m and
                accounts_with_same_agent >= n)

    def check_sensitive_industry(self, person_id):
        """
        检测开户企业是否经营敏感行业
        敏感行业关键字：房地产项目、投资物业管理服务、企业管理咨询服务、投资管理咨询服务，
        或涉及区域特色或支柱产业，例如养殖种植、生物技术、养老服务等

        Args:
            person_id (str): 目标客户ID

        Returns:
            bool: 是否符合敏感行业条件
        """
        sensitive_keywords = ["房地产项目", "投资物业管理服务", "企业管理咨询服务", "投资管理咨询服务", "养殖", "种植",
                              "生物技术", "养老服务"]
        business_scope = self.corporate_data[person_id].get('business_scope', "")

        return any(keyword in business_scope for keyword in sensitive_keywords)

    def check_suspicious_company_type(self, person_id):
        """
        检测开户企业公司性质是否可疑
        可疑条件：注册在P2P网贷平台及工商部门的担保公司、投资公司等

        Args:
            person_id (str): 目标客户ID

        Returns:
            bool: 是否符合可疑公司性质条件
        """
        suspicious_keywords = ["P2P网贷", "担保公司", "投资公司"]
        registered_platform = self.corporate_data[person_id].get('registered_platform', "")

        return any(keyword in registered_platform for keyword in suspicious_keywords)
