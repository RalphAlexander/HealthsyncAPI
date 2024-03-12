# Utility for patient interface
# Functions: Check if patient exists in system, generate unique patient numbers and record numbers

import string
import random


def checkPatient(cursor, PatientNum):
    query_pt = """
    SELECT * 
    FROM patient
    WHERE patientnum ILIKE %s
    """
    try:
        cursor.execute(query_pt,(PatientNum,))
        if not cursor.fetchone():
            return False
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


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

#returns a uniqe patient num
def createRecordNum(cursor):
    characters = string.digits
    generated_string = ""
    for i in range(9):
        generated_string += (random.choice(characters))
    query = """
    SELECT * FROM MedicalRecord WHERE MedicalRecordNum = %s
    """
    cursor.execute(query, (generated_string,))
    if not cursor.fetchone():
        return int(generated_string)
    return createPatientNum(cursor)