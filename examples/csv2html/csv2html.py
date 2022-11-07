#!/usr/bin/env python3
# Convert a CSV file to HTML.
# Usage: python csv2html.py < data/co2-sample.csv > co2-outfile.html
import sys

def main():
    maxwidth = 100
    prin_start()
    count = 0
    while True:
        try:
            line = input()
            if count == 0:
                color = "lightblue" # header
            elif count % 2:
                color = "white"
            else:
                color = "lightgray"
            print_line(line, color, maxwidth)
            count += 1
        except EOFError:
            break
    print_end()

    def prin_start():
        print("<table border='1'>")

    def print_end():
        print("</table>")

    def print_line(line, color, maxwidth):
        print("<tr bgcolor=' {0} '>".format(color))
        fields = extract_fields(line)
        for field in fields:
            if not field:
                print ("<td></td>")
            else:
                number = field.replace(",", "")
                try:
                    x = float(number)
                    print("<td align='right'>{0:d}</td>".format(round(x)))
                except ValueError:
                    field = field.title()
                    field = field.replace(" And ", " and ")
                    field = escape_html(field)
                    if len(field) <= maxwidth:
                        print("<td>{0}</td>".format(field))
                    else:
                        print("<td>{0:.{1}}...</td>".format(field, maxwidth))
        print("</tr>")

    def extract_fields(line):
        fields = []
        field = ""
        quote = None
        for c in line:
            if c in "\"'":
                if quote is None: # start of quoted string
                    quote = c
                elif quote == c: # end of quoted string
                    quote = None
                else:
                    field += c # other quote inside quoted string
                continue
            if quote is None and c == ",": # end of field
                fields.append(field)
                field = ""
            else:
                field += c # accumulating a field
        if field:
            fields.append(field) # add the last field
        return fields

    def escape_html(text):
        text = text.replace("&", "&amp;")
        text = text.replace("<", "&lt;")
        text = text.replace(">", "&gt;")
        return text

    def print_end():
        print("</table>")

    if __name__ == "__main__":
        main()