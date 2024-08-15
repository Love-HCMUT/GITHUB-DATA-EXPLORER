from ..fetch import user_fetch as fetch
import asyncio

async def get_languages(username, TOKEN):
    """
    Get information about the user's languages.
    :param username: The handle for the GitHub user account.
    :return: a dictionary contains languages and corresponding count.
    """
    DEMAND = 10
    repos = await fetch.fetch_repos_name(username, TOKEN)
    languages = {}
    # for repo in repos:
    #     data = await fetch.fetch_repo_languages(username, repo, TOKEN)
    #     for key in data:
    #         languages[key] = languages.get(key, 0) + 1
    coroutines = [fetch.fetch_repo_languages(username, repo, TOKEN) for repo in repos]
    list_data = await asyncio.gather(*coroutines)
    for data in list_data:
        for key in data:
            languages[key] = languages.get(key, 0) + 1
    if (len(languages) < DEMAND): DEMAND = len(languages)
    languages = dict(sorted(languages.items(), key = lambda item: item[1], reverse = True)[:DEMAND])
    return languages