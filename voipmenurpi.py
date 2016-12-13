#!/usr/bin/python
##
## Menu system
## 
## Menu is list of menu items with following format :
## [reference to parent entry identifier,
##  menu entry display title, 
##  positive integer identifier (free choice) if entry goes to submenu if selected OR
##  string with action to be returned when entry is selected]
##

import subprocess
import shlex
import lcd_api

global isOpen

VoipMenu =  [
    [0,"Top",1],
    
    [1,"Pass",2],
    [1,"IP",3],
    [1,"Call",4],

    [2,"Set","setpassword"],
    [2,"Show","showpassword"],

    [3,"ShowMyIP","showmyIP"],
    [3,"Enter IP", "entercallIP"],
    [3,"ShowCallIP","showcallIP"],

    [4,"MakeCall","call"],
    [4,"EndCall","endcall"],
    [4,"Wait", "wait"],

    ]

def getch():
    """
    Reads one character from keyboard without need for pressing RETURN.
    Only works on POSIX/LINUX systems
    """
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch



class menu :

    """
    Menu System typically for 2 line LCD and 2 button navigation.
    structure is list of menu items with following format :
    [reference to parent entry identifier,
    menu entry display title, 
    positive integer identifier (free choice) if entry goes to submenu if selected OR
    string with action to be returned when entrny is selected]
    """
        
    def __init__(self,structure,ExitLabel = "EXIT"):

        # Initialize internal variables
        self._menu = []
        i=0
        r={0:0}

        # Copy menu adding indexes
        for item in structure:
            if isinstance(item[2],int): r[item[2]]=i
            self._menu.append([i,r[item[0]],item[1],item[2]])
            i+=1
        self.key = 1
        self.niveau = 1

        # Build internal dictionnary representing menu structure
        self.struct={}
        for item in self._menu:
            if item[0] != 0 :
                if item[1] not in self.struct : self.struct[item[1]] = []
                self.struct[item[1]].append(item[0])

        # Add EXIT entry for each level
        for key in self.struct:
            index=len(self._menu)
            self._menu.append([index,key,ExitLabel,-1])
            self.struct[key].append(index)

    def display(self,pos=None):
        """
        Displays the current menu entry as :
        1st line : parent entry
        2nd line : current selected item
        """
        if pos is None : pos = self.key
        self.key = pos
        parent = self._menu[pos][1]
        lcd_api.lcd_string(str(self.niveau)+":"+self._menu[parent][2]+" "+self._menu[pos][2], lcd_api.LCD_LINE_1)
        print str(self.niveau)+":"+self._menu[parent][2]
        print self._menu[pos][2]

    def action(self,pos=None):
        """
        Returns action associated with current selected menu item
        None if selected item refers to submenu
        """
        if pos is None : pos = self.key
        self.key=pos
        if isinstance(self._menu[pos][3],str): return self._menu[pos][3]
        return None

    def prev(self,pos=None):
        """
        
        """
        if pos is None : pos = self.key
        self.key=pos
        level = self.struct[self._menu[pos][1]]
        i = level.index(pos)
        i = i-1
        if i < 0: i = len(level)-1
        self.key = level[i]
        
    def next(self,pos=None):
        """
        Advances selection to next menu item in same level.
        Rotates to first item when at end of menu level.
        """
        if pos is None : pos = self.key
        self.key=pos
        level = self.struct[self._menu[pos][1]]
        i=level.index(pos)
        i=i+1
        if i >= len(level): i=0
        self.key=level[i]

    def select(self,pos=None):
        """
        Advances to sub menu or parent menu then returns False, OR
        Returns True if selected menu has to be actioned.
        Returns -1 if selected item is EXIT from first level, i.e. quit the menu
        """
        if pos is None : pos = self.key
        self.key=pos
        if isinstance(self._menu[pos][3],str): return True
        if self._menu[pos][3] > 0:
            self.key = self.struct[self._menu[pos][0]][0]
            self.niveau +=1
            return False
        if self._menu[pos][3] == -1:
            self.key = self._menu[pos][1]
            self.niveau -=1
            if self.key == 0 : return -1
            return False

    def up(self,pos=None):
        """
        Goes up one level and returns True
        Returns False if already on top/first level
        Can typically be used after actionning a selection to return to previous menu item
        """
        if pos is None : pos = self.key
        self.key=pos
        if self.niveau == 1 : return False
        self.key = self._menu[pos][1]
        self.niveau -=1
        return True

