import csv
from datetime import datetime, timedelta
import os


def main():
    team_name = get_valid_team_name()
    # Check if the CSV file exists
    if not os.path.exists("team_data.csv"):
        sprint_details = []
        # Run get_sprint_details six times and append the results to sprint_details
        for i in range(2):
            new_sprint = get_sprint_details(i + 1, sprint_details)
            while new_sprint is None:
                print(
                    "Sprint overlaps with existing sprint. Please choose a different start date."
                )
                new_sprint = get_sprint_details(i + 1, sprint_details)
            sprint_details.append(new_sprint)

        # Save sprint_details to the CSV file
        if all(sprint is not None for sprint in sprint_details):
            save_team_data_to_csv(team_name, sprint_details, "team_data.csv")

            # Call the simulate_delivery_date function from main
            simulate_delivery_date(sprint_details)
        else:
            print("Failed to generate CSV file due to overlapping sprints.")
    else:
        print("CSV file already exists. Skipping data generation.")
    


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
            print("Enter 'Y' to confirm a correct team name")


def get_sprint_details(count, existing_sprints):
    # Get sprint start date from the user
    while True:
        try:
            start_date_str = input(
                f"Enter start date for sprint {count} (YYYY-MM-DD): "
            )
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")

            break
        except ValueError:
            print("Invalid date format. Please enter date in YYYY-MM-DD format.")

    # Get throughput from the user
    while True:
        try:
            throughput = int(input("Enter throughput (number of tasks completed): "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer for throughput.")

    # Get sprint duration from the user
    while True:
        try:
            sprint_duration = int(input("Enter sprint duration (calendar days): "))
            if 7 <= sprint_duration <= 30:
                break
            else:
                print("Sprint duration must be between 7 and 30 days.")
        except ValueError:
            print("Invalid input. Please enter a valid integer for sprint duration.")

    # Check for sprint overlap
    sprint_start = start_date
    sprint_end = start_date + timedelta(days=sprint_duration)
    overlap_detected = any(
        existing_sprint
        and datetime.strptime(existing_sprint.get("sprint_start_date", ""), "%Y-%m-%d")
        < sprint_end
        and datetime.strptime(existing_sprint.get("sprint_start_date", ""), "%Y-%m-%d")
        + timedelta(days=existing_sprint.get("sprint_duration", 0))
        > sprint_start
        for existing_sprint in existing_sprints
    )

    if not overlap_detected:
        return {
            "sprint_start_date": start_date.strftime("%Y-%m-%d"),
            "sprint_throughput": throughput,
            "sprint_duration": sprint_duration,
        }


def save_team_data_to_csv(team_name, sprint_details, file_path="team_data.csv"):
    with open(file_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        # Save team name as a single string in the first cell
        writer.writerow([team_name])

        # Write header row
        writer.writerow(["Sprint Start Date", "Sprint Throughput", "Sprint Duration"])

        # Write sprint data rows
        for sprint_data in sprint_details:
            writer.writerow(
                [
                    sprint_data["sprint_start_date"],
                    sprint_data["sprint_throughput"],
                    sprint_data["sprint_duration"],
                ]
            )


if __name__ == "__main__":
    main()
