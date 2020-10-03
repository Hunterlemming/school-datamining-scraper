import json
from packages.config import DATA
from packages.drivers import go_to_url, get_web_element, get_web_elements
from packages.jofogas.settings import BASE_URL, HUN_GEO


def parse_location(location_element):
    if location_element is None:
        return None
    location = {"full-address": location_element.text, "county": None, "municipality": None}
    for county in HUN_GEO["counties"].keys():
        if county in location["full-address"]:
            location["county"] = county
        for municipality in HUN_GEO["counties"][county]:
            if municipality in location["full-address"]:
                location["municipality"] = municipality
                if location["county"] is None:
                    location["county"] = county
    return location


def parse_item(item):
    record = {
        "url": get_web_element(".//h3[@class='item-title']/a", item).get_attribute("href"),
        "price": {
            "value": int(get_web_element(".//span[@itemprop='price']", item).text.replace(" ", "")),
            "currency": get_web_element(".//span[@class='currency']", item).text.strip()
        }
    }
    # Additional info (could be missing)
    size = get_web_element(".//div[@class='size']", item)
    record["size"] = {
        "value": int(size.text.split(" ")[0]) if size is not None else None,
        "measurement": size.text.split(" ")[1].strip() if size is not None else None
    }
    rooms = get_web_element(".//div[@class='rooms']", item)
    record["rooms"] = rooms.text.split(" ")[0] if rooms is not None else None
    location = get_web_element(".//section[contains(@class, 'cityname')]", item)
    record["location"] = parse_location(location)
    return record


def scrape_page(page_url, page_num=1):
    go_to_url(page_url)
    page = {"id": page_num, "url": page_url, "content":[]}
    item_list = get_web_elements("//div[@itemprop='item']")
    for item in item_list:
        page["content"].append(parse_item(item))
    return page


def scrape_jofogas():
    with open(DATA["output-directory"] + "output.json", "w") as f:
        f.write(json.dumps(scrape_page(BASE_URL)))