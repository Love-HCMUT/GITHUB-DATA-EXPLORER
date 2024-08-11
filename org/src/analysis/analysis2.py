from ..fetch import fetchOrg

async def GetDataOrg(orgname, TOKEN): 
    data = await fetchOrg.fetchOrgInfo(orgname, TOKEN)
    return data