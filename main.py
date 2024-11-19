# importing module
import pypyodbc
import cmd
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

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


def connect_to_database():
    'Connect to the SQL Server database and run a test query.'
    try:
        connection = pypyodbc.connect(
            f'Driver={{SQL Server}};Server={os.getenv("SQL_SERVER")};'
            f'Database={os.getenv("DATABASE")};uid={os.getenv("USER_ID")};'
            f'pwd={os.getenv("PASSWORD")}'
        )
        print("Connection Successfully Established")

        # Create a cursor object using the connection
        cursor = connection.cursor()

        # Run a simple query to test the connection
        cursor.execute("SELECT TOP 1 * FROM dbo.business")

        # Fetch and print the result of the query
        row = cursor.fetchone()
        if row:
            print("Test query executed successfully. Sample row:", row)
        else:
            print("Test query executed successfully, but no data was returned.")

        # Close the cursor and connection
        cursor.close()
        connection.close()
    except pypyodbc.Error as ex:
        print("Error in connection:", ex)


def run_tests():
    'Run test code'
    connect_to_database()


if __name__ == '__main__':
    # Comment out the main command loop
    # MyApp().cmdloop()

    # Run test code
    run_tests()
