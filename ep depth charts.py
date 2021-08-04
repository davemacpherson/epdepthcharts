import csv
from bs4 import BeautifulSoup
import requests
import re
import time
from random import randint

# List of all teams to be passed to the URL
team_list = ["1580/anaheim-ducks","72/arizona-coyotes","52/boston-bruins","53/buffalo-sabres","54/calgary-flames","55/carolina-hurricanes","56/chicago-blackhawks","57/colorado-avalanche","58/columbus-blue-jackets","59/dallas-stars","60/detroit-red-wings","61/edmonton-oilers","62/florida-panthers","79/los-angeles-kings","63/minnesota-wild","64/montreal-canadiens","65/nashville-predators","66/new-jersey-devils","67/new-york-islanders","68/new-york-rangers","69/ottawa-senators","70/philadelphia-flyers","71/pittsburgh-penguins","73/san-jose-sharks","74/st.-louis-blues","75/tampa-bay-lightning","76/toronto-maple-leafs","77/vancouver-canucks","22211/vegas-golden-knights","78/washington-capitals","9966/winnipeg-jets", "27336/seattle-kraken"]
# List of shortened team names to use for output
team_list_short = ["ANA","ARI","BOS","BUF","CGY","CAR","CHI","COL","CBJ","DAL","DET","EDM","FLA","LAK","MIN","MTL","NSH","NJD","NYI","NYR","OTT","PHI","PIT","SJS","STL","TBL","TOR","VAN","VGK","WSH","WPG","SEA"]

# Initialize and loop through the team list
team_no = 0
while team_no < 32:
    # Select the team URL and shortened name from the two lists
    team_id = team_list[team_no]
    team_short = team_list_short[team_no]
    # Assign the URL for the specific team
    url = "https://www.eliteprospects.com/team/{team_id}/depth-chart".format(team_id=team_id)
    # Load the HTML from the URL
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser") 
    # Find the table containing the list of players
    depthtable = soup.find_all("div", class_="table-wizard")[1]
    # Find all the rows of the table
    playerrows = depthtable.find_all('tr')
    # Initialize an empty list to populate for output
    playerlist = []
    # Iterate through all rows of the table
    for i in range(1, len(playerrows)):
        # Check if the row is a header row. If it is, skip it
        checkrow = playerrows[i].select('tr > td')[1].get_text(strip=True)
        if checkrow == "C" or checkrow == "LW" or checkrow == "RW" or checkrow == "D" or checkrow == "G":
            continue
        else:
        # If the row is not a header row, append the output list with the team's shortened name, the player's signing status, the player's name, their contract end year, their cap hit, their EliteProspects URL, and their CapFriendly URL
            playerlist.append([team_list_short[team_no], playerrows[i].select('tr > td')[0].get_text(strip=True), playerrows[i].select('tr > td')[1].get_text(strip=True), playerrows[i].select('tr > td')[3].get_text(strip=True), playerrows[i].select('tr > td')[4].get_text(strip=True), playerrows[i].select('tr > td')[1].find('a').attrs['href'], playerrows[i].select('tr > td')[4].find('a').attrs['href']])
    print(playerlist)
    # Write the output to a CSV file
    with open("depth charts.csv", "a", encoding="utf-16") as f:
        writer = csv.writer(f, delimiter="|")
        writer.writerows(playerlist) 
    # Add one to the team list to move to the next team
    team_no = team_no + 1
    print(team_no)
    # Take a quick nap so we don't make EP angry
    time.sleep(randint(3,5))

