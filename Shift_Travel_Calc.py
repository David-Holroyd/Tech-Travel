import requests
import pandas as pd

# API key
with open('Config.txt') as f:
    api_key = f.read()

# I have the addresses, names, and salesforce IDs of the 25 techs in this file
tech_file = r'C:\Users\DavidHolroyd\Salesforce\Tech Travels\All_Tech_Addresses.xlsx'

tech_df = pd.read_excel(tech_file, usecols=['Name', 'Address', 'City', 'State', 'Zip Code', 'ID'])
print(tech_df)
tech_list = tech_df.values.tolist()  # Convert this dataframe to a list of lists. This lets us iterate over it

# This adds the street address, city, state and zip code into one text string for each time at [6]
for tech in tech_list:
    tech[4] = str(tech[4])
    if len(tech[4]) == 4:
        tech[4] = '0' + tech[4]
    tech.append(tech[1] + ' ' + tech[2] + ', ' + tech[3] + ' ' + tech[4])


# Base url for API. unix time = 1648454400, this corresponds to 3/28/2022 4:00am EST. This is the leaving time for techs
url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&mode=driving&traffic_model=best_guess&departure_time=1648454400"

# Read the SF Account ID and the address from this excel file
account_df = pd.read_csv(r'C:\Users\DavidHolroyd\Salesforce\Tech Travels\Project_0317.csv',
                         usecols=['1000 Recent Accounts', 'Full_Address'])

# This filters out null values, so now the dataframe only has 1000 Accounts and no nulls/blanks.
# Convert the dataframe to a list of lists for iteration later
account_df = account_df[account_df.Full_Address.notnull()]
account_list = account_df.values.tolist()

# Check to make sure we have 1000 Accounts and 25 Techs
print(len(account_list))
print(len(tech_list))

gmaps_results = []
calls = 0

for account in account_list[:50]:  # To avoid overwhelming the API, this was run in groups of 50 accounts (1,250 calls) 
    work = account[1]  # Grab the company address for this company
    sf_id = account[0]  # Grab the company ID for this company
    for tech in tech_list:
        calls += 1
        print(f"Calling Gmaps API {calls}/25,000")
        if calls % 26 == 0:  # Every 25 calls to the API, cache our results in an excel file
            gmaps_results_df = pd.DataFrame(gmaps_results)
            gmaps_results_df.to_excel(r"C:\Users\DavidHolroyd\Salesforce\Tech Travels\Gmaps_results3 0323.xlsx", index=False)
        else:
            pass

        home = tech[6]
        r = requests.get(url + "&origins=" + home + "&destinations=" + work + "&key=" + api_key)  # This calls gmaps API
        print(r)
        print(r.json())
        time = r.json()["rows"][0]["elements"][0]["duration"]["text"]  # Parse the results to get the time (hrs & mins)
        distance = r.json()["rows"][0]["elements"][0]["distance"]["text"]  # Parse the results to get miles
        gmaps_results.append([tech[0], tech[1], tech[2], tech[3], tech[4], tech[5], tech[6], work, sf_id, time, distance])

gmaps_results_df = pd.DataFrame(gmaps_results)

gmaps_results_df.to_excel(r"C:\Users\DavidHolroyd\Salesforce\Tech Travels\Gmaps_All_Results.xlsx", index=False)
