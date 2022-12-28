from notion_client import Client
import arxiv
import pandas as pd
from tqdm import tqdm

from dotenv import load_dotenv
import os

def fetch_table():
    notion = Client(auth=os.getenv("NOTION_TOKEN"))
    papers = notion.databases.query(database_id=os.getenv("NOTION_DATABASE_ID"))

    titles, ids = [], []
    for paper in papers["results"]:
        if not paper["properties"]["Title"]["title"] == []:
            titles.append(paper["properties"]["Title"]["title"][0]["plain_text"])
            ids.append(paper["properties"]["URL"]["url"].split("/")[-1])
    
    df = pd.DataFrame({"title": titles, "id": ids})
    return df
    
def download_papers(df):
    papers = arxiv.Search(id_list=df["id"]).results()
    for i, paper in tqdm(enumerate(papers)):
        title = df["title"][i].replace(" ", "_")
        path = f"papers/{title}.pdf"
        if not os.path.exists(path):
            paper.download_pdf(filename=path)

if __name__ == "__main__":
    load_dotenv()
    df = fetch_table()
    download_papers(df)