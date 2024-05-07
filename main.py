import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import font

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("1200x1000")
        self.configure(bg="black")  # Set background color of the application window

        self.logged_in = False

        self.global_style()

        self.current_frame = False

        container = tk.Frame(self, bg="black")
        container.pack(fill="both", expand=True)

        self.frames = {}

        '''for F in (WelcomePage, LoginPage, AccountCreationPage, HomePage, WatchlistPage, WatchedPage, RecommenderPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.pack(fill="both", expand=True)'''

        self.show_frame(WelcomePage)

    def show_frame(self, cont):
        '''for F in (WelcomePage, LoginPage, AccountCreationPage, HomePage, WatchlistPage, WatchedPage, RecommenderPage):
            container = tk.Frame(self, bg="black")
            container.pack(fill="both", expand=True)
            frame = F(container, self)
            self.frames[F] = frame
            frame.pack(fill="both", expand=True)
        if self.current_frame:
            self.clear_frame(self.current_frame)
        for frame in self.frames.values():
            frame.pack_forget()

        frame = self.frames[cont]
        frame.pack(fill="both", expand=True)'''

        if self.current_frame:
            self.clear_frame(self.current_frame)
        else:
            self.current_frame = tk.Frame(self, bg="black")
            self.current_frame.pack(fill="both", expand=True)

        # Create a new frame instance every time
        new_frame = cont(self.current_frame, self)
        new_frame.pack(fill="both", expand=True)
        self.current_frame = new_frame

    def clear_frame(self, curr):
        for widget in curr.winfo_children():
            widget.destroy()

    def global_style(self):
        # Apply global styling to all widgets
        self.option_add("*foreground", "green")
        self.option_add("*background", "black")

        self.button_style = ttk.Style()
        self.button_style.configure("TButton", padding=(20,10))

        custom_font = font.Font(size=16)
        self.option_add("*Font", custom_font)


    def logout(self):
        print("Logging out...")
        self.logged_in = False
        self.show_frame(WelcomePage)

    def login(self):
        self.logged_in = False
        self.show_frame(LoginPage)


class WelcomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Welcome Page", width=40, height=6)
        label.pack(pady=20, padx=20)
        controller.logged_in = False
        
        label2 = tk.Label(self, text="Returning user?")
        label2.pack()
        button1 = tk.Button(self, text="Login", 
                            command=lambda: controller.show_frame(LoginPage))
        button1.pack()


        label3 = tk.Label(self, text="First time? Sign up for full access to watchlist and movie tracking functionality (it only takes one minute!)")
        label3.pack()
        button2 = tk.Button(self, text="Create Account", 
                            command=lambda: controller.show_frame(AccountCreationPage))
        button2.pack()

        label4 = tk.Label(self, text="Or enter as a guest with limited features and no way to save or rate movies")
        label4.pack()
        button3 = tk.Button(self, text="Continue as Guest",
                            command=lambda: controller.show_frame(HomePage))
        button3.pack()

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        label = tk.Label(self, text="Login Page")
        label.pack()

        self.username_label = tk.Label(self, text="Username:")
        self.username_label.pack(pady=5)

        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self, text="Password:")
        self.password_label.pack(pady=5)

        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = tk.Button(self, text="Login", command=self.login_helper)
        self.login_button.pack(pady=5)

        self.return_button = tk.Button(self, text="Go Back to Welcome Page", command=lambda: controller.show_frame(WelcomePage))
        self.return_button.pack(pady=5)

    def login_helper(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            messagebox.showinfo("Login Successful", "Welcome back!")
            #self.destroy()
            self.controller.logged_in = True
            self.controller.show_frame(HomePage)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
            self.login_helper

class AccountCreationPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Account Creation Page")
        label.pack(pady=10, padx=10)

        label1 = tk.Label(self, text="Choose a username")
        label1.pack(pady=5)

        self.username = tk.Entry(self)
        self.username.pack()

        label2 = tk.Label(self, text="Choose a password")
        label2.pack(pady=5)

        self.password = tk.Entry(self)
        self.password.pack()

        self.submit_button = tk.Button(self, text="Create Account!", command=self.create_account)
        self.submit_button.pack(pady=5)

        self.return_button = tk.Button(self, text="Go Back to Welcome Page", command=lambda: controller.show_frame(WelcomePage))
        self.return_button.pack(pady=5)


    def create_account(self):
        username = self.username.get()
        password = self.password.get()

        if username and password:
            messagebox.showinfo("Account Created", "Account Created, Welcome!")
            self.controller.logged_in = True
            self.controller.show_frame(HomePage)

        else:
            messagebox.showerror("Error!", "Invalid username and/or password. Try again!")
            self.create_account



class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Home Page")
        label.pack(pady=10, padx=10)

        if controller.logged_in:
            logout_button = tk.Button(self, text="Logout", command=lambda: controller.logout())
            logout_button.pack(side="top", anchor="ne", padx=10, pady=10)
            button1 = tk.Button(self, text="Watchlist", 
                            command=lambda: controller.show_frame(WatchlistPage))
            button1.pack()
            button2 = tk.Button(self, text="Watched Movies", 
                            command=lambda: controller.show_frame(WatchedPage))
            button2.pack()

        else:
            login_button = tk.Button(self, text="Login", command=lambda: controller.show_frame(LoginPage))
            login_button.pack(side="top", anchor="ne", padx=10, pady=10)


        
        button3 = tk.Button(self, text="Recommender", 
                            command=lambda: controller.show_frame(RecommenderPage))
        button3.pack()

 
        button4 = tk.Button(self, text="Tutorial", 
                            command=lambda: controller.show_frame(TutorialPage))
        button4.pack(pady=50)


class WatchlistPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Watchlist")
        label.pack(pady=10, padx=10)

        logout_button = tk.Button(self, text="Logout", command=lambda: controller.show_frame(WelcomePage))
        logout_button.pack(side="top", anchor="ne", padx=10, pady=10)

        self.home_button = tk.Button(self, text="Home", command=lambda: controller.show_frame(HomePage))
        self.home_button.pack(side="top", anchor="ne", padx=10, pady=10)

        self.add_button = tk.Button(self, text="Add a movie to your watchlist", command=lambda: controller.show_frame(AddWatchlistPage))
        self.add_button.pack(side="top", anchor="n", padx=10, pady=10)

class AddWatchlistPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Add to Watchlist")
        label.pack(pady=10, padx=10)

        logout_button = tk.Button(self, text="Logout", command=lambda: controller.show_frame(WelcomePage))
        logout_button.pack(side="top", anchor="ne", padx=10, pady=10)

        self.home_button = tk.Button(self, text="Home", command=lambda: controller.show_frame(HomePage))
        self.home_button.pack(side="top", anchor="ne", padx=10, pady=10)

        label = tk.Label(self, text="Search for a movie by name")
        label.pack()

        self.search_text = tk.Entry(self)
        self.search_text.pack()

        search_enter = tk.Button(self, text="Search", command=self.add_helper)
        search_enter.pack()

        cancel_button = tk.Button(self, text="Return to Watchlist", command=lambda: controller.show_frame(WatchlistPage))
        cancel_button.pack()

    def add_helper(self):
        title = self.search_text.get()

        if title == 'Star Wars':
            messagebox.showinfo("Movie found!", "Movie found and will be added to your watchlist")
            
        else:
            messagebox.showerror("No results found", "We did not find any matches, please try searching for a different title.")



class WatchedPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Previously Watched Movies")
        label.pack(pady=10, padx=10)

        logout_button = tk.Button(self, text="Logout", command=lambda: controller.show_frame(WelcomePage))
        logout_button.pack(side="top", anchor="ne", padx=10, pady=10)

        self.home_button = tk.Button(self, text="Home", command=lambda: controller.show_frame(HomePage))
        self.home_button.pack(side="top", anchor="ne", padx=10, pady=10)

        self.add_button = tk.Button(self, text="Add a movie to your previously watched", command=lambda: controller.show_frame(AddToWatchedPage))
        self.add_button.pack(side="top", anchor="n", padx=10, pady=10)

class AddToWatchedPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Add to Previously Watched")
        label.pack(pady=10, padx=10)

        logout_button = tk.Button(self, text="Logout", command=lambda: controller.show_frame(WelcomePage))
        logout_button.pack(side="top", anchor="ne", padx=10, pady=10)

        self.home_button = tk.Button(self, text="Home", command=lambda: controller.show_frame(HomePage))
        self.home_button.pack(side="top", anchor="ne", padx=10, pady=10)

        label = tk.Label(self, text="Enter Movie Title")
        label.pack()

        self.movie_title = tk.Entry(self)
        self.movie_title.pack()

        self.rating = tk.StringVar()

        label = tk.Label(self, text="Select a rating for the movie")
        label.pack(pady=7)

        self.rating_dropdown = tk.OptionMenu(self, self.rating, "1", "2", "3", "4", "5")
        self.rating_dropdown.pack()

        label = tk.Label(self, text="Write a review for the movie (Optional)")
        label.pack()

        self.movie_review = tk.Entry(self)
        self.movie_review.pack()

        review_enter = tk.Button(self, text="Save to previously watched", command=self.add_helper)
        review_enter.pack(pady=10)

        cancel_button = tk.Button(self, text="Return to Previously Watched List", command=lambda: controller.show_frame(WatchedPage))
        cancel_button.pack()

    def add_helper(self):
        print(self.movie_title.get())
        print(self.rating.get())
        print(self.movie_review.get())

        if self.movie_title and self.rating.get() in [str(i) for i in range(6)]:
            messagebox.showinfo("Review Saved!", "Review saved to your previously watched movies")
            
        else:
            messagebox.showerror("Form Error", "Please fill out all fields of the form.")


class RecommenderPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Recommender")
        label.pack(pady=10, padx=10)

        self.home_button = tk.Button(self, text="Home", command=lambda: controller.show_frame(HomePage))
        self.home_button.pack(side="top", anchor="ne", padx=10, pady=10)

        optional = tk.Label(self, text="Filters (Optional)")
        optional.pack(pady=10, padx=10)

        self.min_length = tk.Scale(self, from_=0, to=255, orient='horizontal', label='Min Length (minutes)', length=300)
        self.min_length.set(0)  # Set the default value
        self.min_length.pack()

        self.max_length = tk.Scale(self, from_=0, to=255, orient='horizontal', label='Max Length (minutes)', length=300)
        self.max_length.set(255)  # Set the default value
        self.max_length.pack()

        self.start_year = tk.Scale(self, from_=1920, to=2024, orient='horizontal', label='Start Year', length=300)
        self.start_year.set(1920)
        self.start_year.pack()

        self.end_year = tk.Scale(self, from_=1920, to=2024, orient='horizontal', label='End Year', length=300)
        self.end_year.set(2024)
        self.end_year.pack()

        rec_enter = tk.Button(self, text="Get Recommendation", command=self.get_recommendation)
        rec_enter.pack()

    def get_recommendation(self):
        min = self.min_length.get()
        max = self.max_length.get()
        start_y = self.start_year.get()
        end_y = self.end_year.get()

        if int(min) <= int(max):
            rec_movie = "Jurassic Park"
            messagebox.showinfo("Recommendation!", f"Your recommended movie is {rec_movie}")




class TutorialPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Movie Madness Tutorial")
        label.pack(pady=10, padx=10)

        self.home_button = tk.Button(self, text="Home", command=lambda: controller.show_frame(HomePage))
        self.home_button.pack(side="top", anchor="ne", padx=10, pady=10)


        label2 = tk.Label(self, text="Here's how to interact with our interface")
        label2.pack(pady=10, padx=10)

        label3 = tk.Label(self, text="Jump between pages by hitting buttons with text inside them.\n For example, the pressing the button below could take you to a secret page")
        label3.pack()

        button1 = tk.Button(self, text="Go to secret page")
        button1.pack()

        label3 = tk.Label(self, text="Blank boxes like the one below let you enter text. There will be a heading above it directing you as to what the text entry is for.")
        label3.pack()

        entry1 = tk.Entry(self)
        entry1.pack()

        label4 = tk.Label(self, text="Sliders like the one below let you choose a number in a defined range.\n Click to grab the black rectangle and move and release it at your desired value.")
        label4.pack()

        self.test_scale = tk.Scale(self, from_=0, to=100, orient='horizontal', label='Slider Example', length=300)
        self.test_scale.set(0)  # Set the default value
        self.test_scale.pack()

        return_button = tk.Button(self, text="Return to Home Page", command=lambda: controller.show_frame(HomePage))
        return_button.pack(pady=25)

if __name__ == "__main__":
    app = App()
    app.mainloop()