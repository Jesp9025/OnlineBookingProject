import os, sqlite3, datetime, functools, operator

class resource(object):
    resourceQuantity = int
    resourceManufactorer = str
    resourceModel = str
    resourceSerialNumber = str
    def __init__(self):        
        self.databaseFile = "databaseProject.db"
        self.databaseLocation = os.path.abspath(os.path.dirname(__file__))
        self.path = os.path.join(self.databaseLocation, self.databaseFile)
        self.conn = sqlite3.connect(self.path, check_same_thread=False)



    '''This may or may not bite us in the ass, putting the Queries inside of the method and simply filling out the "holes",
    instead of putting the whole Query inside a single argument'''

    def createResource(self, resourceQuantity, resourceManufacturer, resourceModel, resourceSerialNumber):
        """
        Example: createResource(2, "Lenovo", "DX750", "d231213sddsa")
        """
        try:            
            c = self.conn.cursor()
            c.execute("INSERT INTO Resource (resource_quantity, resource_manufactorer, resource_model, resource_serial_number) VALUES ({}, '{}', '{}', '{}')".format(resourceQuantity, resourceManufacturer, resourceModel, resourceSerialNumber))
            self.conn.commit()
            c.close()
            return True
        except sqlite3.Error as e:
            return "An error occurred:", e.args[0]
        

    def readResource(self, param):
        """Example:\n
        res = resource()\n
        lst = res.readResource('Resource')\n
        for row in lst:\n
            print(row)
        """
        c = self.conn.cursor()
        c.execute("select * from {}".format(param))
        lst = c.fetchall()
        c.close()
        return lst


    def updateResource(self, table, column_name, new_value, where_to_find, name): # Not sure about the names yet
        """
        Example: updateResource("Resource", "resource_Quantity", "30", "resource_Model", "3570")
        """
        try:
            c = self.conn.cursor()
            c.execute("UPDATE {} SET {} = {} WHERE {} = '{}'".format(table, column_name, new_value, where_to_find, name))
            self.conn.commit()
            c.close()
            return True
        except sqlite3.Error as e:
            return "An error occurred:", e.args[0]


    def deleteResource(self, table, instance, name): # Not sure about the names yet
        """
        Example: deleteResource("Resource", "resource_model", "3rd model")
        """
        try:
            c = self.conn.cursor()
            c.execute("DELETE from {} WHERE {} = '{}'".format(table, instance, name))
            self.conn.commit()
            c.close()
            return True
        except sqlite3.Error as e:
            return "An error occurred:", e.args[0]


class Lab(resource):
    labName = str
    labDescription = str
    labResouceID = int

    def createLab(self, labID, labName, labDescription):
        """
        Example: createLab(21235, "Infrastructure", "Students learn how to set up a server")
        """
        try:            
            c = self.conn.cursor()
            c.execute("INSERT INTO Lab (lab_id, lab_name, lab_description) VALUES ({}, '{}', '{}')".format(labID, labName, labDescription))
            self.conn.commit()
            c.close()
            return True
        except sqlite3.Error as e:
            return "An error occurred:", e.args[0]
    
    def readLab(self, param):
        """Example:\n
        lab = Lab()\n
        lst = res.readLab('Lab')\n
        for row in lst:\n
            print(row)
        """
        c = self.conn.cursor()
        c.execute("select * from {}".format(param))
        lst = c.fetchall()
        c.close()
        return lst

    def updateLab(self, table, column_name, new_value, where_to_find, name): # Not sure about the names yet
        """
        Example: updateLab("Lab", "lab_description", "new description", "lab_name", "IoT")
        """
        try:
            c = self.conn.cursor()
            c.execute("UPDATE {} SET {} = {} WHERE {} = '{}'".format(table, column_name, new_value, where_to_find, name))
            self.conn.commit()
            c.close()
            return True
        except sqlite3.Error as e:
            return "An error occurred:", e.args[0]

    def deleteLab(self, table, instance, name): # Not sure about the names yet
        """
        Example: deleteLab("Lab", "lab_name", "IoT")
        """
        try:
            c = self.conn.cursor()
            c.execute("DELETE from {} WHERE {} = '{}'".format(table, instance, name))
            self.conn.commit()
            c.close()
            return True
        except sqlite3.Error as e:
            return "An error occurred:", e.args[0]

