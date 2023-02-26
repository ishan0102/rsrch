# Downloading Yi Tay's favorite language papers of 2022
Let's say you were browsing Twitter and you saw a tweet from Yi Tay, a researcher at Google Brain, about his [favorite NLP papers from 2022](https://www.yitay.net/blog/2022-best-nlp-papers). You want to download them all, but you don't want to click on each link and download them one by one.

With a few lines of Python and a couple `rsrch` commands, you can!

```python
import requests
import re

# Get the HTML of the page
html = requests.get("https://www.yitay.net/blog/2022-best-nlp-papers").text

# Regex match all arXiv abstracts
matches = re.findall(r"https:\/\/arxiv\.org\/abs\/[\w\-]+\.[\w\-]+"
, html)

# Concatenate all the matches into a single string and remove quotes
urls = " ".join(matches).replace('"', '')
print(urls)
```

Now you can run `python cli.py push <urls>` to push all of the papers to your Notion database! You can also run `python cli.py download` to download all of the papers to your `papers/` directory.