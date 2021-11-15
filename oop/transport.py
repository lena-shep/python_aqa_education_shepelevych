import datetime


class Transport:
    def __init__(self, name, fuel, consumption, *kwargs):
        self.name = name
        self.fuel = fuel
        self.consumption = consumption

    def str(self):
        return f"For the {self.name} fuel is {self.fuel}, consumption is {self.consumption} l/100 km."

    def production_date(self):
        d = input("Fill the production date of the transport in format yyyy, mm, dd: ")
        year, month, day = map(int, d.split(','))
        p_date = datetime.date(year, month, day)
        if p_date.year < 2000:
            print(f"Production date of the {self.name} is {p_date.year}. Time to recycle." "\n")
        else:
            print(f"Production date of the {self.name} is {p_date.year}. Can be used" "\n")

    def __bool__(self):
        return self.fuel == "electricity"

    def calculate_fuel_litres(method_to_decorate):
        """decorator - calculate required litres of the fuel for the trip (km)"""
        def wrapper(self, distance):
            print("Congratulation! You are going to the trip.")
            return method_to_decorate(self, distance)
        return wrapper

    @calculate_fuel_litres
    def print_litres_for_trip(self, distance):
        litres_for_trip = distance * self.consumption / 100
        print("For your trip with the consumption %d l/ 100km and distance %d you need %d l of the %s." "\n" % (self.consumption, distance, litres_for_trip, self.fuel))


class FreightTransport(Transport):
    def __init__(self, name, fuel, consumption, length, width, height):
        Transport.__init__(self, name, fuel, consumption)
        self.length = length
        self.width = width
        self.height = height
        self.volume = None

    def calculate_volume(self):
        self.volume = self.length * self.width * self.height
        return f"The volume of admissible transportation is {self.volume} m3."

    def __ge__(self, other):
        return self.volume >= other


class PassengersTransport(Transport):
    def __init__(self, name, fuel, consumption, capacity):
        Transport.__init__(self, name, fuel, consumption)
        self.capacity = capacity

    def __le__(self, other):
        return self.capacity <= other

    @staticmethod
    def print_trunk_volume(trunk_volume):
        print("Volume of the trunk is %d l" % trunk_volume)


class AirTransport(PassengersTransport):
    def __init__(self, name, fuel, consumption, capacity, altitude):
        PassengersTransport.__init__(self, name, fuel, consumption, capacity)
        self.altitude = altitude

    def transport_speed(self):
        return str(f"Altitude of the {self.name} is {self.altitude} km/h.")

    def str(self):
        super().str()
        return f"For the  air transport {self.name} fuel is {self.fuel}, consumption is {self.consumption} l/100 km."


class LandTransport(PassengersTransport):
    def __init__(self, name, fuel, consumption, capacity, wheels):
        PassengersTransport.__init__(self, name, fuel, consumption, capacity)
        self.wheels = wheels

    def str(self):
        super().str()
        return f"For the land transport {self.name} fuel is {self.fuel}, consumption is {self.consumption} l/100 km."


class WaterTransport(FreightTransport):
    def __init__(self, name, fuel=None, consumption=None, length=None, width=None, height=None, depth=None):
        FreightTransport.__init__(self, name, fuel, consumption, length, width, height)
        self.depth = depth

    @property
    def consumption_to_miles(self):
        """For the water transport system shows consumption in miles instead of km"""
        return self.consumption * 1.609


class AirCar(AirTransport, LandTransport):
    def __init__(self, name, fuel, consumption, capacity, altitude=None, wheels=None):
        AirTransport.__init__(self, name, fuel, consumption, capacity, altitude)
        LandTransport.__init__(self, name, fuel, consumption, capacity, wheels)


class Engine(WaterTransport, AirTransport, LandTransport):
    def __init__(self, name, fuel, consumption, length=None, width=None, height=None, depth=None, capacity=None, altitude=None, wheels=None):
        WaterTransport.__init__(self, name, fuel, consumption, length, width, height, depth)
        AirTransport.__init__(self, name, fuel, consumption, capacity, altitude)
        LandTransport.__init__(self, name, fuel, consumption, capacity, wheels)

    def __call__(self, price):
        return f"Price for the fuel required for 100km is {self.consumption * price} uah"


engine = Engine(name="engine", fuel="diesel", consumption=12)
print(engine.__dict__)

# magic method __call__
print(engine(6))


air_car = AirCar("AirCar", "petrol", 12, 4, 2500, 4)
print(air_car.__dict__, "\n")
print(air_car.str(), "\n")

# calculate how much fuel we need for the trip distance 2700km
air_car.print_litres_for_trip(2700)

# check if transport is eco or not (magic method __bool__)
if air_car.__bool__():
    print("%s is eco transport" "\n" % air_car.name)

# print required class of the driver's licence depending on number of passengers in the transport (magic method __le__)
if air_car.__le__(8):
    print("You need driver's license class B")
else:
    print("You need driver's license class D")

# method ask user about the production year and check if it's time to recycle or not"
# air_car.production_date()

# here I check how the @property works
yacht = WaterTransport(name="Yacht", fuel="petrol", consumption=10, length=5, width=3, height=3)
print(yacht.consumption)
yacht.consumption = 14
print(yacht.consumption_to_miles)

# magic method __ge__
yacht.calculate_volume()
print(yacht.volume)
if yacht.__ge__(30):
    print("It's enough volume")
else:
    print("Not enough volume")

# just to check how the @staticmethod works
air_car.print_trunk_volume(150)

