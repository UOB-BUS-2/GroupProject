import datetime

class User:
    def __init__(self, username):
        self.username = username
        self.logged_meals = []

class Meal:
    def __init__(self, carb, protein, veg):
        self.carb = carb
        self.protein = protein
        self.veg = veg
        self.total_emissions = None
        self.date_added = datetime.date.today()

    def calculate_emissions(self):
        # find emissions numbers from csv file
        # self.total_emissions = carb_emissions + protein_emissions + veg_emissions
        pass

    def get_qualitative_impact(self):
        # match self.total_emissions:
            # case < 10:
                # return "very_low"
            # case 10 < x < 20:
                # return "low"
            # case ...
        pass

    def calculate_equivalent_miles(self):
        # car_miles = 15 * self.total_emissions
        # return car_miles
        pass