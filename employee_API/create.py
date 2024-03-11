import string
import random



def CreateHealthCareProvider(cursor, conn, employeeNum, firstName, lastName, titleAbbreviation, departmentAbbreviation, specialtyAbbreviation):
    """
    Description: 
    Given a first name, last name, title, department, and specialty, add a new Employee in the database. Returns the employee number.

    Parameters:
    cursor (psycopg2)               : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
    connection (psycopg2)           : A connection object associated with the database session. This object is used to commit or roll
                                      back the transaction.
    firstName (string)              : First name of the provider to be added.
    lastName (string)               : Last name of the provider to be added.
    departmentAbbreviation (string) : Department of the provider to be added.
    specialtyAbbreviation (string)  : Specialty of the provider to be added.

    Returns:
    boolean: Returns true if HealthCareProvider successfully created
    """
    insertProvider = """
    INSERT INTO healthcareprovider (EmployeeNum, firstname, lastname, titleabbreviation, departmentAbbreviation, currentlyEmployed) VALUES
    (%s, %s, %s, %s, %s, TRUE)
    RETURNING id;
    """
    insertSpecialty = """
    INSERT INTO providerSpecialties (providerid, specialtyabbreviation) VALUES
    (%s, %s)
    """
    try:
        cursor.execute(insertProvider, (employeeNum, firstName, lastName, titleAbbreviation, departmentAbbreviation))
        providerID = int(cursor.fetchone()[0])
        if(specialtyAbbreviation):
            cursor.execute(insertSpecialty, (providerID, specialtyAbbreviation))
        conn.commit()
        return "Succesful"
    except Exception as e:
        print(f"An error occurred: {e}")
        connection.rollback()
        return "Failed"
    
def CreateShift(cursor, connection, employeeNum, shiftStart, duration):
    """
    Description:
    Given an EmployeeNum, shift start datetime, and shift end datetime, only if the employee is not already working
    at the given interval, then insert into ProviderShifts the HealthCareProviderId and shift start and end.
    
    Parameters:
    cursor (psycopg2)       : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
    connection (psycopg2)   : A connection object associated with the database session. This object is used to commit or roll
                              back the transaction.
    employeeNum (string)    : The unique identifier for an employee.
    shiftStart (string)     : A timestamp
    duration (string)       : A interval
    
    Returns:
    boolean: Returns true if shift successfully created
    """
    concurrentShifts = """
    SELECT COUNT(*)
    FROM providerShifts
    WHERE healthcareproviderid = (SELECT id from healthcareprovider WHERE employeeNum ILIKE %s) AND %s < shiftStart::TIMESTAMP + duration AND %s::TIMESTAMP + %s::INTERVAL > shiftStart
    """
    create = """
    INSERT INTO providerShifts(healthcareproviderid, shiftstart, duration) VALUES
    ((SELECT id from healthcareprovider WHERE employeeNum ILIKE %s), %s, %s);
    """
    try:
        #Check to see if any concurrent shifts already exist and return false if true
        cursor.execute(concurrentShifts, (employeeNum, shiftStart, shiftStart, duration))
        if(cursor.fetchone()[0] > 0):
            raise Exception("Concurrent shift already exists for given employee")
        cursor.execute(create, (employeeNum, shiftStart, duration))
        connection.commit()
        return "Successful"
    except Exception as e:
        print(f"An error occurred: {e}")
        # Rollback in case of any error
        connection.rollback()
        return "Failed"

def CreatePatient(cursor, connection, firstName, lastName, sex, birthday, email = "", phone = ""):
    """
    Description: 
    Given a patient name, optional email, optional phone number, sex, birthday and address,
    create a new patient with the given information. Returns the patient number.
    
    Parameters:
    cursor (psycopg2)           : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
    connection (psycopg2)       : A connection object associated with the database session. This object is used to commit or roll
                                  back the transaction.
    firstName (string)          : First name of patient to be added.
    lastName (string)           : Last name of patient to be added.
    sex (char)                  : Sex of patient to be added.
    birthday (string)           : Birthday of patient to be added in any accepted date format.
    city (string)               : City of home address of patient to be added.
    stateAbbreviation (string)  : State of home address of patient to be added.
    address1 (string)           : Address1 of home address of patient to be added.
    address2 (string)           : Address2 of home address of patient to be added.
    postalCode (string)         : Postal code of home address of patient to be added.
    email (string)              : Email of patient to be added in any accepted date format.
    phone (string)              : Phone number of patient to be added in any accepted date format.
    
    Returns: 
    {PatientNum}
    """
    create = """
    INSERT INTO patient(patientnum, firstname, lastname, email, phone, sexid, birthday) VALUES
    (%s, %s, %s, %s, %s, %s, %s)
    """
    if not len(email):
        email = None
    if not len(phone):
        phone = None
    try:
        ptNum = createPatientNum(cursor)
        cursor.execute(create, (ptNum, firstName, lastName, email, phone, sex.upper(), birthday))
        connection.commit()
        return ptNum
    except Exception as e:
        print(f"An error occurred: {e}")
        # Rollback in case of any error
        connection.rollback()
        return "Failed"

#returns a uniqe patient num
def createPatientNum(cursor):
    characters = string.ascii_letters + string.digits
    generated_string = ""
    for i in range(10):
        generated_string += (random.choice(characters))

    query = """
    SELECT * FROM patient WHERE patientNum ILIKE %s
    """
    cursor.execute(query, (generated_string,))
    if not cursor.fetchone():
        return generated_string
    return createPatientNum(cursor)

def CreateMedicalRecord(cursor, connection, appointmentNum, recordText):
    """
    Description: 
    Given an appointment number and record text, create a new medical record. Returns successful if created, or unsuccessful if appointment number not found.

    Parameters:
    cursor (psycopg2)           : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
    connection (psycopg2)       : A connection object associated with the database session. This object is used to commit or roll
                                  back the transaction.
    appointmentNum (string)     : The unique identifier for an appointment.
    recordText (string)         : Record of the medical record.

    Returns:
    boolean: Returns true if medical record successfully created
    """

def CreatePrescription(cursor, connection, medicalRecordNum, medicationAbbreviation, doseInMilligrams, frequency, endDate):
    """
    Description: 
    Given a Medical record number, medication abbreviation, dose, frequency and end, creates a prescription for that patient corresponding to the medical record. Note, two active prescriptions of the same medication are not allowed. Returns successful if prescription created, or unsuccessful if prescription not created.

    Parameters:
    cursor (psycopg2)               : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
    connection (psycopg2)           : A connection object associated with the database session. This object is used to commit or roll
                                      back the transaction.
    medicalRecordNum (string)       : The unique identifier for a medical record.
    medicationAbbreviation (string) : Abbreviation of the name of the medication.
    doseInMilligrams (int)          : The dose of the prescription in milligram (mg).
    frequency (int)                 : The frequency the medication should be taken.
    endDate (string)                : A date of when to stop taking the medication in any accepted date format.

    Returns:
    boolean: Returns true if prescription successfully created
    """