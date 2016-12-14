#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging.config

from src.View.FreeconfFlask.freeconf_flask import FreeconfFlask
_author__ = 'Ondřej Lanč'
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)


if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-P', '--port',
                        nargs='?',
                        default='5000',
                        type=int,
                        help='The port number for the server to listen on. '
                             'Defaults to 5000.'
                        )
    parser.add_argument('-H', '--host',
                        nargs='?',
                        default='127.0.0.1',
                        help='The hostname or IP address for the server to '
                             'listen on. Defaults to 127.0.0.1.'
                        )
    args = parser.parse_args()
    port = args.port
    host = args.host
    import webbrowser
    url = "http://{}:{}".format(host, port)
    webbrowser.open_new(url)

    FreeconfFlask(debug=False).run(host=host, port=port)