class Booking(Lab):
    bookingID = int
    bookingStart = datetime
    bookingEnd = datetime
    isBooked = bool

    def createBooking(self, bookingID, bookingStart, bookingEnd):
        """
        Example: createBooking(21235, "start date?", "end date?")
        """
        try:            
            c = self.conn.cursor()
            c.execute("INSERT INTO Booking (booking_id, booking_start, booking_end) VALUES ({}, '{}', '{}')".format(bookingID, bookingStart, bookingEnd))
            self.conn.commit()
            c.close()
            return True
        except sqlite3.Error as e:
            return "An error occurred:", e.args[0]
    
    def readBooking(self, param):
        """Example:\n
        booking = Booking()\n
        lst = booking.readBooking('Lab')\n
        for row in lst:\n
            print(row)
        """
        c = self.conn.cursor()
        c.execute("select * from {}".format(param))
        lst = c.fetchall()
        c.close()
        return lst

    def updateBooking(self, table, column_name, new_value, where_to_find, name): # Not sure about the names yet
        """
        Example: updateBooking("Booking", "booking_end", "new end date?", "booking_id", "21235")
        """
        try:
            c = self.conn.cursor()
            c.execute("UPDATE {} SET {} = {} WHERE {} = '{}'".format(table, column_name, new_value, where_to_find, name))
            self.conn.commit()
            c.close()
            return True
        except sqlite3.Error as e:
            return "An error occurred:", e.args[0]

    def deleteBooking(self, table, instance, name): # Not sure about the names yet
        """
        Example: deleteBooking("Booking", "booking_id", "21235")
        """
        try:
            c = self.conn.cursor()
            c.execute("DELETE from {} WHERE {} = '{}'".format(table, instance, name))
            self.conn.commit()
            c.close()
            return True
        except sqlite3.Error as e:
            return "An error occurred:", e.args[0]

    def verifyAvailability(self):
        return True

class User(Booking):
    userID = int
    __username = str
    __password = str
    __email = str
    userisAdmin = bool
    accountIsActive = bool

    def createUser(self, userID, username, password, email, userisAdmin, accountIsActive):
        """
        Example: createUser(1564, "jesp9025", "1234", jesp9025@live.dk, True, True)
        """
        try:            
            c = self.conn.cursor()
            c.execute("INSERT INTO User (user_id, user_username, user_password, user_email, user_is_admin, user_account_is_active) VALUES ({}, '{}', '{}', '{}', '{}', '{}')".format(userID, username, password, email, userisAdmin, accountIsActive))
            self.conn.commit()
            c.close()
            return "Succesfully created new user"
        except sqlite3.Error as e:
            return "An error occurred:", e.args[0]

    def verifyUsername(self):
        return True
    
    def verifyUserActiveStatus(self):
        return True
    
    # Fuck my life. convert from tuple to list, from list to str to check password
    def verifyPassword(self, username, password):
        try:
            c = self.conn.cursor()            
            c.execute("SELECT user_password FROM User WHERE user_username = '{}'".format(username))
            got = c.fetchall()
            toList = functools.reduce(operator.add, (got))
            toString = ""
            for i in toList:
                toString += str(i)
            if toString == password:
                c.close
                return True
            else:
                print("Wrong username and password combination")
        except TypeError:
            print("Something went wrong")

    def checkIfAdmin(self):
        return True

#res = resource()
#lst = res.readResource('Resource')
#for row in lst:
#    print(row)

lab = Lab()
#print(lab.createLab(232213, "IoT", "Students learn to work with Arduino etc"))
#print(lab.readLab("Lab"))


#print(res.createResource(2, "Lenovo", "DX850", "d231213sddsa"))
#print(res.updateResource("Resource", "resource_Quantity", "40", "resource_Model", "3570"))
#print(res.deleteResource("Resource", "resource_model", "DX850"))