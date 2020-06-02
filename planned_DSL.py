############################################################
############################################################
######  PLANNED DSL                                 ########
######  Programming Languages Final Project         ########          
######  Prof:   PhD. Israel Pineda                  ########
######  Author: Andres Fernando Cardenas Ponce      ########
######  Date:   May-16-2020                         ######## 
############################################################
############################################################
######  ReadMe:                                     ########
######     This code is an DSL designed to make     ########
######     academic schedules. Classes on the       ########
######     schedule are available from Monday to    ########
######     Saturday at [08:00 - 20:00].             ########
######     To run the code you need python>=2.7     ########
######     and textX library.                       ######## 
######  RunCommand on Linux:                        ########
######     $ python planned_DSL.py                  ########
############################################################
############################################################ 

# Importing needed libraries
# In this case, it allows you in a Python 2 program to have the default interpretation of string literals be Unicode (UTF8)
from __future__ import unicode_literals

# textX is a meta-language for building Domain-Specific Languages (DSLs) in Python.
from textx import metamodel_from_str

# Global variable needed for principal menu
run=True
dayR=''

# Provide our classes for Hour & Class.
# Hour class to identify the hour and minutes
class Hour(object):
    def __init__(self, parent, h, m):
	self.parent=parent
	self.h = h
        self.m = m
	
    # Used to print hours
    def __str__(self):
    	if self.h < 10:
            if self.m < 10:
		return "0{}:0{}".format(self.h, self.m)
	    else:
		return "0{}:{}".format(self.h, self.m)
	if self.m < 10:
	    return "{}:0{}".format(self.h, self.m)
        return "{}:{}".format(self.h, self.m)
    def __unicode__(self):
    	if self.h < 10:
            if self.m < 10:
		return "0{}:0{}".format(self.h, self.m)
	    else:
		return "0{}:{}".format(self.h, self.m)
	if self.m < 10:
	    return "{}:0{}".format(self.h, self.m)

#Class class to identify each our with its different parts
class Class(object):
    def __init__(self,id_c, name, professor, h_start, h_end, day, classroom):
	self.id=id_c
	self.name=name
	self.professor=professor
 	self.h_start=h_start
	self.h_end=h_end
	self.day=day
        self.classroom=classroom

# To get the class name of an object
def cname(o):
    return o.__class__.__name__
    
# Function to check if an input hour is available or in the range of the schedule
def checkschedule(start, end, day):
    # Convert to Hour objects
    h_start=Hour(None,start.h,start.m)
    h_end=Hour(None,end.h,end.m)
    
    # Check if its in the range of the schedule
    condition1 = (
	h_start.h < 8 or h_end.h < 8
        or h_start.h > 20 or h_end.h>20
        or (h_start.h == 20 and h_start.m > 0 )
        or (h_end.h == 20 and h_end.m > 0 )
    )
    if condition1:
	print("(X) Hours of classes are AVAILABLE from Monday to Saturday at [08:00 - 20-00]")
	return False
    
    # Check conditions for don't overlap any class
    for clase in schedule: 
        condition2 = (
	    ((h_start.h <= clase.h_start.h and h_end.h >= clase.h_start.h)     #A           >-----|\\\\\\|-----<

	    or (h_start.h >= clase.h_start.h and h_end.h <= clase.h_end.h)     #B           |\\\>----------<\\\|

	    or (h_end.h <= clase.h_end.h and h_end.h >= clase.h_end.h)         #C           |\\\>-----\\\|-----<   

	    or (h_start.h <= clase.h_start.h and h_end.h >= clase.h_end.h))    #D           >-----|\\\-----<\\\|

	    and day == clase.day 					       #E           on same Day
	)
            
	if(condition2):
	    return False
    return True

# Sort all the classes of the schedule
def sort(lista):
    for i in range(len(lista)-1):
	for j in range(len(lista)-i-1):
	    if lista[j].h_start.h>lista[i].h_start.h:
		temp=lista[j]
                lista[j]=lista[i]
		lista[i]=temp
    return lista

