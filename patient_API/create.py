from util import GenerateAppointmentNum

def AddAddress(cursor, connection, patientNum, city, stateAbbreviation, address1, address2 = "", postalCode = ""):
    """
    Description: 
    Given a patient number and address, adds the address to the patient's file.

    Parameters:
    cursor (psycopg2)           : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
    connection (psycopg2)       : A connection object associated with the database session. This object is used to commit or roll
                                  back the transaction.
    patientNum (string)         : The unique identifier for a patient.
    city (string)               : City of home address of patient to be added.
    stateAbbreviation (string)  : State of home address of patient to be added.
    address1 (string)           : Address1 of home address of patient to be added.
    address2 (string)           : Address2 of home address of patient to be added.
    postalCode (string)         : Postal code of home address of patient to be added.  

    Returns:
    bool
    """
    findAddress = """
    SELECT id
    FROM address
    WHERE address1 ILIKE %s AND address2 ILIKE %s AND postalcode ILIKE %s AND city ILIKE %s AND stateAbbreviation ILIKE %s
    """
    insertAddress = """
    INSERT INTO Address (Address1, Address2, postalCode, city, stateabbreviation) 
    VALUES (%s, %s, %s, %s, %s)
    RETURNING ID;
    """
    insertPatientAddress = """
    INSERT INTO PatientAddresses (PatientID, AddressID) VALUES 
    ((SELECT id FROM Patient WHERE patientNum ILIKE %s), %s);
    """
    try:
        cursor.execute(findAddress, (address1, address2, postalCode, city, stateAbbreviation))
        result = cursor.fetchone()
        #address does not exist
        if not result:
            cursor.execute(insertAddress, (address1, address2, postalCode, city, stateAbbreviation))
            result = cursor.fetchone()[0]
        else:
            result = result[0]
        cursor.execute(insertPatientAddress, (patientNum, result))
        connection.commit()
        return "Succesful"
    except Exception as e:
            print(f"An error occurred: {e}")
            connection.rollback()
            return "Failed"

def ScheduleAppointment(cursor, connection, employeeNum, dateTime, purpose, patientNum = None):
    """
    Description: 
    Given the Employee Num of the provider, date and time, purpose, and optionally patient
    number, creates a new appointment at that time. Return successful if appointment created,
    returns unsuccessful if provider unavailable at the given time or patientNum not found. 
    Duration of the appointment is set to 30 minutes by default.

    Parameters:
    cursor (psycopg2)       : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
    connection (psycopg2)   : A connection object associated with the database session. This object is used to commit or roll
                              back the transaction.
    employeeNum (string)    : The unique identifier for an employee. Identifier for the provider.
    dateTime (string)       : The dateTime of the appointment in any accepted date format.
    purpose (string)        : The purpose of the appointment.
    patientNum (string)     : The unique identifier for a patient.

    Returns:6
    bool
    """

    getEmployeeAvailability = """
    SELECT * 
    FROM HealthCareProvider hcp
        JOIN AppointmentProviders ap ON hcp.Id = ap.HealthCareProviderId
        JOIN Appointment a ON a.id = ap.AppointmentId
    WHERE hcp.EmployeeNum ILIKE %s AND a.date = %s;
    """

    getEmployeeSchedule = """
    SELECT hc.FirstName, hc.LastName, hc.EmployeeNum, ps.shiftstart, ps.duration
    FROM ProviderShifts ps
        JOIN HealthCareProvider hc ON (ps.HealthCareProviderID = hc.ID)
    WHERE hc.EmployeeNum ILIKE %s 
        AND ps.shiftstart <= %s 
        AND (ps.shiftstart + ps.duration) >= %s;
    """

    getPatientId = """
    SELECT ID FROM Patient
    WHERE PatientNum ILIKE %s;
    """
    
    getEmployeeId = """
    SELECT ID FROM HealthCareProvider
    WHERE EmployeeNum ILIKE %s;
    """
    
    insertAppointment = """
    INSERT INTO Appointment (PatientID, date, Purpose, AppointmentNum, Duration)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING ID;
    """
    
    insertAppointmentProvider = """
    INSERT INTO AppointmentProviders (HealthCareProviderID, AppointmentID)
    VALUES (%s, %s)
    """
    
    try:
        # Check if the provider is available
        cursor.execute(getEmployeeAvailability, (employeeNum, dateTime))
        if cursor.fetchone():
            raise Exception("Provider is unavailable at the given time.")
        patientId = None
        

        # Check if the provider is working at that time
        cursor.execute(getEmployeeSchedule, (employeeNum, dateTime, dateTime))
        if not cursor.fetchone():
            raise Exception("Provider is unavailable at the given time.")

        # If a patientNum is provided, check if the patient exists
        if patientNum:
            cursor.execute(getPatientId, (patientNum,))
            patientResult = cursor.fetchone()
            if not patientResult:
                raise Exception("PatientNum not found.")
            patientId = patientResult[0]
        
        # Check if the employee exists
        cursor.execute(getEmployeeId, (employeeNum,))
        employeeResult = cursor.fetchone()
        if not employeeResult:
            raise Exception("EmployeeNum not found.")
        employeeId = employeeResult[0]
        
        # Insert the new appointment, handling null patientNum
        appointmentNum = GenerateAppointmentNum(cursor)
        duration = "30 minutes"
        cursor.execute(insertAppointment, (patientId, dateTime, purpose, appointmentNum, duration))
        insertAppointmentResult = cursor.fetchone()
        if not insertAppointmentResult:
            raise Exception("Problems inserting appointment.")
        appointmentId = insertAppointmentResult[0]
        # Insert into AppointmentProviders
        cursor.execute(insertAppointmentProvider, (employeeId, appointmentId))

        # Commit the transaction
        connection.commit()
        return "Succesful"

    except Exception as e:
        print(f"An error occurred: {e}")
        # Rollback in case of any error
        connection.rollback()
        return "Failed"