import requests
import bs4
from splinter import Browser

class SupremeBot:
    def __init__(self, **info):
        self.base = "http://supremenewyork.com/"
        self.shop_ext = "shop/all/"
        self.checkout_ext = "checkout/"
        self.info = info

    def init_browser(self):
        self.browser = Browser()    # fix for chrome eventually?

    def find_product(self):
        req = requests.get("{}{}{}".format(self.base, self.shop_ext, self.info["category"])).text   # sends back html of page
        soup = bs4.BeautifulSoup(req, "lxml")   # allows us to work with html better

        temp_link = []      # list of links that either had product name or color (should only be one element after loop)
        for link in soup.find_all("a", href=True):
            if link.text == self.info["product"] or link.text == self.info["color"]:
                temp_link.append(link["href"])

        self.final_link = temp_link[0]
        print(self.final_link)


if __name__ == "__main__":
    info = {
        # "driver": "geckodriver",
        "product": "Miles Davis Hooded Sweatshirt",
        "color": "Blue",
        "size": "Large",
        "category": "sweatshirts",
        "namefield": "example",
        "emailfield": "example@example.com",
        "phonefield": "XXXXXXXXXX",
        "addressfield": "example road",
        "city": "example",
        "zip": "72046",
        "country": "GB",
        "card": "visa",
        "number": "1234123412341234",
        "month": "09",
        "year": "2020",
        "ccv": "123"
    }

    bot = SupremeBot(**info)
    bot.find_product()