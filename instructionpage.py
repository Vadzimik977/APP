from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import SlideTransition
from kivy.uix.screenmanager import ScreenManager, Screen
from scanpage import ScanPage
from kivymd.uix.button import MDRectangleFlatButton, MDRoundFlatButton

class InstructionPage(BoxLayout):
    def __init__(self, **kwargs):
        super(InstructionPage, self).__init__(orientation='vertical', **kwargs)

        # Добавляем цветной фон для экрана инструкции
        with self.canvas.before:
            Color(1, 192/255, 203/255, 1)  # Цвет в формате (R, G, B, A)
            self.rect = Rectangle(size=(Window.width, Window.height), pos=self.pos)

        # Читаем текст из файла для инструкции
        with open('instruction_text.txt', 'r', encoding='utf-8') as file:
            instruction_text = file.read()

        # Создаем виджет Label с поддержкой разметки Kivy
        instruction_label = Label(
            text=instruction_text,
            halign='center', valign='top',
            size_hint=(1, 0.8),
            color=(0, 0, 0, 1),
            font_size=20,
            markup=True  # Включаем поддержку разметки
        )
        self.add_widget(instruction_label)

        # Добавляем кнопку "Начать"
        start_button = MDRoundFlatButton(
            text='Начать',
            on_press=self.start_button_pressed,
            text_color='white',
            font_size=25,
            size_hint=(1, 0.1),
            md_bg_color='indigo',
            pos_hint={'center_x': 0.5, 'center_y': 0.1}
        )
        self.add_widget(start_button)

    def start_button_pressed(self, instance):
        # Вызываем метод show_scan_page у экземпляра приложения
        # app = App.get_running_app()
        # app.show_scan_page()
        sm = self.parent.parent

        # Создаем экран для страницы Инструкции
        scan_screen = Screen(name='scan')
        sm.add_widget(scan_screen)

        # Добавляем виджет Инструкции
        scan_page = ScanPage()
        scan_screen.add_widget(scan_page)

        # Переключаемся на новый экран с анимацией
        sm.transition = SlideTransition(direction='left')
        sm.switch_to(scan_screen)
