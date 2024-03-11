from patient_API.patUtil import *
from datetime import datetime, timedelta

def EditPatient(cursor, connection, patientNum, firstName = "", lastName = "", email = "", phone = ""):
    """
    Description: 
    Given the patient number and new information to update, updates the patient file with the new
    information. Returns successful if changed, returns unsuccessful if patient not found.

    Parameters:
    cursor (psycopg2)       : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
    connection (psycopg2)   : A connection object associated with the database session. This object is used to commit or roll
                              back the transaction.
    patientNum (string)     : The unique identifier for a patient.
    firstName (string)      : First name of the patient that will be changed.
    lastName (string)       : Last name of the patient that will be changed.
    email (string)          : Email of the patient that will be changed.
    phone (string)          : Phone number of the patient that will be changed.

    Returns:
    boolean: Returns true if the edit on the database is successful
    """
    update_firstName = """
    UPDATE patient
    SET firstName = %s
    WHERE patientnum ILIKE %s
    """
    update_lastName = """
    UPDATE patient
    SET lastName = %s
    WHERE patientnum ILIKE %s
    """
    update_email = """
    UPDATE patient
    SET email = %s
    WHERE patientnum ILIKE %s
    """
    update_phone = """
    UPDATE patient
    SET phone = %s
    WHERE patientnum ILIKE %s
    """
    try:
        if not checkPatient(cursor, (patientNum,)):
            raise Exception("Patient not found")
        if len(firstName): 
            cursor.execute(update_firstName, (firstName, patientNum))
        if len(lastName): 
            cursor.execute(update_lastName, (lastName, patientNum))
        if len(email):
            cursor.execute(update_email, (email, patientNum))
        if len(phone):
            cursor.execute(update_phone, (phone, patientNum))
        connection.commit()
        return "Successful"
    except Exception as e:
        # In case of any exception, print the error and rollback the transaction.
        print(f"An error occurred: {e}")
        connection.rollback()
        return "Failed"
    

def RemoveAddress(cursor, connection, patientNum, address, city, state):
    """
    Description: 
    Given a patient number and address, remove the address from the patient's file. Returns
    successful if the address is removed, returns unsuccessful if patient or address not found.

    Parameters:
    cursor (psycopg2)           : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
    connection (psycopg2)       : A connection object associated with the database session. This object is used to commit or roll
                                  back the transaction.
    patientNum (string)         : The unique identifier for a patient.
    city (string)               : City of home address of patient to be added.
    stateAbbreviation (string)  : State of home address of patient to be added.
    address1 (string)           : Address1 of home address of patient to be added.
    postalCode (string)         : Postal code of home address of patient to be added.
    
    Returns:
    boolean: Returns true if the address is removed from the patient's record
    """
    
    queryAddress = """
    SELECT addressId, patientid
    FROM patientAddresses
        JOIN address ON address.id = addressid
        JOIN patient ON patient.id = patientid
    WHERE patientID = (SELECT ID from patient WHERE patientnum ILIKE %s) AND address1 ILIKE %s AND city ILIKE %s AND stateabbreviation ILIKE %s
    """
    removeAddress = """
    DELETE FROM patientaddresses
    WHERE addressid = %s AND patientid = %s
    """
    try:
        cursor.execute(queryAddress, (patientNum, address, city, state))
        result = cursor.fetchone()
        if not result:
            raise Exception("Address not found")
        addID = result[0]
        ptID = result[1]
        cursor.execute(removeAddress, (addID, ptID))
        connection.commit()
        return "Succesful"
    except Exception as e:
        # In case of any exception, print the error and rollback the transaction.
        print(f"An error occurred: {e}")
        connection.rollback()
        return "Failed"
    
def EditAppointmentDate(cursor, connection, appointmentNum, newDateTime):
    """
    Description: 
    Given an appointment number and a new date and time, updates the appointment to the scheduled
    date and time if the attending providers are available. Note, can only edit the appointment date
    24 hours or more ahead of the current appointment time. Returns successful if appointment updated,
    returns unsuccessful if appointment not found or unable to change appointment date and time.

    Parameters: 
    cursor (psycopg2)           : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
    connection (psycopg2)       : A connection object associated with the database session. This object is used to commit or roll
                                  back the transaction.
    appointmentNum (string)     : The unique identifier for an appointment.
    newDateTime (string)        : The new datetime to set the appointment to in any accepted dateTime format.

    Returns:
    boolean: Returns true if the appointment edit is successful or not
    """
    
    query ="""
    SELECT *
    FROM appointment
    WHERE appointmentnum = %s AND date > NOW() + '1d'
    """
    update = """
    UPDATE appointment
    SET date = %s
    WHERE appointmentNum = %s
    """
    try:
        cursor.execute(query, (appointmentNum,))
        if not len(cursor.fetchone()):
            raise Exception("Appointment not found or within 24 hours")
        cursor.execute(update, (newDateTime, appointmentNum))
        connection.commit()
        return "Succesful"
    except Exception as e:
        # In case of any exception, print the error and rollback the transaction.
        print(f"An error occurred: {e}")
        connection.rollback()
        return "Failed"
    

# tested basic functionality and cancel within 24 hours
def CancelAppointment(cursor, connection, appointmentNum):
    """
    Description: 
    Given an appointment number, cancels appointments in the system by setting duration to 0 minutes. Note, canceling
    appointments only works 24 hours or more ahead of the appointment time. Returns successful if appointment canceled,
    returns unsuccessful if not found or not canceled. Deletes all associated medical records and prescriptions.

    Parameters:
    cursor (psycopg2)           : A cursor object obtained from a psycopg2 database connection, used to execute database queries.
    connection (psycopg2)       : A connection object associated with the database session. This object is used to commit or roll
                                  back the transaction.
    appointmentNum (string)     : The unique identifier for an appointment.

    Returns:
    boolean: Returns true if the appointment is successfuly canceled
    """
    getAppointmentQuery = """
    SELECT Id, Date
    FROM appointment
    WHERE AppointmentNum = %s
    """
    deleteAppointmentProviders = """
    DELETE FROM AppointmentProviders
    WHERE AppointmentID = %s
    """
    deleteAppointment = """
    DELETE FROM Appointment
    WHERE ID = %s
    """
    try:
        cursor.execute(getAppointmentQuery, (appointmentNum,))
        queryResults = cursor.fetchone()
        if not queryResults:
            raise Exception("Appointment not found")
        appointmentId = queryResults[0]
        appointmentDateTime = queryResults[1]
        
        now = datetime.now()
        if appointmentDateTime - now <= timedelta(hours=24) or now - appointmentDateTime > timedelta(hours=0):
            raise Exception("Appointment has passed or is within 24 hours of scheduled time")
        
        cursor.execute(deleteAppointmentProviders, (appointmentId,))
        cursor.execute(deleteAppointment, (appointmentId,))
        connection.commit()
        return "Succesful"
    
    except Exception as e:
        # In case of any exception, print the error and rollback the transaction.
        print(f"An error occurred: {e}")
        connection.rollback()
        return "Failed"