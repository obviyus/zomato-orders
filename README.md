# zomato-orders

Scripts to pull your Zomato order history

## Instructions

For this script to work, you'll need the following cookies from your Zomato session:
- `cid`
- `PHPSESSID`
- `zat`

To get these, login to your Zomato account on the website and open the developer console (press F12). Go to the Application Tab and look for the Cookies section on the left. Copy the values for the cookies mentioned above and paste them in the `main.py` file.

Video instructions:

# TODO: Add video instructions

## Usage

Install dependencies using poetry:
```bash
poetry install
```

Run the script:
```bash
poetry run python main.py
```

All the parsed order information will be saved in a SQLite database named `zomato_orders.db` in the current directory.

## Contributing

I whipped this up in a couple of minutes so there's definitely some rough edges. I'd also like to do some analysis on the order data so if you have any ideas, feel free to open an issue or a pull request.
