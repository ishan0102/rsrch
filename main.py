from notion_client import Client
from dotenv import load_dotenv
from tqdm import tqdm
import requests
import urllib3
import math
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def fetch_table():
    notion = Client(auth=os.getenv("NOTION_TOKEN"))
    paper_db = notion.databases.query(database_id=os.getenv("NOTION_DATABASE_ID"))

    papers = []
    for paper in paper_db["results"]:
        if not paper["properties"]["Title"]["title"] == []:
            title = paper["properties"]["Title"]["title"][0]["plain_text"]
            url = paper["properties"]["URL"]["url"]
            if not url == None and url.startswith("http"):
                papers.append((title, url))

    return papers


def download_papers(papers):
    if not os.path.exists("papers"):
        os.mkdir("papers")

    for title, url in papers:
        path = f"papers/{title.replace(' ', '_')}.pdf"
        if not os.path.exists(path):
            print(f'\nDownloading "{title}"')
            try:
                r = requests.get(url, stream=True, verify=True)
            except requests.exceptions.SSLError:
                r = requests.get(url, stream=True, verify=False)

            with open(path, "wb") as f:
                for chunk in tqdm(
                    r.iter_content(chunk_size=1024),
                    total=math.ceil(int(r.headers["Content-Length"]) / 1024),
                    unit="KB",
                ):
                    if chunk:
                        f.write(chunk)


if __name__ == "__main__":
    load_dotenv()
    papers = fetch_table()
    download_papers(papers)
