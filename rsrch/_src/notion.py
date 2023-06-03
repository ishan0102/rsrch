import math
import os
from typing import List, Union

import arxiv
import requests
from notion_client import Client
from tqdm import tqdm


class RsrchClient:
    """
    A class to interface with the Notion API and perform operations related to research papers.

    Attributes
    ----------
    notion : Client
        The Notion API client.
    database_id : str
        The ID of the database in Notion.
    """

    def __init__(self, token: str, database_id: str):
        """
        Initializes the RsrchClient with the provided API key and database ID.

        Parameters
        ----------
        token : str
            The API key for Notion. If not provided, raises a ValueError.
        database_id : str
            The ID of the database in Notion. If not provided, raises a ValueError.
        """
        if not token:
            raise ValueError("API key must be provided.")
        if not database_id:
            raise ValueError("Database ID must be provided.")

        self.notion = Client(auth=token)
        self.database_id = database_id

    def _get_paper_properties(self, paper):
        title = paper["properties"]["Title"]["title"][0]["plain_text"]
        url = paper["properties"]["URL"]["url"]
        date = paper["properties"]["Date"]["date"]["start"]
        authors = paper["properties"]["Authors"]["rich_text"][0]["plain_text"]
        return title, url, date, authors

    def fetch_table(self):
        paper_db = self.notion.databases.query(database_id=self.database_id)
        papers = [
            self._get_paper_properties(paper) for paper in paper_db["results"] if paper["properties"]["Title"]["title"]
        ]
        return [paper for paper in papers if paper[1] and paper[1].startswith("http")]

    def _save_paper(self, r, path):
        with open(path, "wb") as f:
            for chunk in tqdm(
                r.iter_content(chunk_size=1024),
                total=math.ceil(int(r.headers["Content-Length"]) / 1024),
                unit="KB",
            ):
                if chunk:
                    f.write(chunk)

    def download(self):
        """
        Downloads all papers from the Notion database and saves them as PDFs.

        The papers are saved in a directory named "papers". Each paper is saved as a separate PDF file.

        If a paper has already been downloaded (i.e., a PDF file with the same name exists in the directory),
        the download is skipped for that paper.

        All download progress is logged to the console.
        """
        print("Downloading papers from Notion...")
        papers = self.fetch_table()

        if not os.path.exists("papers"):
            os.mkdir("papers")

        for title, url, _, _ in papers:
            path = f"papers/{title.replace(' ', '_')}.pdf"
            if not os.path.exists(path):
                print(f'\nDownloading "{title}"')
                r = requests.get(url, stream=True)
                self._save_paper(r, path)

    def create_paper(self, title, url, date, authors):
        self.notion.pages.create(
            parent={"database_id": self.database_id},
            properties={
                "Title": {"title": [{"text": {"content": title}}]},
                "URL": {"url": url},
                "Date": {"date": {"start": date}},
                "Authors": {"rich_text": [{"text": {"content": authors}}]},
            },
        )
        print(f"- {title}")

    def _extract_arxiv_id(self, url):
        if url.startswith("https://arxiv.org/abs/"):
            return url.replace("https://arxiv.org/abs/", "")
        elif url.startswith("https://arxiv.org/pdf/") and url.endswith(".pdf"):
            return url.replace("https://arxiv.org/pdf/", "").replace(".pdf", "")
        elif requests.get(f"https://arxiv.org/abs/{url}").status_code == 200:
            return url
        else:
            print(f"ERROR: {url} is not a valid arXiv abstract URL, PDF URL, or ID.")
            return None

    def upload(self, arxiv_urls: Union[List[str], str]):
        """
        Uploads papers from arXiv to the Notion database.

        The papers to upload are specified by providing their arXiv URLs.

        If a paper with the same title already exists in the database, the upload is skipped for that paper.

        Parameters
        ----------
        arxiv_urls : list of str
            The arXiv URLs of the papers to upload.
        """
        if isinstance(arxiv_urls, str):
            arxiv_urls = [arxiv_urls]

        ids = [self._extract_arxiv_id(url) for url in arxiv_urls if self._extract_arxiv_id(url)]
        if not ids:
            raise ValueError("No valid arXiv URLs provided.")

        papers = self.fetch_table()
        titles = [title for title, _, _, _ in papers]

        print("Uploading papers to Notion...\n")
        results = arxiv.Search(id_list=ids)
        for paper in results.results():
            date = paper.published.isoformat().split("T")[0]
            title = paper.title
            authors = [author.name for author in paper.authors]
            if len(authors) > 5:
                authors = ", ".join(authors[:5]) + ", et al."
            else:
                authors = ", ".join(authors)

            pdf_url = paper.pdf_url

            if title not in titles:
                self.create_paper(title, pdf_url, date, authors)
            else:
                print(f"- {title} (already exists)")

        print("\nDone!")
