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
    query_pt = """
    SELECT * 
    FROM patient
    WHERE patientnum ILIKE %s
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
        cursor.execute(query_pt,(patientNum,))
        if not cursor.fetchone:
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
    

def RemoveAddress(cursor, connection, patientNum, city, stateAbbreviation, address1, postalCode = None):
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
    
    getPatientQuery = """
    SELECT ID
    FROM Patient 
    WHERE PatientNum ILIKE %s;
    """
    
    getAddressQuery = """
    SELECT ID
    FROM Address
    WHERE City ILIKE %s AND StateAbbreviation ILIKE %s AND Address1 ILIKE %s
    """
    
    deletePatientAddress = """
    DELETE FROM PatientAddresses
    WHERE PatientID = %s AND AddressID = %s
    """
    try:
        cursor.execute(getPatientQuery, (patientNum,))
        patientResult = cursor.fetchone()
        # if no patient with patientNum exists
        if not patientResult:
            print(f"Patient {patientNum} does not exist.")
            return False
        patientId = patientResult[0]
        
        addressParams = [city, stateAbbreviation, address1]
        if postalCode:
            getAddressQuery += " AND PostalCode = %s "
            addressParams.append(postalCode)
            
        cursor.execute(getAddressQuery, addressParams)
        addressResult = cursor.fetchone()
        # if no address with given parameters exists
        if not addressResult:
            print("Address with the given parameters does not exist in our database")
            return False
        addressId = addressResult[0]
        
        cursor.execute(deletePatientAddress, (patientId, addressId,))
        
        # Check if the update was successful by looking at rowcount.
        if cursor.rowcount == 0:
            return False  # No rows were updated, hence operation was unsuccessful.
            
        # Commit the changes if there were updates.
        connection.commit()
        print(f"Successfully deleted address from patient {patientNum}.")
        return True  # The edit was successful.

    except Exception as e:
        # In case of any exception, print the error and rollback the transaction.
        print(f"An error occurred: {e}")
        connection.rollback()
        return False
    
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
    
    getAppointmentQuery = """
    SELECT Id
    FROM appointment
    WHERE AppointmentNum = %s
    """
    
    editAppointmentQuery = """
    UPDATE Appointment
    SET date = %s
    WHERE Id = %s
    """
    try:
        cursor.execute(getAppointmentQuery, (appointmentNum,))
        queryResults = cursor.fetchone()
        if not queryResults:
            print(f"Appointment {appointmentNum} does not exist.")
            return False
        appointmentId = queryResults[0]
        cursor.execute(editAppointmentQuery, (newDateTime,appointmentId,))
        # Check if the update was successful
        if cursor.rowcount > 0:
            print(f"Update successful. Rows affected: {cursor.rowcount}")
            connection.commit()
            return True
        
        print("Update failed. No rows were affected.")
        connection.rollback()  # Optional: Rollback if you consider the update critical and want to undo any potential changes
        return False
    
    except Exception as e:
        # In case of any exception, print the error and rollback the transaction.
        print(f"An error occurred: {e}")
        connection.rollback()
        return False

def EditAppointment(cursor, connection, appointmentNum, newDate = None, newDuration = None, newPurpose = None, employeeNum = None):
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
    
    getAppointmentQuery = """
    SELECT Id
    FROM appointment
    WHERE AppointmentNum = %s
    """
    getEmployee = """
    SELECT Id
    FROM HealthCareProvider
    WHERE employeeNum ILIKE %s
    """
    updateAppointmentProvider = """
    UPDATE AppointmentProviders
    SET HealthCareProviderID = %s
    WHERE AppointmentID = %s
    """
    try:
        
        updates = []
        params = []

        if newDate is not None:
            updates.append("date = %s")
            params.append(newDate)
        
        if newDuration is not None:
            updates.append("duration = %s")
            params.append(newDuration)
        
        if newPurpose is not None:
            updates.append("purpose = %s")
            params.append(newPurpose)
        
        employeeId = None
        if employeeNum is not None:
            
            cursor.execute(getEmployee, (employeeNum,))
            employeeResults = cursor.fetchone()
            if not employeeResults:
                print(f"Health Care Provider {employeeNum} does not exist.")
                return False
            employeeId = employeeResults[0]
        
        # Ensure there is at least one field to update.
        if not updates:
            return False
        
        cursor.execute(getAppointmentQuery, (appointmentNum,))
        queryResults = cursor.fetchone()
        if not queryResults:
            print(f"Appointment {appointmentNum} does not exist.")
            return False
        appointmentId = queryResults[0]
        
        update_clause = ', '.join(updates)
        query = f"UPDATE Appointment SET {update_clause} WHERE ID = %s;"
        params.append(appointmentId)
        
        # Execute the update query.
        cursor.execute(query, params)
        if employeeNum:
            cursor.execute(updateAppointmentProvider, (employeeId, appointmentId,))
        # Check if the update was successful
        if cursor.rowcount > 0:
            print("Update successful.")
            connection.commit()
            return True
        
        print("Update failed. No rows were affected.")
        connection.rollback()  # Optional: Rollback if you consider the update critical and want to undo any potential changes
        return False
    
    except Exception as e:
        # In case of any exception, print the error and rollback the transaction.
        print(f"An error occurred: {e}")
        connection.rollback()
        return False
    
# tested and works
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
    
    getAppointmentQuery = """
    SELECT Id
    FROM appointment
    WHERE AppointmentNum = %s
    """
    getEmployee = """
    SELECT Id
    FROM HealthCareProvider
    WHERE employeeNum ILIKE %s
    """
    deleteAppointmentProvider = """
    DELETE FROM AppointmentProviders
    WHERE HealthCareProviderID = %s AND AppointmentID = %s
    """
    try:
        cursor.execute(getAppointmentQuery, (appointmentNum,))
        queryResults = cursor.fetchone()
        if not queryResults:
            print(f"Appointment {appointmentNum} does not exist.")
            return False
        appointmentId = queryResults[0]
        
        cursor.execute(getEmployee, (employeeNum,))
        employeeResults = cursor.fetchone()
        if not employeeResults:
            print(f"Health Care Provider {employeeNum} does not exist.")
            return False
        employeeId = employeeResults[0]
        
        cursor.execute(deleteAppointmentProvider, (employeeId, appointmentId,))
        
        if cursor.rowcount > 0:
            print(f"Update successful. Rows deleted: {cursor.rowcount}")
            connection.commit()
            return True
        
        print("Update failed. No rows were affected.")
        connection.rollback()  # Optional: Rollback if you consider the update critical and want to undo any potential changes
        return False
    
    except Exception as e:
        # In case of any exception, print the error and rollback the transaction.
        print(f"An error occurred: {e}")
        connection.rollback()
        return False
    

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
    
    getAllMedicalRecords = """
    SELECT ID
    FROM MedicalRecord
    WHERE AppointmentID = %s
    """
    
    deletePrescription = """
    DELETE FROM Prescription
    WHERE MedicalRecordID = %s
    """
    
    deleteMedicalRecords = """
    DELETE FROM MedicalRecord
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
            print(f"Appointment {appointmentNum} does not exist.")
            return False
        appointmentId = queryResults[0]
        appointmentDateTime = queryResults[1]
        
        now = datetime.now()
        if appointmentDateTime - now <= timedelta(hours=24):
            print("Appointment is within 24 hours and cannot be cancelled.")
            return False
        
        cursor.execute(getAllMedicalRecords, (appointmentId,))
        medicalRecords = cursor.fetchall()
        
        for record in medicalRecords:
            recordId = record[0]
            cursor.execute(deletePrescription, (recordId,))
        
        cursor.execute(deleteMedicalRecords, (appointmentId,))
        cursor.execute(deleteAppointmentProviders, (appointmentId,))
        cursor.execute(deleteAppointment, (appointmentId,))
        
        if cursor.rowcount > 0:
            print(f"Appointment {appointmentNum} successfuly deleted.")
            connection.commit()
            return True
        
        print("Update failed. No rows were affected.")
        connection.rollback()  # Optional: Rollback if you consider the update critical and want to undo any potential changes
        return False
    
    except Exception as e:
        # In case of any exception, print the error and rollback the transaction.
        print(f"An error occurred: {e}")
        connection.rollback()
        return False