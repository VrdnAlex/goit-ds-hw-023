from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://<username>:<password>@cluster0.j54nsqb.mongodb.net/Cats_test?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri, server_api=ServerApi('1'))

db = client.book


# Функція для виведення всіх записів із колекції
def find_all_cats(client):
    try:
        db = client.book

        result = db.cats.find({})
        for el in result:
            print(el)
    except Exception as e:
        print(f"Error printing cats: {e}")


# Функція для пошуку інформації про кота за ім'ям
def find_cat_by_name(client, cat_name):
    try:
        db = client.book
        cats_collection = db.cats
        cat = cats_collection.find_one({"name": cat_name})

        if cat:
            print(f"Name: {cat['name']}, {cat['age']}, {cat['features']}")
        else:
            print(f"Cat with name '{cat_name}' not found.")
    except Exception as e:
        print(f"Error finding cat: {e}")


# Функція для оновлення віку кота за ім'ям
def update_age_cat(client, cat_name, new_age_cat):
    try:
        db = client.book
        cats_collection = db.cats
        cat = cats_collection.update_one({"name": cat_name}, {"$set": {"age": new_age_cat}})

        if cat.matched_count:
            print(f"Updated age of {cat_name} to {new_age_cat}.")
        else:
            print(f"Cat with name '{cat_name}' not found.")
    except Exception as e:
        print(f"Error updating cat's age: {e}")


# Функція для додавання нової характеристики
def add_new_features(client, cat_name, add_features):
    try:
        db = client.book
        cats_collection = db.cats
        cat = cats_collection.update_one({"name": cat_name}, {"$addToSet": {"features": add_features}})

        if cat.matched_count:
            print(f"Added new feature to {cat_name}.")
        else:
            print(f"Cat with name '{cat_name}' not found.")
    except Exception as e:
        print(f"Error adding feature: {e}")


# Функція для видалення запису з колекції за ім'ям тварини
def delete_one_cat(client, cat_name):
    try:
        db = client.book
        cats_collection = db.cats
        cat = cats_collection.delete_one({"name": cat_name})

        if cat.deleted_count:
            print(f"Cat with name '{cat_name}' has been deleted.")
        else:
            print(f"Cat with name '{cat_name}' not found.")
    except Exception as e:
        print(f"Error deleting cat: {e}")


# Функція для видалення усіх записів із колекції
def delete_all_cats(client):
    try:
        db = client.book

        db.cats.delete_many({})
        print("All cats have been deleted.")
    except Exception as e:
        print(f"Error deleting all cats: {e}")


def main():
    print("Welcome to the Cat Assistant!")

    # Блок commands для асоціації команд з відповідними функціями
    commands = {
        "list": find_all_cats,
        "search": find_cat_by_name,
        "update": update_age_cat,
        "add_feature": add_new_features,
        "delete": delete_one_cat,
        "delete_all": delete_all_cats
    }

    while True:
        user_input = input("Enter a command: ").strip().split(maxsplit=2)
        command = user_input[0].lower()
        args = user_input[1:]

        if command in ["close", "exit"]:
            print("Goodbye!")
            break

        # Перевірка наявності команди в словнику commands
        if command in commands:
            func = commands[command]
            try:
                func(client, *args)
            except TypeError as e:
                print(f"Invalid arguments for command '{command}': {e}")
        elif commands:
            print("Invalid command.")

        elif command == "list":
            find_all_cats(client)
        elif command == "search":
            if len(args) != 1:
                print("Please provide a cat name.")
            else:
                find_cat_by_name(client, args[0])
        elif command == "update":
            if len(args) != 2:
                print("Please provide a cat name and new age.")
            else:
                update_age_cat(client, args[0], int(args[1]))
        elif command == "add_feature":
            if len(args) != 2:
                print("Please provide a cat name and feature to add.")
            else:
                add_new_features(client, args[0], args[1])
        elif command == "delete":
            if len(args) != 1:
                print("Please provide a cat name to delete.")
            else:
                delete_one_cat(client, args[0])
        elif command == "delete_all":
            delete_all_cats(client)
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()