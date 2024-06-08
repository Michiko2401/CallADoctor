# ClinicId = 'C-wTrXvY'
# Clinic need to be able to assign doctor for patient
# Upload photo for doctor
# Button location
from customtkinter import *

import firebase_admin
import uuid
from firebase_admin import credentials, firestore
from tkinter import *
from PIL import Image
from tkinter import messagebox
import numpy as np
from firebase_admin import credentials, storage
import cv2
import random
import string

import gspread
from google.oauth2.service_account import Credentials
import pytz
from datetime import datetime


# Retrieve patient name based on patient ID from the Patients collection

class Patient:
    def __init__(self, appointment_id, patient_id, patient_name, doctor_id, doctor_name, appointment_type, date,
                 medical_concern, medical_docs, prescription, status, time, address):
        self.__appointment_id = appointment_id
        self.__patient_id = patient_id
        self.__patient_name = patient_name
        self.__doctor_id = doctor_id
        self.__doctor_name = doctor_name
        self.__appointment_type = appointment_type
        self.__date = date
        self.__time = time
        self.__medical_concern = medical_concern
        self.__medical_docs = medical_docs
        self.__prescription = prescription
        self.__status = status
        self.__address = address
        self.__clinic_id = None  # Private attribute

    def get_appointment_id(self):
        return self.__appointment_id

    def get_patient_id(self):
        return self.__patient_id

    def get_patient_name(self):
        return self.__patient_name

    def get_doctor_name(self):
        return self.__doctor_name

    def get_doctor_id(self):
        return self.__doctor_id

    def get_appointment_type(self):
        return self.__appointment_type

    def get_date(self):
        return self.__date

    def get_time(self):
        return self.__time

    def get_medical_concern(self):
        return self.__medical_concern

    def get_status(self):
        return self.__status

    def get_address(self):
        return self.__address

    def get_clinic_id(self):
        return self.__clinic_id

    def set_clinic_id(self, clinic_id):
        self.__clinic_id = clinic_id

    def set_appointment_Id(self, appointment_Id):
        self.__appointment_Id = appointment_Id

    def set_patient_Id(self, patient_Id):
        self.__patient_id = patient_Id

    def set_patient_name(self, patient_name):
        self.__patient_name = patient_name

    def set_doctor_id(self, doctor_id):
        self.doctor_id = doctor_id

    def set_doctor_name(self, doctor_name):
        self.__doctor_name = doctor_name

    def set_appointment_type(self, appointment_type):
        self.__appointment_type = appointment_type

    def set_date(self, date):
        self.__date = date

    def set_medical_concern(self, medical_concern):
        self.__medical_concern = medical_concern

    def set_medical_doc(self, medical_doc):
        self.__medical_doc = medical_doc

    def set_prescription(self, prescription):
        self.__prescription = prescription

    def set_status(self, status):
        self.__status = status

    def set_time(self, time):
        self.__time = time

    def set_address(self, address):
        self.__address = address


class Clinic:
    def __init__(self, clinic_Id, name, image, address, email, phone_no, specialty, work_days, start_hours, end_hours,
                 start_break_hours, end_break_hours, description):
        self.__clinic_Id = clinic_Id
        self.__name = name
        self.__image = image
        self.__address = address
        self.__email = email
        self.__phone_no = phone_no
        self.__specialty = specialty
        self.__work_days = work_days
        self.__start_hours = start_hours
        self.__end_hours = end_hours
        self.__start_break_hours = start_break_hours
        self.__end_break_hours = end_break_hours
        self.__description = description

    def get_clinic_Id(self):
        return self.__clinic_Id

    def get_name(self):
        return self.__name

    def get_image(self):
        return self.__image

    def get_address(self):
        return self.__address

    def get_email(self):
        return self.__email

    def get_phone_no(self):
        return self.__phone_no

    def get_specialty(self):
        return self.__specialty

    def get_work_days(self):
        return self.__work_days

    def get_start_hours(self):
        return self.__start_hours

    def get_end_hours(self):
        return self.__end_hours

    def get_description(self):
        return self.__description

    def get_start_break_hours(self):
        return self.__start_break_hours

    def get_end_break_hours(self):
        return self.__end_break_hours

    def set_name(self, name):
        self.__name = name

    def set_image(self, image):
        self.__image = image

    def set_address(self, address):
        self.__address = address

    def set_email(self, email):
        self.__email = email

    def set_phone_no(self, phone_no):
        self.__phone_no = phone_no

    def set_specialty(self, specialty):
        self.__specialty = specialty

    def set_work_days(self, work_days):
        self.__work_days = work_days

    def set_start_hours(self, start_hours):
        self.__start_hours = start_hours

    def set_end_hours(self, end_hours):
        self.__end_hours = end_hours

    def set_start_break_hours(self, start_break_hours):
        self.__start_break_hours = start_break_hours

    def end_start_break_hours(self, end_break_hours):
        self.__end_break_hours = end_break_hours

    def set_description(self, description):
        self.__description = description


class Doctors:
    def __init__(self, doctor_id, address, clinic_id, email, image, language, name, phone_no, qualification,
                 register_status, specialty):
        self.doctor_id = doctor_id
        self.address = address
        self.clinic_id = clinic_id
        self.email = email
        self.image = image
        self.language = language
        self.name = name
        self.phone_no = phone_no
        self.qualification = qualification
        self.register_status = register_status
        self.specialty = specialty

    def get_doctor_id(self):
        return self.doctor_id

    def get_address(self):
        return self.address

    def get_clinic_id(self):
        return self.clinic_id

    def get_email(self):
        return self.email

    def get_image(self):
        return self.image

    def get_language(self):
        return self.language

    def get_name(self):
        return self.name

    def get_phone_no(self):
        return self.phone_no

    def get_qualification(self):
        return self.qualification

    def get_register_status(self):
        return self.register_status

    def get_specialty(self):
        return self.specialty

    def set_address(self, address):
        self.__address = address

    def set_clinicId(self, clinicID):
        self.__clinicID = clinicID

    def set_email(self, email):
        self.__email = email

    def set_image(self, image):
        self.__image = image

    def set_language(self, language):
        self.__language = language

    def set_name(self, name):
        self.__name = name

    def set_phone_no(self, phone_no):
        self.__phone_no = phone_no

    def set_qualification(self, qualification):
        self.__qualification = qualification

    def set_register_status(self, register_status):
        self.__register_status = register_status

    def set_specialty(self, specialty):
        self.__specialty = specialty


cred = credentials.Certificate("serviceAccountKey.json")

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {'storageBucket': 'call-a-doctor-20a5d.appspot.com'})

db = firestore.client()
# Initialize the main application window
app = CTk()
app.geometry("1080x664")
set_appearance_mode("light")

# Frames
frameSideNav = CTkFrame(master=app, fg_color="#5271FF", corner_radius=0, width=80)
frameSideNav.pack(side="left", fill="y")

# Use a regular Tkinter Frame instead of CTkScrollableFrame for frameHome
frameHome = Frame(app, bg="#B5CAFF")  # Use a regular Tkinter Frame
frameHome.pack(side="left", fill="both", expand=True)
frameHome.grid_columnconfigure(0, weight=1)
frameHome.grid_rowconfigure(0, weight=0)


# Functions
def btnMenu_Click():
    print("Menu Button Clicked")


def btnHome_Click():
    print("Home Button Clicked")


def btnBookHis_Click():
    print("Booking History Button Clicked")


def btnLogin_Click():
    print("Login Button Clicked")


def btnSearch_Click():
    print("Search Button Clicked")


def format_date_and_time(timestamp, timezone='Asia/Shanghai'):
    """ Convert and format the timestamp to separate date and time strings. """
    try:
        # Convert the Firestore timestamp to a standard datetime object
        if isinstance(timestamp, datetime):
            dt = timestamp
        else:
            dt = timestamp.to_datetime()

        # Convert to the specified timezone
        target_tz = pytz.timezone(timezone)
        dt_tz = dt.astimezone(target_tz)

        # Format the datetime object to separate date and time strings
        formatted_date = dt_tz.strftime('%B %d, %Y')
        formatted_time = dt_tz.strftime('%I:%M:%S %p %Z')

        return formatted_date, formatted_time
    except Exception as e:
        print(f"Error formatting date and time: {e}")
        return str(timestamp), str(timestamp)  # Return the original timestamp as strings if there's an error


