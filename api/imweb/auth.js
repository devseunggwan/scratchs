const url = "https://api.imweb.me/v2/auth"
const headers = {
    "Content-Type": "application/json",
    "ACCESS-AFFILIATE": "laplacetec",
}

const key = ""
const secretKey = ""

try {    
    const response = await pm.sendRequest({
        url: url,
        method: "POST",
        header: headers,
        body: JSON.stringify({
            "key": key,
            "secret": secretKey
        })
    })
    
    var responseJson = await response.json();
    pm.environment.set("imweb-access-token", responseJson.access_token)

} catch (err) {
    console.error("API 호출 실패:", err);
    console.log("응답 상태:", err.response?.status);
    console.log("응답 내용:", err.response?.data);
}
