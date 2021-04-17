# ################################################################################################################
# This is a utility script designed to execute the shell script larger than the version number mentioned inside a particular file.
# Author: Karishma Londhe 
# ################################################################################################################
# Usage:
# auto_execute_shell.py -s <shell folder> -v <version file folder>
#
#Note: Here, <shell folder> is the path of the folder in which all shell scripts are located and
#            <version file folder> is the path of the folder in which version.txt file is located
# ###########################################################################################################################
#  Algorithm for this script
#
#  1. Take the two directory names as an argument
#        -Directory where all the shell scripts are located
#        -Directory of the version.txt file
#  2. Get the version number mentioned in the version.txt file
#  3. Get the list of shell scripts that contains the number larger than the version number mentioned in the version.txtfile
#  4. Print a message and quit the execution if the number mentioned in the version.txt file is equal to the script with highest number and hence, no further execution will happen.
#  5. Execute all the schell scripts stored in the list (created in Step 3.)
#  6. Update the version.txt file with newer version number once all the applicable shell scripts are executed
#  7. Write all the activities into a log file
################################################################################################################################

import sys
import getopt
import os
import re
import subprocess
import datetime
from string import Template

#-------------------------------------------------------------------------------
def get_command_line_args(argv):
    """Return the two args we need from the command line"""
    
    shell_folder=None
    version_file_folder=None

    try:
      opts, args = getopt.getopt(argv,"h:s:v:",["help=", "shell_folder=", "version_file_folder="])

    except getopt.GetoptError as e:
        sMessage='ERROR: getopt.GetoptError, quitting\n ' + str(e)
        print sMessage
        quit(sMessage, 1)
    for opt, arg in opts:
        if opt == '-h':
            quit(syntax_msg,1) 
        elif opt in ("-s", "--shell_folder"):
            shell_folder = arg
        elif opt in ("-v", "--version_file_folder"):
            version_file_folder = arg
            
    
    return shell_folder, version_file_folder
         
#-------------------------------------------------------------------------------
def check_folder_exists(folder_path):
    """To check if the folder exists, if not then throw a message and quit"""

    if not os.path.exists(folder_path):
        sMsg = 'The folder name "' +folder_path+ '" specfied does not exist. Please enter a valid folder name'
        quit(sMsg, 1)
        
#-------------------------------------------------------------------------------
def get_version_number(version_file_folder):
    """To check get the verion number specified in the file."""
    
    #Call a method to check whether the specified folder exists
    check_folder_exists(version_file_folder)
    
    #Traverse through the folder to get version.txt file
    for (dirpath, dirnames, filenames) in os.walk(version_file_folder):
        for file in filenames:
            
            #Read the file if its version.txt
            if file == "version.txt":
                
                version_file_name =  os.path.join(dirpath,file)
                
                #Open the file in read mode
                input_file = open(version_file_name, "r")
                content_data = input_file.read()
                
                #Convert everything to lower case
                content_data= content_data.lower()
                
                #Fetch the version number
                version_number = re.sub(r"(.*)[a-z]*[\s]*[=][\s]*([0-9]*)", r"\2", content_data)

                #Close the file
                input_file.close()
                
    sMsg = 'The version number mentioned in the file is: '+version_number
    print sMsg
    list_log_of_all_output.append(sMsg)
    
    #write to the log file
    write_list_to_file (output_log_file_name, list_log_of_all_output)
    
    return version_number, version_file_name


#-------------------------------------------------------------------------------
def get_files_to_execute(shell_folder, version_number):
    """Capture only the files larger than the version number for execution"""
    
    #Call a method to check whether the specified folder exists
    check_folder_exists(shell_folder)
    
    #Type conversion
    int_version_number = int(version_number)
    list_files_to_execute=[]
    
    for (dirpath, dirnames, filenames) in os.walk(shell_folder):

        for file in filenames:

            #Extract numbers from file name 
            extract_file_numbers = re.findall('[0-9]+', file)

            str_extract_file_numbers = ''.join(extract_file_numbers)
            int_extract_file_numbers = int(str_extract_file_numbers)

            
            #Create a list of files greater than the version number
            if int_extract_file_numbers > int_version_number:
                list_files_to_execute.append(os.path.join(dirpath,file))
                
    sMsg = '\nMentioned are the list of files for execution:\n'+'\n'.join(list_files_to_execute)
    print sMsg
    
    #write to the log file
    list_log_of_all_output.append(sMsg)
    write_list_to_file (output_log_file_name, list_log_of_all_output)
    
    if len(list_files_to_execute) == 0:
        sMsg = "The version number matches the highest number from the script. Hence, there will be no execution of the scripts.!\n Quitting..."
        print sMsg
        quit(sMsg,1)

    return list_files_to_execute
    