def btnAppointment_Click(clinic_id):
    print("Appointment Button Clicked")

    Appointment_ref = db.collection('AppointmentDetails').where('ClinicId', '==', clinic_id)
    docs = Appointment_ref.stream()

    # Prepare the data
    appointment_data = []
    for doc in docs:
        appointment_details = doc.to_dict()
        appointment_details['AppointmentId'] = doc.id  # Add the document ID to the appointment details
        appointment_data.append(appointment_details)

    # Clear existing widgets in frameAppointment
    for widget in frameAppointment.winfo_children():
        widget.destroy()

    frameAppointment.grid_columnconfigure(0, minsize=50)  # Column for "No."
    frameAppointment.grid_columnconfigure(1, minsize=600)  # Column for "Patient Information"

    lblNo = CTkLabel(master=frameAppointment, text="No.", font=("Inter", 20), text_color="black")
    lblNo.grid(row=0, column=0, sticky="ew", pady=(0, 1), padx=(10, 0))  # Adjusted sticky to center content

    lblPatientInfo = CTkLabel(master=frameAppointment, text="Patient Information", font=("Inter", 20),
                              text_color="black")
    lblPatientInfo.grid(row=0, column=1, columnspan=2, sticky="ew", pady=(0, 1), padx=(10, 0))

    # Create a list to store Patient objects
    patients = []

    row_index = 1  # Initialize row_index outside the loop

    for index, appointment in enumerate(appointment_data, start=1):
        lblIndex = CTkLabel(master=frameAppointment, text=f"{index}.", font=("Inter", 20), text_color="black")
        lblIndex.grid(row=row_index, column=0, sticky="ew", padx=(10, 0), pady=(1, 0))

        appointment_id = appointment.get('AppointmentId')
        print(f"Appointment ID: {appointment_id}")

        # Retrieve patient name based on patient ID from the Patients collection
        patient_id = appointment.get('PatientId', 'N/A')
        patient_name = get_patient_name(patient_id)

        doctor_id = appointment.get('DoctorId', '-')
        doctor_name = get_doctor_name(doctor_id)

        appointment_type = appointment.get('AppointmentType', 'N/A')
        clinic_id = appointment.get('ClinicId', 'N/A')
        date = appointment.get('DateTime', 'N/A')

        # Debugging print to check the date format
        print(f"Original date: {date}")

        if date != 'N/A':
            formatted_date, formatted_time = format_date_and_time(date)  # Format the date and time
        else:
            formatted_date = date
            formatted_time = 'N/A'
        address = appointment.get('PatientAddress', 'N/A')
        medical_concern = appointment.get('MedicalConcern', 'N/A')
        medical_docs = appointment.get('MedicalDocs', 'N/A')
        prescription = appointment.get('Prescription', 'N/A')
        status = appointment.get('Status', 'N/A')

        # Create Patient object and append to patients list
        patient = Patient(appointment_id, patient_id, patient_name, doctor_id, doctor_name, appointment_type,
                          formatted_date, medical_concern, medical_docs, prescription, status, formatted_time, address)
        patients.append(patient)

        # Construct appointment_info string
        appointment_info = (
            f"Patient Name: {patient.get_patient_name()}\n"
            f"Doctor Name: {patient.get_doctor_name()}\n"
            f"Appointment Type: {patient.get_appointment_type()}\n"
            f"Date: {patient.get_date()}\n"
            f"Time: {patient.get_time()}\n"
            f"Medical Concern: {patient.get_medical_concern()}\n"
            f"Status: {patient.get_status()}\n"
        )

        lblAppointments = CTkLabel(master=frameAppointment, text=appointment_info, width=700, height=59,
                                   corner_radius=20, fg_color="white", text_color="#5D5D5D",
                                   font=("Inter", 15), justify="left", anchor="w")
        lblAppointments.grid(row=row_index, column=1, columnspan=2, sticky="ew", padx=(0, 10), pady=(20, 0))

        # Bind click event to the label
        lblAppointments.bind("<Button-1>",
                             lambda event, patient=patient, clinic_id=clinic_id: patient_details(patient, clinic_id))

        row_index += 1  # Increment row_index for the next iteration

    frameAppointment.grid()
    frameClinic.grid_remove()
    frameDoctor.grid_remove()
    framePatient.grid_remove()
    frameEditDoctor.grid_remove()


def SearchDoctor(clinic_id):
    # Fetch all appointment details based on the current doctor
    appointment_ref = db.collection('AppointmentDetails').where('ClinicId', '==', clinic_id)
    appointment_docs = appointment_ref.stream()

    # Collect all unique doctor IDs
    doctor_ids = set()
    for appointment in appointment_docs:
        appointment_data = appointment.to_dict()
        doctor_id = appointment_data.get('DoctorId', 'N/A')
        if doctor_id != 'N/A':
            doctor_ids.add(doctor_id)

    # Fetch doctor details for each unique doctor ID
    doctor_names = []
    for doctor_id in doctor_ids:
        doctor_ref = db.collection('Doctors').document(doctor_id)
        doctor_data = doctor_ref.get().to_dict()
        if doctor_data:
            doctor_name = doctor_data.get('Name', 'N/A')
            doctor_names.append(f"{doctor_name} : {doctor_id}")

    print("Doctor Names:", doctor_names)
    return doctor_names  # Return the list of doctor names


def patient_details(patient, clinic_id):
    print("A patient information has been clicked.")

    # Clear existing widgets in framePatient
    for widget in framePatient.winfo_children():
        widget.destroy()

    # Retrieve appointment type and address
    appointment_type = patient.get_appointment_type()
    print(appointment_type)
    address = patient.get_address()

    # Determine if address should be included based on appointment type
    address_line = f"Address: {address}\n" if appointment_type == 'Home Visit' else ""

    # Display patient details

    appointment_info = (
        f"ID: {patient.get_appointment_id()}\n"
        f"Type: {appointment_type}\n"
        f"Date: {patient.get_date()}\n"
        f"Time: {patient.get_time()}\n"
        f"Address: {address_line}"
        f"Register approval status: {patient.get_status()}\n"
    )
    patient_info = (
        # Patient info
        f"ID: {patient.get_patient_id()}\n"
        f"Name: {patient.get_patient_name()}\n"
        f"Medical Concern: {patient.get_medical_concern()}\n"

    )
    doctor_info = (
        # Doctor info
        f"ID: {patient.get_doctor_id()}\n"
        f"Name: {patient.get_doctor_name()}\n"
    )
    # Appointment
    lblAppointment = CTkLabel(
        master=framePatient, text="Appointment information: ", width=550, height=0, corner_radius=0,
        text_color="Black", font=("Inter", 20, "bold"), justify="left", anchor="w"
    )
    lblAppointment.grid(row=0, column=0, padx=20, pady=0, sticky="enw")

    lblAppointmentInfo = CTkLabel(
        master=framePatient, text=appointment_info, width=550, height=0, corner_radius=0,
        text_color="Black", font=("Inter", 20), justify="left", anchor="w"
    )
    lblAppointmentInfo.grid(row=1, column=0, padx=20, pady=0, sticky="enw")

    # Patient
    lblPatient = CTkLabel(
        master=framePatient, text="Patient information", width=550, height=0, corner_radius=0,
        text_color="Black", font=("Inter", 20, "bold"), justify="left", anchor="w"
    )
    lblPatient.grid(row=2, column=0, padx=20, pady=0, sticky="enw")

    lblPatientInfo = CTkLabel(
        master=framePatient, text=patient_info, width=550, height=0, corner_radius=0,
        text_color="Black", font=("Inter", 20), justify="left", anchor="w"
    )

    lblPatientInfo.grid(row=3, column=0, padx=20, pady=0, sticky="enw")
    # Doctor

    lblDoctor = CTkLabel(
        master=framePatient, text="Doctor information:", width=550, height=0, corner_radius=0,
        text_color="Black", font=("Inter", 20, "bold"), justify="left", anchor="w"
    )
    lblDoctor.grid(row=4, column=0, padx=20, pady=0, sticky="enw")

    lblDoctorInfo = CTkLabel(
        master=framePatient, text=doctor_info, width=550, height=0, corner_radius=0,
        text_color="Black", font=("Inter", 20), justify="left", anchor="w"
    )
    lblDoctorInfo.grid(row=5, column=0, padx=20, pady=0, sticky="enw")

    # Conditionally render the doctor dropdown if there is no doctor ID
    if patient.get_doctor_id() == '-':
        lblChooseDoctor = CTkLabel(
            master=framePatient, text="Choose doctor for patient:", font=("Inter", 20),
            text_color="black"
        )
        lblChooseDoctor.grid(row=6, column=0, padx=20, pady=(10, 5), sticky="w")

        doctor_names = SearchDoctor(clinic_id)
        doctor_var = StringVar()
        doctor_var.set('-')
        doctor_dropdown = OptionMenu(framePatient, doctor_var, *doctor_names,
                                     command=lambda selected_doctor: update_doctor(patient, selected_doctor))
        doctor_dropdown.config(width=20, font=("Inter", 15))
        doctor_dropdown.grid(row=6, column=1, pady=(10, 5), sticky="w")

    btnBack = CTkButton(master=framePatient, text="Back", fg_color="#5271FF", font=("Inter", 20, "bold"),
                        corner_radius=20, command=lambda: btnAppointment_Click(clinic_id))

    btnBack.grid(row=7, column=0, pady=20, padx=(20, 10), sticky="w")

    btnReject = CTkButton(master=framePatient, text="Reject", fg_color="red", font=("Inter", 20, "bold"),
                          corner_radius=20, command=lambda: reject_appointment(patient))
    btnReject.grid(row=7, column=1, pady=20, sticky="e")

    btnAccept = CTkButton(master=framePatient, text="Accept", fg_color="#5271FF", font=("Inter", 20, "bold"),
                          corner_radius=20, command=lambda: accept_appointment(patient))
    btnAccept.grid(row=7, column=2, pady=20, padx=(0, 20), sticky="e")

    framePatient.grid()


