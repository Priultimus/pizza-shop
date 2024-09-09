import json
import decimal
import datetime
from typing import Union


class Encoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime.datetime):
            return str(z)
        elif isinstance(z, decimal.Decimal):
            return float(z)
        else:
            return super().default(z)


def clean_data(data: dict, serialize=False) -> Union[dict, str]:
    data = json.dumps(data, cls=Encoder)
    if serialize:
        return data
    return json.loads(data)
