from models.utils import MongoConn

def get_appointments(collection):
    
    try:
        conn = MongoConn().connect()
        
        patient_ids = [patient['_id'] for patient in conn['Patients'].find()]
        pipeline = {
            "$lookup" : {
                "from" : "Patients",
                "localField": "patientID",
                
            }
        }
        appointments = conn[collection].find({
            "patientID" : {"$in" :patient_ids }
        }).limit(10)
        appointments = [appointment for appointment in appointments]
        return appointments
    except Exception as e:
        return f"Error Occured in fetching appointments {e}"