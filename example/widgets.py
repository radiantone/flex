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
        buttons = self.relation(Button, 'widget')
        return buttons

    @buttons.setter
    def buttons(self, buttons: str) -> None:
        for button in buttons:
            button.widget = self.id
            button.save()

        self._buttons = buttons


Button.create_table(skip_exists=True)
Inventory.create_table(skip_exists=True)
Widget.create_table(skip_exists=True)

button1 = Button(name="button one", quantity=5, id="button1")
button1.save()

wid1 = Widget(name="widget one", quantity=10, id="widget1")
wid1.buttons += [button1]
print("WID1", wid1, wid1.buttons)
wid1.save()

wid2 = Widget(name="widget two", quantity=15, id="widget2")
wid2.save()

inv = Inventory(name="item", quantity=10, id="item1")
inv.save()
inv = Inventory(name="item", quantity=20, id="item2")
inv.save()

results = Widget.execute(f"SELECT * FROM \"Widget\" WHERE quantity<? and id=?", [15, 'widget1'])
for result in results:
    print("RESULT:", result,  result.buttons)

results = Widget.find({'id': 'widget1'}, response=True)
print("FIND:", results.response)
for result in results.all():
    print("RESULT:", result,  result.buttons)

print("DELETE", wid1.delete().response)
print("FIND2", Widget.find({'id': 'widget1', 'name': 'widget one'}))

#results = Widget.execute(f"DELETE FROM \"Widget\" WHERE quantity=? and name='widget one' and id=?", [10, 'widget1'])
#print(results)



