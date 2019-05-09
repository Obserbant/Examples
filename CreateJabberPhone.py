# Import Libraries

import requests

import re, datetime

import xml.etree.ElementTree as ET

import getpass

import sys, os

import ctypes



#Script requires an extension to be provided. It will not create a phone without an extension. This is DEFINITLY a design CHOICE. It also does not update the eup.

def writeerror(a): #Called when a check fails, writes to an error file. Takes a string containing an error message. Does not exit.

			with open('CreatePhoneErrorFile.txt','a') as f:

							f.seek(0) #Resets position in file I think "YOU THINK" or you know? doesanyonereallyknowanythingreally I just looked it up that's correct jeez

							f.write(a)

			return

def writeerrorandexit(a): #Called when a check fails,writes to an error file, provides a pop-up error message, and closes the program. Takes a string containing an error message.

			with open('CreatePhoneErrorFile.txt','a') as f:

							f.seek(0)

							f.write(a)

		   

			ctypes.windll.user32.MessageBoxA(0, a, "Python Error", 1)

			sys.exit()

			return





#Basic Argument Checks, ensure inputs are at least close to the correct sizes-----------------------------------------------------------------------

if len(sys.argv) != 12:

			errortowrite = "Invalid number of arguments. Arguments in order: 1. Call manager, 2 UserToCopy, 3. NewProfileName, 4. NewProfileNumber, 5. New Profile Mask, 6. LevelOfAccess, 7. NewUserID, 8. NewUserName, 9. GSRNumber. 10. Username 11. Ccum Password Length is " + str(len(sys.argv)) + " args: " + str(sys.argv[1:])

			writeerrorandexit(errortowrite)



if len(sys.argv[1]) <2 or len(sys.argv[1])>4:

			a= "Incorrect Call manager. Somehow. " + sys.argv[1]

			writeerrorandexit(a)

if len(sys.argv[2]) <6 or len(sys.argv[2])>15:

			a= "Incorrect user to copy size: " + sys.argv[2]

			writeerrorandexit(a)

if len(sys.argv[3]) <6 or len(sys.argv[3])>15:

			a= "Incorrect new profile name size: " + sys.argv[3]

			writeerrorandexit(a)

if len(sys.argv[4]) <6 or len(sys.argv[4])>15:

			a= "Incorrect new profile Number size. " + sys.argv[4]

			writeerrorandexit(a)     

if len(sys.argv[5]) <5 or len(sys.argv[5])>15:

			a= "Incorrect new profile Mask size: " + sys.argv[5]

			writeerrorandexit(a)

if len(sys.argv[6]) <0 or len(sys.argv[6])>5:

			a= "Incorrect Level of access. Somehow. " + sys.argv[6]

			writeerror(a)

if len(sys.argv[7]) <5 or len(sys.argv[7])>9:

			a= "Incorrect new user ID size. " + sys.argv[7]

			writeerrorandexit(a)

if len(sys.argv[9]) <10 or len(sys.argv[9])>15:

			a= "Incorrect GSR Size. " + sys.argv[9]

			writeerrorandexit(a)

#End basic argument checks, begin Variable Convenience naming-------------------------------------------

Callmanager = sys.argv[1]

UserToCopy = sys.argv[2]

NewProfileName = sys.argv[3]

NewProfileNumber = sys.argv[4]

NewProfileExternalMask = sys.argv[5]

LevelOfAccess = sys.argv[6]

NewUserID = sys.argv[7]

NewUserName = sys.argv[8]

GSRNumber = sys.argv[9]



#End Variable Naming----------------------------------------------------------------------------------

#Getcucm url, converts given abbreviation to cucm address

Desccallmanager = Callmanager

if Callmanager == "HO1":

			Callmanager = "Removed for privacy"

elif Callmanager == "HO8":

			Callmanager = "Removed for privacy"

elif Callmanager == "ME7":

			Callmanager = "Removed for privacy"

elif Callmanager == "HK1":

			Callmanager = "Removed for privacy"

elif Callmanager == "CL10":

			Callmanager = "Removed for privacy"

elif Callmanager == "HK2":

			Callmanager = "Removed for privacy"

elif Callmanager == "CL3":

			Callmanager = "Removed for privacy"

