
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.storage.jsonstore import JsonStore
from .components.dialog_content import AddProductDialog, EditProductDialog
from .components.list_item import MyListItem


class BillingApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.products = []
        self.dialog = MDDialog()
        self.storage = JsonStore("data.json")
        self.icon = "icon.png"

    def build(self):
        return Builder.load_file('main.kv')

    def add_product_to_list(self):
        product_name = self.dialog.content_cls.ids.product_name.text
        product_price = self.dialog.content_cls.ids.product_price.text

        if not product_name or not product_price:
            return


        if not product_price.isnumeric():
            self.dialog.content_cls.ids.product_price.text = ""
            self.dialog.content_cls.ids.product_price.hint_text = "Product price must be numeric"
            return

        product = {"product_name": str(product_name), "product_price": str(product_price)}
        self.products.append(product)
        self.storage.put("products", products=self.products)
        self.refresh_products()

    def on_start(self):
        if not self.storage.exists("products"):
            self.products = []
            self.storage.put("products", products=self.products)
        else:
            self.products = self.storage.get("products")["products"]
        self.refresh_products()

    def on_item_click(self, index):
        self.dialog = MDDialog(
            title="Confirm delete or edit",
            buttons = [
                MDFlatButton(text="cancel", on_release=lambda x: self.dialog.dismiss()),
                MDFlatButton(text="delete", on_release=lambda x: self.delete_product(index)),
                MDFlatButton(text="edit", on_release=lambda x: self.edit_product(index)),
            ] 
        )
        self.dialog.open()
        print(f"item {index} clicked")

    def edit_product(self, index):
        self.dialog.dismiss()
        self.dialog = MDDialog(
            title="Edit product",
            type="custom",
            content_cls=EditProductDialog(),
            buttons = [
                MDFlatButton(text="cancel", on_release=lambda x: self.dialog.dismiss()),
                MDFlatButton(text="save", on_release=lambda x: self.save_product(index))
            ]
        )
        self.dialog.content_cls.ids.product_name.text = self.products[index]["product_name"]
        self.dialog.content_cls.ids.product_price.text = self.products[index]["product_price"]
        self.dialog.open()

    def delete_product(self, index):
        del self.products[index]
        self.storage.put("products", products=self.products)
        self.refresh_products()
        self.dialog.dismiss()

    def add_product(self, index):
        self.dialog = MDDialog(
            title="Add product",
            type="custom",
            content_cls=AddProductDialog(),
            buttons = [
                MDFlatButton(text="cancel", on_release=lambda x: self.dialog.dismiss()),
                MDFlatButton(text="add", on_release=lambda x: self.add_product_to_list()),
            ]
        )
        self.dialog.open()
        self.refresh_products()

    def save_product(self, index):
        self.products[index]["product_name"] = self.dialog.content_cls.ids.product_name.text
        self.products[index]["product_price"] = self.dialog.content_cls.ids.product_price.text
        self.storage.put("products", products=self.products)
        self.refresh_products()
        self.dialog.dismiss()

    def refresh_products(self):
        self.root.ids.container.clear_widgets()
        for i, j in enumerate(self.products):
            self.root.ids.container.add_widget(
                MyListItem(
                    index=i,
                    text=j['product_name'],
                    secondary_text=j['product_price'],
                    handler=self.on_item_click),
            )