#-------------------------------------------------------------------------------
def execute_shell_scripts(list_files_to_execute):
    """Execute the shell scripts"""

    for files_to_execute in list_files_to_execute:
        
        #Execute the shell script using subprocess module
        try:
            out_put=subprocess.check_output(['sh',files_to_execute],stderr=subprocess.STDOUT, shell=True)
            print out_put
            sMsg = "\nExecuted script:  " +str(files_to_execute)
            print sMsg
            
            #write to the log file
            list_log_of_all_output.append(sMsg)
            write_list_to_file (output_log_file_name, list_log_of_all_output)
            
        #Capture an exception in case of error
        except Exception as e:
            sMsg = 'Unable to execute file: ' +str(files_to_execute)
            
            #write to the log file
            list_log_of_all_output.append(sMsg)
            write_list_to_file (output_log_file_name, list_log_of_all_output)
    

#----------------------------------------------------------------------------------------------
def update_version_number(old_version_number, version_file_name):
    """Update the version.txt file with new version number."""

    #Update the version  number
    new_version = old_version_number+1

    #Open the input file in read mode
    file_to_update = open(version_file_name, "r")
    
    #Read file contents to string
    file_data = file_to_update.read()
    
    #Replace the version number
    file_data = file_data.replace(str(old_version_number), str(new_version))
    
    #Close the file
    file_to_update.close()
    
    #Open the input file in write mode
    file_to_update = open(version_file_name, "w")
    
    #Overrite the input file with the updated data
    file_to_update.write(file_data)
    
    #Close the file
    file_to_update.close()
    
    sMsg = "\nThe version.txt file is updated with a newer version number i.e: "+str(new_version)
    print sMsg
    
    #write to the log file
    list_log_of_all_output.append(sMsg)
    write_list_to_file (output_log_file_name, list_log_of_all_output)
    

#-------------------------------------------------------------------------------
def quit(sMsg, iErrorCode = 0):
    """This function is to quit and write the erros/status in log file"""

    final_exit_message = str(iErrorCode) + ' - ' + sMsg
    print final_exit_message
    
    # Write to the log
    list_log_of_all_output.append(final_exit_message)
    write_list_to_file (output_log_file_name, list_log_of_all_output)
    
    # Exit
    sys.exit(iErrorCode)


#-------------------------------------------------------------------------------
def write_list_to_file (file_name, list_to_write):
    """Write all screen output into a log file"""

    with open(file_name,'w') as f:
        f.write('\n'.join(list_to_write))

   
#-------------------------------------------------------------------------------
def main_function():
    """This is the main method from where all the other methods are being called"""

    #Declare a log file name
    global output_log_file_name
    
    #Declare a list to store log details
    global list_log_of_all_output
    list_log_of_all_output=[]
    
    #Get time stamp
    timestamp_string = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    
    #Declare folder name to store log files
    log_folder ="Log_folder"
    
    #Create a log folder to store all log files
    if not os.path.exists(log_folder):
        os.mkdir(log_folder)

    #Set a log file name 
    output_log_file_name = './'+log_folder+'/'+(os.path.basename(__file__)).replace('.py', '')+'_log_'+timestamp_string+'.log'

    #Message to print if incorrect parameters are passed
    syntax_msg_raw = """
        The purpose of the script is to execute shell scripts higher than the version number
        mentiontioned in version.txt file

        Usage: $utility_name -s <shell_folder> -v <version_file_folder>

        <shell_folder>: Path of the folder where all shell scripts are stored
        <version_file_folder>: Path of the folder where version.txt file is stored
        """
        
    global syntax_msg
    
    #substitute the name of the utility
    syntax_msg = Template(syntax_msg_raw).substitute(
                        utility_name = os.path.basename(__file__)
                        )
    
    # Get the command line parms
    shell_folder, version_file_folder = get_command_line_args(sys.argv[1:])
    
    #Exit the script if insufficient parameters are passed
    if not shell_folder  or not version_file_folder :
        quit(syntax_msg, iErrorCode = 1)
        
    #Continue the script execution if all the parameters are passed
    else:
    
        #Call a method to get version number and the version file name
        version_number, version_file_name = get_version_number(version_file_folder)
        
        #Call a method to get a list of files tie executed i.e. the ones which are greater than version number
        list_files_to_execute = get_files_to_execute(shell_folder, version_number)
        
        #Call a method to execute the shell scripts
        execute_shell_scripts(list_files_to_execute)
        
        #Call a amethod to increment the version number and update the version.txt file
        update_version_number(int(version_number), version_file_name)



#-------------------------------------------------------------------------------
if __name__ == "__main__":
    """This script starts from here and runs the main function"""

    # Run the main function
    main_function()
    
    sMsg = "\nEnd of script execution..."
    #Print this at the end of execution
    #write to the log file
    list_log_of_all_output.append(sMsg)
    write_list_to_file (output_log_file_name, list_log_of_all_output)
    print sMsg