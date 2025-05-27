# Part responsible for addresses
class Address:
    def __init__(self, city, street, apartment, postal_code):
        self.city = city
        self.street = street
        self.apartment = apartment
        self.postal_code = postal_code

    def __str__(self):
        return f"{self.street} {self.apartment}, {self.postal_code} {self.city}"