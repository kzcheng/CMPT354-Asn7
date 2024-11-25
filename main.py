"""
Application Requirements
Your application should either have a graphical user interface or a command line interface with a hierarchical menu to support the following functions. Your submitted application should be run directly on the workstations in CSIL. Since we are using Python, you can simply submit a .py file that we can directly run. Note that once the program is running, it should allow the tester to test all its functions and not terminate unless the tester manually closes the window or console. 

The functions to be implemented are as follows:

Login
1. (Done) This function allows the user to log in the interface to have access to all other functionalities. The user must be remembered by the system for further operations in the
same session.
2. (Done) The user must enter a valid user ID.
3. (Done) If the user ID is invalid, an appropriate message should be shown to the user.

Search Business
1. (Done) This function allows the user to search for businesses that satisfy certain criteria.
2. (Done) A user should be able to set the following filters as their search criteria: minimum number of stars, city, and name (or part of the name). The search is not case-sensitive. It means that the search for upper or lower case must return the same results.
3. (Done) The user can choose one of the following three orderings of the results: by name, by city, or by number of stars.
4. (Done) After the search is complete, a list of search results must be shown to the user. The list must include the following information for each business: id, name, address, city and number of stars. The results must be ordered according to the chosen attribute. The results can be shown on the terminal or in a GUI.
5. (Done) If the search result is empty, an appropriate message should be shown to the user.

Search Users
1. (Done) This function allows the user to search for users that satisfy certain criteria.
2. (Done) A user should be able to set the following filters as their search criteria: name (or a part of the name), minimum review count, minimum average stars. The search is not case sensitive.
3. (Done) After the search is complete, a list of search results must be shown to the user. The list must include the following information for each user: id, name, review count, useful, funny, cool, average stars, and the date when the user was registered at Yelp. The results must be ordered by name. The results can be shown on the terminal or in a GUI.
4. (Done) If the search result is empty, an appropriate message should be shown to the user.

Make Friend
1. (Done) A user must be able to select another user from the results of the function Search Users and create a friendship. This can be done by entering the user's ID in a terminal or by clicking on a user in a GUI. The selected user will be a friend of the user that is logged in to the database.
2. (Done) The friendship should be recorded in the Friendship table.

Review Business
1. (Done) A user should be able to review a business.
2. (Done) To make a review, a user must enter the business's ID in a terminal or click on a business returned by Search Business in a GUI.
3. (Done) The user must provide the number of stars (integer between 1 and 5).
4. (Done) The review should be recorded in the Review table. Create a review ID consisting of the ID of the logged user and the current date.
5. The program should update the number of stars and the count of reviews for the reviewed business. You need to make sure that the triggers you implemented in assignment 4 are working properly with your application program.
"""


# importing module
import cmd2
from dotenv import load_dotenv
import os
import sys
from pprint import pprint
from functools import wraps
import pymssql
import uuid
import base64


# Load environment variables from .env file
load_dotenv()

# Global variables
user_id = None
db = None


