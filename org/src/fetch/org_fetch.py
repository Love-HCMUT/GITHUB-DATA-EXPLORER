import aiohttp
import asyncio
import requests
from datetime import datetime, timezone
import pytz
from dateutil.relativedelta import relativedelta

DEFAULT_TOKEN = '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'

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
            
async def fetch_repo_languages(owner, repo, TOKEN):
    """
    Get list languages for the specified repository.
    The value shown for each language is the number of bytes of code written in that language.
    :param owner: The account owner of the repository. The name is not case sensitive.
    :param repo: The name of the repository without the .git extension. The name is not case sensitive.
    :return: a dictionary contains infomation about languages of the repo.
    """
    url = f'https://api.github.com/repos/{owner}/{repo}/languages'
    data = await fetchAPI(url, TOKEN)
    return data
    
async def fetch_repo_info(owner, repo, TOKEN):
    """
    Get some general infomation for the specified repository.
    :param owner: The account owner of the repository. The name is not case sensitive.
    :param repo: The name of the repository without the .git extension. The name is not case sensitive.
    :return: a dictionary contains infomation about stargazers_count, forks_count, watchers_count, open_issues_count, subscribers_count, description, default_branch
    """
    url = f'https://api.github.com/repos/{owner}/{repo}'
    repo_info = await fetchAPI(url, TOKEN)
    keys = ('stargazers_count', 'forks_count', 'watchers_count', 'open_issues_count', 'subscribers_count', 'description', 'default_branch')
    data = {}
    for key in keys:
        data.update({key: repo_info.get(key, 0)})
    return data

async def fetch_repo_branches_name(owner, repo, TOKEN):
    """
    Get name of all branch in the specified repository.
    :param owner: The account owner of the repository. The name is not case sensitive.
    :param repo: The name of the repository without the .git extension. The name is not case sensitive.
    :return: a list contains name of all branch.
    """
    url = f'https://api.github.com/repos/{owner}/{repo}/branches'
    branches = await fetchAPI(url, TOKEN)
    data = []
    for branch in branches:
        data.append(branch['name'])
    return data
        
async def fetch_repo_contributors(owner, repo, TOKEN):
    """
    Get some infomation about contributors in the specified repository.
    :param owner: The account owner of the repository. The name is not case sensitive.
    :param repo: The name of the repository without the .git extension. The name is not case sensitive.
    :return: a dictionary contains infomation about contributors and their contributions
    """
    url = f'https://api.github.com/repos/{owner}/{repo}/contributors'
    contributors = await fetchAPI(url, TOKEN)
    data = {}
    for contributor in contributors:
        data.update({contributor['login']: contributor['contributions']})
    return data

async def fetch_repos_name(orgname, TOKEN):
    """
    Get list public repositories for the specified user.
    :param orgname: Name of the organization.
    :return: a list contains name of all repos
    """
    DEMAND = 5
    result = []
    page = 1
    perpage = 100
    while (True):
        coroutines = [fetchAPI(f'https://api.github.com/orgs/{orgname}/repos?page={page + x}&per_page={perpage}', TOKEN) for x in range(DEMAND)]
        data = await asyncio.gather(*coroutines)
        for repos in data:
            if not repos: continue
            for repo in repos:
                if not repo['fork'] and repo['size']:
                    result.append(repo['name'])
        if (not all(data)): break
        page += DEMAND
    return result

async def fetch_repo_commit_since_until(owner, repo, since, until, TOKEN):
    """
    Get the number of commits for the specifed repo since ... until ...
    :param owner: The account owner of the repository. The name is not case sensitive.
    :param repo: The name of the repository without the .git extension. The name is not case sensitive.
    :param since: Start time.
    :param until: End time.
    :return: The number of commits.
    """
    page = 1
    perpage = 100 
    result = 0
    while (True): 
        data = await fetchAPI(f'https://api.github.com/repos/{owner}/{repo}/commits?since={since}&until={until}&per_page={perpage}&page={page}', TOKEN)
        if (len(data) == 0): break
        result += len(data)
        page += 1
    return result

async def fetch_repo_commits_since(owner, repo, since, TOKEN):
    page = 1
    perpage = 100
    result = []
    while True:
        data = await fetchAPI(f'https://api.github.com/repos/{owner}/{repo}/commits?since={since}&per_page={perpage}&page={page}', TOKEN)
        if len(data) == 0: break
        for commit in data:
            result.append(commit['commit']['committer']['date'])
        page += 1
    return result     
        

