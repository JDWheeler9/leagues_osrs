import requests
import json
import argparse
from datetime import datetime as dt
import os

def fetch_leagues_hiscore_data(username):
    # URL of the API
    url = f"https://secure.runescape.com/m=hiscore_oldschool_seasonal/index_lite.json?player={username}"

    try:
        # Send the POST request
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            return response.json()
        else:
            return f"Request failed with status code: {response.status_code}"
    except Exception as e:
        return f"An error occurred: {str(e)}"


if __name__ == "__main__":
    
    # Setup flags 
    parser = argparse.ArgumentParser(description="Fetch and save Old School RuneScape hiscore data.")
    parser.add_argument("--dry-run", action="store_true", help="Does the lookup without creating files. This is useful for testing that your script is working correct.")
    parser.add_argument("--user", type=str, help="Run the script over the provided user")
    args = parser.parse_args()

    # One off user runs, default to agreed list if not
    if args.user:
        names = [args.user]
    else:
        names = [
                "Noclis",
                "Im sacred", 
                "Lrauq", 
                "GIM Tgump", 
                "Dranathulhu", 
                "EmoArbiter", 
                "FGCBrave", 
                "realNovatose"
                ]

    # Don't create files and just print results. Useful for testing
    if args.dry_run:
        for name in names:
            result = fetch_leagues_hiscore_data(name)
            print("Results for {}:\n{}\n".format(name,result))
    else:
        # Make the daily directory if it doesn't exists, will follow yyyy-mm-dd format
        current_date = dt.now().strftime("%Y-%m-%d")
        directory_path = os.path.join("./daily_runs", current_date)
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            print(f"Directory created: {directory_path}")

        # Fetch the response and write it to a file in the directory
        for name in names:
                with open("{}/{}.json".format(directory_path, name.replace(" ", "_")), "w") as file:
                    result = fetch_leagues_hiscore_data(name)
                    file.write(json.dumps(result, indent=4))
    
