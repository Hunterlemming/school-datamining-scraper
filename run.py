from packages.drivers import initialize_chrome_driver, disconnect
from packages.jofogas.index import scrape_jofogas


if __name__ == "__main__":
    initialize_chrome_driver()
    scrape_jofogas()
    disconnect()
    print("All Done!")
