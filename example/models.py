from dataclasses import dataclass
from flex import DataclassBase


@dataclass
class Inventory(DataclassBase):
    quantity: int = 0

    @classmethod
    @property
    def sort_key(cls) -> str:
        return 'quantity'


@dataclass
class Button(Inventory):
    type: str = "square"
    widget: str = None


@dataclass
class Widget(Inventory):
    theme: str = "default"
    _buttons = [Button(name="button zero", quantity=5, id="button0")]

    @property
    def buttons(self) -> []:
        buttons = self.relation(Button, backref='widget')
        return buttons

    @buttons.setter
    def buttons(self, buttons: str) -> None:
        for button in buttons:
            button.widget = self.id

        self._buttons = buttons

    def save(self):
        super(Widget, self).save()

        for button in self._buttons:
            button.save()
