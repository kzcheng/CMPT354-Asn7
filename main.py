# importing module
import pypyodbc
import cmd
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


# Various types of menus
class BaseMenu(cmd.Cmd):
    def do_exit(self, arg):
        'Exit the application'
        print("Goodbye!")
        return True

    def do_back(self, arg):
        'Go back to the previous menu'
        return True


class SubMenu1(BaseMenu):
    prompt = '(menu1) '

    def do_option1(self, arg):
        'Option 1 in Menu 1'
        print("You selected Option 1 in Menu 1")

    def do_option2(self, arg):
        'Option 2 in Menu 1'
        print("You selected Option 2 in Menu 1")


class MyApp(BaseMenu):
    intro = 'Welcome to MyApp. Type help or ? to list commands.\n'
    prompt = '(myapp) '

    def do_greet(self, arg):
        'Greet the user'
        print("Hello!")

    def do_menu1(self, arg):
        'Enter menu 1'
        print("You are in Menu 1")
        SubMenu1().cmdloop()

    def do_menu2(self, arg):
        'Enter menu 2'
        print("You are in Menu 2")
        # Add more commands or submenus here

    def do_back(self, arg):
        'Back command is disabled in the main menu'
        print("Back command is not available in the main menu")


# Class for connecting to the database
class DatabaseConnection:
    def __init__(self):
        self.connection = None

    def connect(self):
        if self.connection is None:
            self.connection = pypyodbc.connect(
                f'Driver={{SQL Server}};Server={os.getenv("SQL_SERVER")};'
                f'Database={os.getenv("DATABASE")};uid={os.getenv("USER_ID")};'
                f'pwd={os.getenv("PASSWORD")}'
            )
            print("Connection Successfully Established")

    def execute_query(self, query):
        try:
            self.connect()
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
        result = db.execute_query("SELECT TOP 1 * FROM dbo.business")
        if result:
            print("Test query executed successfully. Sample row:", result[0])
        else:
            print("Test query executed successfully, but no data was returned.")
    except pypyodbc.Error as ex:
        print("Error in connection:", ex)
    finally:
        db.close()


if __name__ == '__main__':
    # Comment out the main loop or test code
    # MyApp().cmdloop()
    run_tests()
