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
    DEMAND = 5
    page = 1
    perpage = 100 
    result = 0
    while (True): 
        coroutines = [fetchAPI(f'https://api.github.com/repos/{owner}/{repo}/commits?since={since}&until={until}&per_page={perpage}&page={page + x}', TOKEN) for x in range(DEMAND)]
        list_data = await asyncio.gather(*coroutines)
        # if (len(data) == 0): break
        for data in list_data:
            result += len(data)
        if (not all(list_data)): break
        page += DEMAND
    return result 

async def fetch_repo_commits(owner, repo, TOKEN):
    """
    Get the number of commits for the specified repo in the last 6 months.
    :param owner: The account owner of the repository. The name is not case sensitive.
    :param repo: The name of the repository without the .git extension. The name is not case sensitive.
    :return: a dictionary contains information about the number of commits in the last 6 months.
    """
    FORMAT_STRING = '%Y-%m-%dT%H:%M:%SZ'
    result = {}
    
    until = datetime.now(pytz.UTC)
    temp = until
    until = until.strftime(FORMAT_STRING)
    since = temp.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    since = since.strftime(FORMAT_STRING)
    commits = await fetch_repo_commit_since_until(owner, repo, since, until, TOKEN)
    month_name = temp.strftime('%B')
    result.update({month_name : commits})

    for i in range(5): 
        until = datetime.now(pytz.UTC)
        since = until - relativedelta(months=(i+1))  
        until = until - relativedelta(months=i)
        month_name = since.strftime('%B')
        until = until.strftime(FORMAT_STRING)
        since = since.strftime(FORMAT_STRING)
        commits = await fetch_repo_commit_since_until(owner, repo, since, until, TOKEN)
        result.update({month_name : commits})

    return result