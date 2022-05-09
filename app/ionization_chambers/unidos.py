#####
#
# unidos.py
#
# UHS Electrometer Control Software
# PTW UNIDOS Control Module
# A Blackmore - July 2018
#
# This script provides an electrometer control class for the PTW
# UNIDOS family of electrometers, handling serial communications. 
# Technical reference from PTW's Instruction Manual, "RS232 
# Interface of UNIDOS-E" D545.131.1/0. Designed and built for 
# firmware version 1.10i. 
#
# Version 1.1 - Added rudimentary communication to the Webline and 
# automeasurement modes.
#
#####

# IMPORTS
import serial
import time
#import SendKeys

modes = ["RESET", "MEASURING", "HOLD", "INTEGRATION", "HOLD (INT)", "ZERO", "ERROR", "AUTO", "WAIT"]

# ELECTROMETER CONTROL CLASS

class Unidos:
    def __init__(self):         # Class Initialisation  - Set a variable to store the serial connection and another to store the menu text.
        self.s = None
        self.webline = False
        self.lastMode = 0

    def connect(self):          # Serial Connection Member Function - Initites the serial communication.
        
        
        # Try searching for the UNIDOS on the first 9 COM ports (USB COM ports are often assigned high numbers.)
        for port in ['COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9']: 
            try:
                # Attempt to open this serial port - if it doesn't exist, a SerialException is raised.
                self.s = serial.Serial(port, 9600, timeout = 1)
                print("Connecting..." + port)
                response = self.telegram("PTW")
                    # With the open COM port, send out 'PTW' in ASCII. The UNIDOS will respond if present. 
                if response[0:6] == "UNIDOS":                                  # If there is a UNIDOS-E on the other end, it responds with it's Model and version. 
                    print("Connected to %s on Serial Port %s" % (response, port))
                    print("Locking Keypad")
                    #self.telegram("T1")                                         # Lock the keypad to ensure we're in control (mwahahaha!) and no user interferes
                    return True                                                 # Notify the calling function that we've got a good connection. 
                elif response[:11] == "PTW;UNIDOS2":                                 # A newer unidos (e.g. Webline) response
                    print("Connected to %s on Serial Port %s" % (response, port)) 
                    print("Locking Keypad") 
                    self.webline = True
                    #self.telegram("KEY;0")                                      # Lock the keypad to ensure we're in control (mwahahaha!) and no user interferes
                    return True                                            
                
            
            except (AttributeError, serial.SerialException) as e:               # We're unable to open the serial port (either it doesn't exist or is in use)
                pass 
                                                                       # Go ahead and try the next port. 
        return False                                                            # We've tried all the ports now, so time to give in and notify the calling program.
        
    def disconnect(self):      # Member function to disconnect from the electrometer
        print("\n\nReleasing Keypad & Disconnecting")
        self.telegram("T1") if self.webline else self.telegram("Te1")  # Unlock the keypad.
        self.s.close()         # Close the serial port.
        
    def telegram(self, tele):   # Member function to send a message to the electrometer and recieve a reply. Note: The UNIDOS works on a purely ping-pong relationship. 
        if not self.s is None: # therefore, we ignore any previous messages, and focus only on sending this message and getting a single reply. 
            self.s.reset_input_buffer() # Throw Away any messages that arn't in the Ping-Pong
            sendStr = tele + "\r\n"
            self.s.write(sendStr.encode())  # Write our message command, and attach an end of line character.
            response = self.s.readline().decode(encoding = "ISO-8859-1", errors='ignore').rstrip("\r\n")
            return str(response) # return back the reply, without the end of line characters.
        return "NULL SERIAL"   # Raise an alert if the serial communication has died.


    def get_to_home(self):
        while True:
            esc = self.telegram("C")
            #time.sleep(0.1)
            if esc == "E02":
                break


    def null(self):
        response = self.telegram("N")
        if not response == "NULL SERIAL":                   # This means the electrometer is connected otherwise it would have returned a NULL SERIAL
            if not response == "N":                         # The electrometer failed to null, this can only happen if the electrometer was just turned on and it is not warmed up. The warm-up
                if len(response) > 1:                       # process takes 1 minute and this time is presented in seconds. When the electrometer is doing the warm-up the responce to null is an error E13 time
                    status = "Electrometer warm-up in progress... " # So we split the responce by space and take the second entry in the list which is the time left.
                    time_r = int(response.split(" ")[1].strip())
                    return{"status":status, "time_left":time_r}
                elif response == 'E02':                             # If the electrometer is in a menu it will not be able to null and will return a E02, so we need to get it out of the menu by pressing the while loop.
                    self.get_to_home()
                    self.telegram("N")
            else:
                return {"status": "success", "message": "Nulling in progress, This will take 72 seconds."}
        else:
            return {"status":"Error", "message":"No connection to Electrometer"}


    def change_voltage(self, volts:int) ->str:   # This only works if you are in the home screen, so  make sure you are in the home screen (Out-side the manues)
        while True: 
            check = self.telegram("?W")
            if check == "03":
                break
            else:
                self.telegram("U")
                #time.sleep(0.1)                 # Now you are in the chambers tab 

        self.telegram("E")
        #time.sleep(0.1)

        while True: 
            check = self.telegram("?W")
            if check == "031":
                break
            else:
                self.telegram("D")
                #time.sleep(0.1)

        self.telegram("E")
        #time.sleep(0.1)

        while True: 
            check = self.telegram("V")
            if check == "%s V" %volts:
                break
            else:
                self.telegram("D")
                #time.sleep(0.1)
        
        self.telegram("E")
        time.sleep(5.1)
        self.get_to_home()
        return {"status":"success", "message":"Voltage changed to %s" %volts}


                


    def chabge_int_time(self, time:int):
        self.get_to_home()
        while True:
            check = self.telegram("?W")
            if check == "00":
                break
            else:
                self.telegram("D")
                #time.sleep(0.1)

        self.telegram("E")
        self.telegram("E")
        #time.sleep(0.1)
        self.telegram("{}".format(time))
        self.get_to_home()
        return{'status': 'success', 'message':'internal timer changed to %s seconds' %time}


    def change_mode_electrical(self):
        while True: 
            check = self.telegram("?W")
            if check == "00":
                break
            else:
                self.telegram("U")
                #time.sleep(0.1)
        self.telegram("E")
        #time.sleep(0.1)
        while True: 
            check = self.telegram("?W")
            if check == "001":
                break
            else:
                self.telegram("D")
                #time.sleep(0.1)

        self.telegram("E")
        #time.sleep(0.1)
        while True: 
            check = self.telegram("V")
            if check.strip() == "Electrical":
                break
            else:
                self.telegram("D")
                #time.sleep(0.1)
        self.telegram("E")
        #time.sleep(0.1)
        self.get_to_home()


    def change_mode_dose(self):
        while True: 
            check = self.telegram("?W")
            if check == "00":
                break
            else:
                self.telegram("U")
                #time.sleep(0.1)
        self.telegram("E")
        #time.sleep(0.1)
        while True: 
            check = self.telegram("?W")
            if check == "001":
                break
            else:
                self.telegram("D")
                #time.sleep(0.1)

        self.telegram("E")
        #time.sleep(0.1)
        while True: 
            check = self.telegram("V")
            if check.strip() == "Radiological":
                break
            else:
                self.telegram("D")
                #time.sleep(0.1)
        self.telegram("E")
        #time.sleep(0.1)
        self.get_to_home()

    def select_chamber(self, chamber:str):
        while True: 
            check = self.telegram("?W")
            if check == "03":
                break
            else:
                self.telegram("U")
                #time.sleep(0.1)

        self.telegram("E")
        #time.sleep(0.1)
        self.telegram("E")
        while True:
            chack = self.telegram("V").split(" ")[4]
            if chack == chamber:
                break
            else:
                self.telegram("D")
                #time.sleep(0.1)
        self.telegram("E")
        time.sleep(5.1)
        self.get_to_home()

    
