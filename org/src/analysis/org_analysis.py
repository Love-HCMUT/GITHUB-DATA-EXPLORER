from ..fetch import org_fetch as fetch

async def get_languages(orgname):
    """
    Get information about the user's languages.
    :param orgname: Name of the organization.
    :return: a dictionary contains languages and corresponding percentages
    """
    repos = await fetch.fetch_repos_name(orgname)
    languages = {}
    for repo in repos:
        data = await fetch.fetch_repo_languages(orgname, repo)
        for key, value in data.items():
            languages[key] = languages.get(key, 0) + value
    total = sum(languages.values())
    for language, byte in languages.items():
        percent = round((byte / total) * 100, 1)
        languages.update({language: percent})
    return languages

async def get_org_contributions_last_6_months(orgname):
    """
    Get the total contributions of the specified org in the last 6 months.
    :param orgname: the name of the specified organization.
    :return: a dictionary contains information about the number of commits in the last 6 months.
    """

    repos = await fetch.fetch_repos_name(orgname)
    data = {}
    for repo in repos:
        commits = await fetch.fetch_repo_commits(orgname, repo)
        data.update({repo: commits})
    result = {}
    for repo in repos:
        for month in data[repo].keys():
            result[month] = result.get(month, 0) + data[repo][month]
    return result