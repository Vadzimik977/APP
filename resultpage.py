from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.button import MDRoundFlatButton

class ResultPage(Screen):
    def __init__(self, **kwargs):
        super(ResultPage, self).__init__(**kwargs)
        with self.canvas.before:
            Color(1, 192/255, 203/255, 1)
            self.rect = Rectangle(size=(Window.width, Window.height), pos=self.pos)
        self.create_result_interface()

    def create_result_interface(self):
        result_layout = BoxLayout(orientation='vertical')

        title_label = Label(text="Наши предложения:", font_size=20, color=(0, 0, 0, 1))
        result_layout.add_widget(title_label)

        # Путь к папке с изображениями товаров
        images_folder_path = "images"

        # Имена изображений и соответствующие названия товаров
        products_data = [
            {"image": "Без названия.png", "name": "NIVEA крем для лица"},
            {"image": "Без названия (1).png", "name": "NIVEA увлажняющий крем"},
            {"image": "Без названия (2).png", "name": "ARAVIA Professional"}
        ]

        for product in products_data:
            # Добавление изображения
            product_image = Image(source=f"{images_folder_path}/{product['image']}")
            result_layout.add_widget(product_image)

            # Добавление названия товара
            product_label = Label(text=product["name"], font_size=16, color=(0, 0, 0, 1))
            result_layout.add_widget(product_label)

        # Добавление кнопки "Начать заново"
        restart_button = MDRoundFlatButton(
            text="Начать заново", on_press=self.restart, text_color='white',
            font_size=25, md_bg_color='indigo', size_hint=(1, 0.2),
        )
        result_layout.add_widget(restart_button)

        scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        scroll_view.add_widget(result_layout)

        self.add_widget(scroll_view)

    def restart(self, instance):
        # Import the required class here to avoid circular import
        from scanpage import ScanScreen, ScanPage
        sm = self.parent.parent

        # Create a new ScanScreen instance
        scan_screen = ScanScreen(name='scan')

        # Check if the scan page already exists, or create a new one
        scan_page = ScanPage()
        scan_screen.add_widget(scan_page)

        # Set the transition and switch to the 'scan' screen
        sm.transition = SlideTransition(direction='left')  # Adjust the direction as needed
        sm.switch_to(scan_screen)
