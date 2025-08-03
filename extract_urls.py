import pandas as pd


def extract_url(url):
    url_parts = url.split("/")

    if len(url_parts) != 6:
        return None

    if url_parts[3] == "shop":
        return url

    else:
        return None


if __name__ == "__main__":
    df = pd.read_csv("all_urls.csv", header=None)
    filtered_urls = df[0].apply(extract_url).dropna()

    filtered_urls.to_csv("urls.csv", index=False)
