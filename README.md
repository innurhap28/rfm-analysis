# A1-1. RFM 기반 이커머스 고객 세분화

## 1. 프로젝트 개요

이커머스 데이터(수치, 텍스트, 범주, 날짜, 이미지 배열)를 통합 전처리하는 OOP 파이프라인을 구축하고, EDA 및 RFM 고객 세분화를 수행하여 데이터 기반 비즈니스 전략을 도출한다.

### 핵심 구현 목표
- **멀티모달 벡터 연산**: 외부 이미지/NLP 라이브러리 없이 `NumPy` 배열 연산만으로 이미지 통계량(Mean, Std) 및 텍스트 파생 변수 추출
- **파이프라인 모듈화**: `DataAnalyzer` 클래스 설계 (`load_data`, `handle_missing_values`, `detect_outliers`, `calculate_rfm`)
- **EDA 및 시각화**: 그룹별 결측치 대치, IQR 이상치 탐지 전후 비교, 필수 6종 차트(히스토그램, 박스플롯, 막대그래프, 히트맵, 산점도, 라인차트) 구현
- **RFM 세분화**: 고객을 4개 이상 세그먼트로 분류하고 비즈니스 인사이트 3가지 이상 도출

---

## 2. 데이터 명세

### 데이터셋 정보
- **데이터셋**: H&M Personalized Fashion Recommendations
- **제공 기관**: H&M Group
- **데이터 출처**: Kaggle
- **대회 페이지**: https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations
- **데이터 설명**: https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations/data
- **라이선스 및 이용 조건**: Kaggle Competition Rules 적용

### 데이터셋 선정 이유
H&M의 실제 이커머스 구매 기록과 고객·상품 메타데이터를 함께 제공하는 데이터셋이다. 고객의 구매 이력뿐 아니라 연령, 멤버십 상태, 상품 종류, 색상, 상품 설명 및 이미지 정보를 포함하고 있어 멀티모달 데이터 분석과 RFM 고객 세분화를 함께 수행하기에 적합하다.

### 데이터 구성

| 파일 | 설명 | 주요 식별자 |
|---|---|---|
| `transactions_train.csv` | 고객별 상품 구매 기록 | `customer_id`, `article_id` |
| `customers.csv` | 고객 속성 및 회원 정보 | `customer_id` |
| `articles.csv` | 상품 정보 및 분류·설명 | `article_id` |
| `images/` | 상품 이미지 파일 | `article_id` |

`sample_submission.csv`는 대회 예측 결과 제출용 파일이므로 이번 분석에서는 사용하지 않는다.

### 주요 컬럼

**transactions_train.csv**

| 컬럼 | 설명 |
|---|---|
| `t_dat` | 구매 날짜 |
| `customer_id` | 고객 고유 ID |
| `article_id` | 상품 고유 ID |
| `price` | 구매 상품 가격 값 |
| `sales_channel_id` | 판매 채널 구분 |

**customers.csv**

| 컬럼 | 설명 |
|---|---|
| `customer_id` | 고객 고유 ID |
| `FN` | 패션 뉴스 관련 정보 |
| `Active` | 고객 활성 상태 관련 정보 |
| `club_member_status` | 멤버십 상태 |
| `fashion_news_frequency` | 패션 뉴스 수신 빈도 |
| `age` | 고객 나이 |
| `postal_code` | 우편번호 정보 |

**articles.csv**

| 컬럼 | 설명 |
|---|---|
| `article_id` | 상품 고유 ID |
| `product_code` | 상품 코드 |
| `prod_name` | 상품명 |
| `product_type_name` | 상품 종류 |
| `product_group_name` | 상품 그룹 |
| `graphical_appearance_name` | 상품 패턴 및 외형 |
| `colour_group_name` | 상품 색상 |
| `department_name` | 상품 부서 |
| `index_name` | 상품 분류 |
| `section_name` | 상품 세부 섹션 |
| `garment_group_name` | 의류 그룹 |
| `detail_desc` | 상품 상세 설명 |

### 데이터 연결 구조
- `transactions_train.csv`와 `customers.csv`는 `customer_id`를 기준으로 연결한다.
- `transactions_train.csv`와 `articles.csv`는 `article_id`를 기준으로 연결한다.
- 상품 이미지도 `article_id`를 기준으로 연결한다.
- 이미지 파일은 `article_id`의 앞 세 자리를 기준으로 하위 폴더에 배치되어 있다. 단, 모든 상품에 대응하는 이미지가 존재하지는 않는다.

### RFM 분석 기준

| 지표 | 사용 컬럼 | 계산 방식 |
|---|---|---|
| Recency | `t_dat` | 분석 기준일과 고객별 마지막 구매일의 차이 |
| Frequency | `customer_id` | 고객별 구매 기록 행 개수 |
| Monetary | `price` | 고객별 가격 합계 |

