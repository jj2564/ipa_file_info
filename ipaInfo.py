#  IpaInfo.py

import sys
import os
import re
import glob
import zipfile
import plistlib
import shutil
import optparse
import time
import datetime


def get_value_by_key(path, key):
    with open(path, "r") as f:
        plist_file = f.read()

    index_0 = plist_file.find("<plist")
    index_1 = plist_file.find("</plist>")+len("</plist>")
    plist_string = plist_file[index_0:index_1]

    plist_json = plistlib.readPlistFromString(plist_string)
    value = plist_json[key]

    return value

# unzip ipa to path
def unzip_ipa(path):
#    print("Zip")
    zfile = zipfile.ZipFile(path, "r")
    zfile.extractall(os.path.dirname(path))

def remove_payload(path):
    shutil.rmtree(path, ignore_errors=True)
    
# setting options
def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("-f", "--file", action="store", dest="input_path", help="provide ipa path.")
    
    opts_args = optParser.parse_args()
    return opts_args[0]

def get_file_name(path):
    array_path = os.path.split(path)
    file_name = array_path[1]
    return file_name
    
# main
def main():

    options = get_options()
    input_path = options.input_path
    ipa_file_name = get_file_name(input_path)
    suffix = os.path.splitext(ipa_file_name)[-1]
    
    if suffix == ".ipa" and os.path.isfile(input_path) :
        unzip_ipa(input_path)
    else:
        print("This is not a exist ipa file. ")
        sys.exit(0)
    
    file_dir = os.path.dirname(input_path)
    
    # if ipa in current folder need to add the path.
    if file_dir == "":
        file_dir = os.getcwd()
    
    app_dir = glob.glob( file_dir + "/Payload/*")[0]
    
    info_path = app_dir + "/info.plist"
    xcode_version = get_value_by_key( info_path, "DTXcode")
    bundle_id = get_value_by_key( info_path, "CFBundleIdentifier")
    minimum_ios = get_value_by_key( info_path, "MinimumOSVersion")
    
    embedded_path = app_dir + "/embedded.mobileprovision"
    expiration_date = get_value_by_key( embedded_path, "ExpirationDate")
    expiration_string = expiration_date.strftime("%Y-%m-%d")
    creation_date = get_value_by_key( embedded_path, "CreationDate")
    creation_string = creation_date.strftime("%Y-%m-%d")
    app_name = get_value_by_key( embedded_path, "AppIDName")
    
    
    result_file = input_path+"-info.txt"
    file = open( result_file, "w+")
    
    result_string = (
    ipa_file_name + "\n" +
    "-----------------------------------------" + "\n"
    "App Name           : " + app_name + "\n"
    "Expiration Date    : " + expiration_string + "\n"
    "Bundle ID          : " + bundle_id + "\n"
    "Minimum Support    : " + "iOS " + minimum_ios + "\n"
    "Build Xcode        : " + xcode_version + "\n"
    "Creation Date      : " + creation_string + "\n"
    )
    
    file.write(
        result_string
    )
    file.close()
    
    print(result_string)
    remove_payload(file_dir + "/Payload/")

# init
if __name__ == "__main__":
    main()
    sys.exit(0)
    
