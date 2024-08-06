import requests
import aiohttp
from datetime import datetime, timedelta

TOKEN = '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'

HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization" : f"Bearer {TOKEN}"
}

async def fetch_json(urls):
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



# Get list of repo
async def get_org_repos(org):
    url = f"https://api.github.com/orgs/{org}/repos"
    data = await fetch_json(url)
    return data

# Function to get commits from a repository since a specific date
async def get_repo_commits(org, repo, since):
    url = f"https://api.github.com/repos/{org}/{repo}/commits?since={since}"
    return await fetch_json(url)

# Function to get contributors from a repository in the last six months
async def get_repo_contributors(org, repo):
    # Calculate the date six months ago
    six_months_ago = datetime.now() - timedelta(days=6*30)
    since = six_months_ago.isoformat()

    # Fetch commits since the calculated date
    commits = await get_repo_commits(org, repo, since)
    if not commits:
        return []

    # Dictionary to hold contributors and their contribution count
    contributors = {}
    for commit in commits:
        author = commit.get('author')
        if author:
            login = author.get('login')
            if login:
                if login in contributors:
                    contributors[login] += 1
                else:
                    contributors[login] = 1

    # Convert the contributors dictionary to a list of dictionaries
    return [{"login": login, "contributions": count} for login, count in contributors.items()]

# Get org's member
async def get_org_members(orgname):
    url = f"https://api.github.com/orgs/{orgname}/members"
    return await fetch_json(url)




