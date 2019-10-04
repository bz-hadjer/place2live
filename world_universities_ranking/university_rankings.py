import re
from csv import writer
from datetime import datetime

import requests


def get_current_year():
    """Get the current year"""
    return datetime.now().year


def get_data():
    """Get a list of all the universities and their information"""

    year = get_current_year()
    base = "https://www.timeshighereducation.com/"
    url = f"{base}world-university-rankings/{year}/world-ranking#"
    res = requests.get(url)

    if res.ok:
        part_url = re.search(
            f"world_university_rankings_{year}.*?\\.json", res.text,
        ).group()
        url = f"{base}sites/default/files/the_data_rankings/{part_url}"
        return requests.get(url).json()["data"]
    else:
        return None


def write_to_csv():
    """Write the data into a csv file in the current directory"""

    universities = get_data()
    with open("university_rankings.csv", "w") as csv_file:
        csv_writer = writer(csv_file)

        # Preparing the csv file header
        csv_writer.writerow(
            [
                "rank",
                "name",
                "location",
                "num_FTE_students",
                "num_students_per_staff",
                "international_students",
                "female_male_ratio",
            ],
        )

        # Writing information for each university
        for univ in universities:
            csv_writer.writerow(
                [
                    univ["rank"],
                    univ["name"],
                    univ["location"],
                    univ["stats_number_students"],
                    univ["stats_student_staff_ratio"],
                    univ["stats_pc_intl_students"],
                    univ["stats_female_male_ratio"],
                ],
            )


if __name__ == "__main__":
    write_to_csv()
