import csv


def main():
    name = get_team_name()
    save_team_data_to_csv(name)


def get_team_name():
    # Get user input of team name, allow any format for the user
    response = "n"
    while response == "n":
        team_name = input("Enter the team name: ").strip()
        confirmation = input(f"Is {team_name} the correct name? (Y/N)")
        response = confirmation.lower()
    return team_name


def save_team_data_to_csv(team_name, file_path="team_data.csv"):
    with open(file_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        # Save team name as a single string in the first cell
        writer.writerow([team_name])


if __name__ == "__main__":
    main()
