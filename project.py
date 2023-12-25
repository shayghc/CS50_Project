def main():
    get_team_name()


def get_team_name():
    # Get user input of team name, allow any format for the user
    response = "n"
    while response == "n":
        team_name = input("Enter the team name: ").strip()
        confirmation = input(f"Is {team_name} the correct name? (Y/N)")
        response = confirmation.lower()
    return team_name


if __name__ == "__main__":
    main()