elif Callmanager == "CH1": #Service account doesn't have access to this one, Marks last one of the list I Checked

			Callmanager = "Removed for privacy"

else:

			writeerrorandexit("Call manager not supported yet.")















#Let user know the script has begun.

b = "Creating " + NewProfileName] + " based on " + UserToCopy + "."

ctypes.windll.user32.MessageBoxA(0, b, "Creating Phone", 1)



# Disable SSL Security Warnings 

requests.packages.urllib3.disable_warnings()

#Set username/password to be used in auth

username = sys.argv[10]

auth = sys.argv[11]
         

#---Begin AXL/Soap/Cucm portion ----

soapheaders = {'Content-type':'text/xml', 'SOAPAction':'CUCM:DB ver=10.0'}

#Soap Request to get phone info

soaprequest = '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://www.cisco.com/AXL/API/10.0"><soapenv:Header/><soapenv:Body><ns:getPhone><name>' + UserToCopy + '</name></ns:getPhone></soapenv:Body></soapenv:Envelope>'





AXLRequest = requests.post(Callmanager, data = soaprequest, headers = soapheaders, verify = False, auth=(username,auth))



writeerror(AXLRequest.text)



if AXLRequest.status_code==200: #If first request is successful...
# A series of regex checks to get all the fields needed from the phone2copy to be added to the new phone. Wrote a function for this in IPC version
			if re.search('\<product.{0,80}\>(.{2,80})\<\/product\>',AXLRequest.text): #and if the given pattern is found...
							match = re.search('\<product.{0,80}\>(.{2,80})\<\/product\>',AXLRequest.text) #save the value found between the tags
							NewProduct = "<product>" + match.group(1) + "</product>"#add the tags back... really? Some tags have a uuid="xxx" in them, best to avoid adding that as well.
			else:
							NewProduct = ""#else if not found, dont include the value or the tags in the request
							writeerror("Error. Product not found.")

			if re.search('\<protocol\>(.{2,80})\<\/protocol\>',AXLRequest.text):
							match = re.search('\<protocol\>(.{2,80})\</protocol\>',AXLRequest.text)

							NewProtocol = "<protocol>" + match.group(1) + "</protocol>"
			else:
							newProtocol = ""
							writeerror("Error. Protocol not found.")
							
			NewProfileName = "<name>" + NewProfileName + "</name>"

		   

			if re.search('\<devicePoolName.{0,80}\>(.{2,80})\<\/devicePoolName\>',AXLRequest.text):

							match = re.search('\<devicePoolName.{0,80}\>(.{2,80})\<\/devicePoolName\>',AXLRequest.text)

							devicePoolName = "<devicePoolName>" + match.group(1) + "</devicePoolName>"

			else:

							devicePoolName = ""

							writeerror("Error. DevicePoolName not found.")



			if re.search('\<locationName.{0,80}\>(.{2,80})\<\/locationName\>',AXLRequest.text):

							match = re.search('\<locationName.{0,80}\>(.{2,80})\<\/locationName\>',AXLRequest.text)

							NewLocationName = "<locationName>" + match.group(1) + "</locationName>"

			else:

							NewLocationName = ""

							writeerror("Error. LocationName not found.")

						   

			NewDescription = "<description>" + Desccallmanager + " " + NewUserID + " " + NewUserName + " " + GSRNumber + "</description>" # Description is an amalgamation of several things

			NewUserID = "<ownerUserName>" + NewUserID + "</ownerUserName>"

		   

			if re.search('\<phoneTemplateName.{0,80}\>(.{2,80})\<\/phoneTemplateName\>',AXLRequest.text):

							match = re.search('\<phoneTemplateName.{0,80}\>(.{2,80})\<\/phoneTemplateName\>',AXLRequest.text)

							NewPhoneTemplateName = "<phoneTemplateName>" + match.group(1) + "</phoneTemplateName>"

			else:

							NewPhoneTemplateName = ""

							writeerror("Error. PhoneTemplateName not found.")

			if re.search('\<commonPhoneConfigName.{0,80}\>(.{2,80})\<\/commonPhoneConfigName>',AXLRequest.text):

							match = re.search('\<commonPhoneConfigName.{0,80}\>(.{2,80})\<\/commonPhoneConfigName\>',AXLRequest.text)

							NewCommonPhoneConfigName = "<commonPhoneConfigName>" + match.group(1) + "</commonPhoneConfigName>"

			else:

							NewCommonPhoneConfigName = ""

							writeerror("Error. CommonPhoneConfigName not found.")

			if re.search('\<callingSearchSpaceName.{0,80}\>(.{2,80})\<\/callingSearchSpaceName\>',AXLRequest.text):

							match = re.search('\<callingSearchSpaceName.{0,80}\>(.{2,80})\<\/callingSearchSpaceName\>',AXLRequest.text)

							NewcallingSearchSpaceName = "<callingSearchSpaceName>" + match.group(1) + "</callingSearchSpaceName>"

			else:

							NewcallingSearchSpaceName = ""

						   



			if re.search('\<userLocale.{0,80}\>(.{2,80})\<\/userLocale\>',AXLRequest.text):

							match = re.search('\<userLocale.{0,80}\>(.{2,80})\<\/userLocale\>',AXLRequest.text)

							NewuserLocale = "<userLocale>" + match.group(1) + "</userLocale>"

			else:

							NewuserLocale = ""

						   

						   

			if re.search('\<deviceMobilityMode.{0,80}\>(.{2,80})\<\/deviceMobilityMode\>',AXLRequest.text):

							match = re.search('\<deviceMobilityMode.{0,80}\>(.{2,80})\<\/deviceMobilityMode\>',AXLRequest.text)

							NewdeviceMobilityMode = "<deviceMobilityMode>" + match.group(1) + "</deviceMobilityMode>"

			else:

							NewdeviceMobilityMode = ""

							writeerror("Error. deviceMobilityMode not found.")

						   

			if re.search('\<securityProfileName.{0,80}\>(.{2,80})\<\/securityProfileName\>',AXLRequest.text):

							match = re.search('\<securityProfileName.{0,80}\>(.{2,80})\<\/securityProfileName\>',AXLRequest.text)

							NewsecurityProfileName = "<securityProfileName>" + match.group(1) + "</securityProfileName>"

			else:

							NewsecurityProfileName = ""

							writeerror("Error. securityProfileName not found.")



			if re.search('\<subscribeCallingSearchSpaceName.{0,80}\>(.{2,80})\<\/subscribeCallingSearchSpaceName\>',AXLRequest.text):

							match = re.search('\<subscribeCallingSearchSpaceName.{0,80}\>(.{2,80})\<\/subscribeCallingSearchSpaceName\>',AXLRequest.text)

							NewsubscribeCallingSearchSpaceName = "<subscribeCallingSearchSpaceName>" + match.group(1) + "</subscribeCallingSearchSpaceName>"

			else:

							NewsubscribeCallingSearchSpaceName = ""

						   



			if re.search('\<sipProfileName.{0,80}\>(.{2,80})\<\/sipProfileName\>',AXLRequest.text):

							match = re.search('\<sipProfileName.{0,80}\>(.{2,80})\<\/sipProfileName\>',AXLRequest.text)

							NewsipProfileName = "<sipProfileName>" + match.group(1) + "</sipProfileName>"

			else:

							NewsipProfileName = ""

						   



			Newdisplay = "<display>" + NewUserName + "</display>"



			if re.search('\<routePartitionName.{0,80}\>(.{2,80})\<\/routePartitionName\>',AXLRequest.text):

							match = re.search('\<routePartitionName.{0,80}\>(.{2,80})\<\/routePartitionName\>',AXLRequest.text)

							NewroutePartitionName = "<routePartitionName>" + match.group(1) + "</routePartitionName>"

			else:

							NewroutePartitionName = ""

							writeerror("Error. routePartitionName not found.")



			NewdisplayAscii = "<displayAscii>" + NewUserName + "</displayAscii>"



			if NewProfileExternalMask == "false" or NewProfileExternalMask == "":  #If user doesn't want to provide a mask, program will use user to copied, and change last 4 digits of it to "XXXX"

							if re.search('\<e164Mask\>(.{2,80})\<\/e164Mask\>',AXLRequest.text):

											match = re.search('\<e164Mask\>(.{2,80})\<\/e164Mask\>',AXLRequest.text)

											NewProfileExternalMask = match.group(1)

											NewProfileExternalMask = NewProfileExternalMask[:-4]

											NewProfileExternalMask = NewProfileExternalMask + "XXXX"

											NewProfileExternalMask = "<e164Mask>" + NewProfileExternalMask + "</e164Mask>"

							else:

											NewProfileExternalMask = ""

										   



			if LevelOfAccess == "0" or LevelOfAccess == "1" or LevelOfAccess == "2": #0,1,2 are no video, 3,4 are video enabled

							newvideoCapability = "<videoCapability>0</videoCapability>"

			elif LevelOfAccess == "3" or LevelOfAccess == "4":

							newvideoCapability = "<videoCapability>1</videoCapability>"

			elif LevelOfAccess == "NotJabber":

							newvideoCapability = ""

							writeerrorandexit("Level of access set to N/A.")

			else:

							newvideoCapability = ""

							writeerror("Error. Incorrect Level of Access passed. Or N/A was passed. Somehow.")

		   

			NewProfileNumber = "<pattern>" + NewProfileNumber + "</pattern>"

		   

			if re.search('\<analyticsCollection\>(.{2,80})\<\/analyticsCollection\>',AXLRequest.text):

							match = re.search('\<analyticsCollection\>(.{2,80})\<\/analyticsCollection\>',AXLRequest.text)

							NewanalyticsCollection = "<analyticsCollection>" + match.group(1) + "</analyticsCollection>"

			else:

							NewanalyticsCollection = ""

						   



			if re.search('\<ciscoSupportField\>(.{2,80})\<\/ciscoSupportField\>',AXLRequest.text): #replace user to copy's level with provided level of access

							match = re.search('\<ciscoSupportField\>(.{2,80})\<\/ciscoSupportField\>',AXLRequest.text)

							NewciscoSupportField = match.group(1)

							NewciscoSupportField = re.sub('[01234]',LevelOfAccess, NewciscoSupportField)

							NewciscoSupportField = "<ciscoSupportField>" + NewciscoSupportField + "</ciscoSupportField>"

			else:

							NewciscoSupportField = ""

						   





