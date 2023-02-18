import math
import os

import requests
import urllib3
from dotenv import load_dotenv
from tqdm import tqdm

import utils


def download_papers():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    load_dotenv()
    papers = utils.fetch_table()

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
