const url = "https://api.commerce.naver.com/partner/v1/oauth2/token";
const header = { "content-type": "application/x-www-form-urlencoded" }

const clientId = "";
const clientSecret = "";
const accountId = "";

var timestampForCert = Math.round(Date.now());
var password = clientId + "_" + timestampForCert.toString();
var hashed = CryptoJS.HmacSHA256(password, clientSecret);
var certStr = CryptoJS.enc.Base64.stringify(hashed);

var params = new URLSearchParams({
    client_id: clientId,
    timestamp: timestampForCert.toString(),
    client_secret_sign: certStr,
    grant_type: "client_credentials",
    type: "SELLER",
    account_id: accountId
})

var response = await pm.sendRequest(
    {
        url,
        method: "POST",
        header: header,
        body: params
    }
)
var responseText = await response.text();
var responseJson = JSON.parse(responseText);

pm.environment.set("smartstore_commerce_token", responseJson.access_token)