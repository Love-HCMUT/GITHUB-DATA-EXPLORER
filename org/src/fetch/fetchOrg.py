import aiohttp
import asyncio
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
import numpy as np
import pytz
import requests

TOKEN = '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'

async def fetchAPI(urls, TOKEN):
    HEADERS = {
        "Accept": "application/vnd.github+json",
        "Authorization" : f"Bearer {TOKEN}"
    }
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
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error has occurred: {err}")



async def fetchOrgInfo(orgname, TOKEN): 
    data = await fetchAPI(f'https://api.github.com/orgs/{orgname}', TOKEN)
    list = ['login', 'email', 'followers', 'created_at', 'description', 'location', 'avatar_url']
    Infor = {}
    for e in data.keys(): 
        if e in list: 
            Infor.update({e : data[e]})
    
    # get members
    perpage = 100
    page = 1
    countMem = 0
    while (True): 
        data = await fetchAPI(f'https://api.github.com/orgs/{orgname}/members?per_page={perpage}&page={page}', TOKEN)
        members = np.array(data)
        if (members.size == 0): break 
        countMem += members.size
        page += 1
    
    Infor.update({'members' : countMem})

    return Infor