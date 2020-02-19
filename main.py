#!/usr/bin/python3
import sys
import kivy
kivy.require('1.11.1')

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from sqlite_funcs import *

# Set constants
HEADER_FONT_SIZE = 40
BUTTON_FONT_SIZE = 18


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
		self.u_mid_widgets()
		self.u_bot_widgets()

		self.add_widget(self.u_top_layout)
		self.add_widget(self.u_mid_layout)
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
		# Initialise our popup widget.
		self.u_popup_widget()
		# Bind popup widget to select button.
		self.u_button_select.bind(on_press=self.u_popup.open)

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
		self.u_popup_layout = GridLayout(size_hint_y=None)
		self.u_popup_layout.cols = 1
		self.u_popup_layout.bind(
				minimum_height=self.u_popup_layout.setter('height'))

		# Define scroll view and grid to scroll widget. 
		self.u_popup_scroll = ScrollView(size_hint=(1, 1), 
				size=self.u_popup_layout.size)
		self.u_popup_scroll.add_widget(self.u_popup_layout)

		# Create buttons for popup layout. 
		# Get list of exercises from database.
		self.exercise_list = db_con.get_tables()
		# Index 1 of list contains exercises with spaces in between words. 
		for each in self.exercise_list[1]:
			button = Button(text=each, size_hint_y=None, height=80)
			button.bind(on_press=lambda event, exer = each: self.u_select_call(event, exer))
			self.u_popup_layout.add_widget(button)

		# Define popup widget.
		self.u_popup = Popup(title='Choose an exercise', 
				content=self.u_popup_scroll,
				size_hint=(.8,.8))

	# Middle layout widgets where our main update functionality is. 
	def u_mid_widgets(self):
		# Define float layout for mid section.
		self.u_mid_layout = FloatLayout(size_hint=(1,.5), pos_hint={'y':.2})

		# Define labels.
		self.label_weight = Label(text='Weight', size_hint=(.2,.1), 
				pos_hint={'y':.85, 'x':.075}, halign='right')
		self.label_sets = Label(text='Sets', size_hint=(.2,.1), 
				pos_hint={'y':.85, 'x':.45})
		self.label_reps1 = Label(text='Set 1', size_hint=(.2,.1), 
				pos_hint={'y':.7, 'x':.075})
		self.label_reps2 = Label(text='Set 2', size_hint=(.2,.1), 
				pos_hint={'y':.7, 'x':.45})
		self.label_reps3 = Label(text='Set 3', size_hint=(.2,.1), 
				pos_hint={'y':.55, 'x':.075})
		self.label_reps4 = Label(text='Set 4', size_hint=(.2,.1), 
				pos_hint={'y':.55, 'x':.45})
		self.label_reps5 = Label(text='Set 5', size_hint=(.2,.1), 
				pos_hint={'y':.4, 'x':.075})
		self.label_reps6 = Label(text='Set 6', size_hint=(.2,.1), 
				pos_hint={'y':.4, 'x':.45})
		self.label_reps7 = Label(text='Set 7', size_hint=(.2,.1), 
				pos_hint={'y':.25, 'x':.075})
		self.label_reps8 = Label(text='Set 8', size_hint=(.2,.1), 
				pos_hint={'y':.25, 'x':.45})
		self.label_reps9 = Label(text='Set 9', size_hint=(.2,.1), 
				pos_hint={'y':.1, 'x':.075})
		self.label_reps10 = Label(text='Set 10', size_hint=(.2,.1), 
				pos_hint={'y':.1, 'x':.45})

		# Define text inputs.
		self.input_weight = TextInput(size_hint=(.2,.1), 
				pos_hint={'y':.85, 'x':.25}, multiline=False)
		self.input_sets = TextInput(size_hint=(.2,.1), 
				pos_hint={'y':.85, 'x':.65}, multiline=False)
		self.input_reps1 = TextInput(size_hint=(.2,.1), 
				pos_hint={'y':.7, 'x':.25}, multiline=False)
		self.input_reps2 = TextInput(size_hint=(.2,.1), 
				pos_hint={'y':.7, 'x':.65}, multiline=False)
		self.input_reps3 = TextInput(size_hint=(.2,.1), 
				pos_hint={'y':.55, 'x':.25}, multiline=False)
		self.input_reps4 = TextInput(size_hint=(.2,.1), 
				pos_hint={'y':.55, 'x':.65}, multiline=False)
		self.input_reps5 = TextInput(size_hint=(.2,.1), 
				pos_hint={'y':.4, 'x':.25}, multiline=False)
		self.input_reps6 = TextInput(size_hint=(.2,.1), 
				pos_hint={'y':.4, 'x':.65}, multiline=False)
		self.input_reps7 = TextInput(size_hint=(.2,.1), 
				pos_hint={'y':.25, 'x':.25}, multiline=False)
		self.input_reps8 = TextInput(size_hint=(.2,.1), 
				pos_hint={'y':.25, 'x':.65}, multiline=False)
		self.input_reps9 = TextInput(size_hint=(.2,.1), 
				pos_hint={'y':.1, 'x':.25}, multiline=False)
		self.input_reps10 = TextInput(size_hint=(.2,.1), 
				pos_hint={'y':.1, 'x':.65}, multiline=False)

		# Add widgets to layout.
		self.u_mid_layout.add_widget(self.label_weight)
		self.u_mid_layout.add_widget(self.label_sets)
		self.u_mid_layout.add_widget(self.label_reps1)
		self.u_mid_layout.add_widget(self.label_reps2)
		self.u_mid_layout.add_widget(self.label_reps3)
		self.u_mid_layout.add_widget(self.label_reps4)
		self.u_mid_layout.add_widget(self.label_reps5)
		self.u_mid_layout.add_widget(self.label_reps6)
		self.u_mid_layout.add_widget(self.label_reps7)
		self.u_mid_layout.add_widget(self.label_reps8)
		self.u_mid_layout.add_widget(self.label_reps9)
		self.u_mid_layout.add_widget(self.label_reps10)

		self.u_mid_layout.add_widget(self.input_weight)
		self.u_mid_layout.add_widget(self.input_sets)
		self.u_mid_layout.add_widget(self.input_reps1)
		self.u_mid_layout.add_widget(self.input_reps2)
		self.u_mid_layout.add_widget(self.input_reps3)
		self.u_mid_layout.add_widget(self.input_reps4)
		self.u_mid_layout.add_widget(self.input_reps5)
		self.u_mid_layout.add_widget(self.input_reps6)
		self.u_mid_layout.add_widget(self.input_reps7)
		self.u_mid_layout.add_widget(self.input_reps8)
		self.u_mid_layout.add_widget(self.input_reps9)
		self.u_mid_layout.add_widget(self.input_reps10)

	# Bottom layout widgets.
	def u_bot_widgets(self):
		# Define grid layout to contain our bottom widgets. 
		self.u_bot_layout = GridLayout(size_hint_x=1, size_hint_y=.2,
	 			pos_hint={'y':0})
		self.u_bot_layout.cols = 1

		# Update the selected stat to database.
		self.u_button_update = Button(text='Update', font_size=BUTTON_FONT_SIZE,
				bold=True)
		# Back to main screen button and binding.
		self.u_button_back = Button(text='Back', font_size=BUTTON_FONT_SIZE,
				bold=True)
		self.u_button_back.bind(on_press=self.u_back_call)

		# Add back button widget to grid layout. 
		self.u_bot_layout.add_widget(self.u_button_update)
		self.u_bot_layout.add_widget(self.u_button_back)

	# Call back for popup widget buttons.
	def u_select_call(self, event, exercise):

		latest_stats = db_con.get_latest(exercise)
		# Change text to reflect exercise picked. 
		self.u_label_exercise.text = exercise

		# Delete any text form text input widgets.
		self.input_weight.text = ""
		self.input_sets.text = ""
		self.input_reps1.text = ""
		self.input_reps2.text = ""
		self.input_reps3.text = ""
		self.input_reps4.text = ""
		self.input_reps5.text = ""
		self.input_reps6.text = ""
		self.input_reps7.text = ""
		self.input_reps8.text = ""
		self.input_reps9.text = ""
		self.input_reps10.text = ""

		# Insert stats from database into text input.
		self.input_weight.text = str(latest_stats[1])
		self.input_sets.text = str(latest_stats[2])
		self.input_reps1.text = str(latest_stats[3])
		self.input_reps2.text = str(latest_stats[4])
		self.input_reps3.text = str(latest_stats[5])
		self.input_reps4.text = str(latest_stats[6])
		self.input_reps5.text = str(latest_stats[7])
		self.input_reps6.text = str(latest_stats[8])
		self.input_reps7.text = str(latest_stats[9])
		self.input_reps8.text = str(latest_stats[10])
		self.input_reps9.text = str(latest_stats[11])
		self.input_reps10.text = str(latest_stats[12])

		# Close the popup upon button click.
		self.u_popup.dismiss()

	# Function call for back button.
	def u_back_call(self, event):
		root.screen_manager.current = 'menu'
		root.screen_manager.transition.direction = 'down'


