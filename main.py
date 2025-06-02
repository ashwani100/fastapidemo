from fastapi import FastAPI
from app.models import BookmarkData, ConversationData
from app.dynamo_utils import create_table_if_not_exists, put_item, get_user_data

app = FastAPI()

BOOKMARK_TABLE = "UserBookmarks"
CONVERSATION_TABLE = "UserConversations"

create_table_if_not_exists(
    BOOKMARK_TABLE,
    [{"AttributeName": "user_id", "KeyType": "HASH"}],
    [{"AttributeName": "user_id", "AttributeType": "S"}]
)

create_table_if_not_exists(
    CONVERSATION_TABLE,
    [{"AttributeName": "user_id", "KeyType": "HASH"}],
    [{"AttributeName": "user_id", "AttributeType": "S"}]
)

@app.post("/bookmark/save")
def save_bookmark(data: BookmarkData):
    item = data.dict()
    item["last_search_date"] = item["last_search_date"].isoformat()
    put_item(BOOKMARK_TABLE, item)
    return {"message": "Bookmark saved"}

@app.get("/bookmark/user/{user_id}")
def get_bookmarks(user_id: str):
    return get_user_data(BOOKMARK_TABLE, user_id)

@app.post("/conversation/save")
def save_conversation(data: ConversationData):
    item = data.dict()
    item["last_search_date"] = item["last_search_date"].isoformat()
    put_item(CONVERSATION_TABLE, item)
    return {"message": "Conversation saved"}

@app.get("/conversation/user/{user_id}")
def get_conversations(user_id: str):
    return get_user_data(CONVERSATION_TABLE, user_id)
