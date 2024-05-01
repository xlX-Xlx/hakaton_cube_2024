url = "https://api.coze.com/open_api/v2/chat"

header = {
    "Authorization": "Bearer pat_Y5Z6YnU5v1qWaQozkRqT5OAvhYaka0KaoJCr4R7f1al8TSsH4qKTQZCIhBBqrSLk",
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Host": "api.coze.com",
    "Connection": "keep-alive",
}

data = {
    "bot_id": "7364043444622278662",
    "user": "2982100723509",
    "query": "",
    "stream": False
}

nums = [x ** 2 for x in range(1000)]