from app import app, db, Restaurant, Pizza, RestaurantPizza

# Function to seed the database with initial data
def seed_database():
    # Create Restaurants
    restaurant1 = Restaurant(name="Dominion Pizza", address="Good Italian, Ngong Road, 5th Avenue")
    restaurant2 = Restaurant(name="Pizza Hut", address="Westgate Mall, Mwanzi Road, Nrb 100")

    # Create Pizzas
    pizza1 = Pizza(name="Cheese", ingredients="Dough, Tomato Sauce, Cheese")
    pizza2 = Pizza(name="Pepperoni", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni")

    # Add Restaurants and Pizzas to the session
    db.session.add_all([restaurant1, restaurant2, pizza1, pizza2])
    db.session.commit()

    # Create RestaurantPizzas
    rp1 = RestaurantPizza(price=10, pizza=pizza1, restaurant=restaurant1)
    rp2 = RestaurantPizza(price=12, pizza=pizza2, restaurant=restaurant1)

    # Add RestaurantPizzas to the session
    db.session.add_all([rp1, rp2])
    db.session.commit()

# Register the seed function to run before each request
@app.before_request
def before_request():
    seed_database()

if __name__ == '__main__':
    # Run this script to seed the database
    with app.app_context():
        seed_database()
