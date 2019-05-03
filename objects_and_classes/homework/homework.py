import random
import string
import uuid
from typing import List
from constants import CARS_TYPES
from constants import CARS_PRODUCER
from constants import TOWNS

"""
Вам небхідно написати 3 класи. Колекціонери Гаражі та Автомобілі.
Звязкок наступний один колекціонер може мати багато гаражів.
В одному гаражі може знаходитися багато автомобілів.
Автомобіль має наступні характеристики:
    price - значення типу float. Всі ціни за дефолтом в одній валюті.
    type - одне з перечисленних значеннь з CARS_TYPES в docs.
    producer - одне з перечисленних значеннь в CARS_PRODUCER.
    number - значення типу UUID. Присвоюється автоматично при створенні автомобілю.
    mileage - значення типу float. Пробіг автомобіля в кілометрах.
    Автомобілі можна перівнювати між собою за ціною.
    При виводі(logs, print) автомобілю повинні зазначатися всі його атрибути.
    Автомобіль має метод заміни номеру.
    номер повинен відповідати UUID
Гараж має наступні характеристики:
    town - одне з перечислениз значеннь в TOWNS
    cars - список з усіх автомобілів які знаходяться в гаражі
    places - значення типу int. Максимально допустима кількість автомобілів в гаражі
    owner - значення типу UUID. За дефолтом None.
    Повинен мати реалізованими наступні методи
    add(car) -> Добавляє машину в гараж, якщо є вільні місця
    remove(cat) -> Забирає машину з гаражу.
    hit_hat() -> Вертає сумарну вартість всіх машин в гаражі
Колекціонер має наступні характеристики
    name - значення типу str. Його ім'я
    garages - список з усіх гаражів які належать цьому Колекціонеру. Кількість гаражів за замовчуванням - 0
    register_id - UUID; Унікальна айдішка Колекціонера.
    Повинні бути реалізовані наступні методи:
    hit_hat() - повертає ціну всіх його автомобілів.
    garages_count() - вертає кількість гаріжів.
    сars_count() - вертає кількість машиню
    add_car() - додає машину у вибраний гараж. Якщо гараж не вказаний, то додає в гараж, де найбільше вільних місць.
    Якщо вільних місць немає повинне вивести повідомлення про це.
    Колекціонерів можна порівнювати за ціною всіх їх автомобілів.
"""

class Car:

    def __init__(self, price, type, producer, mileage):
        self.price = price
        self.type = type
        self.producer = producer
        self.mileage = mileage
        self.number = uuid.uuid4()


    def __str__(self):
        return f"Car produser: {self.producer}, type: {self.type}, number: {self.number}, price: {self.price}, spend mileage: {self.mileage}"

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        return self

    def __next__(self):

        if self.current < len(self.cars):
            res = self.cars[self.current]
            self.current += 1
            return res
        else:
            self.current = 0
            raise StopIteration

    def __le__(self, other):
        return self.price <= other.price

    def __lt__(self, other):
        return self.price < other.price

    def __eq__(self, other):
        return self.price == other.price

    def __ne__(self, other):
        return self.price != other.price

    def change_UUID(self):
        self.number = uuid.uuid4()
        return self.number

class Garage:

    garage_cars: List[Car]

    def __init__(self, town, places, garage_cars,  owner=None):
        self.town = town
        self.places = places
        self.cars = garage_cars if garage_cars is not None else []
        self.owner = owner
        self.current = 0

    def __str__(self):
        all_cars = "".join(str(item) for item in self.cars)
        return f"Town: {self.town}, Places: {self.places}, car: {self.cars} ,owner: {self.owner}"

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        return self

    def __next__(self):

        if self.current < len(self.cars):
            res = self.cars[self.current]
            self.current += 1
            return res
        else:
            self.current = 0
            raise StopIteration

    def add(self,new_car):
        if len(self.cars) < self.places:
            self.cars.append(new_car)
            return self
        else:
            return f"Garage haven't got any free places"


    def remove(self,my_car):
        if my_car in self.cars:
            self.cars.remove(my_car)
            print('THE CAR {} WAS DELETED'.format(my_car))
        return self

    def hit_hat(self):
        return sum(car.price for car in self.cars)


