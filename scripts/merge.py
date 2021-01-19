"""
by Qingfeng Xia 2016
Process of generating this ebook
-> replace file name anchor with URL
-> insert gen file into main text
-> merge chapters
-> gen PDF with pandoc
->


utf8 encoding, built may failed on windows for encoding issue
if image link fails, pdf can not be generated!
"""
from __future__ import print_function

FreeCADGitBaseUrl="https://github.com/FreeCAD/FreeCAD/tree/master/"
FreeCADsrcURL=FreeCADGitBaseUrl+'src/'

import os,sys,inspect,glob,datetime

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir+"/chapters")  #some scripts are put under chapters folder

root_folder="../"
input_folder="../chapters/" #chapters md files
build_folder="../build/"
output_folder="../pdf/"
now=datetime.datetime.now()
ts="__%04d%02d%02d" % (now.year, now.month, now.day)
merged_filename_base=build_folder+"merged_"+ts
merged_filename=merged_filename_base+".md"
generating_pdf=True
validating_url = True

os.chdir(currentdir)  # this script must be execute in script folder
if not os.path.exists(os.path.abspath(build_folder)):
    os.mkdir(os.path.abspath(build_folder))

#print input_folder+"*.md"
chapters=[os.path.basename(f) for f in glob.glob(input_folder+"*.md") if os.path.basename(f)[0] in [str(i) for i in range(10)]]

chapters=sorted(chapters, key=lambda f:int(f.split('.')[0]))
#for ch in chapters: print(ch)

CoverPageImage="../images/cover_page.png"
foreword_chapters=[] #
appendices_chapters=["FreeCAD Coding Style.md", "cmake_cheatsheet.md"]
all_chapters=foreword_chapters+chapters+appendices_chapters
all_chapters=[input_folder+f for f in all_chapters]



#tuple of FileName, Summary, Desc
#output unorder list
FileName, Summary, Desc=0,1,2
#import base_folder_desc,  app_folder_desc, gui_folder_desc
from base_folder_desc import BaseFolder
from app_folder_desc import AppFolder
from gui_folder_desc import GuiFolder
from src_folder_desc import SourceFolder
from module_folder_desc import ModuleName,ModuleFolder
from mod_folder_desc import  ModFolder
from part_folder_desc import  PartFolder

FileList=[
{"folderName":"", "obj":SourceFolder, 'descFile':build_folder+"SourceFolder.md",
"inputFile":chapters[1],"anchorText":"## List of files and folders in FreeCAD source folder"},
{"folderName":"Mod/", "obj":ModFolder, 'descFile':build_folder+"ModFolder.md",
"inputFile":chapters[1],"anchorText":"## List of modules in FreeCAD Mod folder"},
{"folderName":"Base/", "obj":BaseFolder, 'descFile':build_folder+"BaseFolder.md",
"inputFile":chapters[2],"anchorText":"## List of header files in Base folder"},
{"folderName":"App/", "obj":AppFolder, 'descFile':build_folder+"AppFolder.md",
"inputFile":chapters[2],"anchorText":"## List of header files in App folder"},
{"folderName":"Gui/", "obj":GuiFolder, 'descFile':build_folder+"GuiFolder.md",
"inputFile":chapters[3],"anchorText":"## List of header files in Gui folder"},
{"folderName":"Mod/"+ModuleName+"/", "obj":ModuleFolder, 'descFile':build_folder+"ModuleFolder.md",
"inputFile":chapters[5],"anchorText":"## List of essential files in Module folder"},
{"folderName":"Mod/Part/", "obj":PartFolder, 'descFile':build_folder+"PartFolder.md",
"inputFile":chapters[5],"anchorText":"### Important headers in Part Module"}
]

### Important headers in Part Module
#########################################################

if sys.version_info[0]<3:
    import urllib2
    def validate_url(url):
        request = urllib2.Request(location)
        request.get_method = lambda : 'HEAD'
        try:
            response = urllib2.urlopen(request)
            return True
        except urllib2.HTTPError:
            return False

else:
    import urllib.request
    def validate_url(url):
        """
        Checks that a given URL is reachable.
        :param url: A URL
        :rtype: bool
        """
        #print(url)
        request = urllib.request.Request(url)
        request.get_method = lambda: 'HEAD'

        try:
            urllib.request.urlopen(request)
            return True
        except urllib.request.HTTPError:
            return False

def check_filechange():
    pass

def link_filelist(s, folderName):
    " description + [fil.h f2.cpp]"
    starti=s.find('[')+1
    endi=s.find(']')
    flist=[f.strip() for f in s[starti:endi].split(' ') if len(f)>3]
    return s[:starti]+", ".join([gen_url(fname,folderName) for fname in flist])+s[endi:]


def gen_url(fname,folderName):
    return '['+fname+"]("+FreeCADsrcURL+folderName+fname+")"
###############################################

