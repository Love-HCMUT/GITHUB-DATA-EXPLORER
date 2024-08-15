import requests
import aiohttp
import asyncio

from datetime import datetime, timedelta
TOKEN = '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'

async def fetch_json(urls, TOKEN):
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

# Get info
async def get_info(user, TOKEN):
    url = f"https://api.github.com/users/{user}"
    data = await fetch_json(url, TOKEN)
    return data

# Get list of repo
async def get_user_repos(user, TOKEN):
    url = f"https://api.github.com/users/{user}/repos"
    data = await fetch_json(url, TOKEN)
    return data

# Get repo's contributors 
async def get_repo_contributors(user,repo, TOKEN):
    url = f"https://api.github.com/repos/{user}/{repo}/contributors"
    return await fetch_json(url, TOKEN)

# Get repo's stars
async def get_repo_stars(user, repo, TOKEN):
    url = f"https://api.github.com/repos/{user}/{repo}"
    repo_data = await fetch_json(url, TOKEN)
    if repo_data:
        return repo_data.get('stargazers_count', 0)
    return 0

# Get repo's pull requests
async def get_repo_pull_requests(user, repo, TOKEN):
    total_prs = 0
    page = 1
    per_page = 100
    url = f"https://api.github.com/repos/{user}/{repo}/pulls?state=all&per_page={per_page}&page={page}"

    while True:
        pulls = await fetch_json(url, TOKEN)
        if not pulls:
            break
        total_prs += len(pulls)
        page += 1
        url = f"https://api.github.com/repos/{user}/{repo}/pulls?state=all&per_page={per_page}&page={page}"

    return total_prs

# Get repo's merge pull requests
async def get_repo_merged_pull_requests(user, repo, TOKEN):
    merged_prs = 0
    page = 1
    per_page = 100
    url = f"https://api.github.com/repos/{user}/{repo}/pulls?state=all&per_page={per_page}&page={page}"

    while True:
        pulls = await fetch_json(url, TOKEN)
        if not pulls:
            break
        for pr in pulls:
            if pr.get('merged_at'):
                merged_prs += 1
        page += 1
        url = f"https://api.github.com/repos/{user}/{repo}/pulls?state=all&per_page={per_page}&page={page}"

    return merged_prs



async def get_repo_commits_by_month(user, repo, since, until, TOKEN):
    url = f"https://api.github.com/repos/{user}/{repo}/commits?since={since}&until={until}"
    return await fetch_json(url, TOKEN)

# async def get_contributions_by_member(user, since, until, TOKEN):
#     repos = await get_user_repos(user, TOKEN)

#     contributions_by_member = {}

#     for repo in repos:
#         try:
#             commits = await get_repo_commits_by_month(
#                 user,
#                 repo['name'],
#                 since,
#                 until,
#                 TOKEN
#             )
#             if commits:
#                 for commit in commits:
#                     login = commit.get('author', {}).get('login', 'unknown')
#                     if login not in contributions_by_member:
#                         contributions_by_member[login] = 0
#                     contributions_by_member[login] += 1
#             else:
#                 print(f"There are no commits in the repository {repo['name']}")
#         except Exception as error:
#             if '409' in str(error):
#                 print(f"Conflict error for repository {repo['name']}: {error}")
#             else:
#                 print(f"An error occurred when retrieving commits from the repository {repo['name']}: {error}")

#     return contributions_by_member


async def get_contributions_by_member(user, since, until, TOKEN):
    repos = await get_user_repos(user, TOKEN)

    contributions_by_member = {}

    async def process_repo(repo):
        try:
            commits = await get_repo_commits_by_month(
                user,
                repo['name'],
                since,
                until,
                TOKEN
            )
            if commits:
                for commit in commits:
                    login = commit.get('author', {}).get('login', 'unknown')
                    if login not in contributions_by_member:
                        contributions_by_member[login] = 0
                    contributions_by_member[login] += 1
            else:
                print(f"There are no commits in the repository {repo['name']}")
        except Exception as error:
            if '409' in str(error):
                print(f"Conflict error for repository {repo['name']}: {error}")
            else:
                print(f"An error occurred when retrieving commits from the repository {repo['name']}: {error}")

    # Tạo một danh sách các task để xử lý tất cả các repo đồng thời
    tasks = [process_repo(repo) for repo in repos]
    
    # Sử dụng asyncio.gather để thực hiện tất cả các task đồng thời
    await asyncio.gather(*tasks)

    return contributions_by_member




# async def get_contributions_last_6_months(user, TOKEN):
#     contributions_by_month = {}

#     for i in range(4):
#         end_date = datetime.now() - timedelta(days=i * 30)
#         start_date = end_date - timedelta(days=30)

#         since = start_date.isoformat()
#         until = end_date.isoformat()

#         month_name = end_date.strftime("%m/%Y")
#         contributions_by_month[month_name] = await get_contributions_by_member(user, since, until, TOKEN)

#     return contributions_by_month




async def get_contributions_last_6_months(user, TOKEN):
    contributions_by_month = {}

    tasks = []

    for i in range(4):
        end_date = datetime.now() - timedelta(days=i * 30)
        start_date = end_date - timedelta(days=30)

        since = start_date.isoformat()
        until = end_date.isoformat()

        month_name = end_date.strftime("%m/%Y")
        
        # Tạo task cho mỗi lời gọi API
        task = asyncio.create_task(get_contributions_by_member(user, since, until, TOKEN))
        tasks.append((month_name, task))

    # Chạy tất cả các task đồng thời
    results = await asyncio.gather(*[task for _, task in tasks])

    # Gán kết quả cho contributions_by_month theo thứ tự tương ứng
    for (month_name, _), result in zip(tasks, results):
        contributions_by_month[month_name] = result

    return contributions_by_month
