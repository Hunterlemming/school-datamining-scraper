import json
from packages.config import DATA
from packages.drivers import go_to_url, get_web_element, get_web_elements
from packages.jofogas.settings import BASE_URL
from packages.jofogas.inner_item import parse_additional_data


def parse_basic_item_info(item):
    record = {
        "url": get_web_element(".//h3[@class='item-title']/a", item).get_attribute("href"),
        "price": {
            "value": int(get_web_element(".//span[@itemprop='price']", item).text.replace(" ", "")),
            "currency": get_web_element(".//span[@class='currency']", item).text.strip()
        }
    }
    return record


def scrape_page(page_url, page_num=1):
    print(f"Accessing page at {page_url} ...")
    go_to_url(page_url)
    print("Done!")
    page = {"id": page_num, "content":[]}
    item_list = get_web_elements("//div[@itemprop='item']")
    print(f"Gathering base information from page {page_num} ...")
    for item in item_list:
        page["content"].append(parse_basic_item_info(item))
    print("Done!")
    for record in page["content"]:
        parse_additional_data(record, record["url"])
    return page


def scrape_jofogas():
    with open(DATA["output-directory"] + "output.json", "w") as f:
        f.write(json.dumps(scrape_page(BASE_URL)))