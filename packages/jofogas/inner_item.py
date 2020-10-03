from packages.drivers import go_to_url, get_web_element


boolean_false_field_description = ("nincs","nem")
boolean_true_field_description = ("van","igen")


def parse_address(record):
    region = get_web_element("//meta[@itemprop='addressRegion']")
    record["address"] = {"region" : region.get_attribute("content").replace(" ", "") if region is not None else None}
    locality = get_web_element("//span[@itemprop='addressLocality']")
    record["address"]["locality"] = locality.text if locality is not None else None
    if record["address"]["region"] == "Budapest":
        record["address"]["region"] = "Pest"
        record["address"]["district"] = record["address"]["locality"]
        record["address"]["locality"] = "Budapest"


def parse_floor(record):
    floor = get_web_element("//div[contains(@class, 'floor')]/span[2]")
    try:
        record["floor"] = {"level": int(floor.text.replace(" ", "")) if floor is not None else None}
    except ValueError:
        record["floor"] = {"level": floor.text.replace(" ", "")}
    lift = get_web_element("//div[contains(@class, 'elevator')]/span[2]")
    lift = lift.text.replace(" ", "") if lift is not None else None
    record["floor"]["has_lift"] = lift
    if lift is not None:
        if lift.lower() in boolean_false_field_description:
            record["floor"]["has_lift"] = False 
        elif lift.lower() in boolean_true_field_description:
            record["floor"]["has_lift"] = True


def parse_category(record):
    category = get_web_element("//meta[@itemprop='category']/following-sibling::span[2]")
    record["category"] = category.text if category is not None else None


def parse_condition(record):
    condition = get_web_element("//div[contains(@class, 'realestate_condition')]/span[2]")
    record["condition"] = condition.text if condition is not None else None


def parse_material(record):
    material = get_web_element("//div[contains(@class, 'building_type')]/span[2]")
    record["material"] = material.text if material is not None else None


def parse_balcony(record):
    balcony = get_web_element("//div[contains(@class, 'balcony')]/span[2]")
    balcony = balcony.text.replace(" ", "") if balcony is not None else None
    record["has_balcony"] = balcony
    if balcony is not None:
        if balcony.lower() in boolean_false_field_description:
            record["has_balcony"] = False
        elif balcony.lower() in boolean_true_field_description:
            record["has_balcony"] = True


def parse_furniture(record):
    furniture = get_web_element("//div[contains(@class, 'has_furniture')]/span[2]")
    furniture = furniture.text.replace(" ", "") if furniture is not None else None
    record["has_furniture"] = furniture
    if furniture is not None:
        if furniture.lower() in boolean_false_field_description:
            record["has_furniture"] = False
        elif furniture.lower() in boolean_true_field_description:
            record["has_furniture"] = True


def parse_parking(record):
    parking = get_web_element("//div[contains(@class, 'parking_type')]/span[2]")
    record["parking"] = parking.text.replace(" ", "") if parking is not None else None


def parse_size(record):
    inner_height = get_web_element("//div[contains(@class, 'inner_height')]/span[2]")
    inner_height = inner_height.text if inner_height is not None else None
    rooms = get_web_element("//div[contains(@class, 'rooms')]/span[2]")
    rooms = int(rooms.text.replace("szoba", "").replace("+", "").replace(" ", "")) if rooms is not None else None
    area = get_web_element("//div[contains(@class, 'size')]/span[2]")
    area_value = int(area.text.split(" ")[0].replace(" ", "")) if area is not None else None
    area_measurement = area.text.split(" ")[1].replace(" ", "") if area is not None else None
    record["size"] = {
        "area": {
            "value": area_value,
            "measurement": area_measurement,
        },
        "inner_height": inner_height,
        "rooms": rooms
    }


def parse_additional_data(record, url):
    print(f"Parsing item at url: {url} ...")
    go_to_url(url)
    parse_address(record)
    parse_size(record)
    parse_category(record)
    parse_condition(record)
    parse_floor(record)
    parse_material(record)
    parse_balcony(record)
    parse_furniture(record)
    print("Done!")
