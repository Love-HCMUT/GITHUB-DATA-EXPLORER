from ..fetch import repo_fetch as fetch

async def get_percent_languages(owner, repo, TOKEN):
    """
    Get the percentage of languages in the specified repository.
    :param owner: The account owner of the repository. The name is not case sensitive.
    :param repo: The name of the repository without the .git extension. The name is not case sensitive.
    :return: a dictionary contains languages and corresponding percentages
    """
    data = await fetch.fetch_repo_languages(owner, repo, TOKEN)
    total = sum(data.values())
    result = {}
    for language, byte in data.items():
        percent = round((byte / total) * 100, 2)
        result.update({language: percent})
    return result

async def get_repo_info(owner, repo, TOKEN):
    """
    Get some general infomation for the specified repository.
    :param owner: The account owner of the repository. The name is not case sensitive.
    :param repo: The name of the repository without the .git extension. The name is not case sensitive.
    :return: a dictionary contains some general information.
    """
    data = await fetch.fetch_repo_info(owner, repo, TOKEN)
    data.update({'branches': await fetch.fetch_repo_branches_name(owner, repo, TOKEN)})
    return data

async def get_languages(username, TOKEN):
    """
    Get information about the user's languages.
    :param username: The handle for the GitHub user account.
    :return: a dictionary contains languages and corresponding percentages
    """
    repos = await fetch.fetch_repos_name(username, TOKEN)
    languages = {}
    for repo in repos:
        data = await fetch.fetch_repo_languages(username, repo, TOKEN)
        for key, value in data.items():
            languages[key] = languages.get(key, 0) + value
    total = sum(languages.values())
    for language, byte in languages.items():
        percent = round((byte / total) * 100, 1)
        languages.update({language: percent})
    return languages

async def get_top_contributors_languages(owner, repo, TOKEN, DEMAND = 3):
    """
    Get information about languages of some top contributors.
    :param owner: The account owner of the repository. The name is not case sensitive.
    :param repo: The name of the repository without the .git extension. The name is not case sensitive.
    :param DEMAND: The number of contributors
    :return: a dictionary contains user and user's languages.
    """
    contributors = await fetch.fetch_repo_contributors(owner, repo, TOKEN)
    number = len(contributors) if len(contributors) < DEMAND else DEMAND
    # contributors = dict(sorted(contributors.items(), key = lambda item: item[1], reverse = True)[:number])
    contributors = list(contributors.keys())[:number]
    result = {}
    for contributor in contributors:
        languages = await get_languages(contributor, TOKEN)
        result.update({contributor: languages})
    
    return result
