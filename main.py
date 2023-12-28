import json
import os
import requests
from tqdm import tqdm
import time
from config import token, groups, url_count


def get_links(group):
    url = f"https://api.vk.com/method/wall.get?domain={group}&count={url_count}&access_token={token}&v=5.137"
    req = requests.get(url)
    src = req.json()
    if os.path.exists(f"data"):
        pass
    else:
        os.mkdir(f'data')
    # проверяем существует ли директория с именем группы
    if os.path.exists(f"data/{group}"):
        pass
    else:
        os.mkdir(f'data/{group}')

    # собираем ID новых постов в список
    fresh_posts_id = []
    posts = src["response"]["items"]

    for fresh_post_id in posts:
        fresh_post_id = fresh_post_id["id"]
        fresh_posts_id.append(fresh_post_id)

    ids = []
    if not os.path.exists(f"data/{group}/id.json"):    
        for item in fresh_posts_id:
            ids.append(item)
        result = []
        # извлекаем данные из постов
        for post in tqdm(posts):
            post_id = post["id"]
            collect_data(post, result, post_id)
    else:
        with open(f'data/{group}/id.json') as file:
            id_list = json.load(file)
        result = []
        # извлекаем данные из постов
        for post in tqdm(posts):
            post_id = post["id"]
            if post_id in id_list:
                ids.append(post_id)
                continue
            else:
                ids.append(post_id)
                collect_data(post, result, post_id)

    if os.path.exists(f'data/{group}/links.json'):
        os.remove(f'data/{group}/links.json')
        with open(f'data/{group}/links.json', 'w') as file:
            json.dump(result, file, indent=4, ensure_ascii=False)
    else:
        with open(f'data/{group}/links.json', 'w') as file:
            json.dump(result, file, indent=4, ensure_ascii=False)
    with open(f"data/{group}/id.json", "w") as file:
        json.dump(ids, file, indent=4, ensure_ascii=False)


def collect_data(post, result, post_id):
    try:
        if "attachments" in post:
            post = post["attachments"]

            # забираем фото
            if post[0]["type"] == "photo":

                photo_quality = [
                    "r",
                    "q",
                    "p",
                    "o",
                    "z",
                    "y"
                ]

                if len(post) > 1:
                    for post_item_photo in post:
                        if post_item_photo["type"] == "photo":
                            for pq in photo_quality:
                                if pq in post_item_photo["photo"]["sizes"][-1]["type"]:
                                    post_photo = post_item_photo["photo"]["sizes"][-1]["url"]
                                    result.append(
                                        post_photo
                                    )
                                    break

                else:
                    pass

    except Exception as ex:
        print(f"Error ID {post_id}!/n Error:{ex}")
    time.sleep(0.1)



def collect(group):
    with open(f'data/{group}/links.json') as file:
        links = json.load(file)
    link = links[-1]
    # response = requests.get(link)
    links.remove(link)
    with open(f'data/{group}/links.json', 'w') as file:
        json.dump(links, file, indent=4, ensure_ascii=False)
    return link
def count():
    all_links = 0
    for group in groups:
        with open(f'data/{group}/links.json') as file:
            links = json.load(file)
        all_links += len(links)
    return all_links

def collect_links():
    for group in groups:
        try:
            with open(f'data/{group}/links.json') as file:
                links = json.load(file)
            if len(links) == 0:
                get_links(group)
            else:
                pass
        except Exception:
            get_links(group)


def collect_on():
    if os.path.exists('data'):
        for group in groups:
            return collect(group)
    else:
        collect_links()
        for group in groups:
            return collect(group)