# Current Stats Screen.
class CurrentStats(FloatLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.c_top_widgets()
		self.c_mid_widgets()
		self.c_bot_widgets()

		self.add_widget(self.c_top_layout)
		self.add_widget(self.c_mid_scroll)
		self.add_widget(self.c_bot_layout)

	# Top Layout Widgets. 
	def c_top_widgets(self):
		# Define grid layout to contain our widgets. 
		self.c_top_layout = GridLayout(size_hint_x=1, size_hint_y=.1,
				pos_hint={'y':.9})
		self.c_top_layout.cols = 1

		# Define header Current Stats
		self.c_label_header = Label(text='Current Stats', 
			font_size=HEADER_FONT_SIZE, bold=True)

		# Place widget to layout.
		self.c_top_layout.add_widget(self.c_label_header)

	# Mid Layout Widgets.
	def c_mid_widgets(self):
		# Define grid layout to contain our widgets. 
		self.c_mid_layout = GridLayout(size_hint_y=None)
		self.c_mid_layout.cols = 1
		self.c_mid_layout.bind(
				minimum_height=self.c_mid_layout.setter('height'))

		# Get list of exercises from database.
		exercise_list = db_con.get_tables()

		for exercise in exercise_list[1]:
			temp_layout =  FloatLayout(size_hint_y=None, height=200)
			temp_label = Label(text=exercise, size_hint_y=None, height=80)
			temp_layout.add_widget(temp_label)
			self.c_mid_layout.add_widget(temp_layout) 

		# Define scroll layout.
		self.c_mid_scroll = ScrollView(size_hint=(1,.8), pos_hint={'y':.1})
		self.c_mid_scroll.add_widget(self.c_mid_layout)

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
		Window.size = (393, 786)
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
	db_con = ConnectDatabase()
	root.run()
