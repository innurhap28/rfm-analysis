import pandas as pd

# 데이터 로드
transactions = pd.read_csv(
    "raw/transactions_train.csv",
    nrows=100_000
)

customers = pd.read_csv(
    "raw/customers.csv"
)

articles = pd.read_csv(
    "raw/articles.csv"
)

# 데이터 크기
print(transactions.shape)
print(customers.shape)
print(articles.shape)

# 앞부분 확인
print(transactions.head())
print(customers.head())
print(articles.head())

# 데이터 타입 및 결측치
transactions.info()
customers.info()
articles.info()

# 통계 요약
print(transactions.describe())
print(customers.describe())
print(articles.describe(include="all"))


# 결측치 확인
# 전체 데이터가 아닌 표본 기준이다
def missing_report(df):
    result = pd.DataFrame({
        "missing_count": df.isnull().sum(),
        "missing_ratio": df.isnull().mean() * 100
    })

    return result.sort_values(
        by="missing_ratio",
        ascending=False
    )

print(missing_report(transactions))
print(missing_report(customers))
print(missing_report(articles))