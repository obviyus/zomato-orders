from time import sleep
import dateparser
import requests
import sqlite3

ORDERS_ENDPOINT = "https://www.zomato.com/webroutes/user/orders"
ZOMATO_COOKIES = {
    "cid": "", # Paste your Zomato cid here
    "PHPSESSID": "", # Paste your PHPSESSID here
    "zat": "", # Paste your zat cookie here
}

COOKIE = "; ".join([f"{key}={value}" for key, value in ZOMATO_COOKIES.items()])


DATABASE_NAME = "zomato_orders.sqlite"
TABLE_NAME = "orders"

conn = sqlite3.connect(DATABASE_NAME)
conn.row_factory = sqlite3.Row

c = conn.cursor()
c.execute(
    """
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY,
        total_cost INTEGER,
        order_time INTEGER,
        restaurant_id INTEGER,
        restaurant_name TEXT,
        establishment TEXTgit chec
    );
    """
)


def get_orders(page: int):
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'cookie': COOKIE,
        'dnt': '1',
        'pragma': 'no-cache',
        'referer': 'https://www.zomato.com/',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    }

    params = (
        ('page', page),
    )

    response = requests.get(ORDERS_ENDPOINT, headers=headers, params=params).json()
    orders = []

    for order in response["entities"]["ORDER"].values():
        print(order["orderId"], order["totalCost"], order["orderDate"], order["resInfo"]["name"] )
        try:
          normalized_cost = int(order["totalCost"].replace("\u20b9", "").replace("₹", "").replace(".", "").replace(",", "") )
          parsed_time = dateparser.parse(order["orderDate"])
        except Exception as e:
          print(e)
          continue

        orders.append({
            "order_id": order["orderId"],
            "total_cost": normalized_cost,
            "order_time": parsed_time.timestamp(),
            "restaurant_id": order["resInfo"]["id"],
            "restaurant_name": order["resInfo"]["name"],
            "establishment": order["resInfo"]["establishment"][0] if len(order["resInfo"]["establishment"]) > 0  else ""
        })

    return orders


def insert_orders(orders):
    for order in orders:
        c.execute(
            f"""
            INSERT INTO {TABLE_NAME} (
                order_id,
                total_cost,
                order_time,
                restaurant_id,
                restaurant_name,
                establishment
            )
            VALUES (
                :order_id,
                :total_cost,
                :order_time,
                :restaurant_id,
                :restaurant_name,
                :establishment
            )
            ON CONFLICT (order_id) DO UPDATE SET
                total_cost = :total_cost,
                order_time = :order_time,
                restaurant_id = :restaurant_id,
                restaurant_name = :restaurant_name,
                establishment = :establishment
            """,
            order
        )

    conn.commit()


def get_all_orders():
    page = 1
    while True:
        orders = get_orders(page)
        if len(orders) == 0:
            break
        insert_orders(orders)
        print(f"Page {page} done")
        page += 1
        sleep(1)


get_all_orders()
