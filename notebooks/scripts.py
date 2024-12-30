from sqlite3 import connect

conn = connect("..\\data\\housing.db")
cur = conn.cursor()
LOAN_TERM_IN_YEARS = 30

def get_annual_interest_rate(year: int) -> float:
    cur.execute("SELECT avg_rate FROM us_mortgage_rate WHERE year = ?", (year,))
    result = cur.fetchone()
    return result[0]


def get_monthly_payment(year: int, mortgage: float) -> float:
    p = mortgage
    r = get_annual_interest_rate(year) / 12
    n = LOAN_TERM_IN_YEARS * 12

    numerator = r * (1 + r) ** n
    denominator = (1 + r) ** n - 1
    return p * (numerator / denominator)



def get_salary_cut_from_mortgage(year: int, mortgage: float, salary: float) -> float:
    monthly_pay = salary / 12
    return get_monthly_payment(year, mortgage) / monthly_pay


def get_salary_cut_from_state_and_year(state: str, year: int):
    cur.execute("SELECT median_salary FROM salary WHERE state = ? AND year = ?", (state, year))
    salary: float = cur.fetchone()[0]

    cur.execute("SELECT typical_home_value FROM house_sale WHERE state = ? and year = ?", (state, year))
    mortgage: float = cur.fetchone()[0]
    return get_salary_cut_from_mortgage(year, mortgage, salary)


def get_us_salary_cut_from_year(year: int):
    cur.execute("SELECT median_salary FROM us_salary WHERE year = ?", (year,))
    salary: float = cur.fetchone()[0]

    cur.execute("SELECT median_sale FROM us_house_sale WHERE year = ?", (year,))
    mortgage: float = cur.fetchone()[0]
    return get_salary_cut_from_mortgage(year, mortgage, salary)
