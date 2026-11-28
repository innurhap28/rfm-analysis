"""H&M 거래 데이터 전처리 및 고객 분석."""

from pathlib import Path

import pandas as pd


class DataAnalyzer:
    def __init__(self, data_path):
        self.df = None
        self.data_path = Path(data_path)

    def load_data(self, nrows=None):
        """거래 행에 고객 및 상품 정보를 연결한다."""
        transactions = pd.read_csv(
            self.data_path / "transactions_train.csv",
            dtype={"customer_id": "string", "article_id": "string"},
            parse_dates=["t_dat"],
            nrows=nrows,
        )
        customers = pd.read_csv(
            self.data_path / "customers.csv",
            usecols=["customer_id", "club_member_status", "age"],
            dtype={"customer_id": "string"},
        )
        articles = pd.read_csv(
            self.data_path / "articles.csv",
            usecols=["article_id", "prod_name", "product_group_name"],
            dtype={"article_id": "string"},
        )
        self.df = transactions.merge(
            customers, on="customer_id", how="left", validate="many_to_one"
        ).merge(articles, on="article_id", how="left", validate="many_to_one")
        return self.df

    def handle_missing_values(self, strategy='group_mean', group_col=None):
        # 결측치 처리 로직
        pass

    def detect_outliers(self, column, threshold=1.5):
        # IQR 기반 이상치 탐지
        q1 = self.df[column].quantile(0.25)
        q3 = self.df[column].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - threshold * iqr
        upper = q3 + threshold * iqr
        return self.df[(self.df[column] < lower) | (self.df[column] > upper)]

    def calculate_rfm(self, customer_col, date_col, amount_col):
        # RFM 점수 계산
        pass
