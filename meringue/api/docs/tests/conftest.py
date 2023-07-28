schema_1 = {
    "servers": [
        {
            "description": "Server 1",
            "url": "https://example-1.com",
        },
        {
            "description": "Server 2",
            "url": "example-2.com",
        },
    ],
}
schema_1_result = {
    "servers": [
        {
            "description": "Server 1",
            "url": "https://example-1.com",
        },
        {
            "description": "Server 2",
            "url": "example-2.com",
        },
    ],
    "info": {
        "description": """Server 1 API: [example-1.com](https://example-1.com)

Server 2 API: [example-2.com](example-2.com)""",
    },
}


schema_2 = {
    "servers": [
        {
            "description": "Server 1",
            "url": "https://example-1.com",
        },
        {
            "description": "Server 2",
            "url": "example-2.com",
        },
    ],
    "info": {"description": "# Test"},
}
schema_2_result = {
    "servers": [
        {
            "description": "Server 1",
            "url": "https://example-1.com",
        },
        {
            "description": "Server 2",
            "url": "example-2.com",
        },
    ],
    "info": {
        "description": """# Test

Server 1 API: [example-1.com](https://example-1.com)

Server 2 API: [example-2.com](example-2.com)""",
    },
}
