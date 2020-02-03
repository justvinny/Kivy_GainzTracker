import kivy
kivy.require('1.11.1')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen

import gym_csv as gc # Simple module made to convert CSV files into dictionaries and vice-versa.

exercises = {} # Dictionary to be used for reading and writing to csv file.
gc.read_from_data(exercises) # Getting data from csv file and save them inside exercises dictionary.


# Main screen for the screen manager.
class MainWindow(FloatLayout):
	# Main Menu Widgets
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.add_widget(Label(text='GainZ Tracker', font_size=100, size_hint=(1,0.25),
							  pos_hint={'top':1}, bold=True))

		self.buttonUpd = Button(text='Update Stats', size_hint=(0.8,0.2), pos_hint={'x':.1, 'top':.76})
		self.buttonUpd.bind(on_press=self.update_stats)
		self.add_widget(self.buttonUpd)

		self.buttonCurrent = Button(text='Current Stats', size_hint=(0.8,0.2), pos_hint={'x':.1, 'top':.51})
		self.buttonCurrent.bind(on_press=self.current_stats)
		self.add_widget(self.buttonCurrent)

		self.buttonExit = Button(text='Exit', size_hint=(0.8,0.2), pos_hint={'x':.1, 'top':.26})
		self.buttonExit.bind(on_press=self.exit_app)
		self.add_widget(self.buttonExit)

		buttons = [self.buttonUpd, self.buttonCurrent, self.buttonExit]

		for each in buttons:

			each.font_size = 60
			each.bold = True

	# Functions binded to buttons for screen transition.
	def update_stats(self, instance):
		gymApp.screen_manager.current ='upd'
		gymApp.screen_manager.transition.direction = 'up'

	def current_stats(self, instance):
		gymApp.screen_manager.current ='curr'
		gymApp.screen_manager.transition.direction = 'up'

	def exit_app(self, instance):
		gymApp.stop()


