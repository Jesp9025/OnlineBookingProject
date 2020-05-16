import os, sqlite3, datetime, functools, operator, random

class Resource(object):
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
        

    def readResource(self):
        """Reads everything in Resource table
        """
        c = self.conn.cursor()
        c.execute("select * from Resource")
        lst = c.fetchall()
        c.close()
        return lst


    def updateResource(self, column_name, new_value, where_column, value): # Not sure about the names yet
        """
        Example: updateResource("resource_Quantity", "30", "resource_Model", "3570")
        """
        try:
            c = self.conn.cursor()
            c.execute("UPDATE Resource SET {} = {} WHERE {} = '{}'".format(column_name, new_value, where_column, value))
            self.conn.commit()
            c.close()
            return True
        except sqlite3.Error as e:
            return "An error occurred:", e.args[0]


    def deleteResource(self, column_name, value): # Not sure about the names yet
        """
        Example: deleteResource("resource_model", "DX850")
        """
        try:
            c = self.conn.cursor()
            c.execute("DELETE FROM Resource WHERE {} = '{}'".format(column_name, value))
            self.conn.commit()
            c.close()
            return True
        except sqlite3.Error as e:
            return "An error occurred:", e.args[0]


class Lab(Resource):
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
    
    def readLab(self):
        """Reads everything in Lab table
        """
        c = self.conn.cursor()
        c.execute("select * from Lab")
        lst = c.fetchall()
        c.close()
        return lst

    def updateLab(self, table, column_name, new_value, where_column, value): # Not sure about the names yet
        """
        Example: updateLab("lab_description", "new description", "lab_name", "IoT")
        """
        try:
            c = self.conn.cursor()
            c.execute("UPDATE Lab SET {} = {} WHERE {} = '{}'".format(column_name, new_value, where_column, value))
            self.conn.commit()
            c.close()
            return True
        except sqlite3.Error as e:
            return "An error occurred:", e.args[0]

    def deleteLab(self, column_name, value): # Not sure about the names yet
        """
        Example: deleteLab("Lab", "lab_name", "IoT")
        """
        try:
            c = self.conn.cursor()
            c.execute("DELETE FROM Lab WHERE {} = '{}'".format(column_name, value))
            self.conn.commit()
            c.close()
            return True
        except sqlite3.Error as e:
            return "An error occurred:", e.args[0]

class Booking(Lab):
    bookingID = int
    bookingStart = datetime
    isBooked = bool

    def createBooking(self, quantity, resourceID, bookingID):
        c = self.conn.cursor()
        c.execute("SELECT resource_quantity FROM Resource WHERE resource_id = {}".format(resourceID))
        lst = c.fetchall()
        #c.close()
        toList = functools.reduce(operator.add, (lst))
        for item in toList:
            if quantity > item:
                print("No can do..")
                return True
            elif quantity <= 0:
                print("No can do again")
                return True
            else:
                bookingStart = datetime.date.today()
                newValue = item - quantity
                Booking.updateResource(self, "resource_quantity", newValue, "resource_id", resourceID)
                try:
                    c.execute("INSERT INTO Booking (booking_id, booking_start) VALUES ({}, '{}')".format(bookingID, bookingStart))
                    self.conn.commit()
                    c.close()
                except sqlite3.IntegrityError as e:
                    print(e)
                    return True
    
    def readBooking(self):
        """Reads everything in Booking table
        """
        c = self.conn.cursor()
        c.execute("select * from Booking")
        lst = c.fetchall()
        c.close()
        return lst

    def deleteOldBookings(self):
        '''Delete bookings that exceed 1 day
        '''
        c = self.conn.cursor()
        c.execute("DELETE FROM Booking WHERE booking_start < DATETIME('NOW', '-1 days');")
        self.conn.commit()
        c.close()
        return True

    def updateBooking(self, column_name, new_value, where_column, value): # Not sure about the names yet
        """
        Example: updateBooking("booking_end", "2020-05-17", "booking_id", "21235")
        """
        try:
            c = self.conn.cursor()
            c.execute("UPDATE Booking SET {} = {} WHERE {} = '{}'".format(column_name, new_value, where_column, value))
            self.conn.commit()
            c.close()
            return True
        except sqlite3.Error as e:
            return "An error occurred:", e.args[0]

    def deleteBooking(self, column_name, value): # Not sure about the names yet
        """
        Example: deleteBooking("Booking", "booking_id", "21235")
        """
        try:
            c = self.conn.cursor()
            c.execute("DELETE FROM Booking WHERE {} = '{}'".format(column_name, value))
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

 
    def verifyUserActiveStatus(self):
        return True
    
    # Fuck my life. convert from tuple to list, from list to str to check password
    def verifyLogin(self, username, password):
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

    def IDGenerator(self, column_name, table):
        ID = random.randint(1, 99999)
        c = self.conn.cursor()
        c.execute("SELECT {} FROM {} WHERE {} = {}".format(column_name, table, ID, column_name))
        lst = c.fetchall()
        for item in lst:
            if item == ID:
                ID = random.randint(1, 99999)
        return ID

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