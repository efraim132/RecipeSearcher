import asciimatics.screen
import asciimatics.scene
import asciimatics.effects
import asciimatics.widgets
from asciimatics.widgets import Frame, ListBox, Layout, Divider, Label
from asciimatics.screen import Screen
from datetime import datetime
import time
import threading
from models import load_recipes, load_users
import os

#TODO: Fix vertical divider between sections
#TODO: Add status for database when implemented
class DashboardFrame(Frame):
    def __init__(self, screen):
        super(DashboardFrame, self).__init__(
            screen,
            screen.height,
            screen.width,
            has_border=True,
            title="Recipe Finder Dashboard"
        )
        
        # Create the main layout
        layout = Layout([1, 1, 1], fill_frame=True)
        self.add_layout(layout)
        
        # Left panel - Recipe Statistics
        layout.add_widget(Label("Recipe Statistics", align="^"), 0)
        layout.add_widget(Divider(), 0)
        self.recipe_labels = []
        for _ in range(6):  # Create labels for each stat
            label = Label("", align="^")
            self.recipe_labels.append(label)
            layout.add_widget(label, 0)
        
        # Add vertical divider between Recipe Statistics and User Statistics
        layout.add_widget(Divider(draw_line=True, height=screen.height), 0)
        
        # Middle panel - User Statistics
        layout.add_widget(Label("User Statistics", align="^"), 1)
        layout.add_widget(Divider(), 1)
        self.user_labels = []
        for _ in range(3):  # Create labels for each stat
            label = Label("", align="^")
            self.user_labels.append(label)
            layout.add_widget(label, 1)
        
        # Add vertical divider between User Statistics and Activity Log
        layout.add_widget(Divider(draw_line=False, height=screen.height), 1)
        
        # Right panel - Activity Log
        layout.add_widget(Label("Activity Log", align="^"), 2)
        layout.add_widget(Divider(), 2)
        self.log = ListBox(
            height=screen.height - 8,
            options=[],
            name="log"
        )
        layout.add_widget(self.log, 2)
        
        # Add a divider between sections
        layout.add_widget(Divider(), 0)
        layout.add_widget(Divider(), 1)
        layout.add_widget(Divider(), 2)
        
        # Footer with timestamp
        self.timestamp = Label("", align="^")
        layout.add_widget(self.timestamp, 0)
        layout.add_widget(self.timestamp, 1)
        layout.add_widget(self.timestamp, 2)
        
        self.fix()

    def update(self, frame_no):
        # Update recipe statistics
        recipes = load_recipes()
        recipe_stats = [
            f"Total Recipes: {len(recipes)}",
            f"High Protein: {sum(1 for r in recipes if 'high_protein' in r['dietary_requirements'])}",
            f"Low Carb: {sum(1 for r in recipes if 'low_carb' in r['dietary_requirements'])}",
            f"Keto: {sum(1 for r in recipes if 'keto' in r['dietary_requirements'])}",
            f"Vegan: {sum(1 for r in recipes if 'vegan' in r['dietary_requirements'])}",
            f"Low Calorie: {sum(1 for r in recipes if 'low_calorie' in r['dietary_requirements'])}"
        ]
        for label, stat in zip(self.recipe_labels, recipe_stats):
            label.text = stat
        
        # Update user statistics
        users = load_users()
        user_stats = [
            f"Total Users: {len(users)}",
            f"Admin Users: {sum(1 for u in users.values() if u.username == 'admin')}",
            f"Regular Users: {sum(1 for u in users.values() if u.username != 'admin')}"
        ]
        for label, stat in zip(self.user_labels, user_stats):
            label.text = stat
        
        # Update timestamp
        self.timestamp.text = f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        # Update log if there are new entries
        if os.path.exists('activity.log'):
            with open('activity.log', 'r') as f:
                log_entries = f.readlines()[-10:]  # Get last 10 entries
                self.log.options = [(entry.strip(), entry.strip()) for entry in log_entries]
        
        super(DashboardFrame, self).update(frame_no)

def log_activity(message):
    with open('activity.log', 'a') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"[{timestamp}] {message}\n")

def run_dashboard():
    try:
        screen = Screen.open()
        scene = asciimatics.scene.Scene(
            [DashboardFrame(screen)],
            -1,
            name="Dashboard"
        )
        screen.play([scene], stop_on_resize=True)
    except Exception as e:
        print(f"Dashboard error: {str(e)}")

def start_dashboard():
    dashboard_thread = threading.Thread(target=run_dashboard)
    dashboard_thread.daemon = True
    dashboard_thread.start()

if __name__ == "__main__":
    start_dashboard()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass