# importing module
import pypyodbc
import cmd


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
    'Connect to the SQL Server database'
    try:
        connection = pypyodbc.connect('Driver={SQL Server};Server=your_server_name;Database=your_database_name;uid=your_user_id;pwd=your_password')
        print("Connection Successfully Established")
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
