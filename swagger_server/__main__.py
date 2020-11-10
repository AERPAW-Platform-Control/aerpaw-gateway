#!/usr/bin/env python3

import connexion

from swagger_server import encoder
import os
from swagger_server.controllers import emulab


def main():
    print(emulab.usercred_file)
    if os.path.exists(emulab.usercred_file):
        os.remove(emulab.usercred_file)
        print('Removed old cert file ' + emulab.usercred_file)
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Aerpaw Gateway'}, pythonic_params=True)
    app.run(port=8080)


if __name__ == '__main__':
    main()