**분석 시 유의사항**
- 원본 거래 데이터에는 별도의 주문 ID와 수량 컬럼이 없다.
- Kaggle 데이터 설명에 따르면 동일한 거래 행이 반복되는 경우 동일 상품의 복수 구매를 의미할 수 있다. 따라서 Frequency는 실제 주문 횟수가 아닌 구매 기록 행 개수를 대리 지표로 사용한다.
- Monetary는 제공된 `price` 값의 합계로 계산하며, 수량 정보가 없으므로 정확한 총 결제액으로 단정하지 않는다.
- 가격의 통화 및 단위는 원본 데이터 정의를 확인하기 전까지 임의로 해석하지 않는다.
- Recency 기준일은 거래 데이터의 최종 구매일로 정의한다.

### 라이선스 및 데이터 이용 조건

본 프로젝트는 Kaggle의 H&M Personalized Fashion Recommendations 대회 데이터를 교육 및 학술 연구 목적으로 활용한다.

Kaggle Competition Rules에 명시된 데이터 이용 조건은 비상업적 목적 및 학술 연구이며, Competition Data를 규칙에 동의하지 않은 제3자에게 전송·복제·공개·재배포하거나 접근 가능하게 제공해서는 안 된다.

이에 따라 다음 사항을 준수한다.
- 원본 CSV 및 이미지 데이터는 Git 저장소에 업로드하지 않는다.
- `.gitignore`에 데이터 디렉토리를 등록하여 원본 데이터가 Git 추적 대상에 포함되지 않도록 한다.
- 데이터 이용 및 공유는 Kaggle 공식 Competition Rules를 따른다.
- 데이터의 상업적 이용이나 재배포를 허용하는 것으로 해석하지 않는다.

참고: https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations/rules

---

## 3. 디렉토리 구조 및 실행 방법

### 디렉토리 구조

```text
rfm-analysis/
├── .venv/                      # Python 가상환경 (Git 제외)
├── data/                       # 원본 및 전처리 데이터 (Git 제외)
├── src/
│   └── pipeline.py             # DataAnalyzer 클래스 모듈
├── notebooks/
│   └── analysis_report.ipynb   # EDA, 통계 분석, 시각화, RFM 분석 리포트
├── README.md
├── requirements.txt            # 프로젝트 의존성
└── .gitignore
```

### 개발 환경 및 제약 사항
- **Python**: 3.8 이상
- **가상환경**: Python `venv`
- **허용 라이브러리**: `NumPy`, `Pandas`, `Matplotlib`, `Seaborn`
- **금지 라이브러리**: OpenCV, Pillow, Scikit-learn, NLTK, 자동 EDA 라이브러리(pandas-profiling, sweetviz 등)

### 가상환경 설치 및 설정

프로젝트별 패키지 의존성을 분리하기 위해 Python 가상환경을 사용한다.

**1. 가상환경 생성**

프로젝트 루트 디렉토리에서 실행한다.

```bash
python3 -m venv .venv
```

**2. 가상환경 활성화**

macOS / Linux:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

활성화되면 터미널 프롬프트에 `(.venv)`가 표시된다.

**3. pip 업데이트 및 라이브러리 설치**

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**4. VS Code 인터프리터 설정**

1. VS Code에서 프로젝트 폴더를 연다.
2. `Cmd + Shift + P`를 눌러 명령 팔레트를 연다.
3. `Python: Select Interpreter`를 검색한다.
4. 프로젝트 내부의 `.venv` 가상환경을 선택한다.

**5. 가상환경 비활성화**

```bash
deactivate
```

### requirements.txt

프로젝트에서 사용하는 라이브러리를 `requirements.txt`에 기록한다.

```text
numpy
pandas
matplotlib
seaborn
```

### 실행 방법

저장소 복제:

```bash
git clone [Repository URL]
cd [Repository Name]
```

가상환경 생성 및 활성화:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

라이브러리 설치:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

분석 파이프라인 실행:

```bash
python src/pipeline.py
```

EDA 및 RFM 분석은 `notebooks/analysis_report.ipynb`에서 진행한다.

---

## 4. 비즈니스 인사이트 (분석 완료 후 작성)

각 인사이트는 아래 3가지 요소를 필수 포함하여 3가지 이상 작성한다.

### 인사이트 1. [제목]
- **(근거)**: 인사이트를 뒷받침하는 수치 또는 그래프 1개 이상
- **(실행)**: 대상 세그먼트 + 실행 방법 + 기대 효과
- **(검증)**: 추가로 필요한 데이터 또는 반증 가능성 1문장

### 인사이트 2. [제목]
- **(근거)**:
- **(실행)**:
- **(검증)**:

### 인사이트 3. [제목]
- **(근거)**:
- **(실행)**:
- **(검증)**: