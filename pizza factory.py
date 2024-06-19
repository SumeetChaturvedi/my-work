
class Pizza:
    def __init__(self, name, sizes):
        self.name = name
        self.sizes = sizes 
        self.toppings = []
        self.crust = None

class Topping:
    def __init__(self, name, price, is_veg):
        self.name = name
        self.price = price
        self.is_veg = is_veg

class Side:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class Order:
    def __init__(self):
        self.pizzas = []
        self.sides = []
        self.total_amount = 0

    def calculate_total(self):
        self.total_amount = sum(pizza.sizes[pizza.size] + sum(topping.price for topping in pizza.toppings) for pizza in self.pizzas) + sum(side.price for side in self.sides)
        return self.total_amount
class Inventory:
    def __init__(self):
        self.pizzas = []
        self.toppings = []
        self.sides = []

    def add_pizza(self, pizza):
        self.pizzas.append(pizza)

    def add_topping(self, topping):
        self.toppings.append(topping)

    def add_side(self, side):
        self.sides.append(side)

#implementing the service
class PizzaFactoryService:
    def __init__(self):
        self.inventory = Inventory()

    def add_pizza_to_menu(self, name, sizes):
        pizza = Pizza(name, sizes)
        self.inventory.add_pizza(pizza)

    def add_topping_to_menu(self, name, price, is_veg):
        topping = Topping(name, price, is_veg)
        self.inventory.add_topping(topping)

    def add_side_to_menu(self, name, price):
        side = Side(name, price)
        self.inventory.add_side(side)

    def place_order(self, order):
        if self.validate_order(order):
            order.calculate_total()
            return order
        else:
            raise ValueError("Order validation failed")

    def validate_order(self, order):
        for pizza in order.pizzas:
            if pizza.size == "Large" and len(pizza.toppings) > 2:
                return False
            if pizza.name.startswith("Veg") and any(not topping.is_veg for topping in pizza.toppings):
                return False
            if pizza.name.startswith("Non-Veg") and any(topping.name == "Paneer" for topping in pizza.toppings):
                return False
        return True
#business rules and unit tests
import unittest

class TestPizzaFactoryService(unittest.TestCase):
    def setUp(self):
        self.service = PizzaFactoryService()
        self.service.add_pizza_to_menu("Deluxe Veggie", {"Regular": 150, "Medium": 200, "Large": 325})
        self.service.add_topping_to_menu("Black Olive", 20, True)
        self.service.add_side_to_menu("Cold Drink", 55)

    def test_order_placement(self):
        order = Order()
        pizza = self.service.inventory.pizzas[0]
        pizza.size = "Regular"
        pizza.toppings.append(self.service.inventory.toppings[0])
        order.pizzas.append(pizza)
        order.sides.append(self.service.inventory.sides[0])
        total = order.calculate_total()
        self.assertEqual(total, 150 + 20 + 55)

    def test_order_validation(self):
        order = Order()
        pizza = self.service.inventory.pizzas[0]
        pizza.size = "Large"
        pizza.toppings.append(self.service.inventory.toppings[0])
        pizza.toppings.append(self.service.inventory.toppings[0])
        pizza.toppings.append(self.service.inventory.toppings[0])
        order.pizzas.append(pizza)
        with self.assertRaises(ValueError):
            self.service.place_order(order)

if __name__ == '__main__':
    unittest.main()

