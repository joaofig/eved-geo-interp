import requests


def download_file(url: str, file_name: str) -> None:
    response = requests.get(url)
    response.raise_for_status()
    with open(file_name, "wb") as f:
        f.write(response.content)
