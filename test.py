import requests

url = "https://spotify23.p.rapidapi.com/search/"

querystring = {"q":"Die for you","type":"tracks","offset":"0","limit":"1","numberOfTopResults":"1"}

headers = {
	"X-RapidAPI-Key": "99db78a117mshf10d54a13f695fep172c0fjsn5044db8fc6e7",
	"X-RapidAPI-Host": "spotify23.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)
res = response.json()
print(res["tracks"]["items"][0]["data"]["uri"])