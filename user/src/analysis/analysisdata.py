from ..fetch import getdata

def is_member_org(repos, user):
    # Duyệt qua tất cả các repo
    for repo, repo_data in repos.items():
        # Lấy danh sách memberCommits của repo hiện tại
        member_commits = repo_data['memberCommits']

        # Kiểm tra xem user có xuất hiện trong memberCommits không
        if user in member_commits:
            return True  # Nếu user xuất hiện, trả về True

    return False  # Nếu user không xuất hiện, trả về False

def update_data(data, user):
    updated_repos = {}
    total_stars = 0
    total_prs = 0
    total_merged_prs = 0
    total_contributions = 0
    total_member_commits = {user: 0}
    total_languages = {}

    for repo, repo_data in data['repos'].items():
        is_member = is_member_org({repo: repo_data}, user)
        
        if is_member:
            filtered_member_commits = {user: repo_data['memberCommits'][user]} if user in repo_data['memberCommits'] else {}

            if user in repo_data['memberCommits']:
                total_member_commits[user] += repo_data['memberCommits'][user]

            repo_contributions = sum(filtered_member_commits.values())

            updated_repos[repo] = {
                'contributions': repo_contributions,
                'languages': repo_data['languages'],
                'memberCommits': filtered_member_commits,
                'stars': repo_data['stars'],
                'pullRequests': repo_data['pullRequests'],
                'mergedPullRequests': repo_data['mergedPullRequests']
            }

            total_stars += repo_data['stars']
            total_prs += repo_data['pullRequests']
            total_merged_prs += repo_data['mergedPullRequests']
            total_contributions += repo_contributions

            # Cộng dồn số dòng code cho từng ngôn ngữ
            for language, lines in repo_data['languages'].items():
                total_languages[language] = total_languages.get(language, 0) + lines

    # Lấy top 3 repos có nhiều sao nhất
    top3 = sorted(updated_repos.items(), key=lambda item: item[1]['stars'], reverse=True)[:3]
    top3_repos = [repo for repo, data in top3]

    data['top3Repos'] = top3_repos    
    data['repos'] = updated_repos
    data['totalStars'] = total_stars
    data['totalPRs'] = total_prs
    data['totalMergedPRs'] = total_merged_prs
    data['totalContributions'] = total_contributions
    data['totalMemberCommits'] = total_member_commits
    data['totalLanguages'] = total_languages
    
    return data
    

async def gather_repo_data(user):
    data = {"repos": {}}
    
    repos = await getdata.get_user_repos(user)
    if repos:
        for repo in repos:
            repo_name = repo['name']
            repo_contributions = 0
            repoLanguages = {}
            member_commits = {}
            repo_stars = 0
            repo_prs = 0
            repo_merged_prs = 0

            # Lấy thông tin contributors
            contributors = await getdata.get_repo_contributors(user, repo_name)
            if isinstance(contributors, list):
                for contributor in contributors:
                    repo_contributions += contributor.get('contributions', 0)
                    login = contributor.get('login')
                    if login:
                        member_commits[login] = member_commits.get(login, 0) + contributor.get('contributions', 0)
            else:
                print(f"Unexpected contributors format for repo {repo_name}:", contributors)

            # # Lấy thông tin languages
            languages = await getdata.fetch_json(f"https://api.github.com/repos/{user}/{repo_name}/languages")
            if languages:
                for language, lines in languages.items():
                    repoLanguages[language] = repoLanguages.get(language, 0) + lines

            # Lấy số sao của repo
            repo_stars = await getdata.get_repo_stars(user, repo_name)

            # Lấy số PR của repo
            repo_prs = await getdata.get_repo_pull_requests(user, repo_name)

            # Lấy số PR đã merge của repo
            repo_merged_prs = await getdata.get_repo_merged_pull_requests(user, repo_name)

            # Lưu thông tin vào data
            data["repos"][repo_name] = {
                "contributions": repo_contributions,
                "languages": repoLanguages,
                "memberCommits": member_commits,
                "stars": repo_stars,
                "pullRequests": repo_prs,
                "mergedPullRequests": repo_merged_prs,
            }
    
    data = update_data(data, user)
    info = await getdata.get_info(user)
    data['info'] = {
        "login": info.get("login"),
        "avatar_url": info.get("avatar_url"),
        "description": info.get("description"),
        "location": info.get("location"),
        "email": info.get("email"),
        "followers": info.get("followers"),
        "following": info.get("following"),
        "created_at": info.get("created_at"),
    }
    return data

async def data_4months(user):
    contributions = await getdata.get_contributions_last_6_months(user)
    # Tạo một dict mới chỉ chứa những tháng mà user đóng góp
    filtered_contributions = {}

    for month, data in contributions.items():
        if user in data:
           filtered_contributions[month] = data[user]
        else:
            # Nếu user không có dữ liệu trong tháng này, thiết lập giá trị là 0
            filtered_contributions[month] = 0

    return filtered_contributions