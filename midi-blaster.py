#Author: Benjamin Caccia
#Email: reverbtank@gmail.com
#Website: www.bcacciaaudio.com 
#Year: 2015
#MIDI Blaster version 0.0.7

import pygame
import pygame.midi
import time	#for MIDI delay time
import os	#for clearing the terminal 	
import sys	#platform identification
from colorama import init, Fore #ANSI color rendering support
from Tkinter import * #the entire Tkinter library. This allows us to kill the root window that is spawned by dialogs.
import tkFileDialog #for pop up dialog for file selection
import codecs #for unicode filename handling

def main_menu():
	
	#identifies OS and appropriately clears the terminal		
	os.system(identify_os())
	global inputMIDI
	global outputMIDI
	print "\nMIDI Blaster 0.0.7"	
	print "------------------- \n \n"
	print "1. Select MIDI Input"
	print "2. Select MIDI Output"
	print "3. Send MIDI"
	

	print(Fore.GREEN)
	print "\nMIDI input:  ", inputMIDI + 1
	print "MIDI output: ", outputMIDI + 1
	print(Fore.RESET)
	while True:
		try:
			inputChoice = int(raw_input("\nEnter the number of your choice: "))
		
		except ValueError:
			print("ERROR! Enter a valid menu choice.")
			#return to the start of the loop
			continue
		
		if inputChoice < 1 or inputChoice > 3:
			print("ERROR! Enter a valid menu choice.")
			continue
		
		else:
			
			if inputChoice == 1:
				inputMIDI = choose_input_device()
				break
				
			if inputChoice == 2:
				outputMIDI = choose_output_device()
				break
				
			if inputChoice == 3:
				midi_send_menu()
				break
		


def midi_send_menu():
	
	os.system(identify_os())
	print "\nMIDI Blaster 0.0.7"	
	print "------------------- \n \n"
	while True:
		print "1. Enter list of MIDI to send"
		print "2. Back"
		print(Fore.GREEN)
		print "\nMIDI input:  ", inputMIDI + 1
		print "MIDI output: ", outputMIDI + 1
		print(Fore.RESET)
		
		try:
			inputChoice = int(raw_input("\nEnter the number of your choice: "))
		
		except ValueError:
			print("ERROR! Enter a valid menu choice.")
			#return to the start of the loop
			continue
		
		if inputChoice < 1 or inputChoice > 2:
			print("ERROR! Enter a valid menu choice.")
			continue
		
		else:
			
			if inputChoice == 1:
				midi_send_entry()
				break
			
			if inputChoice == 2:
				main_menu()
				break	
				
				
def choose_input_device():
	
	os.system(identify_os())
	pygame.init()
	pygame.midi.init()
	
	deviceNum = pygame.midi.get_count()
	defaultDevIn = pygame.midi.get_default_input_id()
	defaultDevOut = pygame.midi.get_default_output_id() 

	print "Number of Devices: [%s]" % deviceNum
	print "Default MIDI input [%s]" % defaultDevIn
	print "Default MIDI output [%s]" % defaultDevOut
	
	print "\nThese are all available MIDI interfaces"
	print "-----------------------------------------------------------"


	#Iterate through and print all available MIDI interfaces	
	for i in range(deviceNum):
	
		interface = pygame.midi.get_device_info(i)
		#trim the first garbage part of the device info string
		print i + 1, interface[1:]

		
	print "-----------------------------------------------------------"
	
	while True:
		try:
			inputChoice = int(raw_input("\nEnter the number of the MIDI interface you want to use for input: "))
	
		except ValueError:
			print("ERROR! Enter a valid interface number.")
			#return to the start of the loop
			continue
			
		if inputChoice > deviceNum or inputChoice < 0:
			print("ERROR! Enter a valid interface number.")
			continue
			
		else:
			#exit the loop
			break
	
	pygame.midi.quit()
	return inputChoice - 1
	
	
def choose_output_device():
	
	os.system(identify_os())
	pygame.init()
	pygame.midi.init()
	
	deviceNum = pygame.midi.get_count()
	defaultDevIn = pygame.midi.get_default_input_id()
	defaultDevOut = pygame.midi.get_default_output_id() 

	print "Number of Devices: [%s]" % deviceNum
	print "Default MIDI input [%s]" % defaultDevIn
	print "Default MIDI output [%s]" % defaultDevOut
	
	print "\nThese are all available MIDI interfaces"
	print "-----------------------------------------------------------"


	#Iterate through and print all available MIDI interfaces	
	for i in range(deviceNum):
	
		interface = pygame.midi.get_device_info(i)
		#trim the first garbage part of the device info string
		print i +1, interface[1:]

		
	print "-----------------------------------------------------------"
	
	while True:
		try:
			outputChoice = int(raw_input("\nEnter the number of the MIDI interface you want to use for output: "))
	
		except ValueError:
			print("ERROR! Enter a valid interface number.")
			#return to the start of the loop
			continue
			
		if outputChoice > deviceNum or outputChoice < 0:
			print("ERROR! Enter a valid interface number.")
			continue
			
		else:
			#exit the loop
			break
	
	pygame.midi.quit()
	return outputChoice - 1
	
	
