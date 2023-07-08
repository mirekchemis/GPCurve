This program is designed to show and calculate peaks based on files generated by Chromelion software.

To run this program:
1) Install python3
2) Install all needed dependencies (from import section in main.py): use pip install
3) Run main.py (e.g. from command line)

To use this program:
1) Have xxx.pdf and xxx.txt in the same folder (see example)
2) Have pdf file containing constants or folder containing these files named like yearmounthdate[RI-or-UV] (see constants_example)

Tips
1) Graphs are lgM scaled
2) Black dash - bulk data
3) Colored dashdot - baseline
4) Colored line - peak
5) Uncheck 'new figure' to locate spectra on the same picture
6) Use 'ADD GAUSS' button to fit gauss curve(s) with spectra
7) 'fix lg intensity' corrects nonlinear dependency between lgM and vol
8) -C - don't touch constants file/folder
9) 'Save to csv' button saves to folder with xxx.pdf and xxx.txt
10) Peaks characteristics are shown in console


Have fun).