def update_doctor(patient, selected_doctor):
    # Update the doctor name and ID in the patient object
    parts = selected_doctor.rsplit(':', 1)  # Split the string into two parts based on the last occurrence of ':'
    doctor_name = parts[0].strip()  # Get the doctor's name
    doctor_id = parts[1].strip() if len(parts) > 1 else ''  # Get the doctor's ID, if available
    patient.set_doctor_name(doctor_name)
    patient.set_doctor_id(doctor_id)

    # Update Firestore with the new doctor information
    appointment_id = patient.get_appointment_id()
    db.collection('AppointmentDetails').document(appointment_id).update({
        'DoctorId': doctor_id,
        'DoctorName': doctor_name
    })

    # Reload and display the updated patient details
    reload_patient_details(appointment_id, patient.get_clinic_id(), patient.get_time())


def accept_appointment(patient):
    appointment_id = patient.get_appointment_id()
    clinic_id = patient.get_clinic_id()
    # Update the status of the appointment in Firestore
    update_appointment_status(appointment_id, "Accept")
    print("Accept")
    # Reload and display the updated patient details
    reload_patient_details(appointment_id, clinic_id, patient.get_time())


def reject_appointment(patient):
    appointment_id = patient.get_appointment_id()
    clinic_id = patient.get_clinic_id()
    # Update the status of the appointment in Firestore
    update_appointment_status(appointment_id, "Reject")
    print("Reject")
    # Reload and display the updated patient details
    reload_patient_details(appointment_id, clinic_id, patient.get_time())


def reload_patient_details(appointment_id, clinic_id, time_format):
    # Updated appointment details from Firestore
    appointment_doc = db.collection('AppointmentDetails').document(appointment_id).get()
    if appointment_doc.exists:
        appointment_data = appointment_doc.to_dict()
        appointment_data['AppointmentId'] = appointment_id

        # Extract the date and time from the appointment data
        appointment_date_time = appointment_data.get('Date', 'N/A')

        # Format the date and time using the existing format
        formatted_date, formatted_time = format_date_and_time(appointment_date_time)

        # Create a new Patient object with the updated data
        updated_patient = Patient(
            appointment_id,
            appointment_data.get('PatientId', 'N/A'),
            get_patient_name(appointment_data.get('PatientId', 'N/A')),
            appointment_data.get('DoctorId', 'N/A'),
            get_doctor_name(appointment_data.get('DoctorId', 'N/A')),
            appointment_data.get('AppointmentType', 'N/A'),
            formatted_date,  # Use the formatted date
            appointment_data.get('MedicalConcern', 'N/A'),
            appointment_data.get('MedicalDocs', 'N/A'),
            appointment_data.get('Prescription', 'N/A'),
            appointment_data.get('Status', 'N/A'),
            time_format,  # Use the provided time format
            appointment_data.get('PatientAddress', 'N/A')
        )

        # Set the clinic_id separately
        updated_patient.set_clinic_id(clinic_id)

        # Display the updated patient details
        patient_details(updated_patient, clinic_id)


def format_date(date_str):
    # Add logic to format date if needed
    return date_str


def format_time(date_str):
    # Add logic to format time if needed
    return date_str


def update_appointment_status(appointment_id, status):
    # Update the status in Firestore
    db.collection('AppointmentDetails').document(appointment_id).update({'Status': status})


# Function to get patient name from ID
def get_patient_name(patient_id):
    patient_doc = db.collection('Patients').document(patient_id).get()
    if patient_doc.exists:
        patient_data = patient_doc.to_dict()
        return patient_data.get('Name', 'N/A')
    else:
        return 'N/A'


# Function to get doctor name from ID
def get_doctor_name(doctor_id):
    if doctor_id == 'N/A':
        return '-'

    doctor_ref = db.collection('Doctors').document(doctor_id)
    doctor_doc = doctor_ref.get()

    if doctor_doc.exists:
        doctor_data = doctor_doc.to_dict()
        return doctor_data.get('Name', '-')
    else:
        return '-'


def generate_doctor_id():
    # Define the range of characters for the ID
    characters = string.ascii_letters + string.digits

    while True:
        # Generate a random ID with the specified format
        doctor_id = 'D-' + ''.join(random.choices(characters, k=6))

        # Check if this ID already exists in the database
        doctor_ref = db.collection('Doctors').document(doctor_id)
        if not doctor_ref.get().exists:
            return doctor_id


def btnDoctor_Click(clinic_id):
    print(f"Fetching doctors for clinic ID: {clinic_id}")
    doctors_ref = db.collection('Doctors').where('ClinicId', '==', clinic_id).where("RegisterApprovalStatus", "==",
                                                                                    "Approved")
    docs = doctors_ref.stream()

    doctor_data_list = []
    for doc in docs:
        doctor_details = doc.to_dict()
        doctor_details['DoctorId'] = doc.id
        doctor_data_list.append(doctor_details)

    # Add an empty doctor entry
    doctor_data_list.append({})

    for widget in frameDoctor.winfo_children():
        widget.destroy()

    frameDoctor.grid_columnconfigure(0, weight=1)
    frameDoctor.grid_columnconfigure(1, weight=1)
    frameDoctor.grid_columnconfigure(2, weight=1)

    rowIndex = 2
    colIndex = 0
    found_doctors = False

    for doctor_details in doctor_data_list[:-1]:  # Exclude the last empty entry
        found_doctors = True
        print(f"Doctor data: {doctor_details}")

        name = doctor_details.get('Name', 'N/A')
        email = doctor_details.get('Email', 'N/A')
        phone_no = doctor_details.get('PhoneNo', 'N/A')
        specialty = doctor_details.get('Specialty', 'N/A')
        language = doctor_details.get('Langauge', 'N/A')

        doctor_info = (
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Phone: {phone_no}\n"
            f"Specialty: {specialty}\n"
            f"Language: {language}\n"
        )

        lblDoctorInfo = CTkLabel(master=frameDoctor, text=doctor_info, width=150, height=100, corner_radius=10,
                                 fg_color="white", text_color="#5D5D5D", font=("Inter", 15), justify="left",
                                 anchor="nw")
        lblDoctorInfo.grid(row=rowIndex, column=colIndex, sticky="nsew", padx=10, pady=(0, 20))

        lblDoctorInfo.bind("<Button-1>", lambda event, data=doctor_details: doctor_details_click(data, clinic_id))

        colIndex += 1
        if colIndex >= 3:
            colIndex = 0
            rowIndex += 1

    # Check if the last entry is empty
    if doctor_data_list and not doctor_data_list[-1]:
        blank_label = CTkLabel(master=frameDoctor, text='', width=150, height=100, corner_radius=10,
                               fg_color="white", text_color="white", font=("Inter", 15), justify="left",
                               anchor="nw")
        blank_label.grid(row=rowIndex, column=colIndex, sticky="nsew", padx=10, pady=(0, 20))
        blank_label.bind("<Button-1>", lambda event: add_doctor(clinic_id))

    if not found_doctors:
        print("No doctors found for this clinic.")

    frameDoctor.grid()
    frameAppointment.grid_remove()
    framePatient.grid_remove()
    frameClinic.grid_remove()
    frameEditDoctor.grid_remove()