#The soap request to create phone based on phone to copy

			soaprequest = '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://www.cisco.com/AXL/API/8.5"><soapenv:Header/><soapenv:Body><ns:addPhone><phone><class>Phone</class>' + NewProduct + NewProtocol + '<protocolSide>User</protocolSide>' + NewProfileName + NewDescription + devicePoolName + NewPhoneTemplateName + NewCommonPhoneConfigName + NewcallingSearchSpaceName + NewLocationName + NewuserLocale + NewUserID + NewdeviceMobilityMode + NewsecurityProfileName + NewsubscribeCallingSearchSpaceName + NewsipProfileName + '<lines><line><index>1</index>' + Newdisplay + '<dirn>' + NewProfileNumber + NewroutePartitionName + '</dirn>' + NewdisplayAscii + NewProfileExternalMask + '</line></lines><vendorConfig>' + newvideoCapability + '<vendorConfig>' + NewanalyticsCollection +NewciscoSupportField + '</vendorConfig></vendorConfig></phone></ns:addPhone></soapenv:Body></soapenv:Envelope>'

		   

			AXLRequest = requests.post(Callmanager, data = soaprequest, headers = soapheaders, verify = False, auth=(username,auth))



		   

			if AXLRequest.status_code==200: #If second request successful...

							ctypes.windll.user32.MessageBoxA(0, "Created Phone!", "Created Phone", 1)

			else:                     

							a = AXLRequest.text + Callmanager + soaprequest

							writeerror(a)

							#If a faultstring is found in response, share it

							if re.search('<faultstring>(.*)</faultstring>',AXLRequest.text):

											match = re.search('<faultstring>(.{0,200})</faultstring>',AXLRequest.text)

											b = "Failed to create phone. Please create manually. Fault string returned: " +  match.group(1)

										   

							else:

											b = "Failed to create phone. Please create manually. No fault string found."

							ctypes.windll.user32.MessageBoxA(0, b.encode('ascii'), "Python Error", 1)

else:#Else If Phone to copy not found

			ctypes.windll.user32.MessageBoxA(0, "Failed to look up user to copy. Is the correct call manager selected?", "Python Error", 1)

			a = "Failed to look up user to copy." + AXLRequest.text + Callmanager + soaprequest

			writeerror(a)
