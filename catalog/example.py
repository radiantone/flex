from models import Asset, Bundle, Availability

# SCENARIO 6:
# Create Asset object, add properties to it, save it (which implicitly creates the table
"""
Create and store an Asset. Create table if doesn't already exist
"""
avail = Availability(id="avail1")
avail.save()
bundle = Bundle(id="bundle1")
bundle.availabilities += [avail]
bundle.save()

asset = Asset(id="asset1")
asset.properties = {'prop1': 'val1', 'prop2': 'val2'}
asset.bundles += [bundle]

asset.save()
