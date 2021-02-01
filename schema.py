ProjectJsonSchema = {
    "type": "object",
    "properties": {
        "project": {
            "type": "object",
            "properties": {
                "nama": { "type": "string" },
                "pekerja": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                },
                "deliverables": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "section": { "type": "string"},
                            "item": { "type": "string"},
                            "subitem": { "type": "string"},
                            "quantity": { "type": "number"},
                            "price": { "type": "number"},
                            "unit": { "type": "string"},
                            "info": { "type": "string"},
                        }
                    }
                },
                "start_date": { "type": "string", "format": "date"},
                "end_date": { "type": "string", "format": "date"}
            },
            "required" : ["nama", "deliverables", "start_date", "end_date"]
        }
    }
}