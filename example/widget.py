from models import Widget


widgets = Widget.find({'id': 'widget1'})
print("WIDGET:", widgets[0], widgets[0].buttons)

for button in widgets[0].buttons:
    print("BUTTON:",button)