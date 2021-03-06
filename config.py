import os
from dotenv import load_dotenv
load_dotenv()

NOTION_TOKEN_V2 = os.getenv("NOTION_TOKEN_V2")
NOTION_ROOT_PAGE_URL = os.getenv("NOTION_ROOT_PAGE_URL")
NOTION_WORKER_PAGE_URL = os.getenv("NOTION_WORKER_PAGE_URL")
NOTION_DELIVERABLES_PAGE_URL = os.getenv("NOTION_DELIVERABLES_PAGE_URL")
NOTION_PROJECT_PAGE_URL = os.getenv("NOTION_PROJECT_PAGE_URL")
REDIS_URL=os.getenv("REDIS_URL")
POSTGRES_HOST=os.getenv("POSTGRES_HOST")
POSTGRES_USER=os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB=os.getenv("POSTGRES_DB")
GMAIL_USER=os.getenv("GMAIL_USER")
GMAIL_PASSWORD=os.getenv("GMAIL_PASSWORD")