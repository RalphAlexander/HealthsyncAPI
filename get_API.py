def get_medical_records(patient_num, cursor):
    try:
        query = """
        SELECT mr.*
        FROM medicalrecord mr 
            JOIN appointment a ON mr.appointmentid  = a.id
            JOIN patient p ON p.id = a.patientid
        WHERE p.patientnum = %s
        ORDER BY mr.date DESC;
        """
        cursor.execute(query, (patient_num,))
        records = cursor.fetchall()
        return records
    except Exception as e:
        print(f"Error retrieving medical records: {e}")
        return []
    

def view_current_prescriptions(patient_num, cursor):

    """
    Description:
    Accessible by employee and patient
    Given a patient Number, return all active prescriptions for that patient.

    Parameters:
    patient_num (int) : The unique identifier for a patient
    cursor (psycopg2) : A cursor object obtained from a psycopg2 database connection, used to execute database queries.

    Return:
    {[MedicationName, Milligrams, Frequence, EndDate]};
    """

    try:
        query = """
        SELECT m.name, pr.milligrams, pr.frequency, pr.endDate
        FROM Prescription pr
            JOIN medicalrecord mr ON mr.id = pr.medicalrecordid
            JOIN appointment a ON a.id = mr.appointmentid 
            JOIN patient p ON p.id = a.patientid
            JOIN medication m ON m.abbreviation = pr.medicationAbbreviation
        WHERE p.patientNum = %s AND pr.enddate > CURRENT_DATE
        ORDER BY pr.enddate DESC;
        """
        cursor.execute(query, (patient_num,))
        records = cursor.fetchall()
        return records
    except Exception as e:
        print(f"Error retrieving medical records: {e}")
        return []