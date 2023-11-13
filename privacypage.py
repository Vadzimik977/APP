# privacypage.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.lang import Builder
from instructionpage import InstructionPage
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.button import MDRectangleFlatButton, MDRoundFlatButton # Import the correct button class
from kivymd.uix.label import MDLabel

Builder.load_string('''
<MarkupLabel>:
    markup: True
    ''')

class MarkupLabel(MDLabel):  # Use MDLabel instead of Label for KivyMD markup
    pass

class PrivacyPolicyPage(BoxLayout):
    def __init__(self, **kwargs):
        super(PrivacyPolicyPage, self).__init__(orientation='vertical', **kwargs)

        # Читаем текст из файла с использованием разметки Kivy
        with open('policy_text.txt', 'r', encoding='utf-8') as file:
            policy_text = file.read()

        # Создаем виджет Label с поддержкой разметки
        privacy_text = MarkupLabel(
            text=policy_text,
            halign='center', valign='top',
            size_hint=(1, 0.8),
            color=(0, 0, 0, 1),
            font_size=20
        )
        self.add_widget(privacy_text)

        # Добавляем кнопку Принять и продолжить
        accept_button = MDRoundFlatButton(  # Use MDRectangleFlatButton instead of MDRaisedButton
            text='Принять и продолжить',
            on_press=self.show_instructions,
            text_color='white',
            font_size=25,
            size_hint=(1, 0.1),
            # color=(0, 0, 0, 1),
            md_bg_color='indigo',
            pos_hint={'center_x': 0.5, 'center_y': 0.1}
        )
        self.add_widget(accept_button)

    def show_instructions(self, instance):
        # Получаем экранный менеджер из корневого виджета
        sm = self.parent.parent

        # Создаем экран для страницы Инструкции
        instruction_screen = Screen(name='instruction')
        sm.add_widget(instruction_screen)

        # Добавляем виджет Инструкции
        instruction_page = InstructionPage()
        instruction_screen.add_widget(instruction_page)

        # Переключаемся на новый экран с анимацией
        sm.transition = SlideTransition(direction='up')
        sm.switch_to(instruction_screen)
