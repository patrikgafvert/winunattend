#!/usr/bin/env python3
import xml.etree.ElementTree as ET
from xml.dom import minidom
import subprocess

BypassText =[]
tree = {}
RunSynchronousCommands_text = ['BypassTPMCheck','BypassSecureBootCheck','BypassRAMCheck']
for ByText in (RunSynchronousCommands_text):
    BypassText += [f"reg add HKLM\\SYSTEM\\Setup\\LabConfig /v {ByText} /t REG_DWORD /d 1 /f"]
settings_text = ["disabled", "specialize", "oobeSystem"]
components_text = ["Microsoft-Windows-Setup","Microsoft-Windows-Deployment","Microsoft-Windows-Shell-Setup", "Microsoft-Windows-International-Core", "Microsoft-Windows-SecureStartup-FilterDriver", "Microsoft-Windows-EnhancedStorage-Adm"]
components_attrib = {"processorArchitecture":"amd64","language":"neutral", "xmlns:wcm":"http://schemas.microsoft.com/WMIConfig/2002/State","xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance","publicKeyToken":"31bf3856ad364e35","versionScope":"nonSxS"}
tree[0] =  ET.Element("unattend", attrib={"xmlns": "urn:schemas-microsoft-com:unattend"})
tree[1] =  ET.SubElement(tree[0], "settings", attrib={"pass":settings_text[0]})
tree[2] =  ET.SubElement(tree[1], "component", attrib={"name":components_text[0],**components_attrib})
tree[3] =  ET.SubElement(tree[2], "UserData")
tree[4] =  ET.SubElement(tree[3], "ProductKey")
tree[5] =  ET.SubElement(tree[4], "Key")
tree[6] =  ET.SubElement(tree[2], "RunSynchronous")
for i, num in enumerate(range(7,13+1,3)):
	tree[num] =  ET.SubElement(tree[6], 'RunSynchronousCommand', attrib={'wcm:action':'add'})
	tree[num+1] =  ET.SubElement(tree[num], 'Order');tree[num+1].text = str(i+1)
	tree[num+1] =  ET.SubElement(tree[num], 'Path');tree[num+1].text = BypassText[i]
tree[16] = ET.SubElement(tree[0], "settings", attrib={"pass":settings_text[1]})
tree[17] = ET.SubElement(tree[16], "component", attrib={"name":components_text[1], **components_attrib})
tree[18] = ET.SubElement(tree[17], 'RunSynchronous')
tree[19] = ET.SubElement(tree[18], 'RunSynchronousCommand', attrib={'wcm:action':'add'})
tree[20] = ET.SubElement(tree[19], 'Order');tree[20].text = str(1)
tree[21] = ET.SubElement(tree[19], 'Path');tree[21].text = "reg add HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\OOBE /v BypassNRO /t REG_DWORD /d 1 /f"
tree[22] = ET.SubElement(tree[0], "settings", attrib={"pass":settings_text[2]})
tree[23] = ET.SubElement(tree[22], "component", attrib={"name":components_text[2], **components_attrib})
tree[24] = ET.SubElement(tree[23], 'OOBE')
tree[25] = ET.SubElement(tree[24], 'ProtectYourPC');tree[25].text = str(3)
tree[26] = ET.SubElement(tree[23], 'UserAccounts')
tree[27] = ET.SubElement(tree[26], 'LocalAccounts')
tree[28] = ET.SubElement(tree[27], 'LocalAccount', attrib={'wcm:action':'add'})
tree[29] = ET.SubElement(tree[28], 'Name');tree[29].text = "Patrik"
tree[30] = ET.SubElement(tree[28], 'DisplayName');tree[30].text = "Patrik"
tree[31] = ET.SubElement(tree[28], 'Group');tree[31].text = "Administrators;Power Users"
tree[32] = ET.SubElement(tree[28], 'Password')
tree[33] = ET.SubElement(tree[32], 'Value');tree[33].text = "UABhAHMAcwB3AG8AcgBkAA=="
tree[34] = ET.SubElement(tree[32], 'PlainText');tree[34].text = "false"
tree[35] = ET.SubElement(tree[23], 'FirstLogonCommands')
tree[36] = ET.SubElement(tree[35], 'SynchronousCommand', attrib={'wcm:action':'add'})
tree[37] = ET.SubElement(tree[36], 'Order');tree[37].text = str(1)
tree[38] = ET.SubElement(tree[36], 'CommandLine');tree[38].text = "net user &quot;Patrik&quot; /logonpasswordchg:yes"
tree[39] = ET.SubElement(tree[22], "component", attrib={"name":components_text[3], **components_attrib})
tree[40] = ET.SubElement(tree[39], 'InputLocale');tree[40].text = "0000041d"
tree[41] = ET.SubElement(tree[39], 'SystemLocale');tree[41].text = "sv-SE"
tree[42] = ET.SubElement(tree[39], 'UserLocale');tree[42].text = "sv-SE"
tree[43] = ET.SubElement(tree[39], 'UILanguage');tree[43].text = "sv-SE"
tree[44] = ET.SubElement(tree[39], 'UILanguageFallback');tree[44].text = "en-US"
tree[45] = ET.SubElement(tree[22], "component", attrib={"name":components_text[4], **components_attrib})
tree[46] = ET.SubElement(tree[45], 'PreventDeviceEncryption');tree[46].text = "true"
tree[47] = ET.SubElement(tree[22], "component", attrib={"name":components_text[5], **components_attrib})
tree[48] = ET.SubElement(tree[47], 'TCGSecurityActivationDisabled')
tree[48].text = str(1)
tree[0].tail = "\n"

# Patch ElementTree so you can use the & char.
def _escape_cdata(text):
	return text
ET._escape_cdata = _escape_cdata
ET.indent(tree[0])
fd = open("unattend.xml", 'w')
fd.write(ET.tostring(tree[0], encoding='utf-8', xml_declaration=True).decode('utf-8').replace("'","\"").replace("\n","\r\n"))
fd.close()

# Make the unattend.xml floppy img.
output = subprocess.run("dd if=/dev/zero of=floppy.img count=1440 bs=1k".split(" "), capture_output=True, shell=False)
output = subprocess.run("mformat -t 80 -h 2 -s 18 -v UNATTEND -N 0 -i floppy.img".split(" "), capture_output=True, shell=False)
output = subprocess.run("mcopy -i floppy.img unattend.xml ::".split(" "), capture_output=True, shell=False)
