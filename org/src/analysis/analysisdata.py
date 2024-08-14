from ..fetch import getdata
import asyncio

def is_member_org(repos, members):
    # Iterate through all repos
    for repo_key, repo_value in repos.items():
        # Get the memberCommits list of the current repo
        member_commits = repo_value.get('memberCommits', {})

        # Check if at least one member in the members list appears in memberCommits
        for member in members:
            if member in member_commits:
                return True  # Return True if at least one member appears

    return False  # Return False if no member appears

def update_data(data, org):
    updated_repos = {}
    total_contributions = 0
    total_member_commits = {}

    for repo, repo_data in data['repos'].items():
        # Check if any member of the organization is part of the repo
        is_member = is_member_org({repo: repo_data}, data['members'])
        
        if is_member:
            filtered_member_commits = {member: repo_data['memberCommits'][member] for member in data['members'] if member in repo_data['memberCommits']}

            for member in filtered_member_commits:
                if member in total_member_commits:
                    total_member_commits[member] += filtered_member_commits[member]
                else:
                    total_member_commits[member] = filtered_member_commits[member]

            repo_contributions = sum(filtered_member_commits.values())

            updated_repos[repo] = {
                'contributions': repo_contributions,
                'memberCommits': filtered_member_commits,
            }

            total_contributions += repo_contributions

    # Sort the total_member_commits by commit count and select the top 10
    sorted_member_commits = dict(sorted(total_member_commits.items(), key=lambda item: item[1], reverse=True))
    top10 = dict(list(sorted_member_commits.items())[:10])

    data['repos'] = updated_repos
    data['totalContributions6Month'] = total_contributions
    data['totalMemberCommits6Month'] = total_member_commits
    data['top10'] = top10  # Add the top 10 contributors to the data

    return data



async def one_repo(repo, data, org, TOKEN):
    repo_name = repo['name']
    repo_contributions = 0
    member_commits = {}
            
    # Get contributors info
    contributors = await getdata.get_repo_contributors(org, repo_name, TOKEN)
    if isinstance(contributors, list):
        for contributor in contributors:
            repo_contributions += contributor.get('contributions', 0)
            login = contributor.get('login')
            if login:
                member_commits[login] = member_commits.get(login, 0) + contributor.get('contributions', 0)
    else:
        print(f"Unexpected contributors format for repo {repo_name}:", contributors)

    # Save info into data
    data["repos"][repo_name] = {
        "contributions": repo_contributions,
        "memberCommits": member_commits
    }
    return data


async def gather_repo_data(org, TOKEN):
    data = {"repos": {}}
    
    repos = await getdata.get_org_repos(org, TOKEN)
    # if repos:
    #     for repo in repos:
    #         repo_name = repo['name']
    #         repo_contributions = 0
    #         member_commits = {}
            
    #         # Get contributors info
    #         contributors = await getdata.get_repo_contributors(org, repo_name, TOKEN)
    #         if isinstance(contributors, list):
    #             for contributor in contributors:
    #                 repo_contributions += contributor.get('contributions', 0)
    #                 login = contributor.get('login')
    #                 if login:
    #                     member_commits[login] = member_commits.get(login, 0) + contributor.get('contributions', 0)
    #         else:
    #             print(f"Unexpected contributors format for repo {repo_name}:", contributors)

    #         # Save info into data
    #         data["repos"][repo_name] = {
    #             "contributions": repo_contributions,
    #             "memberCommits": member_commits
    #         }
    coroutines = [one_repo(repo, data, org, TOKEN) for repo in repos]
    await asyncio.gather(*coroutines)

    # Get organization members
    members = await getdata.get_org_members(org, TOKEN)
    if members:
        data['members'] = [member['login'] for member in members]

    data = update_data(data, org)
    return data