import threading


def add_doctor(clinic_Id):
    print("add new doctor")
    for widget in frameEditDoctor.winfo_children():
        widget.destroy()

    def get_unique_doctor_id():
        while True:
            doctor_id = generate_doctor_id()
            doctor_ref = db.collection('Doctors').document(doctor_id)
            if not doctor_ref.get().exists:
                return doctor_id

    # Generate a unique doctor ID
    entryDoctorId = get_unique_doctor_id()
    entryClinicId = clinic_Id
    entryRegisterStatus = "Pending"
    row_index = 0

    def create_label_and_entry(text, row):
        label = CTkLabel(master=frameEditDoctor, text=text, font=("Inter", 20), justify="left", anchor="w")
        label.grid(row=row, column=0, sticky="w", padx=20, pady=10)
        entry = CTkEntry(master=frameEditDoctor, width=300, height=30, font=("Inter", 20), border_width=0,
                         corner_radius=20)
        entry.grid(row=row, column=1, padx=20, pady=10)
        error_label = CTkLabel(master=frameEditDoctor, text="", font=("Inter", 15), justify="left", anchor="w",
                               text_color="red")
        error_label.grid(row=row, column=2, sticky="w", padx=10)
        return entry, error_label

    entryName, lblErrorName = create_label_and_entry("Name:", row_index)
    row_index += 1
    entryImage, lblErrorImage = create_label_and_entry("Image:", row_index)
    row_index += 1
    entryEmail, lblErrorEmail = create_label_and_entry("Email:", row_index)
    row_index += 1
    entryPhone, lblErrorPhone = create_label_and_entry("Phone No:", row_index)
    row_index += 1
    entryQualification, lblErrorQualification = create_label_and_entry("Qualification:", row_index)
    row_index += 1
    entryLanguage, lblErrorLanguage = create_label_and_entry("Language:", row_index)
    row_index += 1
    entryAddress, lblErrorAddress = create_label_and_entry("Address:", row_index)
    row_index += 1

    btnBack = CTkButton(master=frameEditDoctor, text="Back", fg_color="#5271FF", font=("Inter", 20, "bold"),
                        corner_radius=20, command=lambda: btnDoctor_Click(clinic_Id))
    btnBack.grid(row=row_index, column=0, pady=20, padx=(20, 10), sticky="w")

    btnSave = CTkButton(master=frameEditDoctor, text="Save", fg_color="#5271FF", font=("Inter", 20, "bold"),
                        corner_radius=20,
                        command=lambda: btnSaveNewDoctor_Click(entryDoctorId, entryClinicId, entryName, entryImage,
                                                               entryEmail, entryPhone, entryQualification,
                                                               entryLanguage, entryAddress, entryRegisterStatus,
                                                               lblErrorName, lblErrorImage, lblErrorEmail,
                                                               lblErrorPhone, lblErrorQualification, lblErrorLanguage,
                                                               lblErrorAddress))
    btnSave.grid(row=row_index, column=2, pady=20, padx=10, sticky='e')

    frameEditDoctor.grid()
    frameDoctor.grid_remove()
    frameEditClinic.grid_remove()
    frameAppointment.grid_remove()


def btnSaveNewDoctor_Click(doctor_id, clinic_id, entryName, entryImage, entryEmail, entryPhone,
                           entryQualification, entryLanguage, entryAddress, entryRegisterStatus,
                           lblErrorName, lblErrorImage, lblErrorEmail, lblErrorPhone,
                           lblErrorQualification, lblErrorLanguage, lblErrorAddress):
    # Collect data from entries
    name = entryName.get()
    image = entryImage.get()
    email = entryEmail.get()
    phone = entryPhone.get()
    qualification = entryQualification.get()
    language = entryLanguage.get()
    address = entryAddress.get()

    # Initialize error state
    has_error = False

    # Clear previous error messages
    lblErrorName.configure(text="")
    lblErrorImage.configure(text="")
    lblErrorEmail.configure(text="")
    lblErrorPhone.configure(text="")
    lblErrorQualification.configure(text="")
    lblErrorLanguage.configure(text="")
    lblErrorAddress.configure(text="")

    # Check for missing information
    if not name:
        lblErrorName.configure(text="Please enter doctor name.")
        has_error = True
    if not image:
        lblErrorImage.configure(text="Please upload the doctor image.")
        has_error = True
    if not email:
        lblErrorEmail.configure(text="Please enter doctor email.")
        has_error = True
    if not phone:
        lblErrorPhone.configure(text="Please enter doctor phone number")
        has_error = True
    if not qualification:
        lblErrorQualification.configure(text="Please enter doctor qualification.")
        has_error = True
    if not language:
        lblErrorLanguage.configure(text="Please enter doctor available language. ")
        has_error = True
    if not address:
        lblErrorAddress.configure(text="Please enter doctor home address.")
        has_error = True

    # If there is any error, return early
    if has_error:
        return

    doctor_data = {
        'DoctorId': doctor_id,
        'ClinicId': clinic_id,
        'Name': name,
        'Image': image,
        'Email': email,
        'PhoneNo': phone,
        'Qualification': qualification,
        'Langauge': language,
        'Address': address,
        'RegisterApprovalStatus': entryRegisterStatus
    }

    try:
        doctor_ref = db.collection('Doctors').document(doctor_id)
        doctor_ref.set(doctor_data)  # Create a new document with the generated doctor ID
        print(f"Doctor {doctor_id} added successfully.")
        messagebox.showinfo("Success", f"Doctor {name} has been added successfully.")
    except Exception as e:
        print(f"Error saving doctor: {e}")
        messagebox.showerror("Error", f"Failed to save doctor. Error: {e}")


def doctor_details_click(doctor_data, clinic_id):
    print("Doctor information has been clicked.")

    global selected_clinic_id
    selected_clinic_id = clinic_id

    for widget in frameDoctor.winfo_children():
        widget.destroy()

    doctor_id = doctor_data.get('DoctorId')
    print(f"Doctor ID: {doctor_id}")
    address = doctor_data.get('Address', 'N/A')
    email = doctor_data.get('Email', 'N/A')
    image = doctor_data.get('Image', 'N/A')
    language = doctor_data.get('Langauge', 'N/A')
    name = doctor_data.get('Name', 'N/A')
    phone_no = doctor_data.get('PhoneNo', 'N/A')
    qualification = doctor_data.get('Qualification', 'N/A')
    register_status = doctor_data.get('RegisterApprovalStatus', 'N/A')
    specialty = doctor_data.get('Specialty', 'N/A')

    doctor_info = (
        f"{image}\n"
        f"Doctor ID: {doctor_id}\n"
        f"Name: {name}\n"
        f"Email: {email}\n"
        f"Phone: {phone_no}\n"
        f"Specialty: {specialty}\n"
        f"Qualification: {qualification}\n"
        f"Register Status: {register_status}\n"
        f"Language: {language}\n"
        f"Address: {address}\n"
    )

    lblDoctorDetails = CTkLabel(master=frameDoctor, text=doctor_info, width=100, height=0, corner_radius=0,
                                text_color="Black", font=("Inter", 20), justify="left", anchor="w")
    lblDoctorDetails.grid(row=0, column=0, padx=20, pady=20, sticky="enw")

    btnBack = CTkButton(master=frameDoctor, text="Back", fg_color="#5271FF", font=("Inter", 20, "bold"),
                        corner_radius=20, command=lambda: btnDoctor_Click(clinic_id))
    btnBack.grid(row=1, column=0, pady=20, padx=(20, 10), sticky="w")

    doctor = Doctors(doctor_id, address, clinic_id, email, image, language, name, phone_no, qualification,
                     register_status, specialty)

    btnEdit = CTkButton(master=frameDoctor, text="Edit", fg_color="#5271FF", font=("Inter", 20, "bold"),
                        corner_radius=20, command=lambda: DoctorEdit(doctor, doctor_data, doctor_id, clinic_id))
    btnEdit.grid(row=1, column=1, pady=20, padx=(20, 10), sticky="e")
    frameDoctor.grid()
    frameEditDoctor.grid_remove()
    frameEditClinic.grid_remove()
    frameAppointment.grid_remove()
    frameClinic.grid_remove()
    framePatient.grid_remove()


