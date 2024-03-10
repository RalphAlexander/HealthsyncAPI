def CreateHealthCareProvider(cursor, firstName, lastName, titleAbbreviation, departmentAbbreviation, specialtyAbbreviation):
    """
    Description: 
    Given a first name, last name, title, department, and specialty, add a new Employee in the database. Returns the employee number.

    Parameters:
    cursor (psycopg2)               : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
    firstName (string)              : First name of the provider to be added.
    lastName (string)               : Last name of the provider to be added.
    departmentAbbreviation (string) : Department of the provider to be added.
    specialtyAbbreviation (string)  : Specialty of the provider to be added.

    Return {EmployeeNum}
    """
    
def CreateShift(cursor, employeeNum, shiftStart, shiftEnd):
    """
    Description:
    Given an EmployeeNum, shift start datetime, and shift end datetime, only if the employee is not already working
    at the given interval, then insert into ProviderShifts the HealthCareProviderId and shift start and end.
    
    Parameters:
    cursor (psycopg2)       : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
    employeeNum (string)    : The unique identifier for an employee.
    shiftStart (string)     : A datetime formatted in any accepted format.
    shiftEnd (string)       : A datetime formatted in any accepted format.
    
    Returns:
    {isSuccessful}
    """

def CreatePatient(cursor, firstName, lastName, sex, birthday, city, stateAbbreviation, address1, address2 = None, postalCode = None, email = None, phone = None):
    """
    Description: 
    Given a patient name, optional email, optional phone number, sex, birthday and address,
    create a new patient with the given information. Returns the patient number.
    
    Parameters:
    cursor (psycopg2)           : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
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
    {Patient number}
    """
    
def CreateMedicalRecord(cursor, appointmentNum, recordText):
    """
    Description: 
    Given an appointment number and record text, create a new medical record. Returns successful if created, or unsuccessful if appointment number not found.

    Parameters:
    cursor (psycopg2)           : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
    appointmentNum (string)     : The unique identifier for an appointment.
    recordText (string)         : Record of the medical record.

    Returns:
    {isSuccessful}
    """

def CreatePrescription(cursor, medicalRecordNum, medicationAbbreviation, doseInMilligrams, frequency, endDate):
    """
    Description: 
    Given a Medical record number, medication abbreviation, dose, frequency and end, creates a prescription for that patient corresponding to the medical record. Note, two active prescriptions of the same medication are not allowed. Returns successful if prescription created, or unsuccessful if prescription not created.

    Parameters:
    cursor (psycopg2)               : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
    medicalRecordNum (string)       : The unique identifier for a medical record.
    medicationAbbreviation (string) : Abbreviation of the name of the medication.
    doseInMilligrams (int)          : The dose of the prescription in milligram (mg).
    frequency (int)                 : The frequency the medication should be taken.
    endDate (string)                : A date of when to stop taking the medication in any accepted date format.

    Returns:
    {isSuccessful}
    """