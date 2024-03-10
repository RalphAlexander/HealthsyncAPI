def EditSpecialty(cursor, connection, employeeNum, specialityName):
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
    specialtyName (string)  : Name of the new speciality to be changed.

    Return {added, removed or unsuccesful}
    """
    
def EditHealthCareProvider(cursor, connection, employeeNum, title = None, firstName = None, lastName = None, departmentAbbreviation = None):
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

    Returns {isSuccessful}
    """
    
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
    boolean
    """
    
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
    {isSuccessful}
    """
    

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