'''
    def null(self):            # Member function to perform a background NULL on the electrometer
        if not self.webline:
            response = self.telegram("NULC1") # Set zeroing behaviour to mode 1 (see manual - preserves Ping-Pong by sending reply immediately)
        elif self.webline:
            response = self.telegram("NUL") 
        print (response)                                       # Start the NULL by sending the command
        if response == "NUL":                                                   # If electrometer accepts the command, it returns "NUL"
            print("Performing NULL.... (This takes approx 1minute)")            # Inform the user we may be here a while.
            if self.webline:
                print("Please watch the electrometer! Software Monitoring for Webline not yet implemented.")
            else:
                while True:                                                         # Start watching how long the electrometer has left. 
                    timeLeft = self.telegram("NULT")                                # "Are we nearly there yet?"
                    status = self.telegram("S")                                     # Get the electrometer's overall state.
                    sys.stdout.write("\rTime Remaining: %ss " % int(timeLeft[4:]))  # Let the user know how long we've got left.
                    sys.stdout.flush()                                              # (This is sys.stdout so we can update rather than spam)
                    if not status == "SNUL":                                        # If the status of the electrometer isn't 'NULLING' then break out of our waiting loop.
                        nullErrors = self.telegram("NULE")                          # Collect any nulling errors from the system if there are any.
                        break
                    #time.sleep(1)                                                   # Wait a second before bothering the electrometer again.
                if status == "SRES" and nullErrors == "NULE00000":                  # If the electrometer is ready to measure and has no errors...
                    print("\nNULL Completed Successfully.")                         # We're done! Electrometer will now be RES
                    self.telegram("STA")                                            # Start the Electrometer (In RES, HLD is not allowed)
                    self.telegram("HLD")                                            # Set the Electrometer to HLD ready for measurements.
                else:
                    print("\nNULL Failed: %s" % nullErrors)                         # Something went wrong - tell the user.
        else:
            print("NULL Request Failed: %s" % response)                         # Electrometer rejected the request to start a null (usually means its in the wrong mode)

    def shit_null(self):
        self.telegram("NULC1")

    def defaults(self):     # Member function to set some default values on the electrometer
        print("Setting Voltage to +300V")         # Set Voltage to 300V
        self.voltage("300")                      
        print("Setting Medium Range")             
        self.telegram("RM")                       # Set Range Medium
        print("Setting Charge Reading")
        self.telegram("M0")                       # Set Measurement mode Dose / Charge
        self.telegram("UE")                       # Set Units to Electrical (ie nC)

    def voltage(self, volts):                                               # Member function to change the electrometer's voltage
        response = self.telegram("V"+volts)                                     # Send the command to change voltage
        if response.replace(" ","") == ("V" + volts).replace(" ",""):           # the response will say what the electrometer is changing to - if this is what we requested...
            print("New Voltage Accepted... Waiting 5s")                         # Inform the user,
            #time.sleep(1)                                                       # Give the electrometer 5s to stabilise (it doesn't like communicating during this time.)
            response = self.telegram("V")                                       # Ask the electrometer what its current voltage is
            if response.replace(" ","") == ("V" + volts).replace(" ",""):       # If the voltage is what we requested, great!
                print("Voltage Change Successful")
                return
            else:                                                               # Otherwise, tell the user something went wrong.
                print("Voltage Change Failed. Current Voltage: %s" % response)
        else:
            print("Voltage Change Rejected: %s" % response)                     # Electrometer flat out rejected our request - probably a bad requested voltage

    # Member function to get a measurement reading out of the electrometer. Update refreshes the current reading on the display, clipboard copies the result to clipboard in nC
    def getMeasurement(self, update = False, clipboard = False):        # Both options default to false. 
        if self.webline:
            m = self.telegram("MV").split(";")
            if not m[1] == "1":
                if not update:
                    print("Note - Electrometer not in Charge HLD Mode") 
            
            charge = "Charge:\t%s" % m[4]                                   # The 6th component is the measured charge with exponent.
            time = "Time:\t%s" % m[3]                                       # The 2nd component is the amount of time the measurement has been going for. 
            
            if update:
                sys.stdout.write("\r" + time + "\t\t" + charge + "\t\t" + modes[int(m[1])] + "\t\t")             # If we're updating the display, do the fancy readout. 
                sys.stdout.flush()
                if (self.lastMode == "1") and (m[1] == "7"):
                    print("\n\nDetected End of Measurement \n\n")
                    if clipboard:
                        exp = m[4].split("E")[1]                                    # extract the exponent
                        win32clipboard.OpenClipboard()                              # Open the clipboard and clear it before use.                        
                        win32clipboard.EmptyClipboard()
                        if exp == "-09":                                            # If the reading is in nC then go ahead and copy to clipboard.
                            win32clipboard.SetClipboardText(str(abs(float(m[4].split("E")[0]))), win32clipboard.CF_UNICODETEXT)
                        elif exp == "-12":                                          # Reading is in pC - Convert to nC. 
                            win32clipboard.SetClipboardText(str(abs(float(m[4].split("E")[0]))/1000), win32clipboard.CF_UNICODETEXT)
                        else:
                            win32clipboard.SetClipboardText("Error", win32clipboard.CF_UNICODETEXT)
                            print("Exponent not in nC or pC - Not Copying to Clipboard")
                        win32clipboard.CloseClipboard()                             # Close the clipboard (allow it to be used by other applications)
                self.lastMode = m[1]
            else:
                print(charge)                                               # Otherwise, just write the measured charge and time out to the display.
                print(time)
                if clipboard:                                                   # If we're putting the result on the clipboard
                    exp = m[4].split("E")[1]                                    # extract the exponent
                    win32clipboard.OpenClipboard()                              # Open the clipboard and clear it before use.                        
                    win32clipboard.EmptyClipboard()
                    if exp == "-09":                                            # If the reading is in nC then go ahead and copy to clipboard.
                        win32clipboard.SetClipboardText(str(abs(float(m[4].split("E")[0]))), win32clipboard.CF_UNICODETEXT)
                    elif exp == "-12":                                          # Reading is in pC - Convert to nC. 
                        win32clipboard.SetClipboardText(str(abs(float(m[4].split("E")[0]))/1000), win32clipboard.CF_UNICODETEXT)
                    else:
                        win32clipboard.SetClipboardText("Error", win32clipboard.CF_UNICODETEXT)
                        print("Exponent not in nC or pC - Not Copying to Clipboard")
                    win32clipboard.CloseClipboard()                             # Close the clipboard (allow it to be used by other applications)
            
        else:
            m = self.telegram("D0").split(";")                              # Ask for the measurement data for mode 0 (Charge). Split the response up into the components (see manual)
            charge = "Charge:\t%s" % m[1]                                   # The 6th component is the measured charge with exponent.
            time = "Time:\t%s" % m[1]                                       # The 2nd component is the amount of time the measurement has been going for. 
            if update:
                sys.stdout.write("\r" + time + "\t\t" + charge)             # If we're updating the display, do the fancy readout. 
                sys.stdout.flush()
            else:
                print(charge)                                               # Otherwise, just write the measured charge and time out to the display.
                print(time)
            if clipboard:                                                   # If we're putting the result on the clipboard
                exp = m[1].split("E")[1]                                    # extract the exponent
                win32clipboard.OpenClipboard()                              # Open the clipboard and clear it before use.                        
                win32clipboard.EmptyClipboard()
                if exp == "-09":                                            # If the reading is in nC then go ahead and copy to clipboard.
                    win32clipboard.SetClipboardText(m[1].split("E")[0], win32clipboard.CF_UNICODETEXT)
                elif exp == "-12":                                          # Reading is in pC - Convert to nC. 
                    win32clipboard.SetClipboardText(str(float(m[1].split("E")[0])/1000), win32clipboard.CF_UNICODETEXT)
                else:
                    win32clipboard.SetClipboardText("Error", win32clipboard.CF_UNICODETEXT)
                    print("Exponent not in nC or pC - Not Copying to Clipboard")
                win32clipboard.CloseClipboard()                             # Close the clipboard (allow it to be used by other applications)
     
    # Function to start a new measurement, whatever is currently happening (if another measurement is in progress, this will delete it and start again)
    def startNew(self):
        status = self.telegram("RES")           # Send the RESET command.
        if status == "RES":                     # If the electrometer has accepted that command
            response = self.telegram("STA")     # Send the START command
            if response == "STA":               # If accepted, inform the user and print(a timestamp
                print("%s: Measurement Started" % strftime("%Y-%m-%d %H:%M:%S", gmtime()))
                
    # Function to stop the measurement and copy the result to clipboard. 
    def stopAndCopy(self):
        status = self.telegram("S")             # Inquire what state the electrometer is in, if its currently measuring, go ahead:
        if status.replace(";", "") == "SSTA":                    
            response = self.telegram("HLD")     # Hold the measurement (i.e. show it on screen.)
            if response == "HLD":               # If that was successful, inform the user.
                print("%s: Measurement Stopped" % strftime("%Y-%m-%d %H:%M:%S", gmtime()))
                self.getMeasurement(clipboard = True)  # Get the measured data from the electrometer and copy to clipboard.
                print("\n")
            else:                               # Inform the user if the HLD command didn't work.
                print("%s: Electrometer failed to stop measurement. Please try again." % strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        else:                                   # Inform the user if the electrometer wasn't measuring. 
            print("%s: Stop Requested but Electrometer not currently measuring, state is: %s" % (strftime("%Y-%m-%d %H:%M:%S", gmtime()), status)) 
            
    def autoMeasure(self):
        while True:
            try:
                #time.sleep(1)
                self.getMeasurement(update = True, clipboard = True)
            except:
                pass
# EOF

'''
