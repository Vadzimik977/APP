# main.py
import buldozer
from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from privacypage import PrivacyPolicyPage
from instructionpage import InstructionPage
from scanpage import ScanPage, ScanScreen
from kivymd.uix.button import MDRectangleFlatButton, MDFloatingActionButton, MDRoundFlatButton
import os
import uuid
import shutil
from questionpage import QuestionPage
from resultpage import ResultPage
from kivy.clock import Clock

class StartScreen(Screen):
    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)

        with self.canvas.before:
            # Set the color to pink (255/255, 192/255, 203/255, 1)
            Color(1, 192/255, 203/255, 1)
            self.rect = Rectangle(size=(Window.width, Window.height), pos=self.pos)

        # Bind the size and pos properties to update the Rectangle on changes
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Add logo image
        logo_image = Image(source="images/logo.png", size_hint=(None, None), size=(300, 300),
                           pos_hint={'center_x': 0.5, 'center_y': 0.7})
        self.add_widget(logo_image)

        # Add the rest of your widgets here

    def _update_rect(self, instance, value):
        # Update the position and size of the Rectangle
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class InstructionsScreen(Screen):
    pass

class PrivacyPolicyScreen(Screen):
    pass

class MyApp(MDApp):
    def build(self):
        # Устанавливаем фиксированный размер окна для телефонов (пример для портретной ориентации)
        Window.size = (480, 800)  # Измените на желаемые размеры

        # Создаем менеджер экранов с анимацией выезда сверху
        sm = ScreenManager(transition=SlideTransition())

        # Добавляем стартовый экран
        self.start_screen = StartScreen(name='start')
        sm.add_widget(self.start_screen)

        # Добавляем приветственный текст в центре экрана
        welcome_label = Label(text='Добро пожаловать', font_size=24, halign='center', valign='middle', color=(0, 0, 0, 1))
        self.start_screen.add_widget(welcome_label)

        # Добавляем контейнер для кнопок
        buttons_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))

        # Добавляем кнопку для перехода к Политике конфиденциальности
        privacy_policy_button = MDRoundFlatButton(
            text="НАЧАТЬ",
            text_color='white',
            font_size=25,
            # Replace 'assets/Times_New_Roman.ttf' with the path to your font file
            md_bg_color='indigo',
            on_press=self.show_privacy_policy,
            size_hint=(0.1, 1),
            pos_hint={'center_x': 0.5}
        )
        buttons_layout.add_widget(privacy_policy_button)

        self.start_screen.add_widget(buttons_layout)

        # Create and add the ScanScreen and ScanPage instances
        scan_screen = ScanScreen(name='scan')

        return sm

    def show_privacy_policy(self, instance):
        # Переход к странице Политики конфиденциальности
        sm = self.root
        sm.transition.direction = 'up'  # Направление анимации

        # Создаем экран для страницы с Политикой конфиденциальности
        privacy_screen = PrivacyPolicyScreen(name='privacy')
        sm.add_widget(privacy_screen)

        # Добавляем цветной фон для экрана с Политикой конфиденциальности
        with privacy_screen.canvas.before:
            Color(1, 192/255, 203/255, 1)
            Rectangle(size=(Window.width, Window.height), pos=privacy_screen.pos)

        # Добавляем виджет Политики конфиденциальности
        privacy_page = PrivacyPolicyPage()
        privacy_screen.add_widget(privacy_page)

        # Удаляем предыдущий экран
        sm.remove_widget(self.start_screen)

    def show_instruction_page(self, instance):
        # Переход к странице Инструкции
        sm = self.root
        sm.transition.direction = 'up'  # Направление анимации

        # Создаем экран для страницы Инструкции
        instruction_screen = Screen(name='instruction')
        sm.add_widget(instruction_screen)

        # Добавляем цветной фон для экрана с Инструкцией
        with instruction_screen.canvas.before:
            Color(1, 192 / 255, 203 / 255, 1)
            Rectangle(size=(Window.width, Window.height), pos=instruction_screen.pos)

        # Добавляем виджет Инструкции
        instruction_page = InstructionPage()
        instruction_screen.add_widget(instruction_page)

    def show_scan_page(self, instance):
        # Переход к странице сканирования
        sm = self.root
        sm.transition.direction = 'left'  # Направление анимации

        # Check if the scan screen already exists
        scan_screen = sm.get_screen('scan')
        if not scan_screen:
            scan_screen = ScanScreen(name='scan')
            sm.add_widget(scan_screen)

        # Check if the scan page already exists
        scan_page = scan_screen.children[0] if scan_screen.children else None
        if not scan_page:
            scan_page = ScanPage()
            scan_screen.add_widget(scan_page)

        # Устанавливаем задержку и вызываем show_question_page через 1 секунду
        # Clock.schedule_once(lambda dt: self.show_question_page(dt, sm), 1)

    def show_question_page(self, dt, sm):
        # Создаем экран для страницы вопросов
        question_page = QuestionPage(name='question_page')
        sm.add_widget(question_page)

        # Удаляем предыдущий экран
        sm.current = 'question_page'

    def show_result_page(self, instance):
        # Переход к странице результатов
        sm = self.root
        sm.transition.direction = 'left'  # Направление анимации
        # Создаем экран для страницы результатов
        result_screen = Screen(name='result')
        sm.add_widget(result_screen)
        # Добавляем цветной фон для экрана с результатами
        with result_screen.canvas.before:
            Color(1, 192 / 255, 203 / 255, 1)
            Rectangle(size=(Window.width, Window.height), pos=result_screen.pos)
        # Добавляем виджет результатов
        result_page = ResultPage()
        result_screen.add_widget(result_page)
        # Удаляем предыдущий экран
        sm.remove_widget(self.start_screen)


if __name__ == '__main__':
    MyApp().run()
