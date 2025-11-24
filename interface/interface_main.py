from exceptions.errors import AlreadyExistsError

class MainInterface:
    def __init__(self, auth_service, admin_ui, user_ui):
        self.auth_service = auth_service
        self.admin_ui = admin_ui
        self.user_ui = user_ui

    def menu(self):
        while True:
            print("\nMAIN MENU\n1. Login\n2. Register\n0. Exit")

            choice = input("Select: ")

            if choice == "1":
                username = input("Username: ")
                password = input("Password: ")
                try:
                    user = self.auth_service.login(username, password)
                except Exception as e:
                    print(e)
                    continue

                if user.role == "admin":
                    self.admin_ui.menu()
                else:
                    self.user_ui.menu(user)
            elif choice == "2":
                username = input("Username: ")
                password = input("Password: ")
                try:
                    self.auth_service.register(username, password)
                    print(f"User '{username}' registered")
                except AlreadyExistsError as e:
                    print(e)
            elif choice == "0":
                break
            else:
                print("Invalid choice")