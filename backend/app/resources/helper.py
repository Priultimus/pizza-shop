import json
import datetime
from typing import Union


class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime.datetime):
            return str(z)
        else:
            return super().default(z)


def clean_data(data: dict, serialize=False) -> Union[dict, str]:
    data = json.dumps(data, cls=DateTimeEncoder)
    if serialize:
        return data
    return json.loads(data)
