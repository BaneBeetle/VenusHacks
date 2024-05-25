import requests
from dotenv import load_dotenv # This is where I want to keep my API key secret
import os

def configure(): # In charge of getting .env from my environment, this contains my API key
    load_dotenv()


def get_pages(num_pages=None):
    """
    If num_pages is None, get all pages, otherwise just the defined number.
    """
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

    get_all = num_pages is None
    page_size = 100 if get_all else num_pages

    payload = {"page_size": page_size}
    response = requests.post(url, json=payload, headers=headers)

    data = response.json()

    # Comment this out to dump all data to a file
    # import json
    # with open('db.json', 'w', encoding='utf8') as f:
    #    json.dump(data, f, ensure_ascii=False, indent=4)

    results = data["results"]
    while data["has_more"] and get_all:
        payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
        url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        results.extend(data["results"])

    return results

#pages = get_pages()

#for page in pages:
#    page_id = page["id"]
#    props = page["properties"]
#    #task = props["Task"]["title"][0]["text"]["content"]
#    task = props["Task"]["title"]
#    name = props["Names"]["rich_text"]

#    if (0 < len(task)):
#        task = props["Task"]["title"][0]["text"]["content"]
#        print(task)
#    else:
#        print("Empty!")
    
#    if (0 < len(name)):
#        name = props["Names"]["rich_text"][0]["text"]["content"]
#        print(name)
#    else:
#        print("Empty!")
    #name = props["Name"]["rich_text"][0]["text"]["content"]
    #print(task, name)
    
#def create_page(data: dict):
#    create_url = "https://api.notion.com/v1/pages"#

   # payload = {"parent": {"database_id": DATABASE_ID}, "properties": data}

   # res = requests.post(create_url, headers=headers, json=payload)

   # return res

#title = input("Write a message!\n")
#description = input("Whats your name!\n")
#data = {
#    "Name": {"title": [{"text": {"content": description}}]},
#    "Message": {"rich_text": [{"text": {"content": title}}]}
#}

#create_page(data)

def create_post():
    configure()
    NOTION_TOKEN = os.getenv('NOTION_KEY')
    DATABASE_ID = os.getenv('NOTION_DATABASE_ID')
    headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
    }

    description = input("Whats your name!\n")
    title = input("Write a message!\n")
    data = {
    "Name": {"title": [{"text": {"content": description}}]},
    "Message": {"rich_text": [{"text": {"content": title}}]}
    }

    create_url = "https://api.notion.com/v1/pages"

    payload = {"parent": {"database_id": DATABASE_ID}, "properties": data}

    res = requests.post(create_url, headers=headers, json=payload)

    return res

if __name__ == "__main__":
    create_post()