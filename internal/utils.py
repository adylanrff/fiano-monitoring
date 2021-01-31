import config
from uuid import uuid1
from service.notion import notion_service
from random import choice


def add_new_multi_select_value(collection, prop, value):
    colors = [
        "default",
        "gray",
        "brown",
        "orange",
        "yellow",
        "green",
        "blue",
        "purple",
        "pink",
        "red",
    ]
    
    color = choice(colors)

    collection_schema = collection.get("schema")
    prop_schema = next(
        (v for k, v in collection_schema.items() if v["name"] == prop), None
    )

    if not prop_schema:
        print(
            f'"{prop}" property does not exist on the collection!'
        )
        return 

    if prop_schema["type"] != "multi_select":
        print(f'"{prop}" is not a multi select property!')
        return 

    dupe = next(
        (o for o in prop_schema["options"] if o["value"] == value), None
    )
    if dupe:
        print(f'"{value}" already exists in the schema!')
        return

    prop_schema["options"].append(
        {"id": str(uuid1()), "value": value, "color": color}
    )
    collection.set("schema", collection_schema)