from ..fetch import fetch1 

async def GetRepoContributors(username, reponame): 
    data = await fetch1.fetchRepoContributors(username, reponame)
    return data


async def GetRepoCommits(username, reponame):
    data = await fetch1.fetchRepoCommits(username, reponame)
    return data 


async def GetRepoIssues(username, reponame):
    data = await fetch1.fetchRepoIssues(username, reponame)
    return data 


async def GetRepoPulls(username, reponame):
    data = await fetch1.fetchRepoPulls(username, reponame)
    return data 
