from customtkinter import*
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# Fetch data from Firestore where GRDStatus is 'Approved'
clinics_ref = db.collection('Clinics').where('GRDStatus', '==', 'Approved')
docs = clinics_ref.stream()

# Prepare the data
clinic_data = []
for doc in docs:
    clinic_data.append(doc.to_dict())

root = CTk()
root.title("Clinics with Approved GRDStatus")

frame = CTkFrame(master=root, corner_radius=15, width=600, height=400)
frame.pack(pady=20, padx=20, fill="both", expand=True)

# Display each clinic data
for clinic in clinic_data:
    clinic_info = (
        f"Name: {clinic.get('Name', 'N/A')}\n"
        f"Email: {clinic.get('Email', 'N/A')}\n"
        f"PhoneNo: {clinic.get('PhoneNo', 'N/A')}\n"
        f"Address: {clinic.get('Address', 'N/A')}\n"
        f"GRDStatus: {clinic.get('GRDStatus', 'N/A')}"
    )
    label = CTkLabel(
        master=frame,
        text=clinic_info,
        width=550,
        height=100,
        corner_radius=15,
        fg_color="white",
        text_color="black",
        justify='left'
    )
    label.pack(pady=10, padx=10)

root.mainloop()