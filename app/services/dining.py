import httpx
from bs4 import BeautifulSoup

LENOIR_URL = "https://dining.unc.edu/locations/top-of-lenoir/"
STATIONS = [
    "The Kitchen Table",
    "Simply Prepared",
    "The Grill"
]

def fetch_menu_page() -> str:
    response = httpx.get(LENOIR_URL)
    response.raise_for_status()
    return response.text

def get_station_items(html: str, station_name: str):
    soup = BeautifulSoup(html, "html.parser")

    # Isolate Lunch

    lunch_div = soup.find(
        "div",
        string=lambda text: text is not None and "Lunch" in text,
    )
    if lunch_div is None:
        return []

    lunch_button = lunch_div.parent
    if lunch_button is None:
        return []
    
    lunch_section_id = lunch_button.get("aria-controls")
    if lunch_section_id is None:
        return []
    
    lunch_section = soup.find(id=lunch_section_id)
    if lunch_section is None:
        return []

    # Isolate menu items

    station_button = lunch_section.find(
        "button",
        class_="toggle-menu-station-data",
        string=lambda text: text is not None and station_name in text,
    )

    if station_button is None:
        return []
    
    station_div = station_button.parent

    if station_div is None:
        return []
    
    items = station_div.find_all("li", class_="menu-item-li")

    item_names = []

    for item in items:
        link = item.find("a")

        if link is not None:
            item_names.append(link.get_text(strip=True))

    return item_names


def get_lunch_menu() -> dict[str, list[str]]:
    html = fetch_menu_page()
    res = dict()
    for station in STATIONS:
        res[station] = get_station_items(html, station)
    return res