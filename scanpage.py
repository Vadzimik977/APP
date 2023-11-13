from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.uix.camera import Camera
import os
import uuid
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from questionpage import QuestionPage
from resultpage import ResultPage
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivymd.uix.button import MDRectangleFlatButton, MDRoundFlatButton

class ScanPage(BoxLayout):
    def __init__(self, **kwargs):
        super(ScanPage, self).__init__(orientation='vertical', **kwargs)

        # Добавляем цветной фон для экрана сканирования
        with self.canvas.before:
            Color(1, 192/255, 203/255, 1)
            self.rect = Rectangle(size=(Window.width, Window.height), pos=self.pos)

        # Добавляем виджет Spacer для выравнивания по центру вертикали
        self.add_widget(Label(size_hint_y=None, height=(Window.height - 100) / 2))

        # Инициализируем камеру
        self.camera = None

        # Добавляем кнопку "Сканировать" в центре экрана
        scan_button = MDRoundFlatButton(
            text='Сканировать',
            text_color='white',
            font_size=25,
            md_bg_color='indigo',
            on_press=self.scan_button_pressed,
            size_hint=(None, None),
            size=(200, 100),
            pos_hint={'center_x': 0.5}
        )
        self.add_widget(scan_button)

        # Добавляем виджет Spacer для выравнивания по центру вертикали
        self.add_widget(Label(size_hint_y=None, height=(Window.height - 100) / 2))

        self.progress_bar = ProgressBar(max=1000, size_hint=(None, None), size=(200, 20), pos_hint={'center_x': 0.5})
        self.add_widget(self.progress_bar)
        self.progress_bar.value = 0

    def scan_button_pressed(self, instance):
        # Скрыть кнопку сканирования
        instance.disabled = True

        # Показать ProgressBar
        self.progress_bar.value = 0
        self.progress_bar.visible = True

        # Создать расписание для обновления ProgressBar
        Clock.schedule_interval(self.update_progress, 1 / 30)  # обновление каждые 1/30 секунды

        # Инициализация камеры, когда кнопка нажата
        self.initialize_camera()

        # Показываем страницу с вопросами через 5 секунд
        Clock.schedule_once(self.show_question_page, 5)


    def initialize_camera(self):
        # Try initializing the camera with different indices
        for index in range(4):  # Try indices from 0 to 3
            try:
                self.camera = Camera(index=index, play=True)
                break  # If successful, break out of the loop
            except Exception as e:
                print(f"Error initializing camera with index {index}: {e}")

        if self.camera is None:
            print("Camera not available.")


    def update_progress(self, dt):
        # Увеличиваем значение ProgressBar в зависимости от выполненного прогресса (пример для демонстрации)
        self.progress_bar.value += 0.1  # Подставьте реальные значения в зависимости от вашего процесса

        # Если ProgressBar достиг максимального значения, остановить обновление
        if self.progress_bar.value >= self.progress_bar.max:
            Clock.unschedule(self.update_progress)

        if self.camera is not None:
            # Генерируем уникальный идентификатор для файла
            unique_id = str(uuid.uuid4())
            image_filename = f"photo_{unique_id}.png"

            # Путь для сохранения фотографии
            image_path = os.path.join("photos", image_filename)

            # Сохраняем фотографию
            self.camera.export_to_png(image_path)

            # Отключить ProgressBar и показать кнопку после завершения сканирования
            Clock.schedule_once(lambda dt: self.finish_scan(image_filename), 1)

    def finish_scan(self, image_filename):
        # Отключить ProgressBar
        self.progress_bar.visible = False

        # Создаем экземпляр ScreenManager
        sm = ScreenManager(transition=SlideTransition())

        # Показываем страницу с вопросами через 5 секунд
        Clock.schedule_once(lambda dt: self.show_question_page(sm), 5)

    def show_question_page(self, sm):
        # Создаем экран для страницы вопросов
        sm = self.parent.parent
        question_page = QuestionPage(name='question_page')
        sm.add_widget(question_page)

        # Удаляем текущий экран (ScanScreen)
        sm.remove_widget(self.parent)

        # Добавляем страницу с результатами
        result_page = ResultPage(name='result_page')
        sm.add_widget(result_page)

class ScanScreen(Screen):
    pass