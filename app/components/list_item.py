from kivymd.uix.list import TwoLineIconListItem, IconLeftWidget
from kivymd.uix.dialog import MDDialog



class MyListItem(TwoLineIconListItem):
    def __init__(self, handler, index:int=0, **kwargs):
        super().__init__(**kwargs)
        self.index = index
        self.handler = handler
        self.dialog = MDDialog()
        self.add_widget(IconLeftWidget(icon='shopping-outline'))

    def on_release(self):
        print(self.index)
        self.handler(self.index)
        return super().on_release()