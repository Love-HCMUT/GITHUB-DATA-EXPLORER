from ..fetch import fetch1 

async def GetRepoContributors(username, reponame, TOKEN): 
    data = await fetch1.fetchRepoContributors(username, reponame, TOKEN)
    return data


async def GetRepoCommits(username, reponame, TOKEN):
    data = await fetch1.fetchRepoCommits(username, reponame, TOKEN)
    return data 


async def GetRepoIssues(username, reponame, TOKEN):
    data = await fetch1.fetchRepoIssues(username, reponame, TOKEN)
    return data 


async def GetRepoPulls(username, reponame, TOKEN):
    data = await fetch1.fetchRepoPulls(username, reponame, TOKEN)
    return data 