def identify_os():

		system = sys.platform
		if system == "win32":
			return "cls"
		
		else:
			return "clear"
			
#checks to make sure that input is between 0 and 127			
def midi_range(value):

	while value < 0 or value > 127:
		value = input("Enter a value between 0 and 127:")
		
	else:
		return value
		
			
def channel_range(value):

	while value < 1 or value > 16:
		value = input("Enter a value between 1 and 16:")
		
	else:
		return value
			
#Setup an event loop to listen for MIDI
#Pulled from example code at:
#https://audiodestrukt.wordpress.com/2013/06/23/midi-programming-in-python/


def midi_input():

	while True:
		if inputMIDI.poll():
			print inputMIDI.read(1000)
			
		pygame.time.wait(10)


def midi_send_entry():
	
	os.system(identify_os())
	pygame.init()
	pygame.midi.init()
	global outputMIDI
	global sendRepeat
	
	print "\n\nEnter values in HEX (must be preceded with 0x). Enter delay in milliseconds."
	print "----------------------------------------"
	print "Enter requested values all separated by commas."
	print "\nMain menu = m"
	print "\nSend = n"
	print "\nLoad batch file = i"
	print "\nOutput queue to file = o"
	print "\nDelete entry = d"
	print "\nClear = c"
	print "\nReverse queue order = f"
	print "\nSet number of times to send contents of queue = r"
	#print "\nReplace all status bytes = sr (broken)"
	
	#grants access to globally define variable
	global outputList
	userMIDI = 0
	while userMIDI != "n" or userMIDI != "N":
		#prints entire list for user
		print(Fore.GREEN)
		print "\n\nMIDI items in Queue:", len(outputList)
		print "Send entire Queue x:", sendRepeat 
		print(Fore.RESET)
		
		for i in range(len(outputList)):
			print(Fore.YELLOW)
			print i + 1, " ", outputList[i]
			print(Fore.RESET)
		
		#Example MIDI input values would be "0x90,0x36,0x7F,0"	
		print "\n\n"
		userMIDI = raw_input("Status, Note, Velocity, Send Delay: ")
		
		#userMIDI is split into a list so it can be easily counted without the commas
		listTally = []
		listTally = userMIDI.split(",")
		#checks to make sure that there are 4 values(including commas) being input
		
		
		if userMIDI == "d" or userMIDI == "D":
			userErase = int(raw_input("\nEnter the number of the command to remove: "))
			del outputList[userErase - 1]
			print userErase, " removed successfully!"
			continue
		
		
		elif userMIDI == "c" or userMIDI == "C":
			outputList = []
			continue
		
		
		elif userMIDI == "n" or userMIDI == "N":
			break
		
		elif userMIDI == "f" or userMIDI == "F":
			flipBucket = []
			for i in reversed(outputList):
				flipBucket.append(i)
			
			outputList = flipBucket
			continue
			
		elif userMIDI == "i" or userMIDI == "I":
			midi_batch_send()
			continue

		elif userMIDI == "o" or userMIDI == "O":
			midi_queue_write()
			continue
			
		elif userMIDI == "m" or userMIDI == "M":
			main_menu()
			continue

		elif userMIDI == "r" or userMIDI == "R":
			sendRepeat = int(raw_input("Enter number of times to send the contents of the queue: "))
			continue

			
		#incomplete
		elif userMIDI == "sr" or userMIDI == "SR":
			newList = []
			tempStatusByte = raw_input("\nEnter the new status byte: ")
			
			print outputList[0][0]

			for i in range(len(outputList)):
				print range(len(outputList))
				tempList = list(outputList[0][i])
				tempList[0:4] = tempStatusByte
				outputList[0][i] = ''.join(tempList)
				print outputList
				print range(len(outputList))
			continue
			
		
		
		elif len(listTally) != 4:
			while len(listTally) != 4:
				userMIDI = raw_input("ERROR! You must enter 4 comma separated values!: ")
				listTally = userMIDI.split(",")
			
			else:
				#appends midi to list
				outputList.append([userMIDI])
		
				
		else:
			#appends midi to list
			outputList.append([userMIDI])
	
	
	midi_send(outputMIDI)
	
	

