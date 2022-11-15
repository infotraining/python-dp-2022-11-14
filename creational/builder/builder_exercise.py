import csv
from io import StringIO
from typing import List, Protocol

file_content = '''
Jan Kowalski M 45
Anna Nowak F 23
Zenon Nijaki M 33
Ewa Nowakowska F 19
'''.strip()


class ReportBuilder(Protocol):
    def add_header(self, header: str): ...
    def begin_data(self): ...
    def add_row(self, row: List[str]): ...
    def end_data(self): ...
    def add_footer(self, footer: str): ...
    def get_report(self): ...


class HTMLBuilder:
    def __init__(self):
        self._raport = ''

    def add_header(self, h: str):
        self._raport += f'<h1>{h}</h1>\n'
        return self

    def begin_data(self):
        self._raport += '<table>\n'
        return self

    def add_row(self, row: List[str]):
        self._raport += '<tr>\n'
        for line in row:
            self._raport += f'  <td>{line}</td>\n'
        self._raport += '</tr>\n'
        return self

    def end_data(self):
        self._raport += '</table>'
        return self

    def add_footer(self, footer: str):
        self._raport += f'<div class="footer">{footer}</div>'
        return self

    def get_report(self):
        return self._raport


class CSVBuilder:
    def __init__(self):
        self._raport = ''

    def add_header(self, h: str):
        return self

    def begin_data(self):
        return self

    def add_row(self, row: List[str]):
        self._raport += ', '.join(row) + '\n'
        return self

    def end_data(self):
        return self

    def add_footer(self, footer: str):
        return self

    def get_report(self):
        return self._raport


class CSVBuilderAlt2(ReportBuilder):
    def __init__(self):
        self._stream = StringIO()
        self._csv_writer = csv.writer(self._stream)

    def add_header(self, header: str):
        pass

    def add_footer(self, footer):
        return super().add_footer(footer)

    def begin_data(self):
        pass

    def end_data(self):
        pass

    def add_row(self, row):
        self._csv_writer.writerow(row)
        return self

    def get_report(self):
        self._stream.seek(0)
        return self._stream.read()


class CSVBuilderAlt:
    def __init__(self):
        self._report: List = []

    def add_header(self, header: str):
        self._report.append(header)

    def begin_data(self):
        self._report.clear()

    def add_row(self, row: List[str]):
        self._report.append(",".join(row))

    def end_data(self):
        pass

    def add_footer(self, footer: str):
        pass

    def get_report(self):
        return self._report


class DataParser:
    def __init__(self, builder: ReportBuilder):
        self._builder = builder

    def parse(self, stream: StringIO, title="Report"):
        self._builder.add_header(title)
        self._builder.begin_data()
        for line in stream:
            self._builder.add_row(line.strip().split())
        self._builder.end_data()
        self._builder.add_footer("Copyright")


def main(report_builder, stream):
    parser = DataParser(report_builder)
    parser.parse(stream)
    doc = report_builder.get_report()
    print(doc)


if __name__ == "__main__":
    main(HTMLBuilder(), StringIO(file_content))

    # <h1>Report</h1>
    # <table>
    #   <tr>
    #     <td>Jan</td>
    #     <td>Kowalski</td>
    #     <td>M</td>
    #     <td>45</td>
    #   </tr>
    #   <tr>
    #     <td>Anna</td>
    #     <td>Nowak</td>
    #     <td>F</td>
    #     <td>23</td>
    #   </tr>
    #   <tr>
    #     <td>Zenon</td>
    #     <td>Nijaki</td>
    #     <td>M</td>
    #     <td>33</td>
    #   </tr>
    #   <tr>
    #     <td>Ewa</td>
    #     <td>Nowakowska</td>
    #     <td>F</td>
    #     <td>19</td>
    # ...
    #   </tr>
    # </table>
    # <div class="footer">End of report</div>

    #############################################################

    main(CSVBuilder(), StringIO(file_content))

    # Jan,Kowalski,M,45
    # Anna,Nowak,F,23
    # Zenon,Nijaki,M,33
    # Ewa,Nowakowska,F,19

    ############################################################

    doc = HTMLBuilder() \
        .add_header('footer') \
        .begin_data() \
        .add_row(['one', 'two', 3]) \
        .add_row(['four', 'five', 6]) \
        .end_data() \
        .add_footer('footer') \
        .get_report()

    # <h1>footer</h1>
    # <table>
    #   <tr>
    #     <td>one</td>
    #     <td>two</td>
    #     <td>3</td>
    #   </tr>
    #   <tr>
    #     <td>four</td>
    #     <td>five</td>
    #     <td>6</td>
    #   </tr>
    # </table>
    # <div class="footer">footer</div>
