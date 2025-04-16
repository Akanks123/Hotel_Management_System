import pandas as pd

# Read the hotel and card data
df = pd.read_csv("hotels.csv", dtype={"id": str})
df_cards = pd.read_csv("cards.csv", dtype=str).to_dict(orient='records')


class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()
        self.price = float(df.loc[df["id"] == self.hotel_id, "price"].squeeze())

    def book(self):
        """Book a hotel by changing its availability to no"""
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)

    def available(self):
        """Check if the hotel is available"""
        availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        return availability == "yes"


class ReservationTicket:
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object

    def generate(self):
        content = f"""
        Thank you for your reservation! 
        Here are your booking details:
        Name: {self.customer_name} 
        Hotel name: {self.hotel.name}
        """
        return content


class CreditCard:
    def __init__(self, number):
        self.number = number

    def validate(self, expiration, holder, cvc):
        if any(self.number == str(card["number"]) for card in df_cards):
            return True
        else:
            return False


class Bill:
    def __init__(self, hotel_object, nights=1):
        self.hotel = hotel_object
        self.nights = nights

    def calculate_total(self):
        return self.hotel.price * self.nights

    def generate_receipt(self):
        total = self.calculate_total()
        return f"Total bill for {self.nights} night(s) at {self.hotel.name}: ${total:.2f}"


# Main flow
print(df)
hotel_ID = input("Enter the id of the hotel: ")
hotel = Hotel(hotel_ID)

if hotel.available():
    credit_card = CreditCard(number='1234')
    if credit_card.validate(expiration="12/26", holder="JOHN SMITH", cvc="123"):
        nights = int(input("How many nights would you like to stay? "))
        bill = Bill(hotel_object=hotel, nights=nights)
        print(bill.generate_receipt())
        confirm = input("Do you want to proceed with the booking? (yes/no): ").lower()

        if confirm == "yes":
            hotel.book()
            name = input("Enter your name: ")
            reservation_ticket = ReservationTicket(customer_name=name, hotel_object=hotel)
            print(reservation_ticket.generate())
        else:
            print("Booking cancelled.")
    else:
        print("There was a problem with your payment.")
else:
    print("Hotel is not available.")
