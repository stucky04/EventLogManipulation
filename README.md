# Event Logs and Process Model

The event logs in the folder "Event_Logs_And_Process_Model" are modifications of the real-world event log published in [1]. The process model is built according to the descriptions in [2]. 


# Event Log Manipulation Tool

The event log manipulation tool builds on the classification of data quality issues by [3]. 

## To use existing executable:
1. Download whole "dist" folder with data files included in folder structure
2. Start executable file

## To deploy new executable:
1. make sure you have installed pyinstaller
2. Use pyinstaller with the existing .spec file to create .exe with following command:
pyinstaller --onefile --windowed src/gui.spec src/gui.py
3. navigate to "dist" folder (created by pyinstaller)
4. create new path with empty folders "dist/functionalities/dqi"
5. copy "src/functionalities/dqi/dqi_descriptions.xml" into "dist/functionalities/dqi"

## Explanation of Different Files

In order to use the application as-is, this is not required to read!

If you want to change the existing application and its methods, the following provides some insights about the files and their contents.

1. __LogManipulation.py__
contains the central LogManipulation object, in which the event logs are loaded and all required (modification) methods are called from

2. __gui.py__
contains the code to generate the GUI and its functionalities

3. Modules:

3.1 __Missing.py__
all methods for DQI I1-I9

3.2 __Incorrect.py__
all methods for DQI I10-I18

3.3 __Imprecise.py__
all methods for DQI I19-I25

3.4 __Irrelevant.py__
methods for DQI I26-I27


# References

[1] de Leoni, M. (Massimiliano); Mannhardt, Felix (2015): Road Traffic Fine Management Process. 4TU.ResearchData. Dataset. https://doi.org/10.4121/uuid:270fd440-1057-4fb9-89a9-b699b47990f5 

[2] F. Mannhardt. Multi-perspective Process Mining: Proefschrift. SIKS Dissertation, Eindhoven. 2018.

[3] R. J. C. Bose, R. S. Mans and Wil M. van der Aalst. Wanna improve process mining results? In IEEE (Ed.), IEEE Symposium on
Computational Intelligence and Data Mining (CIDM). IEEE, 2013, pp. 127???134.
