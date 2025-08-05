import os
from dotenv import load_dotenv
from notion_client import Client

def main():
    load_dotenv()  # Load .env file

    notion_token = os.getenv("NOTION_TOKEN")
    database_id = os.getenv("NOTION_DATABASE_ID")

    if not notion_token or not database_id:
        print("❌ Missing NOTION_TOKEN or NOTION_DATABASE_ID in .env")
        return

    notion = Client(auth=notion_token)

    try:
        response = notion.databases.retrieve(database_id=database_id)
        print("✅ Connection successful!")
        print(f"Database title: {response['title'][0]['plain_text']}")
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    main()