def gen_filelist(fname,fileList,folderName=""):
    """generate markdown file list for FreeCAD source tree
    """
    with open(fname,'w') as f:
        for it in fileList:
            if(len(it)==1): #group start
                #f.write('***\n') #sep line. cause error in pdf
                f.write("\n\n**"+it[FileName]+"**\n\n")
                #f.write('***\n') #sep line
                #print('folder group:'+it[FileName])
            else:
                f.write('- '+gen_url(it[FileName],folderName)+"\t\t"+it[Summary]+'\n')
                if len(it)>=Desc+1 and len(it[Desc])>0:
                    desc=it[Desc] #should search and replace cpp file with url link
                    if desc.find('[')>=0 and desc.find(']')>=0:
                        desc=link_filelist(desc, folderName)
                    f.write('\n>'+desc+'\n\n')


def gen_appendix_list():
    pass

#do the replacement before merge, seem only match from the first char
import re
#test regex at http://www.regexr.com/
anchor_text=re.compile(r"\[src\/.+\]") #\.[h|cpp|py]
def repalce_file_url(fname, output_filename):
    print("processing url replacement for file:",fname)
    fin=open(fname)
    with open(output_filename,'w') as fout:
        line_count = 0
        for l in fin.readlines():
            line_count += 1
            m=anchor_text.search(l)  # findall() for multiple matches
            if m:
                # m may have two patterns
                url = FreeCADGitBaseUrl+l[m.start()+1:m.end()-1]
                if validating_url and validate_url(url):
                    lnew=l[:m.start()]+m.group()+'('+url+')'+l[m.end():]
                else:
                    print('{}: is not valid in file `{}` line {}'.format(url, fname, line_count))
                    lnew = l
                fout.write(lnew)
            else:
                fout.write(l)

def file_insert(inputFile, insertedFile, posAnchor):
    print("processing file insert file:",inputFile, insertedFile, posAnchor)
    output_filename=build_folder+os.path.basename(inputFile)
    with  open(output_filename) as fin: #readonly mode
        lines=fin.readlines()
        with open(output_filename,'w') as fout:
            for l in lines:
                fout.write(l)
                if l.find(posAnchor)>=0:
                    print("found anchor text {} in file {}".format(posAnchor,inputFile))
                    with open(insertedFile) as f:
                        for linserted in f.readlines():
                            fout.write(linserted)
    return output_filename
# replace url
for fname in all_chapters:
    output_folder=build_folder
    output_filename=output_folder+os.path.basename(fname)
    repalce_file_url(fname, output_filename)

##########################################
#gen md files to be inserted to chapters
for it in FileList:
    gen_filelist(it['descFile'], it["obj"],it['folderName'])
#file insertion
for it in FileList:
    file_insert(it["inputFile"], it['descFile'], it["anchorText"])

#merging
with open(merged_filename,'w') as merged_file:
    for f in all_chapters:
        with open(build_folder+os.path.basename(f)) as fin:
            for l in fin.readlines():
                merged_file.write(l)
            if generating_pdf:
                merged_file.write('\\pagebreak\n\n')  # raw latex new page, works with 2 newlines followed


##################################################


###################################################
print('\n======convert main content into pdf #####################')
pandoc_options = """
 - code grammar highlighted with color: --highlight-style kate
 - code block is not wrapped by default: --wrap auto
 - show numbering in content --toc
 - TOC with number:  not yet supported
 - chapter header with empty line before and after will be nubmerred  -N
 - page margin setup: -V geometry:paperwidth=4in -V geometry:paperheight=6in -V geometry:margin=.5in
 - give link a color: -V colorlinks
 - page break between chapters:  --chapters
 - pdf template could be modified: where ?

 to locate error:
 `pandoc merged.md -o merged.tex`, then `pandoc merged.tex -o merged.pdf`
"""
print(pandoc_options)

from subprocess import Popen, PIPE
cmd = "pandoc -N %s --wrap auto -s --chapters --highlight-style kate --toc -V geometry:margin=.5in -V colorlinks -o %s.pdf"%(merged_filename, merged_filename_base)
print(cmd)
#print(os.getcwd())
Popen(cmd, shell=True, stdout=PIPE).communicate() #block until finish
#Popen("pandoc %s.tex -o %s.pdf"%(merged_filename_base, merged_filename_base))

#######################################################
print('\n======generate cover page and readme #####################')
#disable page number in cover page
Popen(['pandoc',input_folder+"coverpage.docx", "-o", build_folder+"coverpage.pdf"]).communicate()
Popen(['pandoc',root_folder+"Readme.md", "-o", build_folder+"Readme.pdf"]).communicate()

from PyPDF2 import PdfFileReader, PdfFileMerger
pdf_files = [build_folder+"coverpage.pdf", build_folder+"Readme.pdf", merged_filename_base+".pdf"]
#for f in pdf_files: print(f)
merger = PdfFileMerger()

for filename in pdf_files:
    merger.append(PdfFileReader(filename, "rb"))
final_output_filename = "../pdf/"+"FreeCAD_Mod_Dev_Guide"+ts+".pdf"
if os.path.exists(final_output_filename):
    os.remove(final_output_filename)
merger.write(final_output_filename)
print("final merged file: ", final_output_filename)
print('====== merge done!================')
