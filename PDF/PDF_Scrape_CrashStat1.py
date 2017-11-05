from __future__ import print_function
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

# function that uses pdfminer to process pdfs
# returns string
def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

#Begin pdf consumption
#crashStat = '/Users/iposton/GitHub/PdfScrape/pdfminer-20140328/Files/2015MotoCrashStat_Upd_3_2017.pdf'
resume = '/Users/iposton/GitHub/PdfScrape/pdfminer-20140328/Files/Irene_Chen_Resume_2017_Sep.pdf'
resume_str = convert_pdf_to_txt(resume)

out_file = 'irene_resume_txt.txt'
#Write content of pdf to text file
fo = open(out_file,'w+')
fo.write(resume_str)
fo.close()

# Parse each word, and build a dict
# key = word, value = number of times word appears
pdf_dict = {}
x = 0
lim = 50

fo = open('irene_resume_txt.txt','r')

for line in fo:
    for word in line.split():
        print(word)
        x+=1
        if x == lim:
            break
    if x == lim :
        break

print('here3')

fo.close()

