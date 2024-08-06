from ..fetch import fetchUser

async def GetUserActivies(username):
    data = await fetchUser.fetchTimeActivity(username)
    return data