class Cesar:

    cesar_garages: List[Garage]

    def __init__(self, name, cesar_garages = 0):
        self.name = name
        self.cesar_garages = cesar_garages if cesar_garages is not None else []
        self.register_id = uuid.uuid4()

    def __str__(self):
        all_garages = "".join(str(item) for item in self.cesar_garages)
        return f"Name: {self.name}, Garage: {self.cesar_garages}, Register_id: {self.register_id}"


    def hit_hat(self):
        return sum(item.hit_hat() for item in self.cesar_garages)

    def garages_count(self):
        return len(self.cesar_garages)

    def сars_count(self):
        return sum(len(garage.cars) for garage in self.cesar_garages)


    def add_car(self, car, garage = None):
        new_car_max_free_garage = 0
        if garage == None:
            return max(self.cesar_garages, key = lambda x:(x.places-len(x.cars))).add(car)
        else:
            return garage.add(car)



if __name__ == "__main__":

    cars = []
    for _ in range(random.randint(10,100)):
        car = Car(price=random.uniform(100.5,999.5),
                   type=random.choice(CARS_TYPES),
                   producer=random.choice(CARS_PRODUCER),
                   mileage=random.uniform(0, 1000000),
                   )
        cars.append(car)

    car1 = Car(price=random.uniform(100.5,999.5),
           type=random.choice(CARS_TYPES),
            producer=random.choice(CARS_PRODUCER),
            mileage=random.uniform(0, 1000000),
            )
    car2 = Car(price=random.uniform(100.5,999.5),
           type=random.choice(CARS_TYPES),
            producer=random.choice(CARS_PRODUCER),
            mileage=random.uniform(0, 1000000),
            )

    print ("CAR1: ", car1)
    print ("CAR2: ", car2)

#CHECK UUID CHANGE
    print ("------CHECK UUID CHANGE--------")
    old_number = car1.number
    car1.number = car1.change_UUID()
    print("Change car number:",  car1.number)
    print("The number {} of car {} was changed on: {}".format(old_number, car1.producer, car1.number))

#CHECK COMPARE
    print ("-----CHECK COMPARE-------")
    if car1.price <= car2.price:
        print("price {} car {} biggest then price {} car {}".format(car2.price, car2.producer, car1.price, car1.producer))
    else:
        print("price {} car {} biggest then price {} car {}".format(car1.price, car1.producer, car2.price, car2.producer))

    if car1.price < car2.price:
        print("car {} price {} cheaper then car {} price {}".format(car1.producer, car1.price, car2.producer, car2.price))
    else:
        print("car {} cheaper then car {}".format(car2.producer, car1.producer))


    if car1.price == car2.price:
        print("price {} car {} is equal to price {} car {}".format(car1.price, car1.producer, car2.price, car2.producer))
    else:
        print("Bad compare")

    if car1.price != car2.price:
        print("price car {} isn't equal to price car {}".format(car1.producer, car2.producer))
    else:
       print("Bad compare")

#CHECK GARAGE
    print ("-----CHECK GARAGE------")
    garages = []

    for _ in range(random.randint(1, 3)):
        count_cars = random.randint(1, 2)
        random_place = random.randint(0,3)

        get_car = []

        for i in random.sample(cars,count_cars):
            if i not in get_car:
                cars.remove(i)
                get_car.append(i)

            if count_cars > random_place:
                raise ValueError("Count cars more then count place. RUN PGOGRAM AGAIN")
            else:
                garage = Garage(town = random.choice(TOWNS),
                                places = random_place,
                                garage_cars = get_car )
                garages.append(garage)
                print(garage)
                print("COUNT CARS: ", len(get_car))
                print("COUNT PLACE: ", random_place)
                print("PRICE ALL CAR IN GARAGES: ", garage.hit_hat())
        #print (garage)

    print("BEFORE ADD NEW CAR: ", garages[0])
    print("PRICE ALL CARS IN GARAGE BEFORE ADD CAR: ", garages[0].hit_hat())

    print("AFTER ADD NEW CAR: ", garages[0].add(car1))
    print("PRICE ALL CARS IN GARAGE AFTER ADD CAR: ", garages[0].hit_hat())

    print("BEFORE REMOVE NEW CAR: ", garages[0])
    print("CAR FOR REMOVE: ", garages[0].cars[0])
    print("AFTER REMOVE NEW CAR: ", garages[0].remove(garages[0].cars[0]))

# CHECK CESAR
    print ("-----CHECK CESAR------")

    cesar = Cesar(name='Vasiliy', cesar_garages=garages)

    print(cesar)
    print("SUM PRICE ALL CAR: ", cesar.hit_hat())
    print("COUNT CAR IN ALL GARAGES: ", cesar.сars_count())
    print("ADD CAR TO FREE GARAGE: ", cesar.add_car(car1))
    print("ADD CAR TO SELECTED GARAGE: ", cesar.add_car(car2, garages[0]))
    print("COUNT OF GARAGE:", cesar.garages_count())


print ("-----------------------------------")






