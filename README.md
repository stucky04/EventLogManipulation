# EventLogManipulation

##To use existing executable:
1. Download whole "dist" folder with data files included in folder structure
2. Start executable file

##To deploy new executable:
1. Use pyinstaller with the existing .spec file to create .exe with following command:
pyinstaller --onefile --windowed src/gui.spec src/gui.py
2. copy functionalities/dqi/dqi_descriptions.xml WITH folder structure to the dist folder created by pyinstaller 
