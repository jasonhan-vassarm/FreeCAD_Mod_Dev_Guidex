**Module developer's guide to FreeCAD source code**

by Qingfeng Xia 
http://www.iesensor.com

- 2015-09-18 version 0.1 *for FreeCAD version 0.16-dev*
- 2016-09-18 version 0.2 *for FreeCAD version 0.17-dev*

## License of this book

This ebook is licensed the same as FreeCAD document license 
CC-BY 3.0 <http://creativecommons.org/licenses/by/3.0/>

## Acknowledge to developers of FreeCAD

Original/lead developers:

- [Jürgen Riegel](http://juergen-riegel.net/)
- [Werner Mayer]()
- [yorik van havre](https://www.facebook.com/yorikvanhavre)

Add all contributors see <http://www.freecadweb.org/wiki/index.php?title=Contributors>

## Target audiances: new module developers

Make sure you are familiar with FreeCAD workbench GUI and API as a user:

- [Foundamental document on official wiki for FreeCAD](http://www.freecadweb.org/wiki/)
- [FreeCAD python API document](http://www.freecadweb.org/api/)
- [single file PDF user manual for quick start](http://sourceforge.net/projects/free-cad/files/FreeCAD%20Documentation/)

## Doxygen documents links

[Doxygen generated online documentation of source  for 0.16dev](http://www.iesensor.com/FreeCADDoc/0.16-dev/)

## Why I want to write this book

- Learn the software architecture of FreeCAD: a large open source project
- Learn to use git to contribute to open source projects like FreeCAD
- Save time for new developers to explore the source codde of FreeCAD
- Record personal note and lesson during writing/contributing code to FreeCAD
- Some chapters of this ebook is seeking to be merged into official wiki after reviewed as usable

## Organisation of this book

- Chapters are written in markdown and PDF is generated by `pandoc`
- Python scripts to link *Introduction to header files*: `*_folder_desc.py`
- Python script `merge.py` merges chapters into single md file then PDF

## How to contribute to this ebook

- git clone https://github.com/qingfengxia/FreeCAD_Mod_Dev_Guide.git

****************************************************
