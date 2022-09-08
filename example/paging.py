from models import Widget


results = Widget.execute(f"SELECT * FROM \"Widget\" WHERE quantity<? ", [25, 'widget1'], response=True, limit=1)
print(results.response)

print(results.all())

print(results.next())