def printschedule(schedule,save):
    schedule=sort(schedule)
    monday=[]
    tuesday=[]
    wednesday=[]
    thrusday=[]
    friday=[]
    saturday=[]
    # Define the names of the available Days
    daynames=['MONDAY','TUESDAY','WEDNESDAY','THRUSDAY','FRIDAY','SATURDAY']
    # A list of lists
    tempschedule=[monday,tuesday,wednesday,thrusday,friday,saturday]  
    # Put each class in their respective day
    for clase in schedule:
	if clase.day == 'Monday':
	    tempschedule[0].append(clase)
   	if clase.day == 'Tuesday':
	    tempschedule[1].append(clase)
	if clase.day == 'Wednesday':
	    tempschedule[2].append(clase)
	if clase.day == 'Thrusday':
	    tempschedule[3].append(clase)
	if clase.day == 'Friday':
	    tempschedule[4].append(clase)
	if clase.day == 'Saturday':
	    tempschedule[5].append(clase)
    
    # SAVE IN SCHEDULE.TXT
    if(save):
        Sfile = open("Schedule.txt", "w") 
        Sfile.write("========================================================================================================\n")
        Sfile.write("   ----->  YOUR  SCHEDULE  \n")
	Sfile.write("========================================================================================================\n")
    	for i in range(len(tempschedule)):
            Sfile.write("\n"+daynames[i]+":")
	    # Check if there is no classes
    	    if(len(tempschedule[i])) == 0:
                Sfile.write("\n\tNO CLASSES\n")
                continue
            # Show on screen the classes
            for clase in tempschedule[i]:
                text="\n\t[{}] - {} - professor: {} - hour: [{} - {}]  classroom: {}"
                Sfile.write(text.format(clase.id, clase.name, clase.professor, clase.h_start, clase.h_end, clase.classroom))
            Sfile.write("\n")
        Sfile.write("\n========================================================================================================\n")
	Sfile.close()
    # PRINT ON SCREEN
    else:
        print("\n========================================================================================================")
	for i in range(len(tempschedule)):
            print("\n"+daynames[i]+":")
	    # Check if there is no classes
    	    if(len(tempschedule[i])) == 0:
                print("\tNO CLASSES")
            # Show on screen the classes
            for clase in tempschedule[i]:
                text="\t[{}] - {} - professor: {} - hour: [{} - {}]  classroom: {}"
                print(text.format(clase.id, clase.name, clase.professor, clase.h_start, clase.h_end, clase.classroom))	        
        print("\n========================================================================================================")
        return schedule

def loadschedule(schedule):
    # Trye read Schedule.txt or notify error
    try: 
	Sfile = open("Schedule.txt", "r")
    except:
	print("(!) There is no file Schedule.txt on current directory\n" )
	return schedule
    # Error variable to know
    error = False
    # Check which day is
    for line in Sfile.readlines():
        if line=="\n":
	    continue
	if line[0]=="M":
	    dayR='Monday'
	elif line[0]=="T" and line[1]=="U":
	    dayR='Tuesday'
        elif line[0]=="W":
	    dayR='Wednesday'
	elif line[0] =="T" and line[1]=="H":
	    dayR='Thrusday'
	elif line[0] =="F":
	    dayR='Friday'
	elif line[0] == "S":
	    dayR='Saturday'
	
	# If is a class, get the attributes and add to the schedule
	if(line[0]=='\t' and line[1]=='[' ):
	    pointer = 2
            class_id=''
            # Id
	    while(line[pointer]!=']'):
		class_id+=line[pointer]
		pointer+=1
            pointer+=4
	    class_name=''
	    # Name
	    while(line[pointer]!=' ' or line[pointer + 1]!= '-'):
		class_name+=line[pointer]
		pointer+=1
	    pointer+=14
	    class_professor=''
	    # Professor
	    while(line[pointer]!=' ' or line[pointer + 1]!= '-'):
		class_professor+=line[pointer]
		pointer+=1
            pointer+=10            	    
	    H_start_h=''
	    # H_start Hours
	    while(line[pointer]!=':'):
	        H_start_h+=line[pointer]
		pointer+=1
            pointer+=1
	    H_start_m=''
	    # H_start minutes
   	    while(line[pointer]!=' ' or line[pointer + 1]!= '-'):
		H_start_m+=line[pointer]
		pointer+=1
	    pointer+=3
	    H_end_h=''
            # H_end Hours
	    while(line[pointer]!=':'):
		H_end_h+=line[pointer]
		pointer+=1
	    pointer+=1
	    H_end_m=''
	    # H_end Minutes
	    while(line[pointer]!=']'):
	     	H_end_m+=line[pointer]
		pointer+=1
	    pointer+=14
	    class_classroom=''
	    # Classroom
            while(line[pointer]!='\n'):
		class_classroom+=line[pointer]
		pointer+=1
            # Create Hour objects and Class object
	    h_start=Hour(None,int(H_start_h),int(H_start_m))
            h_end=Hour(None,int(H_end_h),int(H_end_m))
	    if(not checkschedule(h_start, h_end, dayR)):
	        text="(X) ERROR ADDING CLASS: Schedule at {} - {} on "+dayR+ " is UNAVAILABLE\n"
                print(text.format(h_start,h_end))
                error = True
                continue
	    clase=Class(class_id,class_name,class_professor,h_start,h_end,dayR,class_classroom)
	    # Add to current Schedule()
            schedule.append(clase)
    if error:
    	print("(!) A Schedule has been loaded with problems\n")
    else:
	print("(!) A Schedule has been loaded successfuly\n")
    return schedule	
  
