from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.clock import Clock
import os
import uuid
from kivy.app import App
import json
from kivy.metrics import dp
from kivy.core.window import Window
import csv
from kivymd.uix.button import MDRectangleFlatButton, MDRoundFlatButton,MDFlatButton
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivy.graphics import Color, Rectangle
from resultpage import ResultPage
from kivy.uix.screenmanager import SlideTransition
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.label import MDLabel


class QuestionPage(Screen):
    def __init__(self, **kwargs):
        super(QuestionPage, self).__init__(**kwargs)
        with self.canvas.before:
            Color(1, 192/255, 203/255, 1)  # 1, 0, 1, 1 соответствует розовому цвету (RGBA)
            self.rect = Rectangle(size=(Window.width, Window.height), pos=self.pos)

        # Вопросы
        self.questions = [
            {"question": "Вопрос 1. Сколько Вам лет?", "options": ["20-30 лет", "30-40 лет", "40-50 лет","50+ лет"], "correct_answer": 0},
            {"question": "Вопрос 2. На ощупь Ваша кожа?", "options": ["гладкая и бархатистая", "тонкая, почти прозрачная", "утолщенная с неровным рельефом","различная по структуре"], "correct_answer": 0},
            {"question": "Вопрос 3. Заметны ли поры на Вашем лице?", "options": ["незаметны", "едва видны на некоторых зонах", "заметны в области лба, носа, подбородка", "заметны везде"], "correct_answer": 0},
            {"question": "Вопрос 4. Появляется ли жирный блеск на лице?", "options": ["отсутствует, даже чувство сухости кожи", "отсутствует, но дискомфорта нет", "появляется иногда в некоторых зонах","да, на всем лице"], "correct_answer": 0},
            {"question": "Вопрос 5. Бывает ли сухость на лице и когда?",
             "options": ["не бывает", "да, при перепаде температур и в помещении с кондиционером",
                         "да, после применения спиртосодержащих лосьонов и умывания", "практически постоянно"], "correct_answer": 0},
            {"question": "Вопрос 6. Склонна ли Ваша кожа к высыпаниям?",
             "options": ["нет", "нечасто, после стрессов",
                         "часто", "на лице постоянно есть прыщи"],"correct_answer": 0},
            {"question": "Вопрос 7. Как Ваша кожа реагирует на пилинги?",
             "options": ["нет выраженной реакции", "покраснения бывают редко, малозаметны",
                         "покраснения возникают иногда, быстро проходят", "покраснения держаться долго, кожа шелушится"], "correct_answer": 0},
            {"question": "Вопрос 8. Есть ли морщины на лице?",
             "options": ["нет", "только если улыбаюсь или хмурюсь",
                         "немного заметны даже в 'статике'",
                         "есть глубокие морщины на лбу, переносице, носогубные складки"], "correct_answer": 0},
            {"question": "Вопрос 9. Есть ли пигментные пятна на Вашем лице?",
             "options": ["нет", "только веснушки",
                         "на некоторых зонах, не очень заметные",
                         "пигментация заметна, особенно после инсоляции"], "correct_answer": 0},
            {"question": "Вопрос 10. Заметны ои сосуды на Вашем лице?",
             "options": ["нет", "в некоторых зонах",
                         "сосудистая сеточка видна всегда"], "correct_answer": 0},

            # Добавьте свои вопросы
        ]

        # Индекс текущего вопроса
        self.current_question_index = 0

        # Имя файла изображения
        # self.image_filename = ""

        # Создаем интерфейс для вопроса
        self.create_question_interface()
        self.pressed_button = None
    def create_question_interface(self):
        question_layout = BoxLayout(orientation='vertical')

        # Add question label
        question_label = Label(text=self.questions[self.current_question_index]["question"], color=(0, 0, 0, 1))
        question_layout.add_widget(question_label)

        # Add options as buttons with checkboxes
        options_layout = BoxLayout(orientation='vertical')

        for i, option in enumerate(self.questions[self.current_question_index]["options"]):
            option_box = BoxLayout(orientation='horizontal', spacing=10)
            option_checkbox = MDCheckbox(group=f"question_{self.current_question_index}", color=(0, 0, 0, 1),
                                         size_hint=(None, None), )

            option_button = MDRoundFlatButton(
                text=option,
                on_press=self.on_option_pressed,
                text_color='white',
                size_hint=(1, 0.4),
                disabled_color='blue',
                md_bg_color='indigo',  # Yellow background
            )
            option_button.checkbox = option_checkbox

            # option_box.add_widget(option_checkbox)
            option_box.add_widget(option_button)
            options_layout.add_widget(option_box)

        question_layout.add_widget(options_layout)

        # Add "Answer" button
        answer_button = MDRectangleFlatButton(
            text="Ответить",
            on_press=self.check_answer,
            text_color='white',
            font_size=25,
            md_bg_color='orange',
            pos_hint={'center_x': 0.5, 'center_y': 0.1},
            size_hint=(1, 0.1),
        )
        question_layout.add_widget(answer_button)

        # Add scroll view
        scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        scroll_view.add_widget(question_layout)

        self.add_widget(scroll_view)

    def on_option_pressed(self, instance):
        # Reset color of the previously pressed button (if any)
        if self.pressed_button:
            self.pressed_button.md_bg_color = 'indigo'

        # Set the color of the pressed button to blue
        instance.md_bg_color = 'blue'
        self.pressed_button = instance
    def set_image_filename(self, image_filename):
        self.image_filename = image_filename

    def on_option_selected(self, instance):
        # Toggle the state of the attached checkbox when the option button is pressed
        instance.checkbox.active = not instance.checkbox.active
    def on_pre_leave(self):
        self.clear_widgets()
    def check_answer(self, instance):
        # Получаем выбранный ответ
        selected_option = None

        for widget in self.children:
            if isinstance(widget, ScrollView):
                for child_widget in widget.children:
                    if isinstance(child_widget, BoxLayout) and child_widget.orientation == 'vertical':
                        for option_widget in child_widget.children[2].children:  # Индекс 2 - это OptionsLayout
                            if isinstance(option_widget, ToggleButton) and option_widget.state == 'down':
                                selected_option = option_widget.text
                                break

        # Сравниваем с правильным ответом
        correct_answer_index = self.questions[self.current_question_index]["correct_answer"]
        correct_answer = self.questions[self.current_question_index]["options"][correct_answer_index]

        # Сохраняем ответ пользователя и переходим к следующему вопросу
        # self.save_answer(selected_option, correct_answer)

        # Переходим к следующему вопросу или завершаем опрос
        if self.current_question_index < len(self.questions) - 1:
            self.current_question_index += 1
            self.on_pre_leave()  # Добавляем эту строку
            self.create_question_interface()
        else:
            # Получаем экземпляр MyApp
            self.save_user_responses()
            app_instance = App.get_running_app()

            # Создаем экран для страницы Инструкции
            result_screen = Screen(name='result')
            app_instance.root.add_widget(result_screen)
            result_page = ResultPage()
            result_screen.add_widget(result_page)

            # Переключаемся на новый экран с анимацией
            app_instance.root.transition = SlideTransition(direction='left')
            app_instance.root.switch_to(result_screen)
    def save_user_responses(self):
        # Получаем id пользователя (в примере я использую заглушку, замените ее на реальный механизм получения id)
        user_id = str(uuid.uuid4())

        # Создаем или открываем CSV-файл для записи ответов
        csv_filename = "user_responses.csv"
        with open(csv_filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Записываем id пользователя
            writer.writerow([user_id])
            # Записываем варианты ответов пользователя для каждого вопроса
            for i, question in enumerate(self.questions):
                # Опция пользователя идет после id пользователя
                writer.writerow([f"Вопрос {i + 1}", question["options"][question["correct_answer"]]])
        print(f"User {user_id}'s answers saved to {csv_filename}")