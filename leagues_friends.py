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
            
            # Example: Extract data inside a specific tag
            # Adjust the tag name, class, or id based on the structure of the response
            content = soup.find(id="contentHiscores")  # Replace "div" and "stats" with the actual tag/class

            if content:
                 return content.prettify()  # Return the extracted data
                # rows = content.find_all("tr")
                # for row in rows:
                #     datas = row.find_all("td")
                #     for data in datas:
                #         if data.string == "":
                #             continue
                #         else      
            else:
                return "No matching tag found in the response."
        else:
            return f"Request failed with status code: {response.status_code}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

names = ["Noclis", "Im sacred"]
current_date = dt.now().strftime("%Y-%m-%d")
directory_path = os.path.join(".", current_date)
if not os.path.exists(directory_path):
    os.makedirs(directory_path)
    print(f"Directory created: {directory_path}")
else:
    print(f"Directory already exists: {directory_path}")

with open(f"{directory_path}/highscores.md", "w") as file:
    for name in names:
        result = fetch_hiscore_data(name)
        # print(mdf.markdownify(result))
        file.write(mdf.markdownify(result))