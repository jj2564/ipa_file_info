# ipa_file_info
This is for enterprise distribution. It may show the bundle id, build xcode version, expiration date ... 
You edit by yourself if there is something needed or not.
Also provide a exe for windows. Source code may check it on win-branch.

## Enviroment
Python: 2.7
OS: mac os

## How to use
```script
$python ipaInfo.py -f {file_path}
```
or  just use the unix file
```script
$./ipaInfo -f {file_path}
```

## How to use (Win)
Because I use the traditional chinese and cause the coding problem.
So you need to change the coding inside the CMD.
```script
$ chcp 65001
```
This may change the coding to utf-8.
```script
$ ipaInfo.exe -f {file_path}
```
Or you can just remove the text of traditional chinese...


## Result

```
APP_FILE_NAME
-----------------------------------------
證書名稱(App Name) : APP_NAME
Bundle ID : BUNDLE_ID
Team Name : TEAM_NAME
UUID      : UUID
版本號1(ShortVersion)  : 2.1.25.1855
版本號2(BundleVersion) : 1
證書到期日(Expiration Date) : 2021-02-03
最低支援版本(Minimum Support) : iOS 10.0
建造日期(Creation Date) : 2020-02-04
建置環境(Build Xcode)   : 1030
-----------------------------------------
Create By Irving Huang
```

## TODO

There is still lots of problem.  Hope someday can fix those issue
- [ ] Not enter any option may show debug error message.
- [ ] More error proof.
- [ ] Better way to analyze on Win.  
more...