# New window for updating stats.
class UpdateWindow(FloatLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.add_widget(Label(text='Update Stats', size_hint=(1,.1), pos_hint={'top':1},
						bold=True, font_size=40))

		self.choose_exercise()
		self.update_stats()

		self.backButton = Button(text='Back to Main Menu', size_hint=(1,.1), pos_hint={'top':.1})
		self.backButton.bind(on_press=self.update_backto)
		self.add_widget(self.backButton)

	# Main frame to choose exercise to update.
	def choose_exercise(self):
		self.button_dict = {}

		outer_grid = FloatLayout()

		new_grid = GridLayout(size_hint=(1,.8), pos_hint={'x':0,'top':1})
		new_grid.cols = 2

		for each in exercises.keys():
			self.button_dict.setdefault(each, Button(text=each, on_press=lambda *args, ea=each: self.exercise_call(args, ea)))
			new_grid.add_widget(self.button_dict[each])


		outer_grid.add_widget(new_grid)

		self.popout = Popup(title='Pick an exercise', content=outer_grid, size_hint=(.9,.9))

		exit_popup = Button(text='Back', size_hint=(1,.2), pos_hint={'x':0, 'top':.2})
		exit_popup.bind(on_press=self.popout.dismiss)
		outer_grid.add_widget(exit_popup)

		self.main_button = Button(text='Select Exercise', size_hint=(1,.1), pos_hint={'top':.9})
		self.main_button.bind(on_press=self.popout.open)
		self.add_widget(self.main_button)

	def exercise_call(self, instance, exer):
		self.weight.text = exercises[exer]['Weight']
		self.sets.text = exercises[exer]['Sets']
		self.reps.text = exercises[exer]['Reps']
		self.amrap.text = exercises[exer]['AMRAP']
		self.current_exercise.color = (1,1,1,1)
		self.current_exercise.text = exer
		self.popout.dismiss()

	def update_stats(self):
		self.grid_update = GridLayout(size_hint=(1,.7), pos_hint={'top':.8})
		self.grid_update.cols = 2

		self.grid_update.add_widget(Label(text='Current Exercise'))
		self.current_exercise = Label(text=' ')
		self.grid_update.add_widget(self.current_exercise)

		self.grid_update.add_widget(Label(text='Weight'))
		self.weight = TextInput(multiline=False)
		self.grid_update.add_widget(self.weight)

		self.grid_update.add_widget(Label(text='Sets'))
		self.sets = TextInput(multiline=False)
		self.grid_update.add_widget(self.sets)

		self.grid_update.add_widget(Label(text='Reps'))
		self.reps = TextInput(multiline=False)
		self.grid_update.add_widget(self.reps)

		self.grid_update.add_widget(Label(text='AMRAP'))
		self.amrap = TextInput(multiline=False)
		self.grid_update.add_widget(self.amrap)

		self.update_this = Button(text='Update')
		self.update_this.bind(on_press=self.call_update)
		self.grid_update.add_widget(self.update_this)

		self.clear_this = Button(text='Clear')
		self.clear_this.bind(on_press=self.call_clear)
		self.grid_update.add_widget(self.clear_this)

		self.add_widget(self.grid_update)

	def call_update(self, instance):

		if self.weight.text.isdecimal() and self.sets.text.isdecimal() and self.reps.text.isdecimal() and self.amrap.text.isdecimal():
			if len(self.weight.text) <= 3 and len(self.sets.text) <= 3 and len(self.reps.text) <= 3 and len(self.amrap.text) <= 3:
				exercises[self.current_exercise.text]['Weight'] = self.weight.text
				exercises[self.current_exercise.text]['Sets'] = self.sets.text
				exercises[self.current_exercise.text]['Reps'] = self.reps.text
				exercises[self.current_exercise.text]['AMRAP'] = self.amrap.text

				gc.write_to_data(exercises)

				self.weight.text = ''
				self.sets.text = ''
				self.reps.text = ''
				self.amrap.text = ''
				self.current_exercise.color = (0,1,0,1)
				self.current_exercise.text = 'Updated!'


			else:
				self.weight.text = ''
				self.sets.text = ''
				self.reps.text = ''
				self.amrap.text = ''
				self.current_exercise.color = (1,0,0,1)
				self.current_exercise.text = 'Maximum 3 digit length: 0 - 999.'

		else:
			self.weight.text = ''
			self.sets.text = ''
			self.reps.text = ''
			self.amrap.text = ''
			self.current_exercise.color = (1,0,0,1)
			self.current_exercise.text = 'Please enter a decimal'

	def call_clear(self, instance):
		self.weight.text = ''
		self.sets.text = ''
		self.reps.text = ''
		self.amrap.text = ''
		self.current_exercise.color = (1,1,1,1)
		self.current_exercise.text = ''

	def update_backto(self, instance):
		gymApp.screen_manager.current = 'main'
		gymApp.screen_manager.transition.direction = 'down'


# New window for showing current stats.
class CurrentWindow(FloatLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.add_widget(Label(text='Current Stats', size_hint=(1,.1), pos_hint={'top':1},
						bold=True, font_size=40))

		self.grid()

		self.current_stats()

		self.refresh_button = Button(text='Refresh', size_hint=(1,.1), pos_hint={'top':.2})
		self.refresh_button.bind(on_press=self.current_refresh)
		self.add_widget(self.refresh_button)

		self.backButton1 = Button(text='Back to Main Menu', size_hint=(1,.1), pos_hint={'top':.1})
		self.backButton1.bind(on_press=self.current_backto)
		self.add_widget(self.backButton1)

	def grid(self):
		self.grid_current = GridLayout(size_hint=(1,.1), pos_hint={'top':.9})
		self.grid_current.cols = 5

		self.grid_current.add_widget(Label(text='Exercise', size_hint_x=.5))
		self.grid_current.add_widget(Label(text='Kg', size_hint_x=.125))
		self.grid_current.add_widget(Label(text='S', size_hint_x=.125))
		self.grid_current.add_widget(Label(text='R', size_hint_x=.125))
		self.grid_current.add_widget(Label(text='R+', size_hint_x=.125))

		self.add_widget(self.grid_current)

	def current_stats(self):
		self.current_buttons = {}
		self.grid_from_data = GridLayout(size_hint=(1,.6), pos_hint={'top':.8})
		self.grid_from_data.cols = 5

		for a,b in exercises.items():

			self.current_buttons.setdefault(a,{a:Label(text=a, size_hint_x=.5),
										  'Weight': Label(text=b['Weight'], size_hint_x=.125),
										  'Sets': Label(text=b['Sets'], size_hint_x=.125),
										  'Reps': Label(text=b['Reps'], size_hint_x=.125),
										  'AMRAP': Label(text=b['AMRAP'], size_hint_x=.125)
										  })

			self.grid_from_data.add_widget(self.current_buttons[a][a])
			self.grid_from_data.add_widget(self.current_buttons[a]['Weight'])
			self.grid_from_data.add_widget(self.current_buttons[a]['Sets'])
			self.grid_from_data.add_widget(self.current_buttons[a]['Reps'])
			self.grid_from_data.add_widget(self.current_buttons[a]['AMRAP'])

		self.add_widget(self.grid_from_data)

	def current_refresh(self, instance):
		self.grid_from_data.clear_widgets()

		self.current_buttons = {}

		for a,b in exercises.items():

			self.current_buttons.setdefault(a,{a:Label(text=a, size_hint_x=.5),
										  'Weight': Label(text=b['Weight'], size_hint_x=.125),
										  'Sets': Label(text=b['Sets'], size_hint_x=.125),
										  'Reps': Label(text=b['Reps'], size_hint_x=.125),
										  'AMRAP': Label(text=b['AMRAP'], size_hint_x=.125)
										  })

			self.grid_from_data.add_widget(self.current_buttons[a][a])
			self.grid_from_data.add_widget(self.current_buttons[a]['Weight'])
			self.grid_from_data.add_widget(self.current_buttons[a]['Sets'])
			self.grid_from_data.add_widget(self.current_buttons[a]['Reps'])
			self.grid_from_data.add_widget(self.current_buttons[a]['AMRAP'])

	def current_backto(self, instance):
		gymApp.screen_manager.current = 'main'
		gymApp.screen_manager.transition.direction = 'down'


# Main app that has the screen manager which manages all of our windows.
class GymApp(App):
	title = 'Gym Tracker'

	def build(self):
		self.screen_manager = ScreenManager()

		self.main_window = MainWindow()
		screen = Screen(name='main')
		screen.add_widget(self.main_window)
		self.screen_manager.add_widget(screen)

		self.upd_window = UpdateWindow()
		screen = Screen(name='upd')
		screen.add_widget(self.upd_window)
		self.screen_manager.add_widget(screen)

		self.curr_window = CurrentWindow()
		screen = Screen(name='curr')
		screen.add_widget(self.curr_window)
		self.screen_manager.add_widget(screen)

		return self.screen_manager


# Calling our app to run.
if __name__ == '__main__':
	gymApp = GymApp()
	gymApp.run()
