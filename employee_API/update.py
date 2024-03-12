# Update and Delete operations for employee interface


def EditSpecialty(cursor, connection, employeeNum, specialtyAbbreviation):
    """
    Description: 
    Given an employee number and specialty, adds a specialty to an employees file or removes a
    specialty from an employees file if they already have it. Returns “added” if specialty added,
    “removed” if specialty removed, or “unsuccesful” if employeenum or specialty not found. 

    Parameters:
    cursor (psycopg2)       : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
    connection (psycopg2)   : A connection object associated with the database session. This object is used to commit or roll
                              back the transaction.
    employeeNum (string)    : The unique identifier for an employee.
    specialtyName (string)  : Name of the new specialty to be changed.

    Returns:
    {added, removed or unsuccesful}
    """
    checkSpecialtyExists = """
    SELECT COUNT(*)
    FROM providerspecialties 
    WHERE providerid = (SELECT id FROM healthcareprovider WHERE employeenum ILIKE %s) AND specialtyAbbreviation ILIKE %s
    """
    specialtyAbbreviation = specialtyAbbreviation.upper()
    try:
        cursor.execute(checkSpecialtyExists, (employeeNum, specialtyAbbreviation))
        
        if cursor.fetchone()[0] == 0:
            update = """
            INSERT INTO providerSpecialties(providerid, specialtyabbreviation) VALUES
            ((SELECT id FROM healthcareprovider WHERE employeenum ILIKE %s), %s)
            """
            cursor.execute(update, (employeeNum, specialtyAbbreviation))
            connection.commit()
            return "Added"
        else:
            delete = """
            DELETE FROM providerspecialties
            WHERE providerid = (SELECT id FROM healthcareprovider WHERE employeenum ILIKE %s) AND specialtyabbreviation ILIKE %s
            """
            cursor.execute(delete, (employeeNum, specialtyAbbreviation))
            connection.commit()
            return "Removed"
    except Exception as e:
            print(f"An error occurred: {e}")
            connection.rollback()
            return "Unsuccesful"
    
def EditHealthCareProvider(cursor, connection, employeeNum, title = "", firstName = "", lastName = "", departmentAbbreviation = ""):
    """
    Description: 
    Given an employee number and information to update, update given employee file to match the
    given information. Returns successful if the employee is modified, returns unsuccessful if 
    the employee is not found or DepartmentAbbreviation not found.

    Parameters:
    cursor (psycopg2)               : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
    connection (psycopg2)           : A connection object associated with the database session. This object is used to commit or roll
                                      back the transaction.
    employeeNum (string)            : The unique identifier for an employee.
    title (string)                  : Title of the health care provider that will be changed.
    firstName (string)              : First name of the health care provider that will be changed.
    lastName (string)               : Last name of the health care provider that will be changed.
    departmentAbbreviation (string) : Department of the health care provider that will be changed.

    Returns:
    boolean: Returns true if HealthCareProvider successfully edited
    """
    providerExists = """
    SELECT *
    FROM healthcareprovider
    WHERE employeenum ILIKE %s
    """
    updateTitle = """
    UPDATE healthcareprovider
    SET titleabbreviation = %s
    WHERE employeenum ILIKE %s
    """
    updateFirstName = """
    UPDATE healthcareprovider
    SET firstName = %s
    WHERE employeenum ILIKE %s
    """
    updateLastName = """
    UPDATE healthcareprovider
    SET LastName = %s
    WHERE employeenum ILIKE %s
    """
    updateDept = """
    UPDATE healthcareprovider
    SET departmentabbreviation = %s
    WHERE employeenum ILIKE %s
    """
    try:
        cursor.execute(providerExists, (employeeNum,))
        if not cursor.fetchone():
            raise Exception("Employee number not found")
        if(len(title)):
            cursor.execute(updateTitle, (title, employeeNum))
        if(len(firstName)):
            cursor.execute(updateFirstName, (firstName, employeeNum))
        if(len(lastName)):
            cursor.execute(updateLastName, (lastName, employeeNum))
        if(len(departmentAbbreviation)):
            cursor.execute(updateDept, (departmentAbbreviation, employeeNum))
        connection.commit()
        return "Succesful"
    except Exception as e:
        print(f"An error occurred: {e}")
        connection.rollback()
        return "Failed"
    
