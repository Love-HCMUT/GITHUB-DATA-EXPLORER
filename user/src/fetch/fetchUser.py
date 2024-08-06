import aiohttp
import asyncio
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
import numpy as np
import pytz
import requests

TOKEN = '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'

HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization" : f"Bearer {TOKEN}"
}

async def fetchAPI(urls):
    async with aiohttp.ClientSession() as session:
        try: 
            async with session.get(urls, headers=HEADERS) as response:
                response.raise_for_status()
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    print(f"Error: {response.status}, {await response.text()}")
                    return None
        except aiohttp.ClientResponseError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error has occurred: {err}")


# input: a dict contain data for each month, number of months need to analysis
# output: a dict contain data for each month 
def CreateListOfMonth(data, numberOfMonths): 
    current_date = datetime.now()
    months = [(current_date - relativedelta(months=(numberOfMonths- i - 1))).strftime("%B") for i in range(numberOfMonths)]
    ReponseData = { e : 0 for e in months }
    for key, value in data.items():
        if key in ReponseData:
            ReponseData[key] = value
    return ReponseData


# FETCH ACTICITIES WITHIN RECENT 3 MONTHS 
async def fetchTimeActivity(username): 
    perpage = 30
    page = 1 
    month = 0  
    count = 0  #count actitvies in a month
    activities = {} 
    previous_months = datetime.now(pytz.UTC).strftime('%B') #get curent month 
    
    while (month < 7): 
        data = await fetchAPI(f'https://api.github.com/users/{username}/events?per_page={perpage}&page={page}')
        list = np.array(data)
        if (list.size == 0): 
            activities.update({previous_months : count})
            break 
        
        # grap the last element of the list 
        lastElement = list[-1]
        createAt = lastElement['created_at']
        date = datetime.strptime(createAt, "%Y-%m-%dT%H:%M:%SZ")
        month_name = date.strftime("%B")

        if (month_name != previous_months): 
            for e in list: 
                time = e['created_at']
                timeformat = datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
                month_name = timeformat.strftime("%B")
                if (month_name != previous_months): 
                    activities.update({previous_months : count})
                    previous_months = month_name
                    count = 0
                    month += 1
                count += 1
        else: 
            count += list.size
        
        page += 1 #increase page index       
    
    # create response data 
    ReponseData = CreateListOfMonth(activities, 3)
    return ReponseData