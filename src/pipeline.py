"""H&M 거래 데이터 전처리 및 고객 분석."""

from pathlib import Path

import numpy as np
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

    def handle_missing_values(
        self, strategy="group_mean", group_col="club_member_status", column="age"
    ):
        """그룹 통계로 결측치를 채우고 통계가 없는 그룹은 전체 통계를 사용한다."""
        statistics = {"group_mean": "mean", "group_median": "median"}
        if strategy not in statistics:
            raise ValueError(f"지원하지 않는 결측치 대치 전략: {strategy}")
        statistic = statistics[strategy]
        values = self.df[column]
        by_group = self.df.groupby(group_col, dropna=False)[column].transform(statistic)
        self.df[column] = values.fillna(by_group).fillna(values.agg(statistic))
        return self.df

    def add_text_features(self, column="prod_name"):
        self.df["word_count"] = self.df[column].str.split().str.len().astype("Int64")
        return self.df

    @staticmethod
    def image_statistics(pixels):
        """이미지 배열 전체의 픽셀 평균과 모집단 표준편차를 계산한다."""
        return np.mean(pixels, dtype=np.float64), np.std(pixels, dtype=np.float64)

    def detect_outliers(self, column, threshold=1.5):
        # IQR 기반 이상치 탐지
        q1 = self.df[column].quantile(0.25)
        q3 = self.df[column].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - threshold * iqr
        upper = q3 + threshold * iqr
        return self.df[(self.df[column] < lower) | (self.df[column] > upper)]

    def calculate_rfm(
        self, customer_col="customer_id", date_col="t_dat", amount_col="price",
        *, reference_date=None, chunksize=None
    ):
        """현재 거래 데이터 또는 원본 CSV 전체에서 고객별 RFM을 집계한다."""
        if chunksize is None:
            batches = (self.df,)
        else:
            batches = pd.read_csv(
                self.data_path / "transactions_train.csv",
                usecols=[customer_col, date_col, amount_col],
                dtype={customer_col: "string"},
                parse_dates=[date_col],
                chunksize=chunksize,
            )

        totals = None
        for batch in batches:
            valid = batch.dropna(subset=[customer_col, date_col, amount_col])
            partial = valid.groupby(customer_col, sort=False).agg(
                last_purchase=(date_col, "max"),
                frequency=(date_col, "size"),
                monetary=(amount_col, "sum"),
            )
            if totals is None:
                totals = partial
            else:
                totals = pd.concat([totals, partial]).groupby(level=0, sort=False).agg(
                    last_purchase=("last_purchase", "max"),
                    frequency=("frequency", "sum"),
                    monetary=("monetary", "sum"),
                )
        if totals is None or totals.empty:
            raise ValueError("RFM 계산에 사용할 유효 거래가 없습니다.")

        last_purchase = totals.pop("last_purchase")
        latest = last_purchase.max().normalize()
        reference = latest if reference_date is None else pd.Timestamp(reference_date).normalize()
        if reference < latest:
            raise ValueError("분석 기준일은 마지막 거래일보다 빠를 수 없습니다.")

        totals.insert(0, "recency", (reference - last_purchase.dt.normalize()).dt.days)
        for metric, score in (
            ("recency", "r_score"), ("frequency", "f_score"), ("monetary", "m_score")
        ):
            ranks = totals[metric].rank(pct=True, ascending=metric != "recency")
            totals[score] = np.ceil(ranks * 5).astype("int8")

        recent = totals["r_score"] >= 4
        frequent = totals["f_score"] >= 4
        high_spend = totals["m_score"] >= 4
        totals["segment"] = np.select(
            [recent & frequent & high_spend, frequent, recent & (totals["frequency"] == 1),
             totals["r_score"] <= 2],
            ["VIP", "Loyal", "New", "At Risk"],
            default="Regular",
        )
        totals.attrs["reference_date"] = reference
        return totals