def setPass():
    import lcd_api
    from constants import PASSOPTIONS
    
    ip = list('')
    number = 0
    number2 = 0
    s1 = list (PASSOPTIONS)
    notDone = True
    while notDone:
            
        p = getch()
        if p == 'n':
            if number2 == len(s1)-1:
                number2 = 0
            else:
                number2 += 1
        elif p == 'b':
            if number2 == 0:
                number2 = len(s1)-1
            else:
                number2 -= 1
        elif p =='s':
            ip.append(s1[number2])
            number += 1
            number2 = 0
            if number == 10:
                break
            
        print ''.join(ip)+s1[number2]
        lcd_api.lcd_string(''.join(ip)+s1[number2], lcd_api.LCD_LINE_2) 
    
    return ''.join(ip)
        
def setIP():
    import lcd_api
    from constants import IPOPTION
    
    ip = list('')
    number = 0
    number2 = 0
    threezeros = 0
    s1 = list (IPOPTION)
    notDone = True
    while notDone:
                
        if number == 3:
            ip.append('.')
            number = number+1
        if number == 7:
            ip.append('.')
            number = number+1
        if number == 11:
            ip.append('.')
            number = number+1
            
        p = getch()
        if p == 'n':
            if number2 == 9:
                number2 = 0
            else:
                number2 = number2+1
        elif p == 'b':
            if number2 == 0:
                number2 = 9
            else:
                number2 = number2-1
        elif p =='s':
	    if s1[number2] != '0': 
                ip.append(s1[number2])
                threezeros = 0
	    else:
                threezeros += 1
                if threezeros > 2:
                    ip.append('0')
                    threezeros = 0
            number = number+1
            number2 = 0
            if number == 15:
                break
            
        print ''.join(ip)+s1[number2]
        lcd_api.lcd_string(''.join(ip)+s1[number2], lcd_api.LCD_LINE_2) 
    
    return ''.join(ip)
    
    
if __name__ == "__main__":

    import lcd_api
    import os, re
    from constants import *
    import md5

    lcd_api.init()
    m=menu(VoipMenu)
    secondline = ""
    action=""
    password="";
    extIP = "None";
    call_address = '999.999.999.999'
    isOpen = False

    while True:
        os.system("clear")
        m.display()
        
	print secondline
        print action
        lcd_api.lcd_string(secondline, lcd_api.LCD_LINE_2)
        c=getch()
        if c == "x" : break
        if c == "n" : m.next()  # Simulate NEXT button
        if c == "b" : m.prev()  # Sinulate PREV button
        if c == "s":            # Simulate SELECT button
            s=m.select()
            if s :
                if s == -1 : break
                action=m.action()
                if action == "call" or action == "wait":
                    if isOpen is False:
                        try:
                            pid = subprocess.Popen(shlex.split(WAITOPTION), stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                            x = 1
                            while x < 8:
                                secondline = pid.stdout.readline()
                                x+=1
                            Result = re.search('External IP: (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', secondline)
                            if Result:
                                extIP = Result.group(1)
                            pid.stdin.write(b'/X 3\n')
                            hshmd5 = md5.new(password).hexdigest()
                            pid.stdin.write(b'/x %s\n'%hshmd5)
                            pid.stdin.write(b'/e 2\n')
			    if action == "call":
			        pid.stdin.write(b'/c %s\n'%call_address)
				secondline = "Calling"
		            else:
				secondline = "Waiting"
                            isOpen = True
                        except subprocess.CalledProcessError:
                            secondline = 'Error'
                    else:
                        secondline = "Error!"
                elif action == "setpassword":
                    password = setPass()
                elif action == "showpassword":
                    action = password
		    secondline = password
                elif action == "showmyIP":
                    action = extIP
                    secondline = extIP
                elif action == "showcallIP":
                    action = call_address
		    secondline = call_address
                elif action == "entercallIP":
                    call_address = setIP()
                elif action == "endcall":
                    if isOpen == True:
			secondline = "Call Ended"
                        action = pid.communicate("/q")[0]
                        extIP = "None"
                        isOpen = False