def ChangeEmploymentStatus(cursor, connection, employeeNum):
    """
    Description:
    Changes the employment status of the given employee number. Returns their new employment status, or “NA” if employee not found.

    Parameters:
    cursor (psycopg2)       : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
    connection (psycopg2)   : A connection object associated with the database session. This object is used to commit or roll
                              back the transaction.
    employeeNum (string)    : The unique identifier for an employee.

    Returns:
    boolean: Returns true if Employee status successfully updated
    """
    providerExists = """
    SELECT *
    FROM healthcareprovider
    WHERE employeenum ILIKE %s
    """
    updateEmployment = """
    UPDATE HealthCareProvider
    SET CurrentlyEmployed = NOT CurrentlyEmployed
    WHERE ID = (SELECT id from healthcareprovider WHERE employeenum ILIKE %s)
    RETURNING currentlyEmployed
    """
    
    try:
        cursor.execute(providerExists, (employeeNum,))
        if not cursor.fetchone():
            raise Exception("Employee number not found")
        cursor.execute(updateEmployment, (employeeNum,))
        connection.commit()
        return "Currently employed = " + str(cursor.fetchone()[0])
    except Exception as e:
        # In case of any exception, print the error and rollback the transaction.
        print(f"An error occurred: {e}")
        connection.rollback()
        return "Unsuccesful"
    
def CancelShift(cursor, connection, employeeNum, shiftStart):
    """
    Description: 
    Given an employee number and shift start time, sets the matching shifts duration to 0 minutes.
    Return successful if shift modified, returns unsuccessful if shift not found.

    Parameters:
    cursor (psycopg2)       : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
    connection (psycopg2)   : A connection object associated with the database session. This object is used to commit or roll
                              back the transaction.
    employeeNum (string)    : The unique identifier for an employee.
    shiftStart (string)     : The start time of the shift to be canceled.

    Returns:
    boolean: Returns true if shift successfully canceled
    """

    select = """
    SELECT *
    FROM providershifts 
    WHERE healthcareproviderid = (SELECT id FROM healthcareprovider WHERE employeenum ILIKE %s) AND shiftstart = %s
    """
    update = """
    UPDATE providershifts
    SET duration = '0m'
    WHERE healthcareproviderid = (SELECT id FROM healthcareprovider WHERE employeenum ILIKE %s) AND shiftstart = %s
    """
    try:
        cursor.execute(select, (employeeNum, shiftStart))
        if not cursor.fetchone():
            raise Exception("Shift does not exist")
        cursor.execute(update, (employeeNum, shiftStart))
        connection.commit()
        return "Succesful"
    except Exception as e:
        print(f"An error occurred: {e}")
        # Rollback in case of any error
        connection.rollback()
        return "Failed"

def CancelPrescription(cursor, connection, patientNum, medicationAbbreviation):
    """
    Description: 
    Given a patient number and medication abbreviation, it modifies any active prescriptions of 
    that medication to expire on the current day. Returns successful if prescription found and 
    modified, or unsuccessful if not found.

    Parameters:
    cursor (psycopg2)       : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
    connection (psycopg2)   : A connection object associated with the database session. This object is used to commit or roll
                              back the transaction.
    patientNum (string)     : The unique identifier for a patient.
    medicationAbbreviation (string) : Abbreviation of the name of the medication.
    
    Returns:
    {isSuccessful}
    """
    checkPresc = """
    SELECT medicalrecord.id 
    FROM medicalrecord
        JOIN appointment ON appointmentid = appointment.id
        JOIN patient ON patientid = patient.id
        JOIN prescription ON medicalrecord.id = medicalrecordid
    WHERE patientnum ILIKE %s AND medicationabbreviation ILIKE %s AND endDate > CURRENT_DATE
    """
    query = """
    UPDATE prescription
    SET enddate = CURRENT_DATE
    WHERE id IN (
        SELECT prescription.id
        FROM medicalrecord
            JOIN appointment ON appointmentid = appointment.id
            JOIN patient ON patientid = patient.id
            JOIN prescription ON medicalrecord.id = medicalrecordid
        WHERE patientnum ILIKE %s AND medicationabbreviation ILIKE %s AND endDate > CURRENT_DATE)
    """
    try:
        cursor.execute(checkPresc, (patientNum, medicationAbbreviation))
        if not len(cursor.fetchall()):
            raise Exception("Prescription not found")
        cursor.execute(query, (patientNum, medicationAbbreviation))
        connection.commit()
        return "Succesful"
    except Exception as e:
        print(f"An error occurred: {e}")
        connection.rollback()
        return "Failed"


