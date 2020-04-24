from datetime import datetime


class Invoice:
    def __init__(self, document, description, amount, reference_month, reference_year, is_active=True,
                 created_at=datetime.now(), deactive_at=None):
        self.__document = document
        self.__description = description
        self.__amount = amount
        self.__reference_month = reference_month
        self.__reference_year = reference_year
        self.__is_active = is_active
        self.__created_at = created_at
        self.__deactive_at = deactive_at

    def to_json(self):
        return {
            'document': self.__document,
            'description': self.__description,
            'amount': str(self.__amount),
            'reference_month': self.__reference_month,
            'reference_year': self.__reference_year,
            'created_at': str(self.__created_at)
        }

    def _is_active(self):
        is_active = self.__is_active
        return False if is_active is None or is_active == 0 else True

    def insert_values(self):
        return self.__document, \
               self.__description, \
               str(self.__amount), \
               self.__reference_month, \
               self.__reference_year, \
               self._is_active(), \
               str(self.__created_at)

    @classmethod
    def insert_projection(cls):
        return 'document, description, amount, reference_month, reference_year, is_active, created_at'
