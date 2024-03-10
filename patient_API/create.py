def AddAddress(cursor, patientNum, city, stateAbbreviation, address1, address2 = None, postalCode = None):
    """
    Description: 
    Given a patient number and address, adds the address to the patient's file.

    Parameters:
    cursor (psycopg2)           : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
    patientNum (string)         : The unique identifier for a patient.
    city (string)               : City of home address of patient to be added.
    stateAbbreviation (string)  : State of home address of patient to be added.
    address1 (string)           : Address1 of home address of patient to be added.
    address2 (string)           : Address2 of home address of patient to be added.
    postalCode (string)         : Postal code of home address of patient to be added.  

    Returns:
    {isSuccessful}
    """

def ScheduleAppointment(cursor, employeeNum, dateTime, purpose, patientNum):
    """
    Description: 
    Given the Employee Num of the provider, date and time, purpose, and optionally patient
    number,creates a new appointment at that time. Return successful if appointment created,
    returns unsuccessful if provider unavailable at the given time or patientNum not found. 

    Parameters:
    cursor (psycopg2)       : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
    employeeNum (string)    : The unique identifier for an employee.
    dateTime (string)       : The dateTime of the appointment in any accepted date format.
    purpose (string)        : The purpose of the appointment.
    patientNum (string)     : The unique identifier for a patient.

    Returns:
    {isSuccessful}
    """