def EditAppointment(cursor, connection, appointmentNum, newPurpose = "", newDuration = "", patientNum = "", employeeNum = ""):
    """
    Description: 
    Given an appointment number, and the information to change on the appointment, it updates
    the appointment with the new information. Returns successful if appointment updated, returns
    unsuccessful if appointment not found.

    Parameters:
    cursor (psycopg2)           : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
    connection (psycopg2)       : A connection object associated with the database session. This object is used to commit or roll
                                  back the transaction.
    appointmentNum (string)     : The unique identifier for an appointment.
    newDate (string)            : The new date to set the appointment to in any accepted date format to set to.
    newDuration (int)           : The new duration of the appointment in minutes to set to.
    newPurpose (string)         : The new purpose of the appointment to set to.
    employeeNum (string)        : The unique identifier for an employee.

    Returns:
    boolean: Returns true if the appointment edit is successful or not
    """
    
    updatePurpose = """
    UPDATE appointment
    SET purpose = %s
    WHERE appointmentNum = %s
    """
    updatePatientNum = """
    UPDATE appointment
    SET patientid = (SELECT id FROM patient WHERE patientnum ILIKE %s)
    WHERE appointmentnum = %s
    """
    updateDuration = """
    UPDATE appointment
    SET duration = %s
    WHERE appointmentNum = %s
    """
    addProvider = """
    INSERT INTO appointmentProviders (HealthcareProviderID, appointmentid) VALUES
    ((SELECT id FROM healthcareprovider WHERE employeenum ILIKE %s AND currentlyEmployed), (SELECT id FROM appointment WHERE appointmentnum = %s))
    """
    try:
        if len(newPurpose):
            cursor.execute(updatePurpose, (newPurpose, appointmentNum))
        if len(newDuration):
            cursor.execute(updateDuration, (newDuration, appointmentNum))
        if len(patientNum):
            cursor.execute(updatePatientNum, (patientNum, appointmentNum))
        if len(addProvider):
            cursor.execute(addProvider, (employeeNum, appointmentNum))
        connection.commit()
        return "Succesful"
    except Exception as e:
        # In case of any exception, print the error and rollback the transaction.
        print(f"An error occurred: {e}")
        connection.rollback()
        return "Failed"

def RemoveProviderFromAppointment(cursor, connection, employeeNum, appointmentNum):
    """
    Given an appointment number and employee number, removes the provider from a scheduled appointment.
    Returns successful if removed, returns unsuccessful if provider was not scheduled for that appointment. 

    Parameters:
    cursor (psycopg2)           : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
    connection (psycopg2)       : A connection object associated with the database session. This object is used to commit or roll
                                  back the transaction.
    appointmentNum (string)     : The unique identifier for an appointment.
    employeeNum (string)        : The unique identifier for an employee.

    Returns:
    boolean: Returns true if the provider is successfully removed from the appointment
    """
    query = """
    SELECT COUNT(*) FROM appointmentproviders
    WHERE AppointmentID = (SELECT id FROM appointment WHERE appointmentNum = %s)
    """
    deleteAppointmentProvider = """
    DELETE FROM AppointmentProviders
    WHERE HealthCareProviderID = (SELECT id FROM healthcareprovider WHERE employeenum ILIKE %s) AND AppointmentID = (SELECT id FROM appointment WHERE appointmentNum = %s)
    """
    try:
        cursor.execute(query, (appointmentNum,))
        totalProviders = cursor.fetchone()[0]
        if totalProviders == 0:
            raise Exception("Appointment and provider combination not found")
        if totalProviders == 1:
            raise Exception("Appointment must have atleast one provider")
        cursor.execute(deleteAppointmentProvider, (employeeNum, appointmentNum))
        connection.commit()
        return "Succesful"
    except Exception as e:
        # In case of any exception, print the error and rollback the transaction.
        print(f"An error occurred: {e}")
        connection.rollback()
        return "Failed"