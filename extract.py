#!/usr/bin/python
import sys, getopt, inspect, os, subprocess

def myworkspace():
    return os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

def terminate(var):
    print var
    sys.exit(2)

def getRealPackageName(package_name):
    #SEARCHING FOR PACKAGE
    command = "adb shell pm list packages | grep "+package_name
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
    output = process.communicate()
    orginal_package_name = output[0].replace("package:", "")
    counts = orginal_package_name.count('\n')

    if counts > 1:
        print orginal_package_name
        print "\n---------------------------------------"
        print "We found more than "+str(counts)+" Packages"
        text = raw_input("Enter the correct package name: ")
        if text == '':
            terminate("Terminating")
        else:
            orginal_package_name = getRealPackageName(text);
    elif counts == 0:
        print "\n---------------------------------------"
        text = raw_input("No application found with the given package name.\nEnter a correct package name: ")
        if text == '':
            terminate("Terminating")
        else:
            orginal_package_name = getRealPackageName(text);

    orginal_package_name = orginal_package_name.replace("\n", "")
    orginal_package_name = orginal_package_name.replace("\r", "")

    return orginal_package_name;

def runwizard():
    os.system("echo 'Welcome To Android Data Extraction Script'");
    os.system("echo 'Connect Your Android Device'");
    text = raw_input("Press Enter When You Are Ready")
    os.system("echo '--------------------------------------------------------------'");
    os.system("echo 'Listing Your Device'");
    os.system("adb devices -l")
    os.system("echo '--------------------------------------------------------------'");
    package_name = raw_input("Enter Package Name: ")

    package_name = getRealPackageName(package_name)
    os.system("echo 'Package: "+package_name+"'");
    extracting(package_name,'A')

def extracting(package_name,workspace):
    #SEARCHING FOR PACKAGE
    os.system("echo '-------------------------------------------'")
    os.system("echo 'Intitaing Extraction Process'")
    os.system("echo 'Searching For: '"+package_name)
    mobile_workspace = "/sdcard/Android-Extractor/"



    #Creating Folder
    os.system("echo 'Creating Workspace Inside: '"+mobile_workspace)
    command = "adb shell mkdir -p "+mobile_workspace
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
    output = process.communicate()


    os.system("echo 'Copying in Progress... '")
    command = 'adb shell "su -c cp -RFd /data/data/'+package_name+'/ '+mobile_workspace+'"'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
    output = process.communicate()


    #Extracting APK

    if workspace == 'A':
        newworkspace =  myworkspace()
        command  = "adb pull "+mobile_workspace+package_name+"/ '"+newworkspace+"'"
    else:
        command  = "adb pull "+mobile_workspace+package_name+"/ '"+workspace+"'"

    process = subprocess.call(command, shell=True)
    os.system("echo 'Succesfully Completed '")
    sys.exit(2)


def main(argv):
    package_name = ''
    output_folder = 'A'
    try:
        opts, args = getopt.getopt(argv,"hp:o:",["package=","output="])
    except getopt.GetoptError:
        print 'extract.py -p <package name> -o <output folder>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'extract.py -p <package name> -o <output folder>'
            sys.exit()
        elif opt in ("-p", "--package"):
            package_name = arg
        elif opt in ("-o", "--output"):
            output_folder = arg
    if package_name == '' :
        runwizard()
    else:
        package = getRealPackageName(package_name)
        extracting(package,output_folder)


if __name__ == "__main__":
   main(sys.argv[1:])
