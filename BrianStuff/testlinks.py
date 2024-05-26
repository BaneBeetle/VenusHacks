import requests




def try_site(url):
    pattern = '"playabilityStatus":{"status":"ERROR","reason":"Video unavailable"'
    request = requests.get(url)
    return False if pattern in request.text else True


print(try_site("https://www.youtube.com/watch?v=2uQlb5a10ho"))
print(try_site("https://www.youtube.com/user/patrickJMT"))
print(try_site("https://www.youtube.com/watch?v=ws2bzY8rXWY"))