def midi_send(port):
	
	#store this function into a variable so it can easily be deleted and closed at the end
	sender = pygame.midi.Output(port)
	global outputList
	global sendRepeat
	counter = 0
	pygame.init()
	pygame.midi.init()
	
	#try something
	try:
		while counter < sendRepeat:
			#iterate through the list and move each individual list into the tmp variable
			for i in range(len(outputList)):
				tmp1 = 0
				tmp1 =  outputList[i]
				
				#splits all list assets into their own variables
				status, pitch, velocity, delay = tmp1[0].split(",")
				
				if status[0:2] == "0x":
					status = int(status, 16)
					pitch = int(pitch, 16)
					velocity = int(velocity, 16)
					delay = int(delay, 16)
				
				#convert all values to integers so pygame.midi can send them
				else:
					status = int(status)
					pitch = int(pitch)
					velocity = int(velocity)
					delay = int(delay)
				
				#sleeps for defined millisecond amount. Note that sleep command
				#cannot go lower than 10-13ms due to Windows kernel clock rate.
				#Unix based OS can get closer to 1ms.
				time.sleep(float(delay) / float(1000))

				sender.write([[[status, pitch, velocity],0]])
				print i + 1, " ", outputList[i]
			counter += 1
	
	#catch any thrown exceptions due to bad MIDI data that has been entered by the user.		
	except:
		print "\nIllegal operation, check send queue for incorrect values."
		print "Press Enter to return to queue."
		stop = raw_input("")
		midi_send_entry()
		
	#reset the send repeat counter to 1 so it only sends MIDI data once by default.
	sendRepeat = 1	
	del sender
	pygame.midi.quit()
	
	print "\n\n"
	print len(outputList), "messages sent."
	
	print "\n1. Send more MIDI"
	print "2. Main Menu"
	choice = int(raw_input("\nEnter the number of your choice: "))
	
	if choice == 1:
		midi_send_entry()
		
	elif choice == 2:
		main_menu()
	
	else:
		main_menu()


def midi_batch_send():
	print "\nSelect the file that you want to load your MIDI commands from:"
	root = Tk()
	root.withdraw()
	inputFile = tkFileDialog.askopenfilename(parent = root)
	global outputList
	
	try:
		f = open(inputFile)
		tempList = []
		
		for line in f:
			#strip() takes out all \n characters so they are not displayed in the list
			if line == "\n":
				continue
			
			#ignores comment lines which are denoted by a #
			elif '#' in line:
				continue
			
			#it is then appended to the main list
			else:
				tempList.append(line.strip())
				outputList.append(tempList)
				tempList = []
		
		print outputList
		#close the file object
		f.close
		
		#call send function
		midi_send_entry()	
	
	#catch any exception caused by a corrupt file
	except:
		print "Invalid or corrupt file."
		print "Press Enter to return to queue."		
		stop = raw_input("")
		midi_send_entry()

#half implemented, broken		
def midi_queue_write():
	global outputList
	print "\nEnter the filename and location to save your file:"
	root = Tk()
	root.withdraw()
	outputFile = tkFileDialog.asksaveasfilename(defaultextension = '.txt', parent = root)

	#calls codecs.open to deal with unicode filenames
	f = codecs.open(outputFile, encoding ='utf-8', mode='w')

		
	try:
		#iterates through queue and writes list entry plus a newline. Note that notepad doesn't display \n
		for item in outputList:
			f.write(str(item[0] + '\n'))

		#close open file object	
		f.close()
		midi_send_entry()	
		
	except:
		print "Error! Returning to send menu."
		stop = raw_input("")
		midi_send_entry()

def sysex_send(port):
	
	pygame.init()
	pygame.midi.init()
	
	bufferSize = raw_input("Enter in the buffer size: ")
	
	# set the number of the device you want to send with here. Set the buffer size here as well.
	sender = pygame.midi.Output(port, buffer_size = bufferSize) #Set buffer size here.
	
	# Send the SysEx. In the example below, I'm sending a simple Device Inquiry.
	sender.write_sys_ex(0, [0xF0,0x7E,0x0,0x06,0x01,0xF7]) #Put SysEx here. Everything must be preceded with 0X.

	# Delete the sender object and then close all running pygame instances. Makes a clean exit, no crash.
	del sender
	pygame.midi.quit()
	# No progress bar. When sending is complete the app will quit
		

#initializes colorama
init()

#define global variables
inputMIDI = 0
outputMIDI = 0
outputList = []
sendRepeat = 1

#master program loop
while True:
	main_menu()