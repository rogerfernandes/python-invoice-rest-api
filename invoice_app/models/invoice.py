from datetime import datetime


class Invoice:
    def __init__(self, document, description, amount, reference_month, reference_year, is_active=True,
                 created_at=datetime.now(), deactive_at=None):
        self._document = document
        self._description = description
        self._amount = amount
        self._reference_month = reference_month
        self._reference_year = reference_year
        self._is_active = is_active
        self._created_at = created_at
        self._deactive_at = deactive_at

    def to_json(self):
        return {
            'document': self._document,
            'description': self._description,
            'amount': self._amount,
            'reference_month': self._reference_month,
            'reference_year': self._reference_year,
            'created_at': self._created_at
        }

    def is_active(self):
        is_active = self._is_active
        return False if is_active is None or is_active == 0 else True

    def insert_values(self):
        return self._document, \
               self._description, \
               str(self._amount), \
               self._reference_month, \
               self._reference_year, \
               self.is_active(), \
               str(self._created_at)

    @classmethod
    def insert_projection(cls):
        return 'document, description, amount, reference_month, reference_year, is_active, created_at'
