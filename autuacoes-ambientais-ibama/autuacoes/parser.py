#!/usr/bin/env python3
import re

import rows
from rows.fields import slug

from .cities import STATE_NAMES, get_city, split_state_city
from .validators import is_valid_cpf, is_valid_cnpj


REGEXP_CNPJ = re.compile("([0-9]{2}\.[0-9]{3}\.[0-9]{3}/[0-9]{4}-[0-9]{2})")
REGEXP_CPF = re.compile("([0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2})")
REGEXP_NUMBERS = re.compile("[0-9]")
REGEXP_PROCESSO = re.compile("([0-9./-]+)")


class BRMoneyField(rows.fields.DecimalField):
    """DecimalField which decodes from Brazilian format"""

    @classmethod
    def deserialize(cls, value):
        value = (value or "").replace(".", "").replace(",", ".").strip()
        return super().deserialize(value)


class BRDateField(rows.fields.DateField):
    """DateField which decodes from Brazilian format"""

    INPUT_FORMAT = "%d/%m/%Y"


class IbamaPdfExtractor:
    """Extract all pages from an "Autuação Ambiental" PDF, generated by IBAMA"""

    regexp_flags = re.DOTALL | re.MULTILINE
    regexp_start = re.compile(r"MINISTÉRIO DO MEIO AMBIENTE.*", flags=regexp_flags)
    regexp_end = re.compile(
        r"(Pag [0-9]+/[0-9]+|Data: [0-9]{1,2}/.*)", flags=regexp_flags
    )
    field_map = {
        "no": "numero",
        "no_a_i": "numero_auto",
        "no_processo": "numero_processo",
        "nome_autuado": "autuado",
        "status_debito": "status",
        "estado": "unidade_federativa",
    }

    def __init__(self, filename, logger=None):
        self.filename = filename
        self.header = None
        self.logger = logger

    @property
    def total_pages(self):
        return rows.plugins.pdf.number_of_pages(self.filename)

    def convert(self, row):
        """Convert/clean row data"""

        # First, rename fields to make the dataset easier to understand/use
        row = {self.field_map.get(key, key): value for key, value in row.items()}

        # Convert numbers to international format
        row["data_infracao"] = BRDateField.deserialize(row["data_infracao"])
        row["valor_multa"] = BRMoneyField.deserialize(row["valor_multa"])

        # Fix city name, get IBGE code and a better city name version (with
        # accents etc.)
        if len(row["unidade_federativa"]) > 2:
            row["unidade_federativa"] = STATE_NAMES[slug(row["unidade_federativa"])]
        try:
            (
                row["unidade_federativa"],
                row["municipio"],
                row["codigo_ibge_municipio"],
            ) = get_city(row["unidade_federativa"], row["municipio"])
        except ValueError as exp:
            if self.logger is not None:
                self.logger.warning(
                    f"Cannot parse city/state: {row['municipio']}/{row['unidade_federativa']} ({exp.args[0]})"
                )
            row["codigo_ibge_municipio"] = None

        # Detect if document is filled in the desired pattern and clean it
        original_doc = row["cnpj_cpf"]
        doc = (REGEXP_CNPJ.findall(original_doc) or REGEXP_CPF.findall(original_doc))
        if doc:
            doc = "".join(REGEXP_NUMBERS.findall(original_doc))
            row["cnpj_cpf"] = doc
            if (len(doc) == 11 and not is_valid_cpf(doc)) or (len(doc) == 14 and not is_valid_cnpj(doc)):
                self.logger.warning(f"Invalid document: {original_doc}")
        else:
            original_doc = "".join(REGEXP_NUMBERS.findall(original_doc))
            doc_cpf = "0" * (11 - len(original_doc)) + original_doc
            doc_cnpj = "0" * (14 - len(original_doc)) + original_doc
            if len(original_doc) < 11 and is_valid_cpf(doc_cpf):
                row["cnpj_cpf"] = doc_cpf
            elif len(original_doc) < 14 and is_valid_cnpj(doc_cnpj):
                row["cnpj_cpf"] = doc_cnpj
            else:
                row["cnpj_cpf"] = original_doc

        # When value spans to the second line, it gets splitted in two parts,
        # so we must remove space from it:
        row["status"] = (
            row["status"]
            .replace("defes a", "defesa")
            .replace("praz o", "prazo")
            .replace("recurs o", "recurso")
        )
        row["numero"] = row["numero"].replace(" ", "")

        return row

    def fix_rows(self, data):
        """Fix rows returned by the PDF table extraction algorithm

        - Delete repeated headers (pages 2+)
        - Remove empty rows
        - Split colum 4 into 4 and 5 when needed (the content of these cells
          sometimes are nested into one object)
        - Split colum 5 into 5 and 6 when needed (the content of these cells
          sometimes are nested into one object)
        """

        data = list(data)
        if data[0][0] == "Nº":  # Skip header if present
            if self.header is None:
                self.header = rows.fields.make_header(data[0])
            data = data[1:]

        for row in data:
            row = [
                value.replace("\n", " ").strip() if value is not None else None
                for value in row
            ]

            if not any(row):  # Empty row
                continue

            if not row[4]:  # row[3] contains state and city
                row[3], row[4] = split_state_city(row[3])
            if len(REGEXP_NUMBERS.findall(row[4] or "")) in (11, 14):
                # Fix wrong row:
                #     [..., "city doc", None, ...] -> [..., "city", "doc", ...]
                # or:
                #     [..., "city doc", "...", ...] -> [..., "city", "doc", "..." ...]
                doc = (REGEXP_CNPJ.findall(row[4]) or REGEXP_CPF.findall(row[4]))[0]
                start = row[4].find(doc)
                city = row[4][:start].strip()
                name = row[4][start + len(doc):].strip()
                row[4] = city
                if not row[5]:  # Empty, just fill
                    row[5] = doc
                else:  # Must add a column
                    row.insert(5, doc)
                row[6] = name + (row[6] or "")
            if " " in (row[5] or ""):
                # Fix wrong row:
                #     [..., "doc name", None, ...] -> [..., "doc", "name", ...]
                start = row[5].find(" ")
                row[5], row[6] = row[5][:start].strip(), row[5][start + 1 :].strip()
            doc = (REGEXP_CNPJ.findall(row[5]) or REGEXP_CPF.findall(row[5]))
            if doc and len(row[5]) > len(doc[0]):
                row[6] = (row[5][len(doc[0]):] + " " + (row[6] or "")).strip()
                row[5] = doc[0]
            proc = REGEXP_PROCESSO.findall(row[9])
            if proc and len(row[9]) > len(proc[0]):
                row[10] = (row[9][len(proc[0]):] + " " + (row[10] or "")).strip()
                row[9] = proc[0]
            row = dict(zip(self.header, row))

            # Check if row was split in correct order by checking if document
            # is present in another field (when it's not filled).
            if not row["cnpj_cpf"]:
                for value in row.values():
                    if REGEXP_CNPJ.findall(value) or REGEXP_CPF.findall(value):
                        raise ValueError(f"Row parsed incorrectly: {row}")

            yield self.convert(row)

    def extract_page(self, page_number):
        # Using `pdf_table_lines` instead of `import_from_pdf` because it's
        # faster and we can fix the table lines before importing data as a
        # `rows.Table`.
        data = rows.plugins.pdf.pdf_table_lines(
            self.filename,
            page_numbers=(page_number,),
            starts_after=self.regexp_start,
            ends_before=self.regexp_end,
            algorithm="rects-boundaries",
            backend="pdfminer.six",
            y_threshold=7,
        )
        yield from self.fix_rows(data)

    def __iter__(self):
        for page_number in range(1, self.total_pages + 1):
            for row in self.extract_page(page_number):
                yield row


if __name__ == "__main__":
    import argparse
    import logging
    from pathlib import Path

    from rows.utils import CsvLazyDictWriter
    from tqdm import tqdm

    parser = argparse.ArgumentParser()
    parser.add_argument("--log-file", default="parser.log")
    parser.add_argument("input_filename", nargs="+")
    parser.add_argument("output_filename")
    args = parser.parse_args()

    logging.basicConfig(
        filename=args.log_file,
        format="%(asctime)-15s [%(name)s] %(levelname)s: %(message)s",
        level=logging.DEBUG,
    )
    logger = logging.getLogger("parser")

    progress = tqdm(unit_scale=True, unit="rows")
    writer = CsvLazyDictWriter(args.output_filename)
    for filename in args.input_filename:
        iterator = IbamaPdfExtractor(filename, logger=logger)
        progress.desc = f"Parsing {Path(filename).name}"
        for row in iterator:
            writer.writerow(row)
            progress.update()
    writer.close()
    progress.close()
