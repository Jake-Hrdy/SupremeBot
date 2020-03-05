import requests
import bs4
from splinter import Browser
import information

class SupremeBot:
    def __init__(self, **info):
        self.base = "http://supremenewyork.com/"
        self.shop_ext = "shop/all/"
        self.checkout_ext = "checkout/"
        self.info = info

    def init_browser(self):
        self.browser = Browser("chrome")

    def find_product(self):
        try:
            req = requests.get("{}{}{}".format(self.base, self.shop_ext, self.info["category"])).text   # sends back html of page
            soup = bs4.BeautifulSoup(req, "lxml")   # allows us to work with html better
            
            temp_link = []      # list of links that either had product name or color (should only be one element after loop)
            for link in soup.find_all("a", href=True):
                if link.text == self.info["product"] or link.text == self.info["color"]:
                    temp_link.append(link["href"])

            self.final_link = list(set([x for x in temp_link if temp_link.count(x) == 2]))[0]

            return True
        except:
            False

    def visit_site(self):
        try:
            self.browser.visit("{}{}".format(self.base, self.final_link))   # go to item page
            if self.info["size"] != "":
                self.browser.find_option_by_text(self.info["size"]).click() # select correct size
            self.browser.find_by_xpath("/html/body/div/div/div[2]/div/form[2]/div/fieldset[1]/input").click() # add to cart
            return True
        except:
            print("Could not add to cart.")
            return False

    def checkout(self):
        try:
            self.browser.visit("{}{}".format(self.base, self.checkout_ext)) # go to checkout page

            # fill out order form
            self.browser.fill("order[billing_name]", self.info["namefield"])
            self.browser.fill("order[email]", self.info["emailfield"])
            self.browser.fill("order[tel]", self.info["phonefield"])

            self.browser.fill("order[billing_address]", self.info["addressfield"])
            self.browser.fill("order[billing_address_2]", self.info["apt"])
            self.browser.fill("order[billing_zip]", self.info["zip"])
            self.browser.fill("order[billing_city]", self.info["city"])
            self.browser.select("order[billing_state]", self.info["state"])
            self.browser.select("order[billing_country]", self.info["country"])

            self.browser.fill("riearmxa", self.info["number"])
            self.browser.select("credit_card[month]", self.info["month"])
            self.browser.select("credit_card[year]", self.info["year"])
            self.browser.fill("credit_card[meknk]", self.info["ccv"])

            # check the terms and conditions and complete order
            self.browser.find_by_css(".terms").click()
            # self.browser.find_by_value("process payment").click()

            print(info["product"] + " has been purchased.")
        except:
            print("Could not checkout.")


if __name__ == "__main__":
    info = {
        "product":      information.product,
        "color":        information.color,
        "size":         information.size,
        "category":     information.category,
        "namefield":    information.namefield,
        "emailfield":   information.emailfield,
        "phonefield":   information.phonefield,
        "addressfield": information.addressfield,
        "apt":          information.apt,
        "zip":          information.zip,
        "city":         information.city,
        "state":        information.state,
        "country":      information.country,
        "number":       information.number,
        "month":        information.month,
        "year":         information.year,
        "ccv":          information.ccv
    }

    bot = SupremeBot(**info)    # initialize bot
    # ================================================================================
    ''' This will allow you to start the bot right before a drop, so that it will find
        the product as soon as it's available '''
    found_product = False
    max_iter = 20
    counter = 0
    while not found_product and counter < max_iter:
        found_product = bot.find_product()
        counter += 1

    if counter == 1:
        print("Tried ", counter, " time to find product.")
    else:
        print("Tried ", counter, " times to find product.")

    if not found_product:
        # product was never found in the while loop
        raise Exception("Product couldn't be found.")
    # ================================================================================
    # continue because we found the product
    bot.init_browser()
    if bot.visit_site():
        bot.checkout()