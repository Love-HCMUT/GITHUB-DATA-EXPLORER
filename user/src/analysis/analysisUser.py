from ..fetch import fetchUser

async def GetUserActivies(username, TOKEN):
    data = await fetchUser.fetchTimeActivity(username, TOKEN)
    return data
