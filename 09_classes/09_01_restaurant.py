# This is tough and difficulty of 9
class Restaurant:
    """ Model a restaurant with OOP """
    def __init__(self, restaurant_name, cusine_type, location, price_range):
        self.restaurant_name = restaurant_name
        self.cusine_type = cusine_type
        self.location = location
        self.price_range = price_range

    def describe_restaurant (self):
        print (f'The restaurant name is {self.restaurant_name}.')
        print (f'The price is (self.price_range).')

    def can__you_take_a_date(self): 
        if self.price_range < 50:
            print(f"Don't embarrass yourself. It's too expensive!")
        else:
            print(f'You can afford {self.restaurant_name}.')

sh_restaurant = Restaurant("Shawarma House", "Middle Eastern", "Downtown", 30)
sh_restaurant.can__you_take_a_date()