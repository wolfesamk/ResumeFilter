import pandas as pd
import pdfquery

pdf_test = pdfquery.PDFQuery('testpdfresume.pdf')
pdf_test.load()
pdf_test.tree.write('xml_test.xml',pretty_print = True)
pdf_test