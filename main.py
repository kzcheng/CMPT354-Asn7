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
1. This function allows the user to search for businesses that satisfy certain criteria.
2. A user should be able to set the following filters as their search criteria: minimum number of stars, city, and name (or part of the name). The search is not case-sensitive. It means that the search for upper or lower case must return the same results.
3. The user can choose one of the following three orderings of the results: by name, by city, or by number of stars.
4. After the search is complete, a list of search results must be shown to the user. The list must include the following information for each business: id, name, address, city and number of stars. The results must be ordered according to the chosen attribute. The results can be shown on the terminal or in a GUI.
5. If the search result is empty, an appropriate message should be shown to the user.

Search Users
1. This function allows the user to search for users that satisfy certain criteria.
2. A user should be able to set the following filters as their search criteria: name (or a part of the name), minimum review count, minimum average stars. The search is not case sensitive.
3. After the search is complete, a list of search results must be shown to the user. The list must include the following information for each user: id, name, review count, useful, funny, cool, average stars, and the date when the user was registered at Yelp. The results must be ordered by name. The results can be shown on the terminal or in a GUI.
4. If the search result is empty, an appropriate message should be shown to the user.

Make Friend
1. A user must be able to select another user from the results of the function Search Users and create a friendship. This can be done by entering the user's ID in a terminal or by clicking on a user in a GUI. The selected user will be a friend of the user that is logged in to the database.
2. The friendship should be recorded in the Friendship table.

Review Business
1. A user should be able to review a business.
2. To make a review, a user must enter the business's ID in a terminal or click on a business returned by Search Business in a GUI.
3. The user must provide the number of stars (integer between 1 and 5).
4. The review should be recorded in the Review table. Create a review ID consisting of the ID of the logged user and the current date.
5. The program should update the number of stars and the count of reviews for the reviewed business. You need to make sure that the triggers you implemented in assignment 4 are working properly with your application program.
"""


# importing module
import pypyodbc
import cmd2
from dotenv import load_dotenv
import os
import sys
from pprint import pprint


# Load environment variables from .env file
load_dotenv()

# Global variables
user_id = None
db = None


# Decorator to check if user is logged in
def is_logged_in(func):
    def wrapper(self, *args, **kwargs):
        if user_id is None:
            print("You must be logged in to use this function.")
            return
        return func(self, *args, **kwargs)
    return wrapper


# Various types of menus
class BaseMenu(cmd2.Cmd):
    def do_exit(self, arg):
        'Exit the application'
        print("Goodbye!")
        sys.exit(0)
        return True

    def do_back(self, arg):
        'Go back to the previous menu'
        return True


class SubMenu1(BaseMenu):
    intro = 'Type help or ? to list commands.'
    prompt = '(menu1) '

    def do_option1(self, arg):
        'Option 1 in Menu 1'
        print("You selected Option 1 in Menu 1")
        return

    def do_option2(self, arg):
        'Option 2 in Menu 1'
        print("You selected Option 2 in Menu 1")
        return


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
        # Use __hr-GtD9qh8_sYSGTRqXw for testing
        global user_id

        input_id = input("Enter your user ID: ")
        result = db.execute_query(f"SELECT COUNT(*) FROM dbo.user_yelp WHERE user_id = '{input_id}'")
        # pprint(result[0][0])
        if result[0][0] == 0:
            print("User ID not found.")
            user_id = None
            return
        else:
            user_id = input_id
            print(f"Logged in as user: {user_id}")
            return

    @is_logged_in
    def do_menu1(self, arg):
        'Enter menu 1'
        print("You are in Menu 1")
        SubMenu1().cmdloop()
        return

    @is_logged_in
    def do_menu2(self, arg):
        'Enter menu 2'
        print("You are in Menu 2")
        # Add more commands or submenus here
        return

    def do_back(self, arg):
        'Back command is disabled in the main menu'
        print("Back command is not available in the main menu")
        return


# Class for connecting to the database
class DatabaseConnection:
    def __init__(self):
        self.connection = None

    def connect(self):
        if self.connection is None:
            try:
                self.connection = pypyodbc.connect(
                    f'Driver={{SQL Server}};Server={os.getenv("SQL_SERVER")};'
                    f'Database={os.getenv("DATABASE")};uid={os.getenv("USER_ID")};'
                    f'pwd={os.getenv("PASSWORD")}'
                )
                print("Connection Successfully Established")
            except pypyodbc.Error as ex:
                print(f"Error connecting to database: {ex}")

    def execute_query(self, query):
        if self.connection is None:
            print("No database connection.")
            return None
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except pypyodbc.Error as ex:
            print("Error in query execution:", ex)
            return None

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            print("Connection Closed")


# Tests
def run_tests():
    'Run test code'
    connect_to_database_test()


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
    except pypyodbc.Error as ex:
        print("Error in connection:", ex)
    finally:
        db.close()


# Called when the script is run
def main():
    try:
        Yelp().cmdloop()
    except pypyodbc.Error as ex:
        print("Error in connection:", ex)
    finally:
        db.close()


if __name__ == '__main__':
    # Comment out the main loop or test code
    main()
    # run_tests()