def DoctorEdit(doctor, doctor_data, doctor_id, clinic_id):
    print("Edit doctor information")
    frameEditDoctor.grid()

    for widget in frameEditDoctor.winfo_children():
        widget.destroy()

    row_index = 0

    lblDoctorId = CTkLabel(master=frameEditDoctor, text="ID:", font=("Inter", 20), justify="left", anchor="w")
    lblDoctorId.grid(row=row_index, column=0, sticky="w", padx=20, pady=10)
    lblDoctorId = CTkLabel(master=frameEditDoctor, width=300, height=30, font=("Inter", 20),
                           text=doctor.get_doctor_id())
    lblDoctorId.grid(row=row_index, column=1, padx=20, pady=10)

    row_index += 1

    lblName = CTkLabel(master=frameEditDoctor, text="Name:", font=("Inter", 20), justify="left", anchor="w")
    lblName.grid(row=row_index, column=0, sticky="w", padx=20, pady=10)
    entryName = CTkEntry(master=frameEditDoctor, width=300, height=30, font=("Inter", 20), border_width=0,
                         corner_radius=20)
    entryName.insert(0, doctor.get_name())
    entryName.bind("<FocusIn>", clear_entry)
    entryName.grid(row=row_index, column=1, padx=20, pady=10)

    row_index += 1

    lblImage = CTkLabel(master=frameEditDoctor, text="Image:", font=("Inter", 20), justify="left", anchor="w")
    lblImage.grid(row=row_index, column=0, sticky="w", padx=20, pady=10)
    entryImage = CTkEntry(master=frameEditDoctor, width=300, height=30, font=("Inter", 20), border_width=0,
                          corner_radius=20)
    entryImage.insert(0, doctor.get_image())
    entryImage.bind("<FocusIn>", clear_entry)
    entryImage.grid(row=row_index, column=1, padx=20, pady=10)

    row_index += 1

    lblEmail = CTkLabel(master=frameEditDoctor, text="Email:", font=("Inter", 20), justify="left", anchor="w")
    lblEmail.grid(row=row_index, column=0, sticky="w", padx=20, pady=10)
    entryEmail = CTkEntry(master=frameEditDoctor, width=300, height=30, font=("Inter", 20), border_width=0,
                          corner_radius=20)
    entryEmail.insert(0, doctor.get_email())
    entryEmail.bind("<FocusIn>", clear_entry)
    entryEmail.grid(row=row_index, column=1, padx=20, pady=10)

    row_index += 1

    lblPhone = CTkLabel(master=frameEditDoctor, text="Phone No:", font=("Inter", 20), justify="left", anchor="w")
    lblPhone.grid(row=row_index, column=0, sticky="w", padx=20, pady=10)
    entryPhone = CTkEntry(master=frameEditDoctor, width=300, height=30, font=("Inter", 20), border_width=0,
                          corner_radius=20)
    entryPhone.insert(0, doctor.get_phone_no())
    entryPhone.bind("<FocusIn>", clear_entry)
    entryPhone.grid(row=row_index, column=1, padx=20, pady=10)

    row_index += 1

    lblQualification = CTkLabel(master=frameEditDoctor, text="Qualification:", font=("Inter", 20), justify="left",
                                anchor="w")
    lblQualification.grid(row=row_index, column=0, sticky="w", padx=20, pady=10)
    entryQualification = CTkEntry(master=frameEditDoctor, width=300, height=30, font=("Inter", 20), border_width=0,
                                  corner_radius=20)
    entryQualification.insert(0, doctor.get_qualification())
    entryQualification.bind("<FocusIn>", clear_entry)
    entryQualification.grid(row=row_index, column=1, padx=20, pady=10)

    row_index += 1

    lblLanguage = CTkLabel(master=frameEditDoctor, text="Language:", font=("Inter", 20), justify="left", anchor="w")
    lblLanguage.grid(row=row_index, column=0, sticky="w", padx=20, pady=10)
    entryLanguage = CTkEntry(master=frameEditDoctor, width=300, height=30, font=("Inter", 20), border_width=0,
                             corner_radius=20)
    entryLanguage.insert(0, doctor.get_language())
    entryLanguage.bind("<FocusIn>", clear_entry)
    entryLanguage.grid(row=row_index, column=1, padx=20, pady=10)

    row_index += 1

    lblAddress = CTkLabel(master=frameEditDoctor, text="Address:", font=("Inter", 20), justify="left", anchor="w")
    lblAddress.grid(row=row_index, column=0, sticky="w", padx=20, pady=10)
    entryAddress = CTkEntry(master=frameEditDoctor, width=300, height=30, font=("Inter", 20), border_width=0,
                            corner_radius=20)
    entryAddress.insert(0, doctor.get_address())
    entryAddress.bind("<FocusIn>", clear_entry)
    entryAddress.grid(row=row_index, column=1, padx=20, pady=10)

    row_index += 1

    lblSpecialty = CTkLabel(master=frameEditDoctor, text="Specialty:", font=("Inter", 20), justify="left", anchor="w")
    lblSpecialty.grid(row=row_index, column=0, sticky="w", padx=20, pady=10)
    entrySpecialty = CTkEntry(master=frameEditDoctor, width=300, height=30, font=("Inter", 20), border_width=0,
                              corner_radius=20)
    entrySpecialty.insert(0, doctor.get_specialty())
    entrySpecialty.bind("<FocusIn>", clear_entry)
    entrySpecialty.grid(row=row_index, column=1, padx=20, pady=10)

    row_index += 1

    # Create a new frame for the buttons
    button_frame = CTkFrame(master=frameEditDoctor)
    button_frame.grid(row=row_index, column=0, columnspan=2, pady=20, padx=20, sticky="ew")

    # Configure the grid for the button_frame
    button_frame.grid_columnconfigure((0, 1, 2), weight=1)

    btnBack = CTkButton(master=button_frame, text="Back", fg_color="#5271FF", font=("Inter", 20, "bold"),
                        corner_radius=20, command=lambda: doctor_details_click(doctor_data, clinic_id))
    btnBack.grid(row=0, column=0, padx=10, sticky="w")

    btnDelete = CTkButton(master=button_frame, text="Delete", fg_color="red", font=("Inter", 20, "bold"),
                          corner_radius=20, command=lambda: btnDeleteDoctor_Click(doctor_id))
    btnDelete.grid(row=0, column=1, padx=10, sticky="e")

    btnSave = CTkButton(master=button_frame, text="Save", fg_color="#5271FF", font=("Inter", 20, "bold"),
                        corner_radius=20,
                        command=lambda: btnSaveDoctor_Click(doctor_id, entryName, entryImage, entryEmail, entryPhone,
                                                            entryQualification, entryLanguage, entryAddress,
                                                            entrySpecialty))
    btnSave.grid(row=0, column=2, padx=10, sticky="e")

    frameDoctor.grid_remove()
    frameAppointment.grid_remove()
    frameEditClinic.grid_remove()


