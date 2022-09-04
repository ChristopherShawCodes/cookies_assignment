from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re	# the regex module
#email validation
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

from flask_app.config.mysqlconnection import connectToMySQL
# model the class after the friend table from our database



class Order:

    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.type = data['type']
        self.num_of_boxes = data['num_of_boxes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # #This is a static method to validate a new cookie order
    @classmethod
    def order_is_valid(cls,data):
        is_valid = True

        if len(data['name']) <= 0:
            flash("Name Is Required")
            is_valid = False
        if len(data['type']) <= 0:
            flash("Cookie Type Is Required")
            is_valid = False
        if len(data['num_of_boxes']) <= 0:
            flash("But How Many Boxes Did You Get? And Do You Feel Guilty About It?")
            is_valid = False
        return is_valid




    # Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM orders;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('girlscout_cookies').query_db(query)
        # Create an empty list to append our instances of friends
        orders = []
        # Iterate over the db results and create instances of users with cls.
        for order in results:
            orders.append( cls(order) )
        return orders


    #class method to save our friend to the database
    @classmethod
    def save(cls,data):
        query = "INSERT INTO orders (name,type, num_of_boxes, created_at, updated_at)VALUES (%(name)s,%(type)s,%(num_of_boxes)s,NOW(),NOW() );"
        #data is a dictionary that will be passed into the save method from server.py
        #this return statement would return an integer of the id we just created in the database
        return connectToMySQL('girlscout_cookies').query_db(query,data)


    @classmethod
    def get_last(cls):
        query = "SELECT * FROM orders"
        results = connectToMySQL('girlscout_cookies').query_db(query)
        return cls(results[len(results)-1])


    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM orders WHERE id = %(id)s;"
        result = connectToMySQL('girlscout_cookies').query_db(query,data)
        return cls(result[0])


    @classmethod
    def update(cls,data):
        query = "UPDATE orders SET name=%(name)s,type=%(type)s,num_of_boxes=%(num_of_boxes)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL('girlscout_cookies').query_db(query,data)
