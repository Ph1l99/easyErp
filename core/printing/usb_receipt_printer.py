import logging
import barcode as barcode_generator
from barcode.writer import ImageWriter
from escpos.exceptions import USBNotFoundError
from escpos.printer import Usb

import config
from core.printing.exceptions import PrinterDoesNotExistException
from core.printing.generic_printer import GenericPrinter

logger = logging.getLogger(__name__)


class UsbReceiptPrinter(GenericPrinter):
    thermal_usb_printer = None

    def __init__(self):
        self.connect()

    def connect(self):
        try:
            self.thermal_usb_printer = Usb(config.THERMAL_PRINTER_VENDOR_ID, config.THERMAL_PRINTER_PRODUCT_ID, 0, 0x81, 0x03)
        except USBNotFoundError:
            logger.error('Usb device not found. Unable to initialize printer')

    def disconnect(self):
        if self.thermal_usb_printer is not None:
            self.thermal_usb_printer.close()

    def print_repair_receipt(self, barcode: str):
        if self.thermal_usb_printer is not None:
            self.thermal_usb_printer.set(align='center', text_type='bold', height=2)
            self.thermal_usb_printer.text(config.THERMAL_PRINTER_HEADER)
            self.thermal_usb_printer.set(align='center', text_type='normal', height=1)
            self.thermal_usb_printer.text(config.THERMAL_PRINTER_SUB_HEADER)
            self.thermal_usb_printer.set(font='b', align='center', text_type='normal', height=1)
            self.thermal_usb_printer.text(config.THERMAL_PRINTER_SUB_HEADER_CONTACTS)
            self.thermal_usb_printer.image(barcode_generator.get(name='gs1_128', code=barcode, writer=ImageWriter()).render())
            self.thermal_usb_printer.text('\n')
            self.thermal_usb_printer.set(font='a', align='center', text_type='normal', height=1)
            self.thermal_usb_printer.text(config.THERMAL_PRINTER_FOOTER_REPAIR)
            self.thermal_usb_printer.cut()
        else:
            logger.error('Usb receipt printer does not exist')
            raise PrinterDoesNotExistException