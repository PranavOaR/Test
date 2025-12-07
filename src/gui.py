import customtkinter as ctk
from tkinter import messagebox, ttk
import tkinter as tk
from .database import DatabaseManager
import logging

# Set theme
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class FootballApp(ctk.CTk):
    def __init__(self, db_manager: DatabaseManager):
        super().__init__()

        self.db = db_manager
        self.title("⚽ Football League Management System")
        self.geometry("1100x700")

        # Configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create sidebar frame with widgets
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="FLMS", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(padx=20, pady=(20, 10))
        
        self.sidebar_button_1 = ctk.CTkButton(self.sidebar_frame, text="Manage Teams", command=lambda: self.select_frame("teams"))
        self.sidebar_button_1.pack(padx=20, pady=10)
        self.sidebar_button_2 = ctk.CTkButton(self.sidebar_frame, text="Matches", command=lambda: self.select_frame("matches"))
        self.sidebar_button_2.pack(padx=20, pady=10)
        self.sidebar_button_3 = ctk.CTkButton(self.sidebar_frame, text="Leaderboard", command=lambda: self.select_frame("leaderboard"))
        self.sidebar_button_3.pack(padx=20, pady=10)
        self.sidebar_button_4 = ctk.CTkButton(self.sidebar_frame, text="Manage Players", command=lambda: self.select_frame("players"))
        self.sidebar_button_4.pack(padx=20, pady=10)
        self.sidebar_button_5 = ctk.CTkButton(self.sidebar_frame, text="Manage Tournaments", command=lambda: self.select_frame("tournaments"))
        self.sidebar_button_5.pack(padx=20, pady=10)
        
        # Spacer to push bottom items down
        self.spacer = ctk.CTkLabel(self.sidebar_frame, text="", height=50)
        self.spacer.pack(fill="y", expand=True)

        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.pack(padx=20, pady=(10, 0), anchor="w")
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.pack(padx=20, pady=(10, 10))
        
        self.scaling_label = ctk.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.pack(padx=20, pady=(10, 0), anchor="w")
        self.scaling_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%", "150%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.set("100%")
        self.scaling_optionemenu.pack(padx=20, pady=(10, 20))
        

        # Main Content Area
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        self.frames = {}
        self.create_teams_frame()
        self.create_matches_frame()
        self.create_matches_frame()
        self.create_leaderboard_frame()
        self.create_players_frame()
        self.create_tournaments_frame()

        self.select_frame("teams")

    def select_frame(self, name):
        # Hide all frames
        for frame in self.frames.values():
            frame.grid_forget()
        # Show selected frame
        self.frames[name].grid(row=0, column=0, sticky="nsew")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)
        
        # Update Treeview font size manually as it doesn't scale automatically
        style = ttk.Style()
        new_font_size = int(10 * new_scaling_float) # Base size 10
        new_row_height = int(25 * new_scaling_float)
        style.configure("Treeview", font=('Segoe UI', new_font_size), rowheight=new_row_height)
        style.configure("Treeview.Heading", font=('Segoe UI', new_font_size, 'bold'))

    # ---------------- TEAMS FRAME ----------------
    def create_teams_frame(self):
        frame = ctk.CTkFrame(self.main_frame)
        self.frames["teams"] = frame
        frame.grid_columnconfigure(1, weight=1)

        # Header
        ctk.CTkLabel(frame, text="Manage Teams", font=ctk.CTkFont(size=24, weight="bold")).grid(row=0, column=0, columnspan=2, pady=20)

        # Form
        form_frame = ctk.CTkFrame(frame)
        form_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
        
        self.team_name_entry = ctk.CTkEntry(form_frame, placeholder_text="Team Name")
        self.team_name_entry.grid(row=0, column=0, padx=10, pady=10)
        self.coach_name_entry = ctk.CTkEntry(form_frame, placeholder_text="Coach Name")
        self.coach_name_entry.grid(row=0, column=1, padx=10, pady=10)
        self.year_entry = ctk.CTkEntry(form_frame, placeholder_text="Foundation Year")
        self.year_entry.grid(row=0, column=2, padx=10, pady=10)
        
        ctk.CTkButton(form_frame, text="Add Team", command=self.add_team).grid(row=0, column=3, padx=10, pady=10)
        ctk.CTkButton(form_frame, text="Delete Selected", fg_color="red", hover_color="darkred", command=self.delete_team).grid(row=0, column=4, padx=10, pady=10)

        # Table
        # CustomTkinter doesn't have a native Treeview, so we use ttk.Treeview with some styling
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b", borderwidth=0, font=('Segoe UI', 12), rowheight=30)
        style.map('Treeview', background=[('selected', '#1f538d')])
        style.configure("Treeview.Heading", background="#565b5e", foreground="white", relief="flat", font=('Segoe UI', 12, 'bold'))
        style.map("Treeview.Heading", background=[('active', '#3484F0')])

        self.team_tree = ttk.Treeview(frame, columns=("ID", "Name", "Coach", "Year"), show="headings", height=15)
        self.team_tree.heading("ID", text="ID")
        self.team_tree.heading("Name", text="Name")
        self.team_tree.heading("Coach", text="Coach")
        self.team_tree.heading("Year", text="Year")
        self.team_tree.column("ID", width=50)
        self.team_tree.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
        
        self.refresh_teams()

    def refresh_teams(self):
        for i in self.team_tree.get_children():
            self.team_tree.delete(i)
        try:
            teams = self.db.fetch_teams()
            for team in teams:
                # team: (id, name, coach, year, tour_id)
                self.team_tree.insert("", "end", values=(team[0], team[1], team[2], team[3]))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_team(self):
        name = self.team_name_entry.get()
        coach = self.coach_name_entry.get()
        year = self.year_entry.get()
        
        if not name or not coach:
            messagebox.showwarning("Input Error", "Name and Coach are required.")
            return
            
        try:
            year_val = int(year) if year else None
            self.db.add_team(name, coach, year_val)
            messagebox.showinfo("Success", "Team added!")
            self.refresh_teams()
            self.team_name_entry.delete(0, "end")
            self.coach_name_entry.delete(0, "end")
            self.year_entry.delete(0, "end")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_team(self):
        selected = self.team_tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a team to delete.")
            return
        
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this team?"):
            return

        try:
            item = self.team_tree.item(selected[0])
            team_id = item['values'][0]
            self.db.delete_team(team_id)
            messagebox.showinfo("Success", "Team deleted!")
            self.refresh_teams()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------- MATCHES FRAME ----------------
    def create_matches_frame(self):
        frame = ctk.CTkFrame(self.main_frame)
        self.frames["matches"] = frame
        frame.grid_columnconfigure(0, weight=1)

        # Tabs for Matches (Create vs Result)
        tabview = ctk.CTkTabview(frame)
        tabview.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        tabview.add("Match List")
        tabview.add("Create Match")
        tabview.add("Add Result")

        # -- Match List --
        self.match_tree = ttk.Treeview(tabview.tab("Match List"), columns=("ID", "Team1", "Team2", "Date", "Venue", "Status"), show="headings", height=15)
        self.match_tree.heading("ID", text="ID")
        self.match_tree.heading("Team1", text="Team 1")
        self.match_tree.heading("Team2", text="Team 2")
        self.match_tree.heading("Date", text="Date")
        self.match_tree.heading("Venue", text="Venue")
        self.match_tree.heading("Status", text="Status")
        self.match_tree.pack(fill="both", expand=True, padx=10, pady=10)
        ctk.CTkButton(tabview.tab("Match List"), text="Refresh", command=self.refresh_matches).pack(pady=10)

        # -- Create Match --
        cm_frame = ctk.CTkFrame(tabview.tab("Create Match"))
        cm_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.cm_team1_combo = ctk.CTkComboBox(cm_frame, values=[])
        self.cm_team1_combo.pack(pady=10)
        self.cm_team1_combo.set("Select Team 1")
        
        self.cm_team2_combo = ctk.CTkComboBox(cm_frame, values=[])
        self.cm_team2_combo.pack(pady=10)
        self.cm_team2_combo.set("Select Team 2")
        
        self.cm_date_entry = ctk.CTkEntry(cm_frame, placeholder_text="YYYY-MM-DD")
        self.cm_date_entry.pack(pady=10)
        
        self.cm_venue_entry = ctk.CTkEntry(cm_frame, placeholder_text="Venue")
        self.cm_venue_entry.pack(pady=10)
        
        ctk.CTkButton(cm_frame, text="Create Match", command=self.create_match).pack(pady=20)
        ctk.CTkButton(cm_frame, text="Refresh Teams", command=self.load_team_options).pack(pady=5)

        # -- Add Result --
        ar_frame = ctk.CTkFrame(tabview.tab("Add Result"))
        ar_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.ar_match_combo = ctk.CTkComboBox(ar_frame, values=[], width=300)
        self.ar_match_combo.pack(pady=10)
        self.ar_match_combo.set("Select Match")
        
        self.ar_goals1_entry = ctk.CTkEntry(ar_frame, placeholder_text="Team 1 Goals")
        self.ar_goals1_entry.pack(pady=10)
        
        self.ar_goals2_entry = ctk.CTkEntry(ar_frame, placeholder_text="Team 2 Goals")
        self.ar_goals2_entry.pack(pady=10)
        
        ctk.CTkButton(ar_frame, text="Submit Result", command=self.add_match_result).pack(pady=20)
        ctk.CTkButton(ar_frame, text="Refresh Matches", command=self.refresh_matches).pack(pady=5)

        self.match_label_map = {}
        self.team_name_map = {}

    def refresh_matches(self):
        # Clear tree
        for i in self.match_tree.get_children():
            self.match_tree.delete(i)
        
        self.match_label_map = {}
        match_labels = []
        
        try:
            matches = self.db.fetch_matches()
            for m in matches:
                # m: (id, t1_id, t1_name, t2_id, t2_name, date, venue, status)
                self.match_tree.insert("", "end", values=(m[0], m[2], m[4], m[5], m[6], m[7]))
                
                label = f"{m[0]}: {m[2]} vs {m[4]} ({m[5]})"
                self.match_label_map[label] = (m[0], m[1], m[3]) # id, t1_id, t2_id
                match_labels.append(label)
                
            self.ar_match_combo.configure(values=match_labels)
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_team_options(self):
        try:
            teams = self.db.fetch_teams()
            names = [t[1] for t in teams]
            self.team_name_map = {t[1]: t[0] for t in teams}
            self.cm_team1_combo.configure(values=names)
            self.cm_team2_combo.configure(values=names)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def create_match(self):
        t1_name = self.cm_team1_combo.get()
        t2_name = self.cm_team2_combo.get()
        date = self.cm_date_entry.get()
        venue = self.cm_venue_entry.get()
        
        if t1_name == t2_name:
            messagebox.showwarning("Error", "Teams must be different.")
            return
            
        if t1_name not in self.team_name_map or t2_name not in self.team_name_map:
             messagebox.showwarning("Error", "Select valid teams.")
             return

        try:
            self.db.create_match(self.team_name_map[t1_name], self.team_name_map[t2_name], date, venue)
            messagebox.showinfo("Success", "Match created!")
            self.refresh_matches()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_match_result(self):
        match_label = self.ar_match_combo.get()
        if match_label not in self.match_label_map:
            messagebox.showwarning("Error", "Select a valid match.")
            return
            
        match_data = self.match_label_map[match_label]
        match_id, t1_id, t2_id = match_data
        
        try:
            g1 = int(self.ar_goals1_entry.get())
            g2 = int(self.ar_goals2_entry.get())
            
            self.db.add_match_result(match_id, t1_id, g1, t2_id, g2)
            messagebox.showinfo("Success", "Result added!")
            self.refresh_matches()
            self.refresh_leaderboard()
        except ValueError:
            messagebox.showwarning("Error", "Goals must be numbers.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------- LEADERBOARD FRAME ----------------
    def create_leaderboard_frame(self):
        frame = ctk.CTkFrame(self.main_frame)
        self.frames["leaderboard"] = frame
        frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(frame, text="Leaderboard", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        
        self.lb_tree = ttk.Treeview(frame, columns=("Rank", "Team", "P", "W", "D", "L", "GF", "Pts"), show="headings", height=20)
        self.lb_tree.heading("Rank", text="#")
        self.lb_tree.heading("Team", text="Team")
        self.lb_tree.heading("P", text="P")
        self.lb_tree.heading("W", text="W")
        self.lb_tree.heading("D", text="D")
        self.lb_tree.heading("L", text="L")
        self.lb_tree.heading("GF", text="GF")
        self.lb_tree.heading("Pts", text="Pts")
        
        self.lb_tree.column("Rank", width=40)
        self.lb_tree.column("P", width=40)
        self.lb_tree.column("W", width=40)
        self.lb_tree.column("D", width=40)
        self.lb_tree.column("L", width=40)
        self.lb_tree.column("GF", width=50)
        self.lb_tree.column("Pts", width=50)
        
        self.lb_tree.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkButton(frame, text="Refresh", command=self.refresh_leaderboard).pack(pady=20)

    def refresh_leaderboard(self):
        for i in self.lb_tree.get_children():
            self.lb_tree.delete(i)
        try:
            rows = self.db.fetch_leaderboard()
            for idx, row in enumerate(rows, 1):
                # row: (id, name, played, w, d, l, gf, pts)
                self.lb_tree.insert("", "end", values=(idx, row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------- PLAYERS FRAME ----------------
    def create_players_frame(self):
        frame = ctk.CTkFrame(self.main_frame)
        self.frames["players"] = frame
        frame.grid_columnconfigure(1, weight=1)

        # Header
        ctk.CTkLabel(frame, text="Manage Players", font=ctk.CTkFont(size=24, weight="bold")).grid(row=0, column=0, columnspan=2, pady=20)

        # Form
        form_frame = ctk.CTkFrame(frame)
        form_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
        
        # Row 1
        self.p_name_entry = ctk.CTkEntry(form_frame, placeholder_text="Name")
        self.p_name_entry.grid(row=0, column=0, padx=5, pady=5)
        self.p_age_entry = ctk.CTkEntry(form_frame, placeholder_text="Age")
        self.p_age_entry.grid(row=0, column=1, padx=5, pady=5)
        self.p_gender_combo = ctk.CTkComboBox(form_frame, values=["M", "F"])
        self.p_gender_combo.set("M")
        self.p_gender_combo.grid(row=0, column=2, padx=5, pady=5)
        self.p_pos_entry = ctk.CTkEntry(form_frame, placeholder_text="Position")
        self.p_pos_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Row 2
        self.p_height_entry = ctk.CTkEntry(form_frame, placeholder_text="Height (cm)")
        self.p_height_entry.grid(row=1, column=0, padx=5, pady=5)
        self.p_weight_entry = ctk.CTkEntry(form_frame, placeholder_text="Weight (kg)")
        self.p_weight_entry.grid(row=1, column=1, padx=5, pady=5)
        self.p_jersey_entry = ctk.CTkEntry(form_frame, placeholder_text="Jersey No")
        self.p_jersey_entry.grid(row=1, column=2, padx=5, pady=5)
        self.p_team_combo = ctk.CTkComboBox(form_frame, values=[])
        self.p_team_combo.set("Select Team")
        self.p_team_combo.grid(row=1, column=3, padx=5, pady=5)
        
        # Buttons
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ctk.CTkButton(btn_frame, text="Add Player", command=self.add_player).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Update Selected", command=self.update_player).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Delete Selected", fg_color="red", hover_color="darkred", command=self.delete_player).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Clear Form", fg_color="gray", command=self.clear_player_form).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Refresh Teams", command=self.load_player_team_options).pack(side="left", padx=10)

        # Table
        self.player_tree = ttk.Treeview(frame, columns=("ID", "Name", "Age", "Gender", "Pos", "H", "W", "No", "Team"), show="headings", height=15)
        self.player_tree.heading("ID", text="ID")
        self.player_tree.heading("Name", text="Name")
        self.player_tree.heading("Age", text="Age")
        self.player_tree.heading("Gender", text="Gen")
        self.player_tree.heading("Pos", text="Pos")
        self.player_tree.heading("H", text="H(cm)")
        self.player_tree.heading("W", text="W(kg)")
        self.player_tree.heading("No", text="No")
        self.player_tree.heading("Team", text="Team")
        
        self.player_tree.column("ID", width=30)
        self.player_tree.column("Age", width=30)
        self.player_tree.column("Gender", width=30)
        self.player_tree.column("H", width=50)
        self.player_tree.column("W", width=50)
        self.player_tree.column("No", width=30)
        
        self.player_tree.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
        self.player_tree.bind("<<TreeviewSelect>>", self.on_player_select)
        
        self.refresh_players()
        self.load_player_team_options()

    def load_player_team_options(self):
        try:
            teams = self.db.fetch_teams()
            names = [t[1] for t in teams]
            self.team_name_map = {t[1]: t[0] for t in teams} # Update global map
            self.p_team_combo.configure(values=names)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def refresh_players(self):
        for i in self.player_tree.get_children():
            self.player_tree.delete(i)
        try:
            players = self.db.fetch_players()
            for p in players:
                # p: (id, name, age, gen, pos, h, w, no, tid, tname)
                self.player_tree.insert("", "end", values=p)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_player_select(self, event):
        selected = self.player_tree.selection()
        if not selected:
            return
        
        item = self.player_tree.item(selected[0])
        vals = item['values']
        # vals: (id, name, age, gen, pos, h, w, no, tid, tname)
        
        self.p_name_entry.delete(0, "end"); self.p_name_entry.insert(0, vals[1])
        self.p_age_entry.delete(0, "end"); self.p_age_entry.insert(0, vals[2])
        self.p_gender_combo.set(vals[3])
        self.p_pos_entry.delete(0, "end"); self.p_pos_entry.insert(0, vals[4])
        self.p_height_entry.delete(0, "end"); self.p_height_entry.insert(0, vals[5])
        self.p_weight_entry.delete(0, "end"); self.p_weight_entry.insert(0, vals[6])
        self.p_jersey_entry.delete(0, "end"); self.p_jersey_entry.insert(0, vals[7])
        self.p_team_combo.set(vals[9])

    def clear_player_form(self):
        self.p_name_entry.delete(0, "end")
        self.p_age_entry.delete(0, "end")
        self.p_pos_entry.delete(0, "end")
        self.p_height_entry.delete(0, "end")
        self.p_weight_entry.delete(0, "end")
        self.p_jersey_entry.delete(0, "end")
        self.p_team_combo.set("Select Team")

    def get_player_form_data(self):
        name = self.p_name_entry.get()
        age = self.p_age_entry.get()
        gender = self.p_gender_combo.get()
        pos = self.p_pos_entry.get()
        height = self.p_height_entry.get()
        weight = self.p_weight_entry.get()
        jersey = self.p_jersey_entry.get()
        tname = self.p_team_combo.get()
        
        if not (name and age and pos and height and weight and jersey and tname in self.team_name_map):
            messagebox.showwarning("Input Error", "All fields are required and Team must be valid.")
            return None
            
        try:
            return (name, int(age), gender, pos, float(height), float(weight), int(jersey), self.team_name_map[tname])
        except ValueError:
            messagebox.showwarning("Input Error", "Age, Height, Weight, Jersey must be numbers.")
            return None

    def add_player(self):
        data = self.get_player_form_data()
        if not data: return
        
        try:
            self.db.add_player(*data)
            messagebox.showinfo("Success", "Player added!")
            self.refresh_players()
            self.clear_player_form()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_player(self):
        selected = self.player_tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Select a player to update.")
            return

        data = self.get_player_form_data()
        if not data: return
        
        try:
            pid = self.player_tree.item(selected[0])['values'][0]
            self.db.update_player(pid, *data)
            messagebox.showinfo("Success", "Player updated!")
            self.refresh_players()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_player(self):
        selected = self.player_tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Select a player to delete.")
            return
            
        if not messagebox.askyesno("Confirm", "Delete this player?"):
            return

        try:
            pid = self.player_tree.item(selected[0])['values'][0]
            self.db.delete_player(pid)
            messagebox.showinfo("Success", "Player deleted!")
            self.refresh_players()
            self.clear_player_form()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------- TOURNAMENTS FRAME ----------------
    def create_tournaments_frame(self):
        frame = ctk.CTkFrame(self.main_frame)
        self.frames["tournaments"] = frame
        frame.grid_columnconfigure(1, weight=1)

        # Header
        ctk.CTkLabel(frame, text="Manage Tournaments", font=ctk.CTkFont(size=24, weight="bold")).grid(row=0, column=0, columnspan=2, pady=20)

        # Form
        form_frame = ctk.CTkFrame(frame)
        form_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
        
        # Row 1
        self.t_name_entry = ctk.CTkEntry(form_frame, placeholder_text="Tournament Name")
        self.t_name_entry.grid(row=0, column=0, padx=5, pady=5)
        self.t_type_combo = ctk.CTkComboBox(form_frame, values=["League", "Knockout"])
        self.t_type_combo.set("League")
        self.t_type_combo.grid(row=0, column=1, padx=5, pady=5)
        self.t_host_entry = ctk.CTkEntry(form_frame, placeholder_text="Host Country")
        self.t_host_entry.grid(row=0, column=2, padx=5, pady=5)
        
        # Row 2
        self.t_teams_entry = ctk.CTkEntry(form_frame, placeholder_text="No. of Teams")
        self.t_teams_entry.grid(row=1, column=0, padx=5, pady=5)
        self.t_matches_entry = ctk.CTkEntry(form_frame, placeholder_text="No. of Matches")
        self.t_matches_entry.grid(row=1, column=1, padx=5, pady=5)
        self.t_start_entry = ctk.CTkEntry(form_frame, placeholder_text="Start Date (YYYY-MM-DD)")
        self.t_start_entry.grid(row=1, column=2, padx=5, pady=5)
        self.t_end_entry = ctk.CTkEntry(form_frame, placeholder_text="End Date (YYYY-MM-DD)")
        self.t_end_entry.grid(row=1, column=3, padx=5, pady=5)
        
        # Buttons
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ctk.CTkButton(btn_frame, text="Add Tournament", command=self.add_tournament).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Update Selected", command=self.update_tournament).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Delete Selected", fg_color="red", hover_color="darkred", command=self.delete_tournament).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Clear Form", fg_color="gray", command=self.clear_tournament_form).pack(side="left", padx=10)

        # Table
        self.tourn_tree = ttk.Treeview(frame, columns=("ID", "Name", "Type", "Host", "Teams", "Matches", "Start", "End"), show="headings", height=15)
        self.tourn_tree.heading("ID", text="ID")
        self.tourn_tree.heading("Name", text="Name")
        self.tourn_tree.heading("Type", text="Type")
        self.tourn_tree.heading("Host", text="Host")
        self.tourn_tree.heading("Teams", text="Teams")
        self.tourn_tree.heading("Matches", text="Matches")
        self.tourn_tree.heading("Start", text="Start")
        self.tourn_tree.heading("End", text="End")
        
        self.tourn_tree.column("ID", width=30)
        self.tourn_tree.column("Teams", width=50)
        self.tourn_tree.column("Matches", width=50)
        
        self.tourn_tree.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
        self.tourn_tree.bind("<<TreeviewSelect>>", self.on_tourn_select)
        
        self.refresh_tournaments()

    def refresh_tournaments(self):
        for i in self.tourn_tree.get_children():
            self.tourn_tree.delete(i)
        try:
            tourns = self.db.fetch_tournaments()
            for t in tourns:
                # t: (id, name, type, host, teams, matches, start, end)
                self.tourn_tree.insert("", "end", values=t)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_tourn_select(self, event):
        selected = self.tourn_tree.selection()
        if not selected:
            return
        
        item = self.tourn_tree.item(selected[0])
        vals = item['values']
        
        self.t_name_entry.delete(0, "end"); self.t_name_entry.insert(0, vals[1])
        self.t_type_combo.set(vals[2])
        self.t_host_entry.delete(0, "end"); self.t_host_entry.insert(0, vals[3])
        self.t_teams_entry.delete(0, "end"); self.t_teams_entry.insert(0, vals[4])
        self.t_matches_entry.delete(0, "end"); self.t_matches_entry.insert(0, vals[5])
        self.t_start_entry.delete(0, "end"); self.t_start_entry.insert(0, vals[6])
        self.t_end_entry.delete(0, "end"); self.t_end_entry.insert(0, vals[7])

    def clear_tournament_form(self):
        self.t_name_entry.delete(0, "end")
        self.t_host_entry.delete(0, "end")
        self.t_teams_entry.delete(0, "end")
        self.t_matches_entry.delete(0, "end")
        self.t_start_entry.delete(0, "end")
        self.t_end_entry.delete(0, "end")

    def get_tourn_form_data(self):
        name = self.t_name_entry.get()
        ttype = self.t_type_combo.get()
        host = self.t_host_entry.get()
        teams = self.t_teams_entry.get()
        matches = self.t_matches_entry.get()
        start = self.t_start_entry.get()
        end = self.t_end_entry.get()
        
        if not (name and host and teams and matches and start and end):
            messagebox.showwarning("Input Error", "All fields are required.")
            return None
            
        try:
            return (name, ttype, host, int(teams), int(matches), start, end)
        except ValueError:
            messagebox.showwarning("Input Error", "Teams and Matches must be numbers.")
            return None

    def add_tournament(self):
        data = self.get_tourn_form_data()
        if not data: return
        
        try:
            self.db.add_tournament(*data)
            messagebox.showinfo("Success", "Tournament added!")
            self.refresh_tournaments()
            self.clear_tournament_form()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_tournament(self):
        selected = self.tourn_tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Select a tournament to update.")
            return

        data = self.get_tourn_form_data()
        if not data: return
        
        try:
            tid = self.tourn_tree.item(selected[0])['values'][0]
            self.db.update_tournament(tid, *data)
            messagebox.showinfo("Success", "Tournament updated!")
            self.refresh_tournaments()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_tournament(self):
        selected = self.tourn_tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Select a tournament to delete.")
            return
            
        if not messagebox.askyesno("Confirm", "Delete this tournament?"):
            return

        try:
            tid = self.tourn_tree.item(selected[0])['values'][0]
            self.db.delete_tournament(tid)
            messagebox.showinfo("Success", "Tournament deleted!")
            self.refresh_tournaments()
            self.clear_tournament_form()
        except Exception as e:
            messagebox.showerror("Error", str(e))
