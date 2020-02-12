#  IpaInfo.py
# -*- coding: utf-8 -*
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
import subprocess

tags = {"AppIDName": False,
        "UUID": False,
        "TeamName": False,
        "ExpirationDate": False,
        "CreationDate":False}

dictValue = {
        "AppIDName": "",
        "UUID": "",
        "TeamName": "",
        "ExpirationDate": "",
        "CreationDate":""}

VERSION_NUMBER = "1.0"

def get_target_tag(key, l):
    if tags[key]:
        value = l.replace(r"<string>","").replace(r"</string>","").replace("\t","").replace("\n","")
        if key == "ExpirationDate" or key == "CreationDate":
            value = value.replace(r"<date>","").replace(r"</date>","").split("T")[0]
        dictValue[key] = value
        tags[key] = False
    if ("<key>%s</key>"%key) in l:
        tags[key] = True

def get_provisoin_value(path):
    with open(path,"rb") as f:
        plist_file = f.readlines()
        for line in plist_file:
            for key in tags.keys():
                get_target_tag(key,line)

def get_value_by_key(path, key):
    with open(path, "r") as f:
        plist_file = f.read()

    index_0 = plist_file.find("<plist")
    index_1 = plist_file.find("</plist>")+len("</plist>")
    plist_string = plist_file[index_0:index_1]

    plist_json = plistlib.readPlistFromString(plist_string)
    value = plist_json[key]

    f.close()
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
    tool_version = "ipaInfo version : %s" % (VERSION_NUMBER)
    optParser = optparse.OptionParser(version=tool_version)
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

    # allow no "-i" switch for IPA filename if only a single argument
    if ipa_file_name is None:
        if len(sys.argv) > 1:
            ipa_file_name = sys.argv[1]
        else:
            ipa_file_name = ""

    if not os.path.exists(ipa_file_name):
        errors.append('valid input filename not provided')
    
    if suffix == ".ipa" and os.path.isfile(input_path) :
        unzip_ipa(input_path)
    else:
        print("This is not a exist ipa file. ")
        sys.exit(0)
    
    file_dir = os.path.dirname(input_path)

    if file_dir == "":
        file_dir = os.getcwd()
    
    app_dir = glob.glob( file_dir + "/Payload/*")[0]
    
    info_path = app_dir + "/info.plist"
    xcode_version = get_value_by_key( info_path, "DTXcode")
    bundle_id = get_value_by_key( info_path, "CFBundleIdentifier")
    minimum_ios = get_value_by_key( info_path, "MinimumOSVersion")
    short_version = get_value_by_key( info_path, "CFBundleShortVersionString")
    build_version = get_value_by_key( info_path, "CFBundleVersion")
    
    embedded_path = app_dir + "/embedded.mobileprovision"
    get_provisoin_value( embedded_path )
    expiration_string = dictValue["ExpirationDate"]
    creation_string = dictValue["CreationDate"]
    app_name = dictValue["AppIDName"]
    team_name = dictValue["TeamName"]
    uuid = dictValue["UUID"]
    
    result_file = input_path+"-info.txt"
    file = open( result_file, "w+")
    
    result_string = (
    "Tool Version : " + VERSION_NUMBER  + "\n" +
    ipa_file_name + "\n" +
    "-----------------------------------------" + "\n"
    "證書名稱(App Name) : " + app_name + "\n"
    "Bundle ID : " + bundle_id + "\n"
    "Team Name : " + team_name + "\n"
    "UUID      : " + uuid + "\n"
    "版本號1(ShortVersion)  : " + short_version + "\n"
    "版本號2(BundleVersion) : " + build_version + "\n"
    "證書到期日(Expiration Date) : " + expiration_string + "\n"
    "最低支援版本(Minimum Support) : " + "iOS " + minimum_ios + "\n"
    "建造日期(Creation Date) : " + creation_string + "\n"
    "建置環境(Build Xcode)   : " + xcode_version + "\n"
    "-----------------------------------------" + "\n"
    "Create By Irving Huang" + "\n"
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
    