#Interpret the input got, taking the schedule and returning it modified    
def interpret(schedule):
    # to know how many commands are in the model 
    totalinstr = len(model.commands) - 1

    # For all the funtions in the set of commands. To know what to do in each Funtion.    
    for command in model.commands:

            ###### ADD CLASS TO SCHEDULE OPTION
        if cname(command) == 'Add_class':
            h_start=Hour(None,command.clase.h_start.h,command.clase.h_start.m)
            h_end=Hour(None,command.clase.h_end.h,command.clase.h_end.m)
            # Check the Hour
            if(not checkschedule(command.clase.h_start, command.clase.h_end, command.clase.day)):
	        text="(X) ERROR ADDING CLASS: Schedule at {} - {} on "+command.clase.day+ " is UNAVAILABLE\n"
                print(text.format(h_start,h_end))
                return schedule
            # Create an Class Object	
            clase=Class(command.clase.id,command.clase.name,command.clase.professor,h_start,h_end,command.clase.day,command.clase.classroom)
            # Add it to the schedule
            schedule.append(clase)
            text="(+) ADDED class: ["+clase.id+"] on "+clase.day +"  "+ clase.name + " at {} - {}\n"
	    print(text.format(clase.h_start, clase.h_end)) 
            # Check if is the last coomand and return the schedule
            if model.commands.index(command) == totalinstr:
		return schedule

	    ###### DELETE A CLASS ON SCHEDULE OPTION
        elif cname(command) == 'Del_class':
            found = False
            for clase in schedule:
	        if command.id == clase.id:
		    found=True
	            schedule.remove(clase)
	            print("(-) REMOVED class: ["+clase.id+"] "+ clase.name+" on "+clase.day+"\n")
            # If that class is not in the Schedule
            if(not found):
		print("(!) No class with id : ["+command.id+"] in Schedule\n")
            if model.commands.index(command) == totalinstr:
		return schedule

	    ###### DELETE A CLASS ON SPECIFIC DAY OPTION
	elif cname(command) == 'Del_class_onday':
	    found = False
            for clase in schedule:
	        if command.id == clase.id and command.day == clase.day:
		    found=True
                    schedule.remove(clase)
	    	    print("(-) REMOVED class: ["+clase.id+"] "+ clase.name + " on "+clase.day+"\n")
            # if that class is not in Schedule at that day
            if(not found):
		print("(!) No class with id : ["+command.id+"] at "+command.day+" in Schedule\n")
            if model.commands.index(command) == totalinstr:
		return schedule

	    ###### CHECK SCHEDULE OPTION
        elif cname(command) == 'Check':
            h_start=Hour(None, command.h_start.h, command.h_start.m)
            h_end=Hour(None, command.h_end.h, command.h_end.m)
	    if(not checkschedule(command.h_start, command.h_end, command.day)):
	        text="(!) Schedule at {} - {} on "+command.day+ " is UNAVAILABLE\n"
                print(text.format(h_start,h_end))
	    else:
		text="(!) Schedule at {} - {} on "+command.day+ " is AVAILABLE\n"
                print(text.format(h_start,h_end))
            if model.commands.index(command) == totalinstr:
		return schedule

	    ###### PRINT SCHEDULE OPTION
        elif cname(command) == 'Print_schedule':
            # Sort all the classes in the schedule
            printschedule(schedule,False)
            if model.commands.index(command) == totalinstr:
		return schedule
      
	    ###### DELETE SCHEDULE OPTION
        elif cname(command) == 'Del_schedule':
	    print("(!) Whole Schedule has been deleted\n")
	    schedule = []
            if model.commands.index(command) == totalinstr:
		return schedule

	    ###### LOAD SCHEDULE OPTION
	elif cname(command) == 'Load_schedule':
	    schedule = loadschedule(schedule)
            if model.commands.index(command) == totalinstr:
		return schedule	  
            
            ###### SAVE SCHEDULE OPTION
        elif cname(command) == 'Save_schedule':
	    print("(!) Schedule has saved in Schedule.txt on the current directory.\n")
	    printschedule(schedule,True)
            if model.commands.index(command) == totalinstr:
		return schedule	    

	    ###### HELP OPTION
        elif cname(command) == 'Help':
            # Here just print a string that contain the DSL-Schedule functions information
	    print("========================================================================================================") 
            print("FUNCTIONS MANUAL: \n")
            print("   add_class( String id; String name; String professor; Hour h_start; Hour h_end; String day; String classroom )")
            print("   |----->  Add new class to your schedule\n")
     	    print("   del_class( String id )")
            print("   |----->  Delete all classes with same 'id' on the schedule\n")
            print("   del_class_onday( String id, String day )")
            print("   |----->  Delete one classes with same 'id' and same 'day' on the schedule\n")
            print("   check( Hour h_start, Hour h_end )")
            print("   |----->  Check if a specific Hour is available on the Schedule\n")
            print("   print_schedule( void )")
            print("   |----->  Show on screen the Schedule\n")
            print("   del_schedule( void )")
            print("   |----->  Erase all the Schedule saved at session\n")
	    print("   load_schedule( void )")
	    print("   |----->  Load a saved schedule in a .txt file\n")
            print("   save_schedule( void )")
            print("   |----->  Save the current schedule in a .txt file\n")
            print("   help( void )" )
            print("   |----->  Print all commands for DSL Schedule\n")
            print("   exit( void )")
            print("   |----->  Exit DSL Schedule \n")
            print("========================================================================================================\n")

	    ###### EXIT OPTION
        elif cname(command) == 'Exit':
	    print("(!) Good Bye, See you soon!\n")
            global run
            #Change the global function of the Menu 
            run = False
            break
              
	    ###### NO OPTION   
        else:
	    print("(X) ERROR: Your command is not recognized\n ")
            if model.commands.index(command) == totalinstr:
		return schedule


