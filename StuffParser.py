# import os
import time
import random
import re
from bs4 import BeautifulSoup
from requests import get
#
# from db_data import db_session
# from db_data.products import Product
# from db_data.categories import Category

main_url = "https://animeshop-akki.ru/"
sleep_time = 3
count = 0

logs = open("logs.txt", "w")

# db_session.global_init('db/shop.sqlite')

main_req = get(main_url)
parser1 = BeautifulSoup(main_req.content, "lxml")
all_categories = parser1.find_all("span", {"class": "category-menu-item"})
all_categories_href = [elem.findChildren("a")[0].get_attribute_list("href")[0].replace(main_url, "")
                       for elem in
                       all_categories]
filtered_categories_href = [elem for elem in all_categories_href if
                            len(list(
                                filter(lambda x: x, [href.startswith(elem) for href in
                                                     all_categories_href]))) == 1]
filtered_categories_href.remove("svoy_dizayn/anime-opt/")
print(filtered_categories_href)
# for name in filtered_categories_href:
#     if not os.path.isdir(f"static/img/{name.split('/')[0]}"):
#         os.mkdir(f"static/img/{name.split('/')[0]}")
#     if not os.path.isdir(f"static/img/{name}"):
#         os.mkdir(f"static/img/{name}")

for url in filtered_categories_href:
    try:
        cur_ulr = main_url + url
        cur_page = get(cur_ulr)
        cur_parser = BeautifulSoup(cur_page.content, "lxml")
        pages_amount = min(int(
            re.findall(r"всего ([0-9]+) страниц",
                       cur_parser.find_all("div", {"class": "results"})[0].text)[0]), 5)
        print("URL:", cur_ulr, file=logs)
        print("Количество страниц:", pages_amount, end="\n\n", file=logs)
        for page_number in range(1, pages_amount + 1):
            try:
                subpage = get(cur_ulr + f"?page={page_number}")
                parser2 = BeautifulSoup(subpage.content, "lxml")
                aTagObjects = [elem.findChildren("a")[0] for elem in
                               parser2.find_all("h6", {"class": "card-title"})]
                for aTagObject in aTagObjects:
                    try:
                        count += 1
                        item_url = aTagObject.get_attribute_list("href")[0]
                        item_req = get(item_url)
                        parser3 = BeautifulSoup(item_req.content, "lxml")

                        ITEM_NAME = aTagObject.text
                        ITEM_PRICE = int(
                            parser3.find_all("meta", itemprop="price")[0].get_attribute_list(
                                "content")[0])
                        ITEM_AMOUNT = random.randint(1, 100)
                        ITEM_PIC_URL = \
                        parser3.find_all("meta", property="og:image")[0].get_attribute_list(
                            "content")[0]
                        ITEM_CATEGORY = \
                            parser3.find_all("meta", property="product:category")[
                                0].get_attribute_list("content")[0]
                        ITEM_LOCAL_PATH = f"static/img/{url}{item_url.split('/')[-1]}.jpg"

                        print("Ссылка на товара:", item_url, file=logs)
                        print("Название товара:", ITEM_NAME, file=logs)
                        print("Стоймость товара:", ITEM_PRICE, file=logs)
                        print("Категория товара:", ITEM_CATEGORY, file=logs)
                        print("Количество товара:", ITEM_AMOUNT, file=logs)
                        print("Ссылка на картинку:", ITEM_PIC_URL, file=logs)
                        print("Локальный путь:", ITEM_LOCAL_PATH, file=logs)
                        print("Номер товара:", count, file=logs)

                        item_img_content = get(ITEM_PIC_URL).content
                        with open('pics/' + ITEM_LOCAL_PATH.split('/')[-1], "wb") as f:
                            f.write(item_img_content)
                            print("Картинка сохранена:", ITEM_LOCAL_PATH + "\n", file=logs)

                        # db_sess = db_session.create_session()
                        #
                        # category = Category(name=ITEM_CATEGORY)
                        # db_sess.add(category)
                        # category = db_sess.query(Category).filter(Category.name == ITEM_CATEGORY).first()
                        #
                        # product = Product(
                        #     name=ITEM_NAME,
                        #     pics='pics/' + ITEM_LOCAL_PATH.split('/')[-1],
                        #     content=item_url,
                        #     amount=ITEM_AMOUNT,
                        #     price=ITEM_PRICE
                        # )

                        # product.categories.append(category)
                        # db_sess.add(product)
                        # db_sess.commit()

                        print(f"Товар \"{ITEM_NAME}\" успешно записан, номер={count}")
                        time.sleep(sleep_time)
                    except Exception as f:
                        print("ERROR!!!", str(f), file=logs)
                        continue
            except Exception as f:
                print("ERROR!!!", str(f), file=logs)
                continue
    except Exception as f:
        print("ERROR!!!", f, file=logs)
        continue
logs.close()
