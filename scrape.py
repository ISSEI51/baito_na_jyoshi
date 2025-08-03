import pandas as pd
import re
from concurrent.futures import ThreadPoolExecutor

from access_url import access_url


COLUMNS = ["社名", "電話番号", "所在地", "代表者", "事業内容", "企業URL"]


def scrape(url):
    soup = access_url(url)
    data = dict.fromkeys(COLUMNS)
    try:
        tel = soup.find("p", class_="recruit-offerNumber").get_text()
        data["電話番号"] = clean_text(tel)
    except:
        print("tel is not found")
        data["電話番号"] = ""

    try:
        table = soup.find("div", class_="detail-secondary__company u-inner")
        for column in COLUMNS[:1] + COLUMNS[2:5]:
            data[column] = parse_table(table, column)
    except:
        return None

    try:
        data["企業URL"] = soup.find("a", class_="company-link").get_text()
    except:
        data["企業URL"] = ""

    print(data)
    return data


def clean_text(text):
    return re.sub(r"[\s\u3000]", "", text)


def parse_table(table, column):
    try:
        column = table.find("p", string=column)
        li = column.find_parent("li")
        value = li.find_all("p")[1].get_text()
        value = clean_text(value)

    except:
        value = ""

    return value


if __name__ == "__main__":
    df = pd.read_csv("urls.csv", header=None)
    urls = df.iloc[:, 0].to_list()

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(scrape, urls))

    data_list = []
    for result in results:
        if result:
            data_list.append(result)

    new_df = pd.DataFrame(data_list)
    new_df.to_csv(
        f"20250803【國政】バイトな女子_{len(new_df)}件.csv",
        index=False,
        encoding="utf-8-sig",
    )
