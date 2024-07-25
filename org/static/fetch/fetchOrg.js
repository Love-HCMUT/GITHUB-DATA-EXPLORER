console.log(1)

export async function fetchAPI(urls) {
    try {
        let response = await fetch(urls)
        if (!response.ok) throw new Error("Erroe while fetch API ", urls)
        let data = await response.json()
        // console.log(data)
        return data
    }
    catch(err) {
        console.error(err)
    }
}

