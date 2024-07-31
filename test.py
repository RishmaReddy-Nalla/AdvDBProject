from models.utils import MongoConn


def get_appointments(collection):

    conn = MongoConn().connect()
    
    patient_ids = [patient['_id'] for patient in conn['Patients'].find()]
    appointments = conn[collection].find({
        "patientID" : {"$in" :patient_ids }
    }).limit(10)
    appointments = [appointment for appointment in appointments]
    print(appointments)

get_appointments('Appointments')