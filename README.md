# Shell_Python_UseCase
Language Used: 	Python2.7 --> auto_execute_shell_ver2.7.py
				Python3.7.4 --> auto_execute_shell_ver3.py

Purpose of the script:
The purpose of the script is to execute the shell scripts that contains the number larger than the version number mentioned in the version.txt file.

Mentioned are the files and folders used:
Type: File
Name: auto_execute_shell_ver2.7.py 
	This is the main python utility developed using python2.7.
	Note: auto_execute_shell_ver3.py is developed to execute using Python3.7.4.

Type: Folder
Name: Use_case/Shell/
	This folder contains all the dummy shell scripts which can be used for execution.
	
Type: Folder
Name: Use_case/Version/
	This folder contains version.txt file with a version number.
	
Usage:
Execute the script using below steps/commands:

	1. git clone https://github.com/karishmalondhe123/Shell_Python_UseCase.git
	2. Change directory to Use_case/
		cd Use_case/
	3. Execute the python utility:
		python.exe auto_execute_shell_ver2.7.py -s Shell/ -v Version/
		where,
			Shell/ and Version/ are the folders.
			
Algorithm:
1. Take the two directory names as an argument
	python.exe auto_execute_shell_ver2.py -s Shell/ -v Version/	
      -Directory where all the shell scripts are located
      -Directory of the version.txt file
2. Get the version number mentioned in the version.txt file
3. Get the list of shell scripts that contains the number larger than the version number mentioned in the version.txtfile
4. Print a message and quit the execution if the number mentioned in the version.txt file is equal to the script with highest number and hence, no further execution will happen.
5. Execute all the schell scripts stored in the list (created in Step 3.)
6. Update the version.txt file with newer version number once all the applicable shell scripts are executed
7. A folder will be created tp store log files where all the activities are written into a log file
