#!/usr/bin/python3

import sqlite3
import sys
import kivy
kivy.require('1.11.1')

from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


# Set constants
HEADER_FONT_SIZE = 40
BUTTON_FONT_SIZE = 18

# Connect to our database.
def read_from_db():
	pass


# Main Menu Screen.
class MainMenu(FloatLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.w_main_menu()

	# Contains main menu widgets.
	def w_main_menu(self):
		# Define our title label.
		self.label_title = Label(text='GainZ TrackeR', 
				font_size=50, bold=True, 
				size_hint=(.8, .2), pos_hint={'x':.1, 'y':.8})

		# Define our buttons.
		# Update button and binding.
		self.button_update = Button(text='Update Stats', 
				font_size=BUTTON_FONT_SIZE, bold=True, 
				size_hint=(.8, .1), pos_hint={'x':.1, 'y':.7})
		self.button_update.bind(on_press=self.switch_to_update)

		# Current button and binding.
		self.button_current = Button(text='Current Stats', 
				font_size=BUTTON_FONT_SIZE, bold=True, 
				size_hint=(.8, .1), pos_hint={'x':.1, 'y':.55})
		self.button_current.bind(on_press=self.switch_to_current)

		# Quit button and binding.
		self.button_quit = Button(text='Quit', 
				font_size=BUTTON_FONT_SIZE, bold=True, 
				size_hint=(.8, .1), pos_hint={'x':.1, 'y':.4})
		self.button_quit.bind(on_press=sys.exit)

		# Add our widgets to the layout.
		self.add_widget(self.label_title)
		self.add_widget(self.button_update)
		self.add_widget(self.button_current)
		self.add_widget(self.button_quit)

	# Transition to UpdateStats screen.
	def switch_to_update(self, event):
		root.screen_manager.current = 'update'
		root.screen_manager.transition.direction = 'up'

	# Transition to CurrentStats screen.
	def switch_to_current(self, event):
		root.screen_manager.current = 'current'
		root.screen_manager.transition.direction = 'up'

# Update Stats Screen.
class UpdateStats(FloatLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.u_top_widgets()
		self.u_popup_widget()
		self.u_bot_widgets()

		self.add_widget(self.u_top_layout)
		self.add_widget(self.u_bot_layout)
		

	# Top layout widgets.
	def u_top_widgets(self):
		# Define grid layout to contain our top widgets.
		self.u_top_layout = GridLayout(size_hint_x=1, size_hint_y=.3,
				pos_hint={'y':.7})
		self.u_top_layout.cols = 1

		# Update stats header. 
		self.u_label_header = Label(text='Update Stats',
				font_size=HEADER_FONT_SIZE, bold=True)

		# Select exercise button.
		self.u_button_select = Button(text='Select Exercise',
				font_size=BUTTON_FONT_SIZE, bold=True)

		# Text changes depending on currently selected exercise.
		self.u_label_exercise = Label(text="Bench Press",
				font_size=25, bold=True)

		# Add all widgets to top layout.
		self.u_top_layout.add_widget(self.u_label_header)
		self.u_top_layout.add_widget(self.u_button_select)
		self.u_top_layout.add_widget(self.u_label_exercise) 

	# Pop up window.
	def u_popup_widget(self):
		# Define grid layout for popup widget.
		self.u_popup_layout = GridLayout()
		self.u_popup_layout.cols = 1

		# Define popup widget.
		self.u_popup = Popup(title='Choose an exercise', 
				content=self.u_popup_layout,
				size_hint=(.8,.8))
		
		# Create buttons for popup layout. 
		# Placeholder. Code needs to be changed for SQLite3.
		self.example = ['Bench Press', 'Lat Pulldown', 'Triceps', 'Biceps']
		for each in self.example:
			button = Button(text=each)
			self.u_popup_layout.add_widget(button)

		# Bind function call to button from u_top_widgets.
		self.u_button_select.bind(on_press=self.u_popup.open)

	# Bottom layout widgets.
	def u_bot_widgets(self):
		# Define grid layout to contain our bottom widgets. 
		self.u_bot_layout = GridLayout(size_hint_x=1, size_hint_y=.1,
	 			pos_hint={'y':0})
		self.u_bot_layout.cols = 1

		# Back to main screen button and binding.
		self.u_button_back = Button(text='Back', font_size=BUTTON_FONT_SIZE,
				size_hint=(1,1), bold=True)
		self.u_button_back.bind(on_press=self.u_back_call)

		# Add back button widget to grid layout. 
		self.u_bot_layout.add_widget(self.u_button_back)

	# Function call for back button.
	def u_back_call(self, event):
		root.screen_manager.current = 'menu'
		root.screen_manager.transition.direction = 'down'


# Current Stats Screen.
class CurrentStats(FloatLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.c_bot_widgets()

		self.add_widget(self.c_bot_layout)

	# Bottom Layout Widgets.
	def c_bot_widgets(self):
		# Define grid layout to contain our widgets. 
		self.c_bot_layout = GridLayout(size_hint_x=1, size_hint_y=.1,
				pos_hint={'y':0})
		self.c_bot_layout.cols = 1 

		# Back to main screen button and binding. 
		self.c_button_back = Button(text='Back', font_size=BUTTON_FONT_SIZE,
				size_hint=(1,1), bold=True)
		self.c_button_back.bind(on_press=self.c_back_call)

		# Add back button widget to grid layout. 
		self.c_bot_layout.add_widget(self.c_button_back)

	# Function call for back button.
	def c_back_call(self, event):
		root.screen_manager.current = 'menu'
		root.screen_manager.transition.direction = 'down'


# This is our Main App and Screen Manager.
class Main(App):
	def build(self):
		# Screen Manager which will hold all of our windows/screens.
		self.screen_manager = ScreenManager()

		# Main menu screen.
		self.main_menu = MainMenu()
		self.s_main_menu = Screen(name='menu')
		self.s_main_menu.add_widget(self.main_menu)
		self.screen_manager.add_widget(self.s_main_menu)

		# Update Stats screen. This is where we can update our new stats. 
		self.update_stats = UpdateStats()
		self.s_update_stats = Screen(name='update')
		self.s_update_stats.add_widget(self.update_stats)
		self.screen_manager.add_widget(self.s_update_stats)

		# Current Stats screen. 
		# This shows us what our current stats are for all exercises. 
		self.current_stats = CurrentStats()
		self.s_current_stats = Screen(name='current')
		self.s_current_stats.add_widget(self.current_stats)
		self.screen_manager.add_widget(self.s_current_stats)

		return self.screen_manager


# Run our app.
if __name__ == '__main__':
	root = Main()
	root.run()
