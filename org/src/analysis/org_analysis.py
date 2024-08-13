from ..fetch import org_fetch as fetch
import asyncio

# async def get_languages(orgname, TOKEN):
#     """
#     Get information about the user's languages.
#     :param orgname: Name of the organization.
#     :return: a dictionary contains languages and corresponding percentages
#     """
#     repos = await fetch.fetch_repos_name(orgname, TOKEN)
#     languages = {}
#     for repo in repos:
#         data = await fetch.fetch_repo_languages(orgname, repo, TOKEN)
#         for key, value in data.items():
#             languages[key] = languages.get(key, 0) + value
#     total = sum(languages.values())
#     for language, byte in languages.items():
#         percent = round((byte / total) * 100, 2)
#         languages.update({language: percent})
#     return languages

async def get_languages(orgname, TOKEN):
    """
    Get information about the user's languages.
    :param orgname: Name of the organization.
    :return: a dictionary contains languages and corresponding percentages
    """
    repos = await fetch.fetch_repos_name(orgname, TOKEN)
    languages = {}
    # for repo in repos:
    #     data = await fetch_repo_languages(orgname, repo, TOKEN)
    #     for key, value in data.items():
    #         languages[key] = languages.get(key, 0) + value
    coroutines = [fetch.fetch_repo_languages(orgname, repo, TOKEN) for repo in repos]
    list_data = await asyncio.gather(*coroutines)
    for data in list_data:
        for key, value in data.items():
            languages[key] = languages.get(key, 0) + value
    total = sum(languages.values())
    for language, byte in languages.items():
        percent = round((byte / total) * 100, 2)
        languages.update({language: percent})
    return languages

# async def get_org_contributions_last_6_months(orgname, TOKEN):
#     """
#     Get the total contributions of the specified org in the last 6 months.
#     :param orgname: the name of the specified organization.
#     :return: a dictionary contains information about the number of commits in the last 6 months.
#     """

#     repos = await fetch.fetch_repos_name(orgname, TOKEN)
#     data = {}
#     for repo in repos:
#         commits = await fetch.fetch_repo_commits(orgname, repo, TOKEN)
#         data.update({repo: commits})
#     result = {}
#     for repo in repos:
#         for month in data[repo].keys():
#             result[month] = result.get(month, 0) + data[repo][month]
#     return result
async def get_org_contributions_last_6_months(orgname, TOKEN):
    """
    Get the total contributions of the specified org in the last 6 months.
    :param orgname: the name of the specified organization.
    :return: a dictionary contains information about the number of commits in the last 6 months.
    """

    repos = await fetch.fetch_repos_name(orgname, TOKEN)
    data = {}
    # for repo in repos:
    #     commits = await fetch_repo_commits(orgname, repo, TOKEN)
    #     data.update({repo: commits})
    coroutines = [fetch.fetch_repo_commits(orgname, repo, TOKEN) for repo in repos]
    list_commits = await asyncio.gather(*coroutines)
    for i in range(len(repos)):
        data.update({repos[i]: list_commits[i]})
    result = {}
    for repo in repos:
        for month in data[repo].keys():
            result[month] = result.get(month, 0) + data[repo][month]
    return result