# Decorator to check if user is logged in
def is_logged_in(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if user_id is None:
            print("You must be logged in to use this command.")
            return
        return func(self, *args, **kwargs)
    return wrapper


# Various types of menus
class BaseMenu(cmd2.Cmd):
    def __init__(self):
        super().__init__()
        self.hidden_commands.append('alias')
        self.hidden_commands.append('edit')
        self.hidden_commands.append('macro')
        self.hidden_commands.append('run_pyscript')
        self.hidden_commands.append('run_script')
        self.hidden_commands.append('set')
        self.hidden_commands.append('shell')
        self.hidden_commands.append('shortcuts')
        self.hidden_commands.append('quit')
        self.hidden_commands.append('test')

    def do_exit(self, arg):
        'Exit the application'
        print("Goodbye!")
        sys.exit(0)
        return True

    def do_back(self, arg):
        'Go back to the previous menu'
        return True


class Yelp(BaseMenu):
    intro = 'Welcome to Yelp Database Interactor. Type help or ? to list commands.'
    prompt = '(yelp) '

    def __init__(self):
        super().__init__()
        global db
        db = DatabaseConnection()
        db.connect()

    def do_login(self, arg):
        'Login with a user ID'
        # A user ID for testing: GyeRXCZnZOVOukMmzlLC1A
        global user_id

        input_id = input("Enter your user ID: ")
        result = db.execute_query(f"SELECT COUNT(*) AS count FROM dbo.user_yelp WHERE user_id = '{input_id}'")
        # pprint(result)
        if result[0]['count'] == 0:
            print("User ID not found.")
            user_id = None
            return
        else:
            user_id = input_id
            print(f"Logged in as user: {user_id}")
            return

    @is_logged_in
    def do_search_business(self, arg):
        'Search for businesses based on criteria'
        min_stars = input("Enter minimum number of stars (default 0): ").strip()
        if not min_stars:
            min_stars = 0
        city = input("Enter city (leave blank for any): ").strip()
        name = input("Enter business name or part of the name (leave blank for any): ").strip()
        order_by = input("Order by (name/city/stars): ").strip().lower()

        query = f"SELECT * FROM dbo.business WHERE stars >= {min_stars}"

        if city:
            query += f" AND LOWER(city) = LOWER('{city}')"
        if name:
            query += f" AND LOWER(name) LIKE LOWER('%{name}%')"

        if order_by == "name":
            query += " ORDER BY name"
        elif order_by == "city":
            query += " ORDER BY city"
        elif order_by == "stars":
            query += " ORDER BY stars"
        else:
            print("Invalid order by option. Defaulting to order by name.")
            query += " ORDER BY name"

        results = db.execute_query(query)
        if not results:
            print("No businesses found matching the criteria.")
        else:
            pprint(results)

    @is_logged_in
    def do_search_users(self, arg):
        'Search for users based on criteria'
        name = input("Enter user name or part of the name (leave blank for any): ").strip()
        min_review_count = input("Enter minimum review count (default 0): ").strip()
        if not min_review_count:
            min_review_count = 0
        min_avg_stars = input("Enter minimum average stars (default 0): ").strip()
        if not min_avg_stars:
            min_avg_stars = 0

        query = f"SELECT * FROM dbo.user_yelp WHERE review_count >= {min_review_count} AND average_stars >= {min_avg_stars}"

        if name:
            query += f" AND LOWER(name) LIKE LOWER('%{name}%')"

        query += " ORDER BY name"

        results = db.execute_query(query)
        if not results:
            print("No users found matching the criteria.")
        else:
            pprint(results)

    @is_logged_in
    def do_make_friend(self, arg):
        'Make a friend with another user'
        # Another random user ID for testing: rd9nxNBDINxLke0zAvibLQ
        friend_id = input("Enter the user ID of the person you want to befriend: ").strip()

        if not friend_id:
            print("User ID cannot be empty.")
            return

        if friend_id == user_id:
            print("You cannot befriend yourself.")
            return

        # Check if the friend exists
        result = db.execute_query(f"SELECT COUNT(*) AS count FROM dbo.user_yelp WHERE user_id = '{friend_id}'")
        if result[0]['count'] == 0:
            print("User ID not found.")
            return

        # Insert the friendship record
        success = db.execute_non_query(f"INSERT INTO dbo.friendship (user_id, friend) VALUES ('{user_id}', '{friend_id}')")
        if success:
            print(f"User {friend_id} has been added as a friend.")
        else:
            print("Failed to add friend. Please try again.")

    @is_logged_in
    def do_review_business(self, arg):
        'Review a business'
        # A random business ID for testing: 4IeEE942bigAMf-N3JSuxA
        # Actually, it's not random at all. This is a business that have been reviewed by a friend of GyeRXCZnZOVOukMmzlLC1A
        business_id = input("Enter the business ID you want to review: ").strip()
        stars = input("Enter the number of stars (1-5): ").strip()

        if not business_id or not stars:
            print("Business ID and stars are required.")
            return

        try:
            stars = int(stars)
            if stars < 1 or stars > 5:
                print("Stars must be an integer between 1 and 5.")
                return
        except ValueError:
            print("Stars must be an integer between 1 and 5.")
            return

        # Generate a random CHAR(22) for review_id
        review_id = base64.urlsafe_b64encode(uuid.uuid4().bytes).decode('utf-8').rstrip('=\n')[:22]

        # Insert the review record
        success = db.execute_non_query(f"INSERT INTO dbo.review (review_id, user_id, business_id, stars) VALUES ('{review_id}', '{user_id}', '{business_id}', {stars})")
        if success:
            print(f"Review for business {business_id} has been added.")
        else:
            print("Failed to add review. Please try again.")

    def do_back(self, arg):
        'Back command is disabled in the main menu'
        print("Back command is not available in the main menu")
        return

    def do_test(self, arg):
        'Test command'
        print("Unfortunately, there is nothing that needs to be tested.")
        return


# Class for connecting to the database
class DatabaseConnection:
    def __init__(self):
        self.connection = None

    def connect(self):
        if self.connection is None:
            try:
                self.connection = pymssql.connect(
                    server=os.getenv("SQL_SERVER"),
                    user=os.getenv("USER_ID"),
                    password=os.getenv("PASSWORD"),
                    database=os.getenv("DATABASE")
                )
                print("Connection Successfully Established")
            except pymssql.Error as ex:
                print(f"Error connecting to database: {ex}")

    def execute_query(self, query):
        if self.connection is None:
            print("No database connection.")
            return None
        try:
            cursor = self.connection.cursor(as_dict=True)
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except pymssql.Error as ex:
            print("Error in query execution:", ex)
            return None

    def execute_non_query(self, query):
        if self.connection is None:
            print("No database connection.")
            return False
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            cursor.close()
            return True
        except pymssql.Error as ex:
            print("Error in query execution:", ex)
            return False

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            print("Connection Closed")


# Tests
def run_tests():
    'Run test code'
    try:
        global user_id
        user_id = "GyeRXCZnZOVOukMmzlLC1A"
        Yelp().do_review_business("")
    except pymssql.Error as ex:
        print("Error in connection:", ex)
    finally:
        db.close()


def connect_to_database_test():
    'Connect to the SQL Server database and run a test query.'
    try:
        db = DatabaseConnection()
        db.connect()
        result = db.execute_query("SELECT TOP 1 * FROM dbo.user_yelp")
        if result:
            print("Test query executed successfully. Sample row:", result[0])
        else:
            print("Test query executed successfully, but no data was returned.")
    except pymssql.Error as ex:
        print("Error in connection:", ex)
    finally:
        db.close()


# Called when the script is run
def main():
    try:
        Yelp().cmdloop()
    except pymssql.Error as ex:
        print("Error in connection:", ex)
    finally:
        db.close()


if __name__ == '__main__':
    # Comment out the main loop or test code
    main()
    # run_tests()
