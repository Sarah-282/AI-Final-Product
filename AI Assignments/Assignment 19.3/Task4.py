import pandas as pd
from pandas.testing import assert_frame_equal


def employees_above_salary(
    employees: pd.DataFrame, minimum_salary: int
) -> pd.DataFrame:
    """Select employee names and salaries above the given salary threshold."""
    return employees.loc[
        employees["salary"] > minimum_salary, ["name", "salary"]
    ].reset_index(drop=True)


if __name__ == "__main__":
    employees = pd.DataFrame(
        {
            "name": ["Ava", "Ben", "Cara", "Dev"],
            "salary": [62000, 50000, 75000, 48000],
            "department": ["Sales", "IT", "Finance", "IT"],
        }
    )

    actual = employees_above_salary(employees, 50000)
    expected = pd.DataFrame(
        {"name": ["Ava", "Cara"], "salary": [62000, 75000]}
    )
    assert_frame_equal(actual, expected)
    print(actual.to_string(index=False))