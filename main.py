import argparse

import client.client as client
import client.gui as gui

import server.server as server


def main():
    # add parser
    parser = argparse.ArgumentParser(description='Choos what buzzer sub-command to run')

    # add subparsers
    subparsers = parser.add_subparsers(help='available sub-commands')

    # start server
    subparser_start = subparsers.add_parser('start', help='start server')
    subparser_start.set_defaults(func=server.main)

    # server request
    subparser_request = subparsers.add_parser('request', help='request server')
    subparser_request.add_argument('--ip', type=str, default='101.101.1.2', help='server ip')
    subparser_request.add_argument('--port', type=int, default=12345, help='server port')
    subparser_request.set_defaults(func=client.main)

    # run GUI
    subparser_gui = subparsers.add_parser('gui', help='run GUI')
    subparser_gui.add_argument('--ip', type=str, default='101.101.1.2', help='server ip')
    subparser_gui.add_argument('--port', type=int, default=12345, help='server port')
    subparser_gui.add_argument('--physical_buzzers', action='store_true', default=False, help='wheter or not to require physical buzzers')
    subparser_gui.set_defaults(func=gui.start_gui)

    # run function
    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
