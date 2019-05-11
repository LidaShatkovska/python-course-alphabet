# coding=utf-8
import random
import string
import uuid
import json
import pickle
import codecs

from ruamel.yaml import YAML
from typing import List
from constants import CARS_TYPES
from constants import CARS_PRODUCER
from constants import TOWNS

yaml = YAML()

"""
---HW4-------
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

"""
---HW5----
Для попереднього домашнього завдання.

Для класів Колекціонер Машина і Гараж написати методи, які зберігають стан обєкту в файли формату
yaml, json, pickle відповідно.

Для класів Колекціонер Машина і Гараж написати методи, які конвертують обєкт в строку формату
yaml, json, pickle відповідно.

Для класу Колекціонер Машина і Гараж написати методи, які створюють інстанс обєкту
з (yaml, json, pickle) строки відповідно

Для класу Колекціонер Машина і Гараж написати методи, які створюють інстанс обєкту
з (yaml, json, pickle) файлу відповідно

Advanced
Добавити опрацьовку формату ini
"""

class Car:

    def __init__(self, price: float, car_type: string, producer: string, mileage: float):
        self.price = round(price,2)
        self.car_type = car_type
        self.producer = producer
        self.mileage = round(mileage,2)
        self.number = uuid.uuid4()
        self.car_set = ({'producer': self.producer, 'car_type': self.car_type, 'number': str(self.number), 'price': self.price, 'mileage': self.mileage})


    def __repr__(self):
        return f"\nproducer: {self.producer}, car_type: {self.car_type}, " \
               f"number: {self.number}, price: {self.price}, mileage: {self.mileage}"


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


    @staticmethod
    def to_json(obj):
        car_data = {"price": obj.price, "car_type": obj.car_type, "producer": obj.producer,  \
                    "mileage": obj.mileage, "number": str(obj.number) }
        return car_data


    @classmethod
    def from_json(cls,car_json_data):
        price = round(car_json_data['price'],2)
        car_type = car_json_data['car_type']
        producer = car_json_data['producer']
        mileage = round(car_json_data['mileage'], 2)
        number = uuid.uuid4()
        new_car = Car(price=price, car_type=car_type, producer=producer, mileage=mileage)
        return new_car


    def save_json_into_file(self):
        car_data = Car.to_json(self)
        with open("cars_data.json", 'w') as file:
            json.dump(car_data, file)


    def save_json_into_str(self):
        car_data = Car.to_json(self)
        json_formatted_str = json.dumps(car_data)
        return json_formatted_str


    @classmethod
    def instance_from_json_file(cls):
        with open("cars_data.json", "r") as read_file:
            new_car_dict = json.load(read_file)
            new_car = Car.from_json(new_car_dict)
            print("NEW_CAR_TYPE: {}\nNEW_CAR_FROM_JSON_FILE: {}".format(type(new_car),new_car) )
        return new_car


    @classmethod
    def instance_from_json_str(cls,json_formatted_str):
        new_car = json.loads(json_formatted_str, object_hook= Car.from_json)
        print("NEW_CAR_TYPE: {}\nNEW_CAR_FROM_JSON_STR: {}".format(type(new_car), new_car))
        return new_car



class Garage:

    def __init__(self, town: string, places: int, garage_cars: List[Car],  owner=None):
        self.town = town
        self.places = places
        self.garage_cars = garage_cars if garage_cars is not None else []
        self.owner = owner
        self.current = 0
        self.yaml = YAML()
        self.garage_set = ({'town': self.town, 'places': self.places, 'owner': self.owner, 'garage_cars': self.garage_cars})


    def __repr__(self):
        return f"\n{self.garage_set} "


    def add(self, new_car: string):
        if len(self.garage_cars) < self.places:
            self.garage_cars.append(new_car.car_set)
            return self
        else:
            return ("Garage haven't got any free places")


    def remove(self, my_car: string):
        if my_car in self.garage_cars:
            self.cagarage_carsrs.remove(my_car)
            print('THE CAR WAS DELETED!')
        return self


    def hit_hat(self):
        return round(sum(car['price'] for car in self.garage_cars),2)


    @classmethod
    def from_yaml(cls, new_garage_dict):
        town = new_garage_dict['town']
        places = new_garage_dict['places']
        owner = new_garage_dict['owner']
        cars = []
        for item in new_garage_dict['garage_cars']:
            cars.append(Car.from_json(dict(item)).car_set)
        new_garage = Garage(town=town, places=places, owner=owner, garage_cars=cars)
        return new_garage


    @classmethod
    def instance_from_yaml_file(cls):
        with open("garages_data.yaml", "r") as read_file:
            new_garage_dict = yaml.load(read_file)
            new_garage = Garage.from_yaml(new_garage_dict)
            print("NEW_GARAGE_TYPE: {}\nNEW_INSTANC_GARAGE_FROM_YAML_FILE: {}".format(type(new_garage), new_garage))
        return new_garage


    def to_yaml(self):
        garage_data = {'town': self.town, 'places': self.places, 'owner':self.owner, 'garage_cars': self.garage_cars}
        return garage_data


    def save_yaml_into_file(self):
        with open("garage_result.yaml", "w") as file:
            yaml.dump(self.garage_set , file)


    def save_yaml_into_str(self):
        garage_data = Garage.to_yaml(self)
        yaml_formatted_str = str(garage_data)
        return yaml_formatted_str


    @staticmethod
    def instance_from_yaml_str(yaml_formatted_str: str):
        yaml_str = yaml.load(yaml_formatted_str)
        new_instance = Garage.from_yaml(yaml_str)
        print("INSTANCE FROM YAML STR:", type(new_instance), new_instance)
        return new_instance

class Cesar:

    def __init__(self, name: string, cesar_garages: List[Garage]):
        self.name = name
        self.cesar_garages = cesar_garages if cesar_garages is not None else []
        self.register_id = uuid.uuid4()
        self.cesar_set = ({'name': self.name, 'register_id': self.register_id, 'cesar_garages': self.cesar_garages })


    def __repr__(self):
        return f"CESAR NAME: {self.name}, " \
               f"\nREGISTER_ID: {self.register_id}, " \
               f"\nCOUNT OF GARAGE: {self.garages_count()}, " \
               f"\nCOUNT CAR IN ALL GARAGES:  {self.cars_count()}, " \
               f"\nSUM PRICE ALL CAR:  {self.hit_hat()}" \
               f"\nGARAGE: {self.cesar_garages}, "


    @staticmethod
    def compare_cesar(cesar_list: list):
        return max((cesar for cesar in cesar_list), key=lambda x: x.hit_hat() )


    def hit_hat(self):
        return round(sum(item.hit_hat() for item in self.cesar_garages),2)


    def garages_count(self):
        return len(self.cesar_garages)


    def cars_count(self):
        return sum(len(garage.garage_cars) for garage in self.cesar_garages)


    def add_car(self, car: string, garage = None):
        if garage is None:
            return max(self.cesar_garages, key = lambda x:(x.places-len(x.cars))).add(car)
        else:
            return garage.add(car)


    def pickle_to_str(self):
        pickle_formatted_str = codecs.encode(pickle.dumps(self), "base64").decode()
        return pickle_formatted_str


    def pickle_to_file(self):
        pickle_formatted_str = self.pickle_to_str()
        with open("pickle_data.txt", "wb") as file:
            pickle.dump(pickle_formatted_str, file)


    @staticmethod
    def instance_from_pickle_str(pickle_str: str):
        new_cesar = pickle.loads(codecs.decode(pickle_str.encode(), "base64"))
        return new_cesar


    @classmethod
    def instance_from_pickle_file(cls):
        with open('pickle_data.txt', 'rb') as file:
            pickle_str = pickle.load(file)
            new_cesar = Cesar.instance_from_pickle_str(pickle_str)
        return new_cesar



if __name__ == "__main__":

    cars = []
    for car_counter in range(random.randint(10, 100)):
        car = Car(price=random.uniform(100.5, 999.5),
                  car_type=random.choice(CARS_TYPES),
                  producer=random.choice(CARS_PRODUCER),
                  mileage=random.uniform(0, 1000000),
                  )
        cars.append(car.car_set)

    car1 = Car(price=random.uniform(100.5, 999.5),
               car_type=random.choice(CARS_TYPES),
               producer=random.choice(CARS_PRODUCER),
               mileage=random.uniform(0, 1000000),
               )
    car2 = Car(price=random.uniform(100.5, 999.5),
               car_type=random.choice(CARS_TYPES),
               producer=random.choice(CARS_PRODUCER),
               mileage=random.uniform(0, 1000000),
               )

    #print ("CAR1: ", car1)
    #print ("CAR2: ", car2)



    # # CHECK UUID CHANGE
    # print ("\n------CHECK UUID CHANGE--------")
    # old_number = car1.number
    # car1.number = car1.change_UUID()
    # print("The number {} of car {} was changed on: {}".format(old_number, car1.producer, car1.number))
    #
    # # CHECK COMPARE
    # print ("\n-----CHECK COMPARE-------")
    # if car1.price <= car2.price:
    #     print(
    #         "price {} car {} biggest then price {} car {}".format(car2.price, car2.producer, car1.price, car1.producer))
    # else:
    #     print(
    #         "price {} car {} biggest then price {} car {}".format(car1.price, car1.producer, car2.price, car2.producer))
    #
    # if car1.price < car2.price:
    #     print(
    #         "car {} price {} cheaper then car {} price {}".format(car1.producer, car1.price, car2.producer, car2.price))
    # else:
    #     print("car {} cheaper then car {}".format(car2.producer, car1.producer))
    #
    # if car1.price == car2.price:
    #     print(
    #         "price {} car {} is equal to price {} car {}".format(car1.price, car1.producer, car2.price, car2.producer))
    #
    # if car1.price != car2.price:
    #     print("price car {} isn't equal to price car {}".format(car1.producer, car2.producer))

    #print ("\n-----CHECK GARAGE------")
    CESAR_NAME = ["Oleg", "Vitaliya", "Marina", "Grisha", "Petr"]
    cesars = []
    for cesar_counter in range(random.randint(1, 1)):
        garages = []
        for garage_counter in range(random.randint(1, 3)):
            count_cars = random.randint(1, 4)
            random_place = random.randint(0, 10)

            get_car = []
            for i in random.sample(cars, count_cars):
                if i not in get_car:
                    cars.remove(i)
                    get_car.append(i)

            if count_cars > random_place:
                raise ValueError("Count cars more then count place. RUN PGOGRAM AGAIN")
            else:
                garage = Garage(town=random.choice(TOWNS),
                                    places=random_place,
                                    garage_cars=get_car)
                # print (garage)
                # print("\nCOUNT CARS: ", len(get_car))
                # print("COUNT PLACE: ", random_place)
                # print("PRICE ALL CAR IN GARAGES: ", garage.hit_hat())

            garages.append(garage)
    cesar = Cesar(name=random.choice(CESAR_NAME), cesar_garages=garages)
    cesars.append(cesar)

    print ("\n-----CHECK CESAR------")
    for item in cesars:
          print(item, "\n")

#-------HW5 CHECK------------

    print ('\n----JSON------')
    car1.save_json_into_file()
    json_str = car1.save_json_into_str()
    new_car_file = Car.instance_from_json_file()
    print()
    new_car_str = Car.instance_from_json_str(json_str)

    print ('\n----YAML------')
    garage1 = Garage.instance_from_yaml_file()
    print()
    garage1.save_yaml_into_file()
    yaml_str = garage1.save_yaml_into_str()
    Garage.instance_from_yaml_str(yaml_str)

    print ("\n-----PICKLE------")

    cesars[0].pickle_to_file()
    new_cesar_file = Cesar.instance_from_pickle_file()
    print ('NEW_CESAR_FROM_PICKLE_FILE:', '\n', new_cesar_file)
    pickle_str = cesar.pickle_to_str()

    new_cesar_str = Cesar.instance_from_pickle_str(pickle_str)
    print ('\nNEW_CESAR_FROM_PICKLE_STR', '\n', new_cesar_str)


    #print ("THE RICHEST CESAR IS: ", (Cesar.compare_cesar(cesars)).name)

    # print("\n----CHECK ADD CARS----------")
    # print("BEFORE ADD NEW CAR: ", garages[0])
    # print("PRICE ALL CARS IN GARAGE BEFORE ADD CAR: ", garages[0].hit_hat())
    #
    # print("\nAFTER ADD NEW CAR: ", garages[0].add(car1))
    # print("PRICE ALL CARS IN GARAGE AFTER ADD CAR: ", garages[0].hit_hat())
    #
    # print("\nBEFORE REMOVE NEW CAR: ", garages[0])
    # print("\nCAR FOR REMOVE: ", garages[0].cars[0])
    # print("\nAFTER REMOVE NEW CAR: ", garages[0].remove(garages[0].cars[0]))
    #
    # print("\nADD CAR TO FREE GARAGE: ", cesars[0].add_car(car1))
    # print("\nADD CAR TO SELECTED GARAGE: ", cesars[0].add_car(car2, garages[0]))

print ("-----------------------------------")