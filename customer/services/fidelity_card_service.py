from customer.exceptions import FidelityCardAlreadyAssignedException
from customer.models import FidelityCard


class FidelityCardService:

    def is_fidelity_card_available(self, barcode):
        try:
            if barcode is not None:
                FidelityCard.objects.get(is_active=True, barcode=barcode, customer__isnull=True)
        except FidelityCard.DoesNotExist:
            raise FidelityCardAlreadyAssignedException
        return True

    def is_fidelity_card_linked_to_customer(self, barcode):
        try:
            FidelityCard.objects.get(barcode=barcode, customer__isnull=True)
        except FidelityCard.DoesNotExist:
            raise FidelityCardAlreadyAssignedException
        return False
