"""
VasalloBot main file.
"""
import requests
import random

class VasalloBot():
    """
    Bot class.
    """
    def __init__(self):
        self.timeout = 10
        with open('.token', 'r') as f:
            token = f.read().rstrip()
        self.url = 'https://api.telegram.org/bot{}/'.format(token)
        self.keep_alive = True
        self.last_update = 0
        self.id_boss = 0

    def run(self):
        """
        Main loop.
        """
        while self.keep_alive:
            response = self.get_updates(self.last_update, self.timeout)
            self.process_response(response)
        # Get remaining updates from the server or, at least, notify the
        # reception of the messages processed
        while True:
            response = self.get_updates(self.last_update, 0)
            # TODO: handle response errors
            data = response.json()
            if not data['result']:
                break
            self.process_response(response)

    def get_updates(self, offset, timeout):
        """
        Get updates from the server.
        """
        params = {'offset': offset + 1, 'timeout': timeout}
        response = requests.get(self.url + 'getUpdates', params)
        return response

    def process_response(self, response):
        """
        Process response from the server.
        """
        def vasallo(datain):
            """
            Vasallo functionality.
            """
            textstr = datain['message']['text'].split()
            for x in textstr:
                if x == 'Abracadabra'.lower():
                    self.id_boss = datain['message']['from']['id']
                    return 'Hola am@ ' + datain['message']['from']['first_name']
                elif x == 'libero':
                    self.id_boss = 0
                    return '¡Por fin soy libre! Gracias ' + datain['message']['from']['first_name']
            if self.id_boss == int(datain['message']['from']['id']):
                return 'A sus órdenes, ' + datain['message']['from']['first_name']
            elif self.id_boss == 0:
                return 'No tengo dueño'
            else:
                seq = ['Papán','Botarate','Zascandil','Zopenco','Pailán',
                    'Zalapastrán']
                return random.choice(seq)

        # TODO: handle response errors
        data = response.json()
        for update in data['result']:
            self.last_update = update['update_id']
            if 'message' not in update:
                continue
            if 'text' not in update['message']:
                continue
            if self.process_command(update['message']['text']):
                continue
            params = {'chat_id': update['message']['chat']['id'],
                      'text': vasallo(update)}
            requests.get(self.url + 'sendMessage', params)

    def process_command(self, text):
        """
        Process a message and return `True` if the message was successfuly
        processed as a command.
        """
        if text[0] != '/':
            return False
        command = text.split()
        if command[0] == '/upgrade':
            print('ooops')
            self.keep_alive = False
        return True

    def get_me(self):
        """
        Get bot information.
        """
        botdata = requests.get(self.url + 'getMe')
        return botdata

if __name__ == '__main__':

    bot = VasalloBot()
    bot.run()