def btnSaveDoctor_Click(doctor_id, entryName, entryImage, entryEmail, entryPhone, entryQualification, entryLanguage,
                        entryAddress, entrySpecialty):
    print("Update doctor information")

    updated_data = {
        'Name': entryName.get(),
        'Image': entryImage.get(),
        'Email': entryEmail.get(),
        'PhoneNo': entryPhone.get(),
        'Qualification': entryQualification.get(),
        'Langauge': entryLanguage.get(),
        'Address': entryAddress.get(),
        'Specialty': entrySpecialty.get()
    }

    doctor_ref = db.collection('Doctors').document(doctor_id)
    doctor_ref.update(updated_data)
    print(f"Doctor {doctor_id} updated successfully.")

    # Display the update confirmation popup
    messagebox.showinfo("Update Successful", "Doctor information has been updated successfully.")

    # Relocate to btnDoctor_Click and display frameDoctor
    btnDoctor_Click(selected_clinic_id)


def btnDeleteDoctor_Click(doctor_id):
    # Display a warning box to confirm deletion
    confirmation = messagebox.askokcancel("Confirmation", "Are you sure you want to delete this doctor's information?")

    if confirmation:
        # User clicked 'OK', proceed with deletion
        doctor_ref = db.collection('Doctors').document(doctor_id)
        doctor_ref.delete()
        print(f"Doctor {doctor_id} deleted successfully.")
        btnDoctor_Click(selected_clinic_id)
        # Optionally, you can navigate back to the list of doctors or perform any other action you need after deleting
    else:
        # User clicked 'Cancel', navigate back to the list of doctors
        btnDoctor_Click(selected_clinic_id)


def clear_entry(event):
    event.widget.delete(0, "end")


def btnClinic_Click(clinic_id):
    global selected_clinic_id
    selected_clinic_id = clinic_id  # Store the clinic_id in a global variable
    print("Clinic Button Clicked")

    frameClinic.grid()  # Display the clinic frame
    frameDoctor.grid_remove()  # Hide the doctor frame
    frameAppointment.grid_remove()  # Hide the appointment frame if it is shown
    framePatient.grid_remove()
    frameEditDoctor.grid_remove()

    # Clear existing widgets in frameClinic
    for widget in frameClinic.winfo_children():
        widget.destroy()

    try:
        clinic_doc = db.collection('Clinics').document(clinic_id).get()
        if clinic_doc.exists:
            clinic_data = clinic_doc.to_dict()

            # Create a Clinic object with the retrieved data
            clinic = Clinic(
                clinic_id,
                clinic_data.get('Name', 'N/A'),
                clinic_data.get('Image', 'N/A'),
                clinic_data.get('Address', 'N/A'),
                clinic_data.get('Email', 'N/A'),
                clinic_data.get('PhoneNo', 'N/A'),
                clinic_data.get('Specialty', 'N/A'),
                clinic_data.get('WorkDays', 'N/A'),
                clinic_data.get('StartHours', 'N/A'),
                clinic_data.get('EndHours', 'N/A'),
                clinic_data.get('StartBreak', 'N/A'),
                clinic_data.get('EndBreak', 'N/A'),
                clinic_data.get('Description', 'N/A')
            )

            # Configure grid to make it responsive
            for i in range(6):
                frameClinic.grid_columnconfigure(i, weight=1)

            row_index = 0

            # Fetch data from Firestore where AppStatus is 'Approved'
            clinics_ref = db.collection('Clinics').where('AppStatus', '==', 'Approved')
            docs = clinics_ref.stream()

            # Prepare the data
            clinic_data_list = []
            for doc in docs:
                clinic_dict = doc.to_dict()
                clinic_dict['clinicId'] = doc.id
                clinic_data_list.append(clinic_dict)

            row_index = 2

            # Fetch the Firebase Storage bucket
            bucket = storage.bucket()

            # Display each clinic data
            for clinic_info in clinic_data_list:
                clinic_id = clinic_info['clinicId']

                # Fetch image from Firestore
                img_clinic_list = clinic_info.get('Image')
                blob = bucket.blob(img_clinic_list)
                if blob.exists():
                    arr = np.frombuffer(blob.download_as_string(), np.uint8)
                    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)

                    # Convert the numpy array to a PIL Image object
                    pil_img_clinic_list = Image.fromarray(img)
                    ctk_img_clinic_list = CTkImage(pil_img_clinic_list, size=(220, 150))
                else:
                    ctk_img_clinic_list = None

                lbl_clinic_image = CTkLabel(
                    master=frameClinic, text="", image=ctk_img_clinic_list,
                    bg_color="transparent", width=220, height=150
                )
                lbl_clinic_image.grid(row=row_index, column=0, columnspan=6, sticky="ew", padx=10, pady=0)

            clinic_info = (
                f"Name: {clinic.get_name()}\n"
                f"Clinic user ID: {clinic.get_clinic_Id()}\n"
                f"Specialty: {clinic.get_specialty()}\n"
                f"Phone number: {clinic.get_phone_no()}\n"
                f"Email address: {clinic.get_email()}\n"
                f"Address: {clinic.get_address()}\n"
                f"Description: {clinic.get_description()}"
            )
            row_index += 1

            btn_edit = CTkButton(
                master=frameClinic, text="Edit", fg_color="#5271FF", font=("Inter", 20, "bold"),
                corner_radius=20, width=150,  # Reduced width
                command=btnEditClinic_Click
            )
            btn_edit.grid(row=row_index, column=2, columnspan=2, pady=20,
                          sticky="ew")  # Adjusted column and span to center the button

            row_index += 1

            lbl_clinics = CTkLabel(
                master=frameClinic, text=clinic_info, width=550, height=0, corner_radius=0,
                fg_color="#DCC6FF", text_color="#5D5D5D", font=("Inter", 20), justify="left", anchor="w"
            )
            lbl_clinics.grid(row=row_index, column=0, columnspan=6, sticky="ew", padx=10, pady=0)

            row_index += 1

            # Extracting and formatting the working hours
            work_days = clinic.get_work_days().split(", ")
            start_hours = clinic.get_start_hours().split(", ")
            end_hours = clinic.get_end_hours().split(", ")
            start_breaks = clinic.get_start_break_hours().split(", ")
            end_breaks = clinic.get_end_break_hours().split(", ")

            # Adding headers
            headers = ["Day", "Start Hour", "End Hour", "Break Start", "Break End"]
            for col_index, header in enumerate(headers):
                header_label = CTkLabel(
                    master=frameClinic, text=header, width=100, height=0, corner_radius=0,
                    fg_color="#5271FF", text_color="white", font=("Inter", 15), justify="center"
                )
                header_label.grid(row=row_index, column=col_index, padx=5, pady=5, sticky="ew")

            row_index += 1

            # Display working hours information
            for i in range(len(work_days)):
                day_label = CTkLabel(
                    master=frameClinic, text=work_days[i], width=100, height=0, corner_radius=0,
                    fg_color="#DCC6FF", text_color="#5D5D5D", font=("Inter", 15), justify="center"
                )
                day_label.grid(row=row_index, column=0, padx=5, pady=5, sticky="ew")

                start_hour_label = CTkLabel(
                    master=frameClinic, text=start_hours[i], width=100, height=0, corner_radius=0,
                    fg_color="#DCC6FF", text_color="#5D5D5D", font=("Inter", 15), justify="center"
                )
                start_hour_label.grid(row=row_index, column=1, padx=5, pady=5, sticky="ew")

                end_hour_label = CTkLabel(
                    master=frameClinic, text=end_hours[i], width=100, height=0, corner_radius=0,
                    fg_color="#DCC6FF", text_color="#5D5D5D", font=("Inter", 15), justify="center"
                )
                end_hour_label.grid(row=row_index, column=2, padx=5, pady=5, sticky="ew")

                start_break_label = CTkLabel(
                    master=frameClinic, text=start_breaks[i], width=100, height=0, corner_radius=0,
                    fg_color="#DCC6FF", text_color="#5D5D5D", font=("Inter", 15), justify="center"
                )
                start_break_label.grid(row=row_index, column=3, padx=5, pady=5, sticky="ew")

                end_break_label = CTkLabel(
                    master=frameClinic, text=end_breaks[i], width=100, height=0, corner_radius=0,
                    fg_color="#DCC6FF", text_color="#5D5D5D", font=("Inter", 15), justify="center"
                )
                end_break_label.grid(row=row_index, column=4, padx=5, pady=5, sticky="ew")

                row_index += 1

            # Ensure the parent frame has proper configuration to center its content
            frameHome.grid_columnconfigure(0, weight=1)
        else:
            print(f"No document found for clinic_id: {clinic_id}")
    except Exception as e:
        print(f"Error fetching clinic data: {e}")


