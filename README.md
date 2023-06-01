<img src="./img/logo.png" width="200">

_Dataclass aware ORM with pluggable backends (DynamoDB included)_.

## Install
Install virtual environment and dependencies using `make install`
```bash
$ make install
$ source venv/bin/activate
(venv) $ 

```
## Run
Start the compose stack, which runs local versions of dynamodb and api gateway
```bash
(venv) $ docker compose up -d 
```

## Usage
Run the example below using:
```bash
(venv) $ export DYNAMODB=http://localhost:8009
(venv) $ python example/widgets.py
````

### Examples

```python
from dataclasses import dataclass
from flex import FlexObject


@dataclass
class Inventory(FlexObject):
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


# SCENARIO 1:
# Create table, Button, Widget, Add Buton to Widget. Save Widget
""" Create tables """
Button.create_table(skip_exists=True)
Widget.create_table(skip_exists=True)

""" Create a Button """
button1 = Button(name="button one", quantity=5, id="button1")

""" Create a Widget """
wid1 = Widget(name="widget one", quantity=10, id="widget1")

""" Add a button to widget1's existing list of buttons """
wid1.buttons += [button1]
print("WID1", wid1, wid1.buttons)
""" Save widget 1 """
wid1.save()

""" Create another widget """
wid2 = Widget(name="widget two", quantity=15, id="widget2")
wid2.save()

# SCENARIO 2:
# Issue SQL to find Widgets
""" Execute arbitrary SQL on the Widget table """
results = Widget.execute(f"SELECT * FROM \"Widget\" WHERE quantity<? and id=?", [15, 'widget1'])
for result in results:
    print("RESULT:", result, result.buttons)

# Find widgets using template object
""" Find Widget objects using template """
results = Widget.find({'id': 'widget1'}, response=True)
print("FIND:", results.response)

for result in results.all():
    print("RESULT:", result, result.buttons)

# SCENARIO 3:
# Delete specific widget by instance
""" Delete widget instance using instance method"""
print("DELETE widget1", wid1.delete().response)

# SCENARIO 4:
# Delete specific widget by template object
""" Try to find deleted object """
print("FIND2", Widget.find({'id': 'widget1', 'name': 'widget one'}))

# SCENARIO 5:
# Create table, Add Inventory Items
""" Create tables """
Inventory.create_table(skip_exists=True)

""" Create some Inventory objects and save them """
inv = Inventory(name="item", quantity=10, id="item1")
inv.save()
inv = Inventory(name="item", quantity=20, id="item2")
inv.save()

""" Delete widget2 using Class.delete(...) 
print("DELETE widget2", Widget.delete({'id': 'widget2', 'quantity': 15}))

results = Widget.execute(f"DELETE FROM \"Widget\" WHERE quantity=? and name='widget one' and id=?", [10, 'widget1'])
print(results)
"""
```