# async def fetch_repo_commits(owner, repo, TOKEN):
#     """
#     Get the number of commits for the specified repo in the last 6 months.
#     :param owner: The account owner of the repository. The name is not case sensitive.
#     :param repo: The name of the repository without the .git extension. The name is not case sensitive.
#     :return: a dictionary contains information about the number of commits in the last 6 months.
#     """
#     FORMAT_STRING = '%Y-%m-%dT%H:%M:%SZ'
#     FORMAT_LABEL = '%d-%B'
#     result = {}
    
#     until = datetime.now(pytz.UTC)
#     temp = until
#     until = until.strftime(FORMAT_STRING)
#     since = temp.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
#     since = since.strftime(FORMAT_STRING)
#     month_name = temp.strftime(FORMAT_LABEL)
#     commits = await fetch_repo_commit_since_until(owner, repo, since, until, TOKEN)
#     result.update({month_name : commits})

#     for i in range(5): 
#         until = datetime.now(pytz.UTC)
#         since = until - relativedelta(months=(i+1))
#         until = until - relativedelta(months=i)
#         month_name = since.strftime(FORMAT_LABEL)
#         until = until.strftime(FORMAT_STRING)
#         since = since.strftime(FORMAT_STRING)
#         commits = await fetch_repo_commit_since_until(owner, repo, since, until, TOKEN)
#         print(since)
#         result.update({month_name : commits})

#     return result

async def fetch_repo_commits(owner, repo, TOKEN):
    FORMAT_STRING = '%Y-%m-%dT%H:%M:%SZ'
    FORMAT_LABEL = '%d-%B'
    result = {}
    DEMAND = 6
    # Declare time
    today = datetime.now(pytz.UTC)
    list_time = [today - relativedelta(months=x) for x in range(DEMAND, 0, -1)]
    list_time.append(today)
    
    commits = await fetch_repo_commits_since(owner, repo, list_time[0], TOKEN)
    
    # Format time
    list_time_formatted = [time.strftime(FORMAT_STRING) for time in list_time]
    
    # Labels
    list_time_labels = [time.strftime(FORMAT_LABEL) for time in list_time]
    
    # Prepare
    for label in list_time_labels:
        result[label] = 0
        
    for date_commit in commits:
        for i in range(len(list_time_formatted) - 1):
            if list_time_formatted[i] <= date_commit < list_time_formatted[i + 1]:
                result[list_time_labels[i + 1]] = result.get(list_time_labels[i + 1], 0) + 1
        
    return result
    
##########################################################################################
async def get_org_contributions_last_6_months(orgname, TOKEN):
    """
    Get the total contributions of the specified org in the last 6 months.
    :param orgname: the name of the specified organization.
    :return: a dictionary contains information about the number of commits in the last 6 months.
    """
    repos = await fetch_repos_name(orgname, TOKEN)
    data = {}
    # for repo in repos:
    #     commits = await fetch_repo_commits(orgname, repo, TOKEN)
    #     data.update({repo: commits})
    coroutines = [fetch_repo_commits(orgname, repo, TOKEN) for repo in repos]
    list_commits = await asyncio.gather(*coroutines)
    for i in range(len(repos)):
        data.update({repos[i]: list_commits[i]})
    result = {}
    for repo in repos:
        for month in data[repo].keys():
            result[month] = result.get(month, 0) + data[repo][month]
    return result

async def get_languages(orgname, TOKEN):
    """
    Get information about the user's languages.
    :param orgname: Name of the organization.
    :return: a dictionary contains languages and corresponding percentages
    """
    repos = await fetch_repos_name(orgname, TOKEN)
    languages = {}
    # for repo in repos:
    #     data = await fetch_repo_languages(orgname, repo, TOKEN)
    #     for key, value in data.items():
    #         languages[key] = languages.get(key, 0) + value
    coroutines = [fetch_repo_languages(orgname, repo, TOKEN) for repo in repos]
    list_data = await asyncio.gather(*coroutines)
    for data in list_data:
        for key, value in data.items():
            languages[key] = languages.get(key, 0) + value
    total = sum(languages.values())
    for language, byte in languages.items():
        percent = round((byte / total) * 100, 2)
        languages.update({language: percent})
    return languages

# import time
# start = time.time()
# data = asyncio.run(get_org_contributions_last_6_months('TickLabVN', DEFAULT_TOKEN))
# print(data)
# end = time.time()
# print('TIME:', end - start)