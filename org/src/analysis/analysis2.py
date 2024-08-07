from ..fetch import fetchOrg

async def GetDataOrg(orgname):  
    data = await fetchOrg.fetchOrgInfo(orgname)
    return data
