# -------------------------------------------------------
# BASE CLASS
# -------------------------------------------------------

class MenuItem:
    """
    Base class that represents any item on the restaurant menu.
    Every menu item has a name and a price. Subclasses can
    override total_price() to add custom pricing logic
    (e.g. tax, surcharge).
    """

    def __init__(self, name, price):
        """
        Constructor: stores the item name and unit price.

        Parameters:
            name (str):  display name of the item.
            price (float): base price before any adjustments.
        """
        self.name = name
        self.price = price  # base unit price

    def total_price(self):
        """
        Returns the final price for this item.
        Subclasses override this to add surcharges or
        apply category-specific rules.
        """
        return self.price

    def description(self):
        """
        Returns a short human-readable description of the item.
        Subclasses override this to include their extra attributes.
        """
        return f"{self.name} — ${self.price:.2f}"


# SUBCLASS 1: Beverage

class Beverage(MenuItem):
    """
    Represents a drink. Adds two beverage-specific attributes:
      - is_alcoholic: bool — used for discount logic in Order.
      - mls: int     — serving size (informational).

    Alcoholic beverages carry a 10% sin tax on top of the
    base price.
    """

    def __init__(self, name, price, is_alcoholic, mls):
        # Call the parent constructor to set name and price
        super().__init__(name, price)
        self.is_alcoholic = is_alcoholic
        self.mls = mls

    def total_price(self):
        """
        Alcoholic drinks get a 10% sin tax added.
        Non-alcoholic drinks return the base price.
        """
        if self.is_alcoholic:
            alcoholic_tax = self.price * 0.10
            return self.price + alcoholic_tax
        return self.price

    def description(self):
        if self.is_alcoholic:
            type = "alcoholic"
        else:
            type = "non-alcoholic"
        return (
            f"[Beverage] {self.name} ({self.mls}ml, {type})"
            f" — ${self.total_price():.2f}"
        )


# SUBCLASS 2: Appetizer

class Appetizer(MenuItem):
    """
    Represents a starter dish. Extra attributes:
      - is_vegan: bool — for dietry info.
      - portion: str         — e.g. "individual", "to share".

    Shareable appetizers ('to share') get a 15% upcharge
    because they use larger portions.
    """

    def __init__(self, name, price, is_vegan, portion):
        super().__init__(name, price)
        self.is_vegan = is_vegan
        self.portion = portion  # "individual" | "to share"

    def total_price(self):
        """
        Shareable appetizers cost 15% more than the base price
        because they're larger portions.
        """
        if self.portion == "to share":
            return self.price * 1.15
        return self.price

    def description(self):
        # diet = "vegetarian" if self.is_vegan else "non-veg"
        # return (
        #     f"[Appetizer] {self.name} ({self.portion}, {diet})"
        #     f" — ${self.total_price():.2f}"
        # )
        if self.is_vegan:
            diet = "vegetarian"
        else:
            diet = "non-veg"
        return (
            f"[Appetizer] {self.name} ({self.portion}, {diet})"
            f" — ${self.total_price():.2f}"
        )

# SUBCLASS 3: MainCourse

class MainCourse(MenuItem):
    """
    Represents a main dish. Extra attributes:
      - protein: str            — type of protein (chicken, beef…).
      - has_garnish: bool — whether a side dish is included.

    Dishes that include a side dish get $2.50 added to
    the base price (side costs reflected transparently).
    """

    def __init__(self, name, price, protein, has_garnish):
        super().__init__(name, price)
        self.protein = protein
        self.has_garnish = has_garnish

    def total_price(self):
        """
        Add $2.50 for side dishes that are included.
        """
        # cost_garnish = 2.50 if self.has_garnish else 0
        # return self.price + cost_garnish
        if self.has_garnish:
            cost_garnish = 2.50
        else:
            cost_garnish = 0
        return self.price + cost_garnish

    def description(self):
        if self.has_garnish:
            garnish = "with side"
        else:
            garnish = "no side"
        return (
            f"[Main] {self.name} ({self.protein}, {garnish})"
            f" — ${self.total_price():.2f}"
        )


# ORDER CLASS

