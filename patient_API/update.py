def EditPatient(cursor, patientNum, firstName = None, lastName = None, email = None, phone = None):
    """
    Description: 
    Given the patient number and new information to update, updates the patient file with the new
    information. Returns successful if changed, returns unsuccessful if patient not found.

    Parameters:
    cursor (psycopg2)       : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
    patientNum (string)     : The unique identifier for a patient.
    firstName (string)      : First name of the patient that will be changed.
    lastName (string)       : Last name of the patient that will be changed.
    email (string)          : Email of the patient that will be changed.
    phone (string)          : Phone number of the patient that will be changed.

    Return {isSuccessful}
    """
    
def RemoveAddress(cursor, patientNum, city, stateAbbreviation, address1, PostalCode = None):
    
    """
    Description: 
    Given a patient number and address, remove the address from the patient's file. Returns
    successful if the address is removed, returns unsuccessful if patient or address not found.

    Parameters:
    cursor (psycopg2)           : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
    patientNum (string)         : The unique identifier for a patient.
    city (string)               : City of home address of patient to be added.
    stateAbbreviation (string)  : State of home address of patient to be added.
    address1 (string)           : Address1 of home address of patient to be added.
    postalCode (string)         : Postal code of home address of patient to be added.
    
    Returns:
    {isSuccessful}
    """
    
def EditAppointmentDate(cursor, appointmentNum, newDateTime):
    """
    Description: 
    Given an appointment number and a new date and time, updates the appointment to the scheduled
    date and time if the attending providers are available. Note, can only edit the appointment date
    24 hours or more ahead of the current appointment time. Returns successful if appointment updated,
    returns unsuccessful if appointment not found or unable to change appointment date and time.

    Parameters: 
    cursor (psycopg2)           : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
    appointmentNum (string)     : The unique identifier for an appointment.
    newDateTime (string)        : The new datetime to set the appointment to in any accepted dateTime format.

    Returns:
    {isSuccessful}
    """

def EditAppointment(cursor, appointmentNum, newDate = None, newDuration = None, newPurpose = None, employeeNum = None):
    """
    Description: 
    Given an appointment number, and the information to change on the appointment, it updates
    the appointment with the new information. Returns successful if appointment updated, returns
    unsuccessful if appointment not found.

    Parameters:
    cursor (psycopg2)           : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
    appointmentNum (string)     : The unique identifier for an appointment.
    newDate (string)            : The new date to set the appointment to in any accepted date format to set to.
    newDuration (int)           : The new duration of the appointment in minutes to set to.
    newPurpose (string)         : The new purpose of the appointment to set to.
    employeeNum (string)        : The unique identifier for an employee.

    Returns:
    {isSuccessful}
    """
    
def RemoveProviderFromAppointment(cursor, employeeNum, appointmentNum):
    """
    Given an appointment number and employee number, removes the provider from a scheduled appointment.
    Returns successful if removed, returns unsuccessful if provider was not scheduled for that appointment. 

    Parameters:
    cursor (psycopg2)           : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
    appointmentNum (string)     : The unique identifier for an appointment.
    employeeNum (string)        : The unique identifier for an employee.

    Returns:
    {isSuccessful}
    """

def CancelAppointment(cursor, appointmentNum):
    """
    Description: 
    Given an appointment number, cancels appointments in the system by setting duration to 0 minutes. 
    Note, canceling appointments only works 24 hours or more ahead of the appointment time. Returns successful 
    if appointment canceled, returns unsuccessful if not found or not canceled.

    Parameters:
    cursor (psycopg2)           : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
    appointmentNum (string)     : The unique identifier for an appointment.

    Returns:
    {isSuccessful}
    """
    
