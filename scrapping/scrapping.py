import requests
from bs4 import BeautifulSoup

from schemas import Banner, BannerGroup, Interval
from utils import parse_timestamp


def scrap_global_banners():
    url = "https://bluearchive.wiki/wiki/Banner_List_(Global)"
    return _scrap_banners(url)


def scrap_japan_banners():
    url = "https://bluearchive.wiki/wiki/Banner_List"
    return _scrap_banners(url)


def _scrap_banners(url: str):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.select("table")[0]

    banner_groups: list[BannerGroup] = []

    for row in table.select("tbody tr"):
        tds = row.select("td")
        if len(tds) < 3:
            continue

        image_td, characters_td, period_td = tds

        # период
        start_raw, end_raw = period_td.text.split(" — ")
        interval = Interval(start=parse_timestamp(start_raw), end=parse_timestamp(end_raw))

        # создать или получить информацию о баннере
        banner_group = next((group for group in banner_groups if group.interval == interval), None)

        if not banner_group:
            characters_td_content = characters_td.text.lower()

            banner_group = BannerGroup(index=len(banner_groups), is_limited=False, is_fest=False, interval=interval)
            banner_groups.append(banner_group)

        # теги
        if "limited" in row["class"]:
            banner_group.is_limited = True

        if "anniversary" in characters_td_content or "festival" in characters_td_content:
            banner_group.is_fest = True

        # получить информацию о баннере
        banner = Banner(image_url="")
        banner_group.banners.append(banner)

        # ссылка на изображение
        if img := image_td.select_one("img"):
            banner.image_url = str(img["src"])

        # список персонажей
        if includes := characters_td.select_one("i"):
            includes.decompose()

        links = characters_td.select("a")
        for link in links:
            name = str(link["title"])
            banner.characters.append(name)

    return banner_groups
