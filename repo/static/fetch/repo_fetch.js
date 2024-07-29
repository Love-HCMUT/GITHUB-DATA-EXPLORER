export async function fetchAPI(urls) {
    try {
        let response = await fetch(urls)
        if (!response.ok) throw new Error("Error while fetching API ", urls)
        let data = response.json()
        return data
    }
    catch(err) {
        console.error(err)
    }
}