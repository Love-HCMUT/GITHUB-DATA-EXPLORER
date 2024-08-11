from ..fetch import user_fetch as fetch

async def get_languages(username, TOKEN):
    """
    Get information about the user's languages.
    :param username: The handle for the GitHub user account.
    :return: a dictionary contains languages and corresponding count.
    """
    repos = await fetch.fetch_repos_name(username, TOKEN)
    languages = {}
    for repo in repos:
        data = await fetch.fetch_repo_languages(username, repo, TOKEN)
        for key in data:
            languages[key] = languages.get(key, 0) + 1
    return languages