import logging
from typing import TextIO
from csv import QUOTE_NONE, Dialect, DictReader, DictWriter, Sniffer

from django.conf import settings

logger = logging.getLogger(__name__)


class CSVDialect(Dialect):
    """
        CSV parsing and generation options.
        Set settings as required.
    """
    delimiter = getattr(settings, 'CSV_DELIMITER', ',')
    quotechar = getattr(settings, 'CSV_QUOTECHAR', '"')
    escapechar = getattr(settings, 'CSV_ESCAPECHAR', '\\')
    lineterminator = getattr(settings, 'CSV_LINETERMINATOR', '\n')
    quoting = getattr(settings, 'CSV_QUOTING', QUOTE_NONE)
    skipinitialspace = getattr(settings, 'CSV_SKIP_INITIAL_SPACE', True)
    doublequote = getattr(settings, 'CSV_DOUBLE_QUOTE', False)
    strict = getattr(settings, 'CSV_STRICT', True)


class CSVHandler:
    @classmethod
    def reader(cls, file_name: str, dialect: Dialect = None, encoding: str = 'utf-8-sig') -> list:
        """
            CSV Reader class
        """
        logger.info(f'Reading file {file_name}')
        data = list()
        with open(file_name, 'r', encoding=encoding) as csv_file:
            dialect = cls._detect_dialect(csv_file, dialect)
            for row in DictReader(csv_file, dialect=dialect):
                data.append(row)
        return data

    @classmethod
    def _detect_dialect(cls, csv_file: TextIO, dialect: Dialect) -> Dialect:
        number_of_rows = 1024
        start_of_file = 0
        if not dialect:
            dialect = Sniffer().sniff(csv_file.read(number_of_rows))
            csv_file.seek(start_of_file)
        return dialect

    @classmethod
    def writer(cls, header: list, data: list, output, dialect: Dialect = CSVDialect) -> None:
        """
            CSV Writer class
        """
        writer = DictWriter(output, fieldnames=header, dialect=dialect)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
        return output
