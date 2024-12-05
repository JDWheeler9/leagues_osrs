import requests
from bs4 import BeautifulSoup
import markdownify as mdf
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
    url = "https://secure.runescape.com/m=hiscore_oldschool_seasonal/hiscorepersonal"

    # Parameters to include in the body
    payload = {
        "user1": username,
        "submit": "Submit"
    }

    try:
        # Send the POST request
        response = requests.post(url, data=payload)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML response using BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Find just the highscores data
            content = soup.find(id="contentHiscores")

            # Only add if we got something back
            if content:
                 return content.prettify()  # Return the extracted data, in a pretty html format  
            else:
                return "No matching tag found in the response."
        else:
            return f"Request failed with status code: {response.status_code}"
    except Exception as e:
        return f"An error occurred: {str(e)}"


### Main script start

# Add any new names here
names = ["Noclis", "Im sacred", "Lrauq", "GIM Tgump", "Dranathulhu", "EmoArbiter", "FGCBrave", "realNovatose"]

# Make directory for current day
current_date = dt.now().strftime("%Y-%m-%d")
directory_path = os.path.join(".", current_date)
if not os.path.exists(directory_path):
    os.makedirs(directory_path)
    print(f"Directory created: {directory_path}")
else:
    print(f"Directory already exists: {directory_path}")

# Fetch and write to files
with open(f"{directory_path}/highscores.md", "w") as file:
    for name in names:
        result = fetch_hiscore_data(name)
        file.write(mdf.markdownify(result))

print("Link to file: https://github.com/JDWheeler9/leagues_osrs/blob/main/" + current_date +"/highscores.md")