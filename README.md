# rsrch
Manage your research papers through your CLI. This project lets you update a Notion database with arXiv links and download PDFs of papers to your local machine.

<p align="center">
    <img width="1095" alt="image" src="https://user-images.githubusercontent.com/47067154/219932040-ab4962f8-b01e-4d94-9eba-77a155b0e933.png">
</p>

## Installation
1. Create an [internal integration](https://www.notion.so/help/create-integrations-with-the-notion-api) in Notion.

2. [Add the integration](https://www.notion.so/help/add-and-manage-connections-with-the-api#add-connections-to-pages) to the database you want to download from.

3. Create a `.env` file with the following variables:

    ```
    NOTION_TOKEN=secret_XXXXXXXX
    NOTION_DATABASE_ID=XXXXXXXXXXXXXXXX
    ```
    Your `NOTION_TOKEN` can be found in your [integrations page](https://www.notion.so/my-integrations) and is called the **Internal Integration Token**. The `NOTION_DATABASE_ID` can be found in the [URL of your database](https://www.notion.so/my-integrations) (`https://www.notion.so/{workspace_name}/{database_id}?v={view_id}`).

4. Install local dependencies:

    ```bash
    python3 -m venv venv
    pip install -r requirements.txt
    ```

5. **Important**: Your Notion database must have the following columns with the corresponding types:
    - **Title**: `Title`
    - **URL**: `URL`
    - **Date**: `Date`
    - **Authors**: `Text`

    You can add more columns, but these are the ones that are required.

## Usage
Activate the virtual environment:

```bash
source venv/bin/activate
```

### Download
This will download all the papers from your Notion database to the `papers/` directory.

```bash
cd src
python cli.py download
```

<p>
    <img width="1097" alt="image" src="https://user-images.githubusercontent.com/47067154/219932318-54b37a51-850f-4ab2-b916-43361816fa91.png">
</p>

### Push
You can push arXiv abstract links, PDF links, or IDs to your Notion database and have it autofill all of the relevant fields.

```bash
cd src
python cli.py push https://arxiv.org/abs/1706.03762
```

<p>
    <img width="1095" alt="image" src="https://user-images.githubusercontent.com/47067154/219932341-a44ff798-3fd0-46f8-8a43-3a22b5dcdcf8.png">
</p>

Alternatively, you can add non-arXiv links manually to Notion.


## Notes
- Uploading papers to Notion is currently only supported for arXiv links. Papers with titles that already exist in the database will not be uploaded.
- The script will download the PDFs to the `papers/` directory. If you want to change this, you can change the `path` variable in `main.py`.
- I plan on adding support for other databases in the future, but for now it only works with Notion databases.

### Bash Functions
For those of us that use the command line a lot, you can add the following functions to your `.bashrc` file to make it easier to use:

#### Download any new research papers
```bash
function get_papers() {
    # Go to rsrch directory
    cd ~/Documents/projects/rsrch

    # Download papers
    source venv/bin/activate
    python src/cli.py download
    cd papers
}
```

#### Push any new research papers
```bash
function add_papers() {
    # Go to rsrch directory
    cd ~/Documents/projects/rsrch

    # Push papers
    source venv/bin/activate
    python src/cli.py push $*
}
```

Now you can just run `get_papers` or `add_papers` with `N` arXiv links to download or push papers to your Notion database!

### Resources
- [Notion API](https://developers.notion.com/)