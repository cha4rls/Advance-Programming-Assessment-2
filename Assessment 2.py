import requests
import tkinter as tk
from tkinter import messagebox, Listbox, Scrollbar

class SportsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sports Team Information App")
        self.root.geometry("850x500")
        self.root.resizable(False, False)  # Make the window not resizable

        self.team_label = tk.Label(root, text="Enter Team Name:")
        self.team_label.pack()

        self.team_entry = tk.Entry(root)
        self.team_entry.pack()

        self.search_button = tk.Button(root, text="Search", command=self.search_team)
        self.search_button.pack()

        self.team_info_label = tk.Label(root, text="Team Information:")
        self.team_info_label.pack()

        self.team_info_text = tk.Text(root, height=5, width=40)
        self.team_info_text.pack()

        self.team_image_label = tk.Label(root)
        self.team_image_label.pack()

        self.players_label = tk.Label(root, text="Players:")
        self.players_label.pack()

        self.players_listbox = Listbox(root, selectmode=tk.SINGLE, height=5, width=40)
        self.players_listbox.pack()

        self.scrollbar = Scrollbar(root, command=self.players_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.players_listbox.config(yscrollcommand=self.scrollbar.set)

    def search_team(self):
        team_name = self.team_entry.get()
        if team_name:
            team_info, team_image, players = self.get_team_info(team_name)
            if team_info:
                self.team_info_text.delete(1.0, tk.END)
                self.team_info_text.insert(tk.END, team_info)

                if team_image:
                    self.show_team_image(team_image)

                self.populate_players_list(players)
            else:
                messagebox.showerror("Error", "Team not found or API error.")
        else:
            messagebox.showwarning("Warning", "Please enter a team name.")

    def get_team_info(self, team_name):
        api_url = "https://www.thesportsdb.com/api/v1/json/3/searchteams.php"
        params = {"t": team_name}
        try:
            response = requests.get(api_url, params=params)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            data = response.json()
            teams = data.get("teams", [])

            if teams:
                team = teams[0]
                team_info = f"Team Name: {team['strTeam']}\nSport: {team['strSport']}\nStadium: {team['strStadium']}"
                team_image = team['strTeamBadge'] if 'strTeamBadge' in team else None
                players = self.get_players(team['idTeam'])
                return team_info, team_image, players
            else:
                return None, None, None
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")
            return None, None, None
        except Exception as e:
            print(f"Error: {e}")
            return None, None, None

    def get_players(self, team_id):
        api_url = "https://www.thesportsdb.com/api/v1/json/3/lookup_all_players.php"
        params = {"id": team_id}
        try:
            response = requests.get(api_url, params=params)
            response.raise_for_status()
            data = response.json()
            return [player['strPlayer'] for player in data.get('player', [])]
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")
            return []
        except Exception as e:
            print(f"Error: {e}")
            return []

    def show_team_image(self, image_url):
        response = requests.get(image_url)
        img_data = response.content

        image = tk.PhotoImage(data=img_data)
        self.team_image_label.config(image=image, width=image.width(), height=image.height())
        self.team_image_label.image = image

    def populate_players_list(self, players):
        self.players_listbox.delete(0, tk.END)
        for player in players:
            self.players_listbox.insert(tk.END, player)

if __name__ == "__main__":
    root = tk.Tk()
    app = SportsApp(root)
    root.mainloop()