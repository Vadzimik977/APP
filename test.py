from kivy.app import App
from kivy.uix.camera import Camera

class CameraTestApp(App):
    def build(self):
        camera = Camera(index=0, play=True)
        return camera

if __name__ == '__main__':
    CameraTestApp().run()