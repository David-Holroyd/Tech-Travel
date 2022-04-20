# Tech-Travel
Work Project


In order to accurately calculate travel distance from a field technician's home to a jobsite, this script found the distance to the 1000 most common customers.
The 1000 recent customers were determined by information in Salesforce. A total of 25,000 API calls were done in groups of 1,250.
The results were parsed to get the travel distance and time, using 4am on a Monday as the departure time. 
This information was then uploaded to a new object in Salesforce, with 2 flow automations to pull this information into the Shift object.
