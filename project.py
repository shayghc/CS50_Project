import csv
from datetime import datetime, timedelta
import os
import random
import numpy as np

SIMULATIONS = 10000
NUM_ITEMS_TO_FORECAST = 100
MINIMUM_SPRINTS_DATA = 2


def main():
    team_name = get_valid_team_name()
    # Check if the CSV file exists
    if not os.path.exists("team_data.csv"):
        sprint_details = []
        # Run get_sprint_details six times and append the results to sprint_details
        for i in range(MINIMUM_SPRINTS_DATA):
            new_sprint = get_sprint_details(i + 1, sprint_details)
            while new_sprint is None:
                print(
                    "Sprint overlaps with existing sprint. Please choose a different start date."
                )
                new_sprint = get_sprint_details(i + 1, sprint_details)
            sprint_details.append(new_sprint)

            ####

        # Save sprint_details to the CSV file
        if all(sprint is not None for sprint in sprint_details):
            save_team_data_to_csv(team_name, sprint_details, "team_data.csv")

            # Perform Monte Carlo simulation
            result = monte_carlo_simulation("team_data.csv", SIMULATIONS, NUM_ITEMS_TO_FORECAST)

            print(f"\nMonte Carlo Simulation Results:")
            print(f"Estimated Mean Delivery Date: {result['mean_delivery_date'].strftime('%Y-%m-%d')}")
            print(f"Confidence Interval: [{result['lower_bound'].strftime('%Y-%m-%d')}, {result['upper_bound'].strftime('%Y-%m-%d')}]")
            print(f"Confidence Level: {result['confidence_level']}\n")


            ####
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


####

def monte_carlo_simulation(file_path, num_simulations, num_items):
    # Load historical throughput data from CSV
    historical_data = load_historical_data(file_path)

    if len(historical_data) < MINIMUM_SPRINTS_DATA:
        print("Error: Insufficient historical data for simulation.")
        return None

    # Generate random samples based on historical throughput data
    samples = generate_samples(historical_data, num_simulations, num_items)

    # Calculate mean and standard deviation of the simulated delivery dates
    mean_delivery_date = np.mean(samples)
    std_dev_delivery_date = np.std(samples)

    # Calculate confidence intervals
    confidence_level = 0.97
    z_score = calculate_z_score(confidence_level)
    margin_of_error = z_score * (std_dev_delivery_date / np.sqrt(num_simulations))

    # Calculate confidence intervals for delivery date
    lower_bound = mean_delivery_date - margin_of_error
    upper_bound = mean_delivery_date + margin_of_error

    return {
        "mean_delivery_date": mean_delivery_date,
        "lower_bound": lower_bound,
        "upper_bound": upper_bound,
        "confidence_level": confidence_level
    }



def load_historical_data(file_path):
    throughput_data = []

    try:
        with open(file_path, newline="") as csvfile:
            reader = csv.DictReader(csvfile)

            # Skip the first line (team name)
            next(reader)

            # Check if the expected columns are present in the CSV file
            required_columns = ["Sprint Start Date", "Sprint Throughput", "Sprint Duration"]

            if not all(column in reader.fieldnames for column in required_columns):
                return throughput_data

            for row in reader:

                try:
                    start_date = datetime.strptime(row["Sprint Start Date"], "%Y-%m-%d")
                    throughput = int(row["Sprint Throughput"])
                    duration = int(row["Sprint Duration"])

                    end_date = start_date + timedelta(days=duration)
                    throughput_data.extend([end_date] * throughput)
                except (KeyError, ValueError) as e:
                    print(f"Error processing row: {row}. {e}")

    except FileNotFoundError as e:
        print(f"Error: CSV file not found at '{file_path}'.")

    return throughput_data


def generate_samples(historical_data, num_simulations, num_items):
    samples = []

    for _ in range(num_simulations):
        # Randomly sample historical delivery dates
        sampled_dates = random.sample(historical_data, num_items)
        # Calculate the maximum date among the sampled dates
        max_delivery_date = max(sampled_dates)
        samples.append(max_delivery_date)

    return samples


def calculate_z_score(confidence_level):
    # Two-tailed z-score for the given confidence level
    return np.abs(np.percentile(np.random.normal(size=100000), (1 - confidence_level) * 100 / 2))



if __name__ == "__main__":
    main()
