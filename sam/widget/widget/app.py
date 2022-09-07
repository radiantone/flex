import json
import flex
from example.models import Widget


def lambda_handler(event, context):
    widgets = Widget.find({'id': 'widget1'})

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "flex:hello world",
            "widget": str(widgets[0])
            # "location": ip.text.replace("\n", "")
        }),
    }
