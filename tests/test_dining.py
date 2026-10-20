import httpx
from fastapi.testclient import TestClient

from app.main import app
from app.services.dining import get_station_items

client = TestClient(app)

html = """
<button aria-controls="tabinfo-2">
    <div>Lunch (11am-3pm)</div>
</button>

<div id="tabinfo-2">
    <div class="menu-station">
        <button class="toggle-menu-station-data">
            The Kitchen Table
        </button>

        <ul>
            <li class="menu-item-li">
                <a>Chicken</a>
            </li>
            <li class="menu-item-li">
                <a>Rice</a>
            </li>
        </ul>
    </div>
</div>
"""

def test_get_station_items():
    result = get_station_items(html, "The Kitchen Table")

    assert result == ["Chicken", "Rice"]


def test_get_station_items_missing_station():
    result = get_station_items(html, "Fake Station")

    assert result == []

def test_lunch_unavailable(monkeypatch):
    def fake_get_lunch_menu():
        raise httpx.HTTPError("UNC Dining is down")
    
    monkeypatch.setattr(
        "app.main.get_lunch_menu",
        fake_get_lunch_menu,
    )

    response = client.get("/dining/lunch")

    assert response.status_code == 503
    assert response.json() == {
        "detail": "UNC Dining service is currently unavailable"
    }
