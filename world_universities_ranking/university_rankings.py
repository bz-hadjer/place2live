import re
from csv import writer
from datetime import datetime

import requests


def get_current_year():
    return datetime.now().year


def get_data(year):
    """Get a list of all the universities and their information"""

    response = requests.get(
        f"https://www.timeshighereducation.com/world-university-rankings/{year}/world-ranking#!/length/-1/sort_by/rank/sort_order/asc/cols/stats"
    )

    if response.ok:
        part_url = re.search(
            f"world_university_rankings_{year}.*?\\.json", response.text
        ).group()
        url = f"https://www.timeshighereducation.com/sites/default/files/the_data_rankings/{part_url}"
        return requests.get(url).json()["data"]


def write_to_csv(universities):
    """Write the data into a csv file in the current directory"""

    with open("university_rankings.csv", "w") as f:
        w = writer(f)

        # Preparing the csv file header
        w.writerow(
            [
                "rank",
                "name",
                "location",
                "num_FTE_students",
                "num_students_per_staff",
                "international_students",
                "female_male_ratio",
            ]
        )

        # Writing information for each university
        for univ in universities:
            w.writerow(
                [
                    univ["rank"],
                    univ["name"],
                    univ["location"],
                    univ["stats_number_students"],
                    univ["stats_student_staff_ratio"],
                    univ["stats_pc_intl_students"],
                    univ["stats_female_male_ratio"],
                ]
            )


if __name__ == "__main__":
    year = get_current_year()
    data = get_data(year)
    write_to_csv(data)
