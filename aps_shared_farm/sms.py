import requests
from aps_shared_farm.config import ShurjoBartaConnectConfig
from urllib.parse import urlencode, quote_plus
import uuid


class ShurjoBartaSMS(object):
    # http://<server>:8080/bulksms/bulksms?
    # username=XXXX&password=YYYYY&type=Y&dlr=Z&destination=QQQQQQQQQ&source=RRRR&message=
    # SSSSSSSS<&url=KKKK>
    def __init__(self, destination=None, message=None):
        self.server = f'https://{ShurjoBartaConnectConfig.SERVER}/{ShurjoBartaConnectConfig.END_POINT}'
        self.username = ShurjoBartaConnectConfig.USERNAME
        self.password = ShurjoBartaConnectConfig.PASSWORD
        self.destination = destination
        self.message = message
        self.uniq_id = str(uuid.uuid4())
        pass

    def send(self):
        sms_data = {
            'API_USER': self.username,
            'API_PASSWORD': self.password,
            'MOBILE': self.destination,
            'MESSAGE': self.message,
            'MESSAGE_ID': self.uniq_id
        }
        r = requests.post(self.server, sms_data, verify=False)
        self.response = r.json()
        print(r.status_code)
        # self.update_current_credit()

        return self.response
