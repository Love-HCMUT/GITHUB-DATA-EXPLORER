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

async def fetch_repos_name(username, TOKEN):
    """
    Get list public repositories for the specified user.
    :param username: The handle for the GitHub user account.
    :return: a list contains name of all repos
    """
    data = []
    page = 1
    perpage = 30
    while (True):
        repos = await fetchAPI(f'https://api.github.com/users/{username}/repos?page={page}&per_page={perpage}', TOKEN)
        if (len(repos) == 0): break
        for repo in repos:
            if not repo['fork'] and repo['size']:
                data.append(repo['name'])
        page += 1
    return data

async def fetch_repo_commit_since_until(owner, repo, TOKEN, since, until):
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
    commits = await fetch_repo_commit_since_until(owner, repo, TOKEN, since, until)
    month_name = temp.strftime('%B')
    result.update({month_name : commits})

    for i in range(5): 
        until = datetime.now(pytz.UTC)
        since = until - relativedelta(months=(i+1))  
        until = until - relativedelta(months=i)
        month_name = since.strftime('%B')
        until = until.strftime(FORMAT_STRING)
        since = since.strftime(FORMAT_STRING)
        commits = await fetch_repo_commit_since_until(owner, repo, TOKEN, since, until)
        result.update({month_name : commits})
    return result