def btnEditClinic_Click():
    global selected_clinic_id
    print(f"Edit Clinic Button Clicked for clinic_id: {selected_clinic_id}")

    frameClinic.grid()  # Display the clinic frame
    frameDoctor.grid_remove()  # Hide the doctor frame
    frameAppointment.grid_remove()  # Hide the appointment frame if it is shown
    frameEditDoctor.grid_remove()

    for widget in frameClinic.winfo_children():
        widget.destroy()

    clinic_doc = db.collection('Clinics').document(selected_clinic_id).get()
    if clinic_doc.exists:
        clinic_data = clinic_doc.to_dict()

        # Create a Clinic object with the retrieved data
        clinic = Clinic(
            selected_clinic_id,
            clinic_data.get('Name', 'N/A'),
            clinic_data.get('Image', 'N/A'),
            clinic_data.get('Address', 'N/A'),
            clinic_data.get('Email', 'N/A'),
            clinic_data.get('PhoneNo', 'N/A'),
            clinic_data.get('Specialty', 'N/A'),
            clinic_data.get('WorkDays', 'N/A'),
            clinic_data.get('StartHours', 'N/A'),
            clinic_data.get('EndHours', 'N/A'),
            clinic_data.get('StartBreak', 'N/A'),
            clinic_data.get('EndBreak', 'N/A'),
            clinic_data.get('Description', 'N/A')
        )

        row_index = 0

        def add_label_entry(row, text, value):
            label = CTkLabel(master=frameClinic, text=text, font=("Inter", 20), justify="left", anchor="w")
            label.grid(row=row, column=0, sticky="w", padx=20, pady=10)
            entry = CTkEntry(master=frameClinic, width=300, height=30, font=("Inter", 20))
            entry.insert(0, value)
            entry.bind("<FocusIn>", clear_entry)
            entry.grid(row=row, column=1, padx=20, pady=10)
            return entry

        entryName = add_label_entry(row_index, "Name:", clinic.get_name())
        row_index += 1
        entryImage = add_label_entry(row_index, "Image:", clinic.get_image())
        row_index += 1
        entryAddress = add_label_entry(row_index, "Address:", clinic.get_address())
        row_index += 1
        entryEmail = add_label_entry(row_index, "Email address:", clinic.get_email())
        row_index += 1
        entryPhone = add_label_entry(row_index, "Phone number:", clinic.get_phone_no())
        row_index += 1
        entrySpecialty = add_label_entry(row_index, "Specialty:", clinic.get_specialty())
        row_index += 1
        entryDescription = add_label_entry(row_index, "Description:", clinic.get_description())
        row_index += 1

        frameTimeTable.grid()
        # Adding the table headers
        headers = ["Day", "Include", "Start Work Hour", "End Work Hour", "Start Break Hour", "End Break Hour"]
        for col_index, header in enumerate(headers):
            header_label = CTkLabel(
                master=frameTimeTable, text=header, width=100, height=0, corner_radius=0,
                fg_color="#5271FF", text_color="white", font=("Inter", 15), justify="center"
            )
            header_label.grid(row=row_index, column=col_index, padx=5, pady=5, sticky="ew")

        row_index += 1

        workdays_abbrev = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        work_days = clinic.get_work_days().split(", ")
        start_hours = clinic.get_start_hours().split(", ")
        end_hours = clinic.get_end_hours().split(", ")
        start_breaks = clinic.get_start_break_hours().split(", ")
        end_breaks = clinic.get_end_break_hours().split(", ")

        # Generate time options for drop-down menus
        time_options = ['time'] + [f"{hour:02d}:{minute:02d}" for hour in range(24) for minute in (0, 30)]

        # Displaying the table rows for each workday
        workdays_vars = {}
        for i, day in enumerate(workdays_abbrev):
            var = IntVar(value=1 if day in work_days else 0)
            workdays_vars[day] = var

            def toggle_entries(var, *entries):
                def callback():
                    state = 'normal' if var.get() == 1 else 'disabled'
                    for entry in entries:
                        entry.configure(state=state)

                return callback

            lbl = CTkLabel(master=frameClinic, text=day, font=("Inter", 15))
            lbl.grid(row=row_index, column=0, padx=5, pady=5, sticky="ew")

            chk_day = Checkbutton(master=frameClinic, variable=var)
            chk_day.grid(row=row_index, column=1, padx=5, pady=5, sticky="ew")

            # Drop-down menus for start and end working hours
            start_work_hour = CTkOptionMenu(
                master=frameClinic, values=time_options, state='normal' if var.get() == 1 else 'disabled'
            )
            start_work_hour.set(start_hours[i] if var.get() == 1 else "time")
            start_work_hour.grid(row=row_index, column=2, padx=5, pady=5, sticky="ew")

            end_work_hour = CTkOptionMenu(
                master=frameClinic, values=time_options, state='normal' if var.get() == 1 else 'disabled'
            )
            end_work_hour.set(end_hours[i] if var.get() == 1 else "time")
            end_work_hour.grid(row=row_index, column=3, padx=5, pady=5, sticky="ew")

            start_break_hour = CTkOptionMenu(
                master=frameClinic, values=time_options, state='normal' if var.get() == 1 else 'disabled'
            )
            start_break_hour.set(start_breaks[i] if var.get() == 1 else "time")
            start_break_hour.grid(row=row_index, column=4, padx=5, pady=5, sticky="ew")

            end_break_hour = CTkOptionMenu(
                master=frameClinic, values=time_options, state='normal' if var.get() == 1 else 'disabled'
            )
            end_break_hour.set(end_breaks[i] if var.get() == 1 else "time")
            end_break_hour.grid(row=row_index, column=5, padx=5, pady=5, sticky="ew")

            chk_day.configure(
                command=toggle_entries(var, start_work_hour, end_work_hour, start_break_hour, end_break_hour))

            row_index += 1

        # Adding the Back and Save buttons
        btnBack = CTkButton(master=frameClinic, text="Back", fg_color="#5271FF", font=("Inter", 20, "bold"),
                            corner_radius=20, command=lambda: btnClinic_Click(selected_clinic_id))
        btnBack.grid(row=row_index, column=0, pady=20)

        btnSave = CTkButton(master=frameClinic, text="Save", fg_color="#5271FF", font=("Inter", 20, "bold"),
                            corner_radius=20, command=lambda: btnSaveClinic_Click(clinic, workdays_vars))
        btnSave.grid(row=row_index, column=1, pady=20, sticky='e')
    else:
        print(f"No document found for clinic_id: {selected_clinic_id}")


# Function to save the edited clinic data
def btnSaveClinic_Click(entryName, entryImage, entryAddress, entryEmail, entryPhone, entrySpecialty, workdays_vars,
                        work_hours_entries, break_hours_entries, entryDescription):
    global selected_clinic_id

    # Collect the updated data from the entries and checkboxes
    updated_data = {
        'Name': entryName.get(),
        'Image': entryImage.get(),
        'Address': entryAddress.get(),
        'Email': entryEmail.get(),
        'PhoneNo': entryPhone.get(),
        'Specialty': entrySpecialty.get(),
        'Description': entryDescription.get(),
        'WorkDays': ', '.join([day for day, var in workdays_vars.items() if var.get() == 1]),
        'StartHours': ', '.join(
            [', '.join([entry[0].get() for entry in work_hours_entries[day]]) for day in workdays_vars.keys() if
             workdays_vars[day].get() == 1]),
        'EndHours': ', '.join(
            [', '.join([entry[1].get() for entry in work_hours_entries[day]]) for day in workdays_vars.keys() if
             workdays_vars[day].get() == 1]),
        'StartBreak': ', '.join(
            [', '.join([entry[0].get() for entry in break_hours_entries[day]]) for day in workdays_vars.keys() if
             workdays_vars[day].get() == 1]),
        'EndBreak': ', '.join(
            [', '.join([entry[1].get() for entry in break_hours_entries[day]]) for day in workdays_vars.keys() if
             workdays_vars[day].get() == 1])
    }

    # Update the clinic document in the database
    db.collection('Clinics').document(selected_clinic_id).update(updated_data)
    print("Clinic data saved successfully")

    # Clear existing widgets in the clinic frame
    for widget in frameClinic.winfo_children():
        widget.destroy()

    # Call the btnClinic_Click function to display the updated information
    btnClinic_Click(selected_clinic_id)


