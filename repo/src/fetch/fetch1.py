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
        except aiohttp.ClientResponseError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error has occurred: {err}")



#GET 10 GREATEST CONTRIBUTORS 
async def fetchRepoContributors(username, reponame, TOKEN): 
    perpage = 100
    contributors = {}
    page = 1
    count = 0
    while (count < 10): 
        data = await fetchAPI(f'https://api.github.com/repos/{username}/{reponame}/contributors?per_page={perpage}&page={page}', TOKEN)
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
async def fetchRepoCommitSinceUntil(username, reponame, since, until, TOKEN):
    page = 1
    perpage = 100 
    count = 0
    while (True): 
        data = await fetchAPI(f'https://api.github.com/repos/{username}/{reponame}/commits?since={since}&until={until}&per_page={perpage}&page={page}', TOKEN)
        list = np.array(data)
        if (list.size == 0): break
        count += list.size
        page += 1
    return count 


# FETCH COMMITS WITHIN 6 RECENT MONTHS 
async def fetchRepoCommits(username, reponame, TOKEN): 
    commitLine = {}
    # fetch commits in the current months, since the first until current date 
    until = datetime.now(pytz.UTC) # get current date 
    temp = until
    until = until.strftime('%Y-%m-%dT%H:%M:%SZ')  # format string 
    since = temp.replace(day=1, hour=0, minute=0, second=0, microsecond=0)  #define the start of current month
    since = since.strftime('%Y-%m-%dT%H:%M:%SZ') #format string 
    commits = await fetchRepoCommitSinceUntil(username, reponame, since, until, TOKEN)
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
        commits = await fetchRepoCommitSinceUntil(username, reponame, since, until, TOKEN)
        commitLine.update({month_name : commits})

    return commitLine


#FETCH ISSUES SINCE 
async def fetchRepoIssuesSince(username, reponame, since, TOKEN):
    page = 1
    perpage = 100 
    count = 0
    while (True): 
        data = await fetchAPI(f'https://api.github.com/repos/{username}/{reponame}/issues?since={since}&per_page={perpage}&page={page}', TOKEN)
        list = np.array(data)
        if (list.size == 0): break
        count += list.size
        page += 1
    return count 


# FETCH ISSUES WITHIN RECENT 6 MONTHS 
async def fetchRepoIssues(username, reponame, TOKEN): 
    issuesLine = {} 
    since = datetime.now(pytz.UTC) # get current date 
    temp = since # mark current date
    since = since.replace(day=1, hour=0, minute=0, second=0, microsecond=0) #get beginning of current months 
    month_name = since.strftime('%B')  #get name of months
    since = since.strftime('%Y-%m-%dT%H:%M:%SZ')  #format string 
    issues = await fetchRepoIssuesSince(username, reponame, since, TOKEN)
    issuesLine.update({month_name : issues})
    
    previous_count = issues #previous months 

    for i in range(5):
        since = temp # get the beginning of current month
        since = since - relativedelta(months=(i+1))  # i months ago 
        month_name = since.strftime('%B')  #get name of months
        since = since.strftime('%Y-%m-%dT%H:%M:%SZ')  #format string 
        issues = await fetchRepoIssuesSince(username, reponame, since, TOKEN)  #calculate i months ago
        issues -= previous_count     
        previous_count += issues
        issuesLine.update({month_name : issues})

    return issuesLine


# input: a dict contain data for each month, number of months need to analysis
# output: a dict contain data for each month 
def CreateListOfMonth(data, numberOfMonths): 
    current_date = datetime.now()
    months = [(current_date - relativedelta(months=(numberOfMonths-i-1))).strftime("%B") for i in range(numberOfMonths)]
    ReponseData = { e : 0 for e in months }
    for key, value in data.items():
        if key in ReponseData:
            ReponseData[key] = value
    return ReponseData


# FETCH PULL REQUEST WITHIN RECENT 6 MONTHS 
async def fetchRepoPulls(username, reponame, TOKEN): 
    RequestLine = {}
    page = 1
    perpage = 100
    count = 0
    previous_months = datetime.now(pytz.UTC).strftime('%B') #curent month 
    while (True): 
        data = await fetchAPI(f'https://api.github.com/repos/{username}/{reponame}/pulls?per_page={perpage}&page={page}', TOKEN)
        list = np.array(data)
        if (list.size == 0): 
            RequestLine.update({previous_months : count})
            break
        page += 1
       
        for e in list: 
            createAt = e['created_at']
            date = datetime.strptime(createAt, "%Y-%m-%dT%H:%M:%SZ")
            month_name = date.strftime("%B")
            if (month_name != previous_months): 
                RequestLine.update({previous_months : count})
                previous_months = month_name
                count = 0
            count += 1

    ReponseData = CreateListOfMonth(RequestLine, 6)
    return ReponseData