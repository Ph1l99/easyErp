import logging

from customer.exceptions import FidelityCardAlreadyAssignedException
from customer.models import FidelityCard

logger = logging.getLogger(__name__)


class FidelityCardService:
    @classmethod
    def is_fidelity_card_available(cls, barcode):
        try:
            if barcode is not None:
                FidelityCard.objects.get(is_active=True, barcode=barcode, customer__isnull=True)
        except FidelityCard.DoesNotExist:
            logger.warning('Fidelity card is already assigned to another user')
            raise FidelityCardAlreadyAssignedException
        return True

    @classmethod
    def is_fidelity_card_linked_to_customer(cls, barcode):
        try:
            FidelityCard.objects.get(barcode=barcode, customer__isnull=True)
        except FidelityCard.DoesNotExist:
            logger.warning('Fidelity card is already assigned to another user')
            raise FidelityCardAlreadyAssignedException
        return False