class Order:
    """
    Represents a customer's order for one table.
    Holds a list of MenuItem objects.
    """

    def __init__(self, table_number):
        """
        Constructor: initializes an empty order for a given table.

        Parameters:
            table_number (int): table number, for display purposes.
        """
        self.table_number = table_number
        # This list will hold all MenuItem (or subclass) objects
        self.items = []

    def add_item(self, item):
        """
        Adds a MenuItem (or subclass instance) to the order.

        Parameters:
            item (MenuItem): the item to add.
        """
        if not isinstance(item, MenuItem):
            print(f"Error: '{item}' is not a valid menu item.")
            return
        self.items.append(item)
        print(f"  Added: {item.name}")

    def _count_MainCourse(self):
        """Helper: counts how many MainCourse items are in the order."""
        counter = 0
        for item in self.items:
            if isinstance(item, MainCourse):
                counter += 1
        return counter

    def _count_Beverage(self):
        """Helper: counts how many alcoholic Beverage items are in the order."""
        counter = 0
        for item in self.items:
            if isinstance(item, Beverage) and item.is_alcoholic:
                counter += 1
        return counter

    def total(self):
        """
        Calculates the bill by Summing total_price() for each item.
        Returns:
            float: final amount to pay.
        """
        subtotal = 0
        for item in self.items:
            subtotal += item.total_price()

        total_final = subtotal 

        return total_final

    def show_bill(self):
        """
        Prints the full itemized bill to the console,
        including applied discounts and the final total.
        """
        print("\n" + "=" * 55)
        print(f"  TABLE {self.table_number} — BILL")
        print("=" * 55)

        if not self.items:
            print("  No items ordered yet.")
            return

        # Print each item
        for item in self.items:
            print(f"  {item.description()}")

        # Print final total
        print("-" * 55)
        total = self.total()
        print(f"  {'TOTAL':44s} ${total:.2f}")
        print("=" * 55)


# -------------------------------------------------------
# MENU —  (used as the restaurant's catalog)
# -------------------------------------------------------

def build_menu():
    """
    Creates and returns a dictionary with all available
    menu items grouped by category.
    """
    menu = {
        # --- Beverages ---
        "mineral_water":    Beverage("Sparkling water",      2.50, False, 500),
        "lemonade":         Beverage("Lemonade",             3.80, False, 400),
        "craft_beer":       Beverage("Craft beer",           6.50, True,  330),
        "red_wine_glass":   Beverage("Red wine (glass)",     8.00, True,  150),

        # --- Appetizers ---
        "ceviche":          Appetizer("Ceviche",             9.50, False, "individual"),
        "cheese_board":     Appetizer("Cheese board",       14.00, True,  "to share"),
        "calamari":         Appetizer("Fried calamari",     10.50, False, "to share"),

        # --- Main courses ---
        "salmon_grill":     MainCourse("Grilled salmon",    22.00, "fish",    True),
        "beef":             MainCourse("Beef tenderloin",   28.00, "beef",    True),
        "chicken_marsala":  MainCourse("Chicken marsala",   18.50, "chicken", True),
        "risotto_funghi":   MainCourse("Mushroom risotto",  16.00, "none",    False),
        "pasta_carbonara":  MainCourse("Pasta carbonara",   15.50, "pork",    False),
    }
    return menu


# -------------------------------------------------------
# Test
# -------------------------------------------------------


menu = build_menu()

# ----- Order 1
print("\n>>> Building order for table 4...")
table_order4 = Order(table_number=4)
table_order4.add_item(menu["craft_beer"])
table_order4.add_item(menu["red_wine_glass"])
table_order4.add_item(menu["cheese_board"])
table_order4.add_item(menu["salmon_grill"])
table_order4.add_item(menu["beef"])
table_order4.add_item(menu["chicken_marsala"])
table_order4.show_bill()
# ----- Order 2
print("\n>>> Building order for table 2...")
table_order2 = Order(table_number=2)
table_order2.add_item(menu["lemonade"])
table_order2.add_item(menu["ceviche"])
table_order2.add_item(menu["risotto_funghi"])
table_order2.show_bill()
# ----- Order 3
print("\n>>> Building order for table 7...")
table_order7 = Order(table_number=7)
table_order7.add_item(menu["craft_beer"])
table_order7.add_item(menu["red_wine_glass"])
table_order7.add_item(menu["calamari"])
table_order7.add_item(menu["pasta_carbonara"])
table_order7.show_bill()