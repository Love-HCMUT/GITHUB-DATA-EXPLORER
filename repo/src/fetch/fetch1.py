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
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error has occurred: {err}")


#GET 10 GREATEST CONTRIBUTORS 
async def fetchRepoContributors(username, reponame): 
    perpage = 100
    contributors = {}
    page = 1
    count = 0
    while (count < 10): 
        data = await fetchAPI(f'https://api.github.com/repos/{username}/{reponame}/contributors?per_page={perpage}&page={page}')
        list = np.array(data)
        if (list.size == 0): break
        index = 0
        while (count < 10 and index < list.size):
            contributors.update({list[index]['login'] : list[index]['contributions']})
            count += 1
            index += 1
        page += 1
    return contributors


#FETCH COMMITS SINCE ... UNTIL ...
async def fetchRepoCommitSinceUntil(username, reponame, since, until):
    page = 1
    perpage = 100 
    count = 0
    while (True): 
        data = await fetchAPI(f'https://api.github.com/repos/{username}/{reponame}/commits?since={since}&until={until}&per_page={perpage}&page={page}')
        list = np.array(data)
        if (list.size == 0): break
        count += list.size
        page += 1
    return count 


# FETCH COMMITS WITHIN 6 RECENT MONTHS 
async def fetchRepoCommits(username, reponame): 
    commitLine = {}
    # fetch commits in the current months, since the first until current date 
    until = datetime.now(pytz.UTC) # get current date 
    temp = until
    until = until.strftime('%Y-%m-%dT%H:%M:%SZ')  # format string 
    since = temp.replace(day=1, hour=0, minute=0, second=0, microsecond=0)  #define the start of current month
    since = since.strftime('%Y-%m-%dT%H:%M:%SZ') #format string 
    commits = await fetchRepoCommitSinceUntil(username, reponame, since, until)
    month_name = temp.strftime('%B')   # name of current month
    commitLine.update({month_name : commits}) # update list 

    # fetch commits for remaining 5 months 
    for i in range(5): 
        until = datetime.now(pytz.UTC)
        since = until - relativedelta(months=(i+1))  
        until = until - relativedelta(months=i)  #calculate time 
        month_name = since.strftime('%B')   #get name of months
        until = until.strftime('%Y-%m-%dT%H:%M:%SZ') #string format 
        since = since.strftime('%Y-%m-%dT%H:%M:%SZ') #string format 
        commits = await fetchRepoCommitSinceUntil(username, reponame, since, until)
        commitLine.update({month_name : commits})

    return commitLine





