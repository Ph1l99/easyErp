import logging

import barcode
from barcode.writer import ImageWriter
from brother_ql import BrotherQLRaster
from brother_ql.backends.helpers import send
from brother_ql.conversion import convert

import config
from core.printing.exceptions import PrinterErrorException, PrinterDoesNotExistException, \
    PrinterBarcodeGenerationException
from core.printing.generic_printer import GenericPrinter

logger = logging.getLogger(__name__)


class UsbLabelPrinter(GenericPrinter):
    label_usb_printer = None

    def __init__(self):
        self.connect()

    def connect(self):
        self.label_usb_printer = BrotherQLRaster(config.LABEL_PRINTER_MODEL)
        self.label_usb_printer.exception_on_warning = True

    def disconnect(self):
        if self.label_usb_printer is not None:
            self.label_usb_printer = None

    def print_label(self, barcode_string: str):
        if self.label_usb_printer is not None:
            try:
                # Create image of barcode from its string
                barcode_image = self._generate_barcode_image_from_string(barcode_string=barcode_string)

                # Resize it to fit the label
                barcode_image = barcode_image.resize(config.LABEL_PRINTER_LABEL_RESIZE_DIMENSIONS)

                # Create instruction set
                instructions = convert(
                    qlr=self.label_usb_printer,
                    images=[barcode_image],
                    label=config.LABEL_PRINTER_LABEL_SIZE,
                    rotate='90', threshold=70.0,
                    dither=False,
                    compress=False,
                    red=False,
                    dpi_600=False,
                    hq=True,
                    cut=True

                )

                # send instructions to printer
                return send(instructions=instructions, backend_identifier='pyusb',
                            printer_identifier=config.LABEL_PRINTER_CONNECTION_STRING, blocking=True)
            except Exception:
                logger.error('Unable to print label')
                raise PrinterErrorException
        else:
            logger.error('Usb label printer does not exist')
            raise PrinterDoesNotExistException

    def _generate_barcode_image_from_string(self, barcode_string: str):
        try:
            return barcode.get(name='gs1_128', code=barcode_string, writer=ImageWriter()).render()
        except Exception:
            logger.error(f'Unable to generate barcode stream from code %{barcode_string}')
            raise PrinterBarcodeGenerationException
