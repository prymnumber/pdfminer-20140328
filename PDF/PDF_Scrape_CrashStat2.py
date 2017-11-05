from __future__ import print_function
import warnings

warnings.filterwarnings("ignore")

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
import os
#import matplotlib %inline
#matplotlib.style.use('ggplot')
import matplotlib.pyplot as plt
#from ggplot import *
import pandas as pd


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
    pagenos = set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

#global stuff
filler_words = {'the','of','to','and','in','for','is','were','will','on','or','a','an'}

# Begin pdf consumption
#pdf_file = '/Users/iposton/GitHub/PdfScrape/pdfminer-20140328/Files/Irene_Chen_Resume_2017_Sep.pdf'
pdf_file = '/Users/iposton/GitHub/PdfScrape/pdfminer-20140328/Files/v2_2015MotoCrashStat_Upd_3_2017.pdf'
#pdf_file = '/Users/iposton/GitHub/PdfScrape/pdfminer-20140328/Files/administrative_guide_vacations.pdf'
#pdf_file = '/Users/iposton/GitHub/PdfScrape/pdfminer-20140328/Files/recruiting_and_hiring_of_regular_staff.pdf'
pdf_file_str = convert_pdf_to_txt(pdf_file)

out_file = 'PDF_text_outputtxt'
# Write content of pdf to text file
fo = open(out_file, 'w+')
fo.write(pdf_file_str)
fo.close()

# Parse each word, and build a dict
# key = word, value = number of times word appears
pdf_dict = {}
x = 0
lim = 0

# open the converted file
fo = open(out_file, 'r')

# initialize dictionary with file name and size (in bytes)
pdf_dict[out_file] = os.path.getsize(out_file)

# for each word in file, count how many times it exist in the file
for line in fo:
    for word in line.split():

        #if word already exist, just increment count
        if pdf_dict.has_key(word):
            pdf_dict[word] = pdf_dict[word] + 1
        #if wordis new, then add to list
        else:
            #word is not one of fller_words
            pdf_dict[word] = 1

        if lim <> 0:
            x += 1
            if x == lim:
                break
    if lim <> 0:
        if x == lim:
            break

fo.close()

# Overwrite initialization settings and put actual word count as value for the file name
pdf_dict[out_file] = len(pdf_dict)

#count how many words are in the file
total_words = 0
for i in pdf_dict:
    if i <> out_file:
        total_words += pdf_dict[i]

print("Total words:", total_words)
print("There are", pdf_dict[out_file], "unique words in document", out_file)

# sort dict in descending order (highest count first)
ordered_pdf_dict = sorted(pdf_dict.items(), key=lambda t: t[1], reverse=True)

# x=0
# for i in ordered_pdf_dict:
#    x+=1
#    print(i)
#    if x==5:
#        break

# convert dict into pandas dataframe for plotting
pdf_df = pd.DataFrame(pdf_dict.items(), columns=['Word', 'Word Count'])
pdf_df_limit = pdf_df.sort_values(["Word Count"], ascending=False)[1:15]
print('Panda frame')
print(pdf_df_limit.head(15))

#plot bar chart
b = plt.figure()
pdf_df_limit.plot.bar(x='Word')
plt.show(b)


print('very end')

exit()
