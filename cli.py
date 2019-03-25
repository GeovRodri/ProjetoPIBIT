import argparse
from commons.Utils import Utils
from drivers.AlibabaDriver import AlibabaDriver
from drivers.AwsDriver import AwsDriver
from drivers.AzureDriver import AzureDriver
from drivers.GoogleDriver import GoogleDriver
from drivers.OracleDriver import OracleDriver


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cloud", help='Digite a cloud desejada', type=str)

    """ Iniciando docker """
    Utils.start_docker()

    args = parser.parse_args()
    if args.cloud == 'all' or args.cloud == 'aws':
        prices_drive = AwsDriver()
        prices_drive.get()
        del prices_drive

    if args.cloud == 'all' or args.cloud == 'azure':
        prices_drive = AzureDriver()
        prices_drive.get()
        del prices_drive

    if args.cloud == 'all' or args.cloud == 'google':
        prices_drive = GoogleDriver()
        prices_drive.get()
        del prices_drive

    if args.cloud == 'all' or args.cloud == 'alibaba':
        prices_drive = AlibabaDriver()
        prices_drive.get()
        del prices_drive

    if args.cloud == 'all' or args.cloud == 'oracle':
        prices_drive = OracleDriver()
        prices_drive.get()
        del prices_drive


if __name__ == '__main__':
    main()
