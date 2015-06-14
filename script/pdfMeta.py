"""
pip search pypdf
sudo pip install PyPDF2
"""

from PyPDF2 import PdfFileReader

fname = ''

inputPdf = PdfFileReader(open(fname, 'rb'))

print inputPdf.getDocumentInfo()

#TODO class print info given pdf name
