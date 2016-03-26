from lxml import html
import sys

class CsvContentExtractor:
    ''' Extracts content from a web page and prints a csv line with the extracted data.
    The constructor parameter column_description is a list of dictionaries that contain
    description of the data that needs to be extracted: column name, xpath, default
    value if the xpath fails and transformation function which changes the data extracted
    by the xpath query. '''

    def __init__(self, csv_delimiter, column_description):
        self.delim = csv_delimiter
        self.column_description = column_description

    def get_csv(self, tree):
        c_values = []
        for column in self.column_description:
            c_name = column['name']
            c_xpath = column['xpath']
            c_default = column['default']
            c_transform = column['transform']

            c_value = tree.xpath(c_xpath)
            if c_transform:
                c_value = c_transform(c_value)

            c_values.append(c_value)

        format_str = ("{:s};" * len(c_values))[:-1]
        print(format_str.format(*tuple(c_values)))
        sys.stdout.flush()
