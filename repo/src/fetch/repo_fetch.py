import aiohttp
import asyncio
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
            
async def fetch_repo_languages(owner, repo):
    """
    Get list languages for the specified repository.
    The value shown for each language is the number of bytes of code written in that language.
    :param owner: The account owner of the repository. The name is not case sensitive.
    :param repo: The name of the repository without the .git extension. The name is not case sensitive.
    :return: a dictionary contains infomation about languages of the repo.
    """
    url = f'http://api.github.com/repos/{owner}/{repo}/languages'
    data = await fetchAPI(url)
    return data
    
async def fetch_repo_info(owner, repo):
    """
    Get some general infomation for the specified repository.
    :param owner: The account owner of the repository. The name is not case sensitive.
    :param repo: The name of the repository without the .git extension. The name is not case sensitive.
    :return: a dictionary contains infomation about stargazers_count, forks_count, watchers_count, open_issues_count, subscribers_count, description, default_branch
    """
    url = f'http://api.github.com/repos/{owner}/{repo}'
    repo_info = await fetchAPI(url)
    keys = ('stargazers_count', 'forks_count', 'watchers_count', 'open_issues_count', 'subscribers_count', 'description', 'default_branch')
    data = {}
    for key in keys:
        data.update({key: repo_info.get(key, 0)})
    return data

async def fetch_repo_branches_name(owner, repo):
    """
    Get name of all branch in the specified repository.
    :param owner: The account owner of the repository. The name is not case sensitive.
    :param repo: The name of the repository without the .git extension. The name is not case sensitive.
    :return: a list contains name of all branch.
    """
    url = f'http://api.github.com/repos/{owner}/{repo}/branches'
    branches = await fetchAPI(url)
    data = []
    for branch in branches:
        data.append(branch['name'])
    return data
        
async def fetch_repo_contributors(owner, repo):
    """
    Get some infomation about contributors in the specified repository.
    :param owner: The account owner of the repository. The name is not case sensitive.
    :param repo: The name of the repository without the .git extension. The name is not case sensitive.
    :return: a dictionary contains infomation about contributors and their contributions
    """
    url = f'http://api.github.com/repos/{owner}/{repo}/contributors'
    contributors = await fetchAPI(url)
    data = {}
    for contributor in contributors:
        data.update({contributor['login']: contributor['contributions']})
    return data

async def fetch_user_repos_name(username):
    """
    Get list public repositories for the specified user.
    :param username: The handle for the GitHub user account.
    :return: a list contains name of all repos
    """
    url = f'http://api.github.com/users/{username}/repos'
    repos = await fetchAPI(url)
    data = []
    for repo in repos:
        if not repo['fork']:
            data.append(repo['name'])
    return 

async def get_user_languages(username):
    """
    Get information about the user's languages.
    :param username: The handle for the GitHub user account.
    :return: a dictionary contains languages and corresponding percentages
    """
    repos = await fetch_user_repos_name(username)
    languages = {}
    for repo in repos:
        data = await fetch_repo_languages(username, repo)
        for key, value in data.items():
            languages[key] = languages.get(key, 0) + value
    total = sum(languages.values())
    for language, byte in languages.items():
        percent = round((byte / total) * 100, 1)
        languages.update({language: percent})
    return languages

async def get_top_contributors_languages(owner, repo, DEMAND = 3):
    """
    Get information about languages of some top contributors.
    :param owner: The account owner of the repository. The name is not case sensitive.
    :param repo: The name of the repository without the .git extension. The name is not case sensitive.
    :param DEMAND: The number of contributors
    :return: a dictionary contains user and user's languages.
    """
    contributors = await fetch_repo_contributors(owner, repo)
    number = len(contributors) if len(contributors) < DEMAND else DEMAND
    contributors = dict(sorted(contributors.items(), key = lambda item: item[1], reverse = True)[:number])
    result = {}
    for contributor in contributors:
        languages = await get_user_languages(contributor)
        result.update({contributor: languages})
    
    return result

# print(asyncio.run(get_top_contributors_languages('krahets', 'hello-algo')))
for _ in range(60):
    print(asyncio.run(fetch_repo_languages('krahets', 'hello-algo')))