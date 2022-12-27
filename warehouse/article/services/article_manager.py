import random
import string


class ArticleManager:
    @classmethod
    def generate_unique_barcode(cls, length: int):
        return ''.join(random.choices(string.digits, k=length))