if __name__ == '__main__':

    # Here is defined the grammar that will be interpreted by textX to return an Python object called meta-model
    grammar = """
    Planned: commands*=Functions;
    Functions: Add_class | Del_class_onday | Del_class | Check | Print_schedule | Del_schedule | Load_schedule | Save_schedule | Exit | Help;
    Add_class: 'add_class('clase=Class')';
    Del_class: 'del_class('id=STRING')';
    Del_class_onday: 'del_class_onday('id=STRING','day=Day')';
    Check: 'check('h_start=Hour','h_end=Hour','day=Day')';
    Print_schedule: 'print_schedule('void=''')';
    Del_schedule: 'del_schedule('void=''')';
    Load_schedule: 'load_schedule('void=''')';
    Save_schedule: 'save_schedule('void=''')';
    Exit: 'exit('void=''')';
    Help: 'help('void=''')';
    Class: id=STRING','name=STRING','professor=STRING','h_start=Hour','h_end=Hour','day=Day','classroom=STRING;
    Day: 'Monday' | 'Tuesday' | 'Wednesday' | 'Thursday' | 'Friday' | 'Saturday';
    Hour: h=INT':'m=INT;
    """ 

    # Create meta-model from the grammar string
    mm = metamodel_from_str(grammar)

    # Those are some examples of commands that we can insert in the program
    """model_str = 
        add_class('PL','Programming Languages','Israel Pineda',08:00,11:00,Wednesday,'ONLINE')
	add_class('MN','Wireless Networks','Christian Iza',14:00,17:00,Wednesday,'ONLINE')
        add_class('PL','Programming Languages','Israel Pineda',12:00,14:00,Tuesday,'ONLINE')
        add_class('MN','Wireless Networks','Christian Iza',13:00,15:00,Friday,'ONLINE')
        add_class('IS','Information Security','Oscar Chang',08:00,10:00,Friday,'ONLINE')
        add_class('IS','Information Security','Oscar Chang',08:00,11:00,Tuesday,'ONLINE')
        add_class('TP','Project Titulation','No Professor',08:00,13:00,Saturday,'MAT-LAB')
        check(20:00,21:00,Wednesday)
        del_class_onday('IS',Tuesday)
	del_schedule()        
	print_schedule()        
    """

    ### MENU
    # Define the schedule and the Principal Menu
    schedule=[]
    while run:
        try:
            # Ask user for an option and convert it to unicode string type
            model_str=raw_input(">>> ").decode('utf-8')
            if not model_str:
                continue
            # Meta-model knows how to parse and instantiate models.
            model = mm.model_from_str(model_str)
	    # At this point model is a plain Python object graph with instances of 
            # dynamically created classes and attributes following the grammar
            schedule = interpret(schedule)
	except Exception as e:
            # If there is an error it Shows it
            error='PlannedDSL_'+repr(e)[5:]+"\nUse 'help()' option to see all the functions syntax \n"
            print(error)
	
