#Print Unicode characters.
import unicodedata
import sys

# Deffine the header of the program
def print_unicode_table(word):
    print("decimal hex chr {0:^40}".format("name"))
    print("------- ----- --- {0:-<40}".format(""))
    code = ord(" ")
    end = sys.maxunicode
# While the code is less than the end of the unicode table
    while code < end:
        c = chr(code)
        name = unicodedata.name(c, "*** unknown ***")
        if word is None or word in name.lower():
            print("{0:7} {0:5X} {0:^3c} {1}".format(code, name.title()))
        code += 1
# If the program is called with a argument "-h" or "--help" print the help
if __name__ == "__main__":
    word = None
    if len(sys.argv) > 1:
        if sys.argv[1] in ("-h", "--help"):
            print("usage: {0} [string]".format(sys.argv[0]))
            word = 0
        else:
            word = sys.argv[1].lower()
# If the word is not empty
    if word != 0:
        print_unicode_table(word)