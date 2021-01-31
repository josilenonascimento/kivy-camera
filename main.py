# coding: utf-8

from kivy.lang import Builder
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.popup import Popup
from time import strftime
from kivy.graphics import Color, Rectangle
from kivy.animation import Animation


kv = """
#:import Factory kivy.factory.Factory

<MyPopup>:
	title: "Change resolution camera:"

	BoxLayout:
		orientation: "vertical"
		
		BoxLayout:
			orientation: "vertical"
			padding: 10
			spacing: 10

			Button:
				text: "320x240"
				size_hint: 1, .1
				on_release: root.change_size(self.text)

			Button:
				text: "640x480"
				size_hint: 1, .1
				on_release: root.change_size(self.text)

		Button:
			text: "Close"
			on_press: root.dismiss()
			size_hint: 1, .1


<MyCamera>:
	orientation: "vertical"

	FloatLayout:
		Camera:
			id: camera
		
		StackLayout:
			orientation: "rl-bt"

			Button:
				text: "Capture"
				size_hint: .5, .1
				on_release: root.capture()

			Button:
				text: "Resize"
				size_hint: .5, .1
				on_press: Factory.MyPopup().open()

"""

Builder.load_string(kv)


class MyPopup(Popup):

	def change_size(self, *args):
		size_str = args[0].split("x")
		
		width = int(size_str[0])
		height = int(size_str[1])

		Window.size = width, height 
		

class MyCamera(BoxLayout):

	def __init__(self, **kwargs):
		super(MyCamera, self).__init__(**kwargs)	

		Window.bind(on_resize=self.change_resolution)
	
	def change_resolution(self, *args):
		self.ids.camera.resolution = Window.size
	
	def capture(self, *args):
		camera = self.ids.camera
					
		timestamp = strftime("%Y%m%d%H%M%S") 
		camera.export_to_png("capture_webcam_{}.png".format(timestamp))
	
		with camera.canvas.after:
			Color(1, 1, 1, .3)
			Rectangle(pos=camera.pos, size=camera.size)

		anim = Animation(opacity=0, duration=.2)
		anim.start(camera)
		anim.bind(on_complete=self.flash)
	
	def flash(self, *args):
		camera = args[1]	
		camera.canvas.after.clear()
		camera.opacity = 1


class MainApp(App):
	
	def build(self):
		return MyCamera()


my_app = MainApp()
my_app.title = "Kivy Camera" 

if __name__ == "__main__":
	my_app.run()