# Assuming this is the last part of your script, you can pack the initial frame
frameHome.pack(fill="both", expand=True)

ClinicId = 'C-wTrXvY'
# Side Navigation Bar
imgBtnMenu = Image.open("C:/Users/michi/PycharmProjects/DCS2103_Aug2023/SE Project/Images/menu.png")
btnMenu = CTkButton(master=frameSideNav, text="", image=CTkImage(imgBtnMenu, size=(45, 35)),
                    fg_color="transparent", command=btnMenu_Click)
btnMenu.place(relx=0.5, rely=0.06, anchor="center")

# Create a frame for the toolbar and the label
toolbar_label_frame = CTkFrame(master=frameHome, fg_color="transparent")
toolbar_label_frame.grid(row=1, column=0, sticky="ew")
toolbar_label_frame.grid_columnconfigure(0, weight=1)
# Create a frame to hold the label and button
navBtnFrame = CTkFrame(master=toolbar_label_frame, fg_color="transparent")
navBtnFrame.grid(row=0, column=1, padx=(5, 0), pady=0)


imgBtnHome = Image.open("C:/Users/michi/PycharmProjects/DCS2103_Aug2023/SE Project/Images/home-icon-white.png")
btnHome = CTkButton(master=frameSideNav, text="", image=CTkImage(imgBtnHome, size=(50, 50)),
                    fg_color="transparent", command=btnHome_Click)
btnHome.place(relx=0.5, rely=0.3, anchor="center")

imgBtnBookHis = Image.open("C:/Users/michi/PycharmProjects/DCS2103_Aug2023/SE Project/Images/booking-history-white.png")
BtnBookHis = CTkButton(master=frameSideNav, text="", image=CTkImage(imgBtnBookHis, size=(60, 60)),
                       fg_color="transparent", command=btnBookHis_Click)
BtnBookHis.place(relx=0.5, rely=0.5, anchor="center")

# Logo
imgHomeLogo = Image.open("C:/Users/michi/PycharmProjects/DCS2103_Aug2023/SE Project/Images/logo.png")
lblHomeLogo = CTkLabel(master=frameHome, text="", bg_color="white", image=CTkImage(imgHomeLogo, size=(453, 198)))
lblHomeLogo.grid(row=0, column=0, sticky="ewn")

# Clinic View Label with blue background
lblClinicView = CTkLabel(master=toolbar_label_frame, text="Clinic View", font=("Inter", 30), text_color="black")
lblClinicView.grid(row=0, column=0, sticky="w", pady=(0, 5), padx=(0, 0))

# Adding the Navigation Toolbar inside the toolbar_label_frame
# Create a label for the image inside the frame
imgBtnSchedule = Image.open("C:/Users/michi/PycharmProjects/DCS2103_Aug2023/SE Project/Images/schedule-2.png")

# Create the button inside the frame
# Create the button with the image and label

navBtnAppointment = CTkButton(master=navBtnFrame, text="Appointments", text_color="Black",
                              command=lambda: btnAppointment_Click(ClinicId),
                              image=CTkImage(imgBtnSchedule, size=(40, 40)),
                              fg_color="#FFF9BE", font=("Inter", 20), width=50, height=50, corner_radius=0)

# Place the button in the toolbar
navBtnAppointment.grid(row=0, column=1, padx=0, pady=0)

imgBtnDoctor = Image.open("C:/Users/michi/PycharmProjects/DCS2103_Aug2023/SE Project/Images/doctor.png")

# Create the button inside the frame
navBtnDoctor = CTkButton(master=toolbar_label_frame, text="Doctors", text_color="Black",
                         image=CTkImage(imgBtnDoctor, size=(30, 30)),
                         command=lambda: btnDoctor_Click('C-nh6tvr'),
                         fg_color="#C8FFD4", font=("Inter", 20), width=50, height=50, corner_radius=0)

# Place the button in the toolbar
navBtnDoctor.grid(row=0, column=2, padx=0, pady=0)

# Create the button with the image and label

# Add the image to the button
imgBtnClinic = Image.open("C:/Users/michi/PycharmProjects/DCS2103_Aug2023/SE Project/Images/hospital.png")

# Create the button with the image and label
navBtnClinic = CTkButton(master=toolbar_label_frame, text="Clinic Settings", text_color="Black",
                         command=lambda: btnClinic_Click('C-wTrXvY'),  # Use lambda to pass the parameter
                         image=CTkImage(imgBtnClinic, size=(30, 30)),
                         fg_color="#DCC6FF", font=("Inter", 20), width=50, height=50, corner_radius=0)

# Place the button in the toolbar
navBtnClinic.grid(row=0, column=3, padx=0, pady=0)

# Create a large frame below the navigation bar
frameAppointment = CTkScrollableFrame(master=frameHome, fg_color="#FFF9BE", )  # Adjust color as needed
frameAppointment.grid(row=2, column=0, sticky="nsew", pady=0)  # Use sticky="nsew" to fill height and width

framePatient = CTkScrollableFrame(master=frameHome, fg_color="#FFF9BE", )  # Adjust color as needed
framePatient.grid(row=2, column=0, sticky="nsew", pady=0)  # Use sticky="nsew" to fill height and width

frameDoctor = CTkScrollableFrame(master=frameHome, fg_color="#C8FFD4", height=900)  # Adjust color as needed
frameDoctor.grid(row=2, column=0, sticky="sew", pady=0)  # Fill the remaining space in the frame
frameDoctor.grid_remove()

frameEditDoctor = CTkScrollableFrame(master=frameHome, fg_color="#C8FFD4", height=900)  # Adjust color as needed
frameEditDoctor.grid(row=2, column=0, sticky="sew", pady=0)  # Fill the remaining space in the frame
frameEditDoctor.grid_remove()

frameClinic = CTkScrollableFrame(master=frameHome, width=800, fg_color="#DCC6FF")  # Adjust color as needed
frameClinic.grid(row=2, column=0, sticky="nsew")
frameClinic.grid_remove()  # Fill the remaining space in the frame

frameEditClinic = CTkScrollableFrame(master=frameHome, fg_color="#DCC6FF")
frameEditClinic.grid(row=2, column=0, sticky="nsew")
frameEditClinic.grid_remove()

frameTimeTable = CTkScrollableFrame(master=frameEditClinic, fg_color="transparent")
frameTimeTable.grid(row=2, column=0, sticky="nsew")
frameTimeTable.grid_remove()

btnAppointment_Click(ClinicId)
document_name = "CAD DB"
sheet_name = "AppointmentDetails"

# Ensure the main frame is properly expanded
frameHome.grid_rowconfigure(2, weight=1)
frameHome.grid_columnconfigure(0, weight=1)
# Configure row and column weights to allow children to expand
frameAppointment.grid_rowconfigure(0, weight=1)
frameAppointment.grid_columnconfigure(2, weight=1)

framePatient.grid_rowconfigure(0, weight=1)
framePatient.grid_columnconfigure(2, weight=1)

frameDoctor.grid_rowconfigure(0, weight=1)
frameDoctor.grid_columnconfigure(0, weight=1)

frameClinic.grid_columnconfigure(0, weight=1)
frameClinic.grid_columnconfigure(1, weight=1)

frameEditClinic.grid_rowconfigure(0, weight=1)
frameEditClinic.grid_columnconfigure(0, weight=1)

# Run the application
app.mainloop()
