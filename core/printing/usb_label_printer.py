from io import BytesIO

from PIL import Image
from barcode import Gs1_128
from barcode.writer import SVGWriter
from brother_ql import BrotherQLRaster
from brother_ql.backends.helpers import send
from brother_ql.conversion import convert

import config
from core.printing.exceptions import PrinterErrorException, PrinterDoesNotExistException, \
    PrinterBarcodeGenerationException
from core.printing.generic_printer import GenericPrinter


class UsbLabelPrinter(GenericPrinter):
    label_usb_printer = None

    def connect(self):
        self.label_usb_printer = BrotherQLRaster(config.LABEL_PRINTER_MODEL)
        self.label_usb_printer.exception_on_warning = True

    def disconnect(self):
        if self.label_usb_printer is not None:
            self.label_usb_printer = None

    def print_label(self, barcode: str):
        if self.label_usb_printer is not None:
            try:
                # Create image of barcode from its string
                barcode_image = Image.open(self._generate_barcode_image_from_string(barcode=barcode))

                # Resize it to fit the label
                barcode_image.resize(config.LABEL_PRINTER_LABEL_RESIZE_DIMENSIONS)

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
                send(instructions=instructions, backend_identifier='pyusb',
                     printer_identifier=config.LABEL_PRINTER_IDENTIFIER, blocking=True)
            except Exception:
                raise PrinterErrorException
        else:
            raise PrinterDoesNotExistException

    def _generate_barcode_image_from_string(self, barcode: str):
        try:
            result_output = BytesIO()
            Gs1_128(barcode, writer=SVGWriter()).write(result_output)
            return result_output
        except Exception as e:
            raise PrinterBarcodeGenerationException