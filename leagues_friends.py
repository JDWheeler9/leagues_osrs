import requests
import json
from datetime import datetime as dt
import os

def fetch_hiscore_data(username):
    """
    Fetches the hiscore data for a given username.
    
    Args:
        username (str): The username to query.
    
    Returns:
        str: Extracted data from the HTML response or a message indicating no data was found.
    """
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


### Main script start

# Add any new names here
names = ["Noclis", "Im sacred", "Lrauq", "GIM Tgump", "Dranathulhu", "EmoArbiter", "FGCBrave", "realNovatose"]

# Make directory for current day
current_date = dt.now().strftime("%Y-%m-%d")
directory_path = os.path.join("./daily_runs", current_date)
if not os.path.exists(directory_path):
    os.makedirs(directory_path)
    print(f"Directory created: {directory_path}")
else:
    print(f"Directory already exists: {directory_path}")

# Fetch and write to files
for name in names:
        with open("{}/{}.json".format(directory_path, name.replace(" ", "_")), "w") as file:
            result = fetch_hiscore_data(name)
            print(name + ":")
            print(result)
            file.write(json.dumps(result, indent=4))