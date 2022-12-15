from escpos.exceptions import USBNotFoundError
from escpos.printer import Usb

import config
from core.printing.generic_printer import GenericPrinter


class UsbThermalPrinter(GenericPrinter):

    thermal_usb_printer = None

    def __init__(self):
        self.connect()

    def connect(self):
        try:
            self.thermal_usb_printer = Usb(config.THERMAL_PRINTER_VENDOR_ID, config.THERMAL_PRINTER_PRODUCT_ID, 0)
        except USBNotFoundError:
            print('USb not found') # todo logging

    def disconnect(self):
        if self.thermal_usb_printer is not None:
            self.thermal_usb_printer.close()


    def print_repair_receipt(self, barcode: str):
        self.thermal_usb_printer.set(align='center', text_type='bold', height=2)
        self.thermal_usb_printer.text(config.THERMAL_PRINTER_HEADER)
        self.thermal_usb_printer.set(align='center', text_type='normal', height=1)
        self.thermal_usb_printer.text(config.THERMAL_PRINTER_SUB_HEADER)
        self.thermal_usb_printer.barcode(barcode, 'GS1-128', function_type='B')
        self.thermal_usb_printer.text('\n')
        self.thermal_usb_printer.text(config.THERMAL_PRINTER_FOOTER_REPAIR)
        self.thermal_usb_printer.cut()

