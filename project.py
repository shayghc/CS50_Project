import csv
from datetime import datetime


def main():
    name = get_valid_team_name()
    save_team_data_to_csv(name)
    sprint_details = get_sprint_details()
    print("Sprint Date:", f"{sprint_details}")


def get_valid_team_name():
    # Get user input of team name, allow any format (except blank) for the user
    while True:
        team_name = input("Enter the team name: ").strip()
        confirmation = input(f"Is {team_name} the correct name? (Y/N)").lower()

        if team_name and confirmation == "y":
            return team_name
        elif not team_name:
            print("Sorry, team name cannot be blank")
        else:
            print("Invalid response. Please enter 'Y' to confirm")


def save_team_data_to_csv(team_name, file_path="team_data.csv"):
    with open(file_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        # Save team name as a single string in the first cell
        writer.writerow([team_name])


def get_sprint_details():
    # Get sprint start date from the user
    while True:
        try:
            start_date_str = input("Enter sprint start date (YYYY-MM-DD): ")
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            print(start_date)
            break
        except ValueError:
            print("Invalid date format. Please enter date in YYYY-MM-DD format.")

    return {
        "start_year": start_date.strftime("%Y-%m-%d")
        }


if __name__ == "__main__":
    main()
