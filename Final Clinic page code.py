import smtplib
from email.message import EmailMessage
from io import BytesIO

from customtkinter import *
import firebase_admin
from firebase_admin import firestore
from tkinter import *
from firebase_admin import credentials, storage
import random
import string
from PIL import ImageDraw
from customtkinter import CTkImage
from PIL import Image, ImageTk
import numpy as np
import cv2
from tkinter import messagebox
import pytz
from datetime import datetime


class Appointment:
    def __init__(self, appointment_id, appointment_type, clinic_id, date_time, date, time, clinic_name, doctor_id,
                 doctor_name,
                 medical_concern, medical_doc, patient_address, patient_id, patient_name, patient_phone, prescription,
                 status):
        self.__appointment_id = appointment_id
        self.__appointment_type = appointment_type
        self.__clinic_id = clinic_id
        self.__date_time = date_time
        self.__date = date
        self.__time = time
        self.__clinic_name = clinic_name
        self.__doctor_id = doctor_id
        self.__doctor_name = doctor_name
        self.__medical_concern = medical_concern
        self.__medical_doc = medical_doc
        self.__patient_address = patient_address
        self.__patient_id = patient_id
        self.__patient_name = patient_name
        self.__patient_phone = patient_phone
        self.__prescription = prescription
        self.__status = status

    def get_appointment_id(self):
        return self.__appointment_id

    def get_appointment_type(self):
        return self.__appointment_type

    def get_clinic_id(self):
        return self.__clinic_id

    def get_date_time(self):
        return self.__date_time

    def get_date(self):
        return self.__date

    def get_time(self):
        return self.__time

    def get_clinic_name(self):
        return self.__clinic_name

    def get_doctor_id(self):
        return self.__doctor_id

    def get_doctor_name(self):
        return self.__doctor_name

    def get_medical_concern(self):
        return self.__medical_concern

    def get_medical_doc(self):
        return self.__medical_doc

    def get_patient_address(self):
        return self.__patient_address

    def get_patient_id(self):
        return self.__patient_id

    def get_patient_name(self):
        return self.__patient_name

    def get_patient_phone(self):
        return self.__patient_phone

    def get_prescription(self):
        return self.__prescription

    def get_status(self):
        return self.__status

    def set_clinic_id(self, clinic_id):
        self.__clinic_id = clinic_id

    def set_patient_phone(self, patient_phone):
        self.__patient_phone = patient_phone

    def set_appointment_id(self, appointment_id):
        self.__appointment_id = appointment_id

    def set_patient_id(self, patient_id):
        self.__patient_id = patient_id

    def set_patient_name(self, patient_name):
        self.__patient_name = patient_name

    def set_clinic_name(self, clinic_name):
        self.__clinic_name = clinic_name

    def set_doctor_id(self, doctor_id):
        self.__doctor_id = doctor_id

    def set_doctor_name(self, doctor_name):
        self.__doctor_name = doctor_name

    def set_appointment_type(self, appointment_type):
        self.__appointment_type = appointment_type

    def set_date_time(self, date_time):
        self.__date_time = date_time

    def set_date(self, date):
        self.__date = date

    def set_time(self, time):
        self.__time = time

    def set_medical_concern(self, medical_concern):
        self.__medical_concern = medical_concern

    def set_medical_doc(self, medical_doc):
        self.__medical_doc = medical_doc

    def set_prescription(self, prescription):
        self.__prescription = prescription

    def set_status(self, status):
        self.__status = status

    def set_address(self, patient_address):
        self.__patient_address = patient_address


class Patient:
    def __init__(self, appointment_id, patient_id, patient_name, doctor_id, doctor_name, appointment_type, date,
                 medical_concern, medical_docs, prescription, status, time, address, clinic_id):
        self.__clinic_id = clinic_id
        self.doctor_id = doctor_id
        self.__appointment_id = appointment_id
        self.__medical_doc = medical_docs
        self.__appointment_Id = patient_name
        self.__patient_id = patient_id
        self.__patient_name = doctor_name
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
                 specialty, workdays):
        self.__doctor_id = doctor_id
        self.__address = address
        self.__clinic_id = clinic_id
        self.__email = email
        self.__image = image
        self.__language = language
        self.__name = name
        self.__phone_no = phone_no
        self.__qualification = qualification
        self.__specialty = specialty
        self.__workdays = workdays

    def get_doctor_id(self):
        return self.__doctor_id

    def get_address(self):
        return self.__address

    def get_clinic_id(self):
        return self.__clinic_id

    def get_email(self):
        return self.__email

    def get_image(self):
        return self.__image

    def get_language(self):
        return self.__language

    def get_name(self):
        return self.__name

    def get_phone_no(self):
        return self.__phone_no

    def get_qualification(self):
        return self.__qualification

    def get_workdays(self):
        return self.__workdays

    def get_specialty(self):
        return self.__specialty

    def set_address(self, address):
        self.__address = address

    def set_clinicId(self, clinic_id):
        self.__clinic_id = clinic_id

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

    def set_specialty(self, specialty):
        self.__specialty = specialty

    def set_workdays(self, workdays):
        self.__workdays = workdays


cred = credentials.Certificate("serviceAccountKey.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {'storageBucket': 'call-a-doctor-20a5d.appspot.com'})

db = firestore.client()
bucket = storage.bucket()

app = CTk()
app.geometry("1080x664")
set_appearance_mode("light")

# Global variable
global frameDeclineAppointment
global frameAppointment
global navBtnFrame
global imgBtnBack
global frameClinic
global frameTimeTable
global frameDoctor
global frameEditClinic
global framePatient
global frameEditDoctor
global frameHome
global selected_clinic_id

# ClinicId = 'C-wTrXvY'
current_filter_type = "Pending"
sender_email = "CallADoctor2024@outlook.com"
sender_email_password = "P7EMtmk8Vw3Y"


def format_date_and_time(date_time, timezone='Asia/Kuala_Lumpur'):
    try:
        # print(f"\nOriginal date and time: {date_time}")

        # Convert the Firestore date_time to a standard datetime object
        if isinstance(date_time, datetime):
            dt = date_time
        else:
            dt = date_time.to_datetime()

        # Convert to the specified timezone
        target_tz = pytz.timezone(timezone)
        dt_tz = dt.astimezone(target_tz)

        # Format the datetime object to separate date and time strings
        formatted_date = dt_tz.strftime('%B %d, %Y')
        formatted_time = dt_tz.strftime('%I:%M %p')
        timezone_abbr = dt_tz.strftime('%Z')

        # print(f"Formatted date: {formatted_date}")
        # print(f"Formatted time: {formatted_time} {timezone_abbr}")

        return formatted_date, formatted_time

    except Exception as e:
        print(f"Error formatting date and time: {e}")
        return str(date_time), str(date_time)


def get_patient_name(patient_id):
    patient_doc = db.collection('Patients').document(patient_id).get()
    if patient_doc.exists:
        patient_data = patient_doc.to_dict()
        patient_name = patient_data.get('Name', 'N/A')
        # print(f"\nPatient ID: {patient_id}")
        # print(f"Patient name: {patient_name}")
        return patient_name
    else:
        return 'N/A'


def get_patient_phone(patient_id):
    patient_doc = db.collection('Patients').document(patient_id).get()
    if patient_doc.exists:
        patient_data = patient_doc.to_dict()
        patient_name = patient_data.get('PhoneNo', 'N/A')
        # print(f"\nPatient ID: {patient_id}")
        # print(f"Patient name: {patient_name}")
        return patient_name
    else:
        return 'N/A'


def get_patient_address_from_database(patient_id):
    patient_doc = db.collection('Patients').document(patient_id).get()
    if patient_doc.exists:
        patient_data = patient_doc.to_dict()
        patient_address = patient_data.get('Address', 'N/A')
        # print(f"\nPatient ID: {patient_id}")
        # print(f"Patient address: {patient_address}\n")
        return patient_address
    else:
        return 'N/A'


def on_filter_change(filter_type, clinic_id, frameAppointmentList):
    global current_filter_type
    global appointments_ref

    current_filter_type = filter_type

    # Filter the appointment details to display
    appointments_ref = db.collection('AppointmentDetails').where('ClinicId', '==', clinic_id)

    if filter_type == "Pending":
        appointments_ref = appointments_ref.where('Status', '==', 'Pending')
    elif filter_type == "Accepted":
        appointments_ref = appointments_ref.where('Status', '==', 'Accepted')
    elif filter_type == "Rejected":
        appointments_ref = appointments_ref.where('Status', '==', 'Rejected')

    get_appointment_list(filter_type, appointments_ref, frameAppointmentList)


def btnAppointment_Click(clinic_id):
    global selected_clinic_id
    global frameClinic
    global navBtnFrame
    global frameDoctor
    global frameAppointment
    global framePatient
    global frameEditDoctor
    global frameDeclineAppointment
    global frameHome
    global current_filter_type
    print("Appointment Button Clicked")

    for widget in frameAppointment.winfo_children():
        widget.destroy()

    # Search and filter section
    search_filter_frame = CTkFrame(master=frameAppointment, width=40, height=200, fg_color="transparent")
    search_filter_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)

    frameAppointmentList = CTkFrame(master=frameAppointment, bg_color="transparent", fg_color="transparent")
    frameAppointmentList.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

    def search_appointments(event=None):
        search_term = tbSearch.get().strip()
        get_appointment_list(current_filter_type, appointments_ref, frameAppointmentList, search_term=search_term)

    dropSearch = CTkOptionMenu(
        master=search_filter_frame, values=["Pending", "Accepted", "Rejected", "All"],
        fg_color="white", dropdown_fg_color="white", button_color="white", button_hover_color="white", width=206,
        height=59, anchor="center", corner_radius=20, font=("Inter", 20), text_color="#898989",
        command=lambda selected_value: on_filter_change(selected_value, clinic_id, frameAppointmentList)
    )

    # Set the initial value of the drop-down list to the current filter type
    dropSearch.set(current_filter_type)
    dropSearch.grid(row=1, column=0, sticky="nw", padx=47, pady=40)

    tbSearch = CTkEntry(master=search_filter_frame, fg_color="white", width=700, height=59, corner_radius=20,
                        font=("Inter", 15),
                        text_color="#5D5D5D", border_width=0)
    tbSearch.grid(row=1, column=0, sticky="new", padx=(238, 47), pady=40)
    tbSearch.bind("<Return>", search_appointments)

    lblBehindSearch = CTkLabel(master=search_filter_frame, text="|", font=("Inter", 28), text_color="#5271FF",
                               bg_color="white",
                               width=18, height=59)
    lblBehindSearch.grid(row=1, column=0, sticky="nw", padx=237, pady=40)

    imgBtnSearch = Image.open("C:/Users/michi/PycharmProjects/DCS2103_Aug2023/SE Project/Images/search.png")
    BtnSearch = CTkButton(master=search_filter_frame, text="", image=CTkImage(imgBtnSearch, size=(25, 25)),
                          fg_color="white",
                          corner_radius=0, anchor="center", width=25, command=search_appointments)
    BtnSearch.grid(row=1, column=0, sticky="ne", padx=60, pady=55)

    on_filter_change(current_filter_type, clinic_id, frameAppointmentList)

    # Display frameAppointment and hide other frames
    frameAppointment.grid()
    navBtnFrame.grid()
    frameClinic.grid_remove()
    frameDeclineAppointment.grid_remove()
    frameEditDoctor.grid_remove()
    framePatient.grid_remove()
    frameDoctor.grid_remove()


def get_appointment_list(filter_type, appointments_ref, frameAppointmentList, search_term=None):
    try:
        # Clear existing widgets in frameAppointmentList
        for widget in frameAppointmentList.winfo_children():
            widget.destroy()

        # Fetch data from Firestore
        docs = appointments_ref.stream()

        # Prepare the data
        appointment_data_list = []
        for doc in docs:
            appointment_dict = doc.to_dict()
            appointment_dict['appointmentId'] = doc.id  # Get the document ID as the appointment ID
            appointment_data_list.append(appointment_dict)

        # Add labels for "No." and "Appointment Information"
        lblNo = CTkLabel(master=frameAppointmentList, text="No.", font=("Inter", 20, "bold"), text_color="#5D5D5D")
        lblNo.grid(row=0, column=0, sticky="w", pady=(10, 5), padx=(10, 0))

        lblAppointmentInfoLabel = CTkLabel(master=frameAppointmentList, text="Appointment Information",
                                           font=("Inter", 20, "bold"),
                                           text_color="#5D5D5D")
        lblAppointmentInfoLabel.grid(row=0, column=1, sticky="w", pady=(10, 5), padx=(10, 0))

        # Display each appointment data
        index = 1  # Initialize index outside the loop
        for appointment_info in appointment_data_list:
            appointment_id = appointment_info['appointmentId']

            # Fetch appointment data from Firestore using the appointment ID
            appointment_doc = db.collection('AppointmentDetails').document(appointment_id).get()
            if appointment_doc.exists:
                appointment_data = appointment_doc.to_dict()

                # Format date and time
                patient_Id = appointment_data.get('PatientId')
                date, time = format_date_and_time(appointment_data.get('DateTime'))
                patient_name = get_patient_name(patient_Id)
                doctor_name = get_doctor_name(appointment_data.get('DoctorId'))
                clinic_name = get_clinic_name(appointment_data.get('ClinicId'))
                address = get_patient_address_from_database(patient_Id)
                phone_no = get_patient_phone(patient_Id)

                # Filter appointments based on search term
                if search_term:
                    search_parts = search_term.lower().split()
                    patient_full_name = patient_name.lower()
                    doctor_full_name = doctor_name.lower()

                    match_found = False
                    for part in search_parts:
                        if part in patient_full_name:
                            match_found = True
                            break
                        elif part in doctor_full_name:
                            match_found = True

                    if not match_found:
                        continue  # Skip this appointment if search term not found in patient name

                # Create a new Appointment object with the updated data
                appointment = Appointment(
                    appointment_id=appointment_id,
                    appointment_type=appointment_data.get('AppointmentType', 'N/A'),
                    clinic_id=appointment_data.get('ClinicId', 'N/A'),
                    date_time=appointment_data.get('DateTime', 'N/A'),
                    date=date,
                    time=time,
                    clinic_name=clinic_name,
                    doctor_id=str(appointment_data.get('DoctorId', 'N/A')),
                    doctor_name=doctor_name,
                    medical_concern=appointment_data.get('MedicalConcern', 'N/A'),
                    medical_doc=appointment_data.get('MedicalDocs', 'N/A'),
                    patient_address=address,
                    patient_id=patient_Id,
                    patient_name=patient_name,
                    patient_phone=phone_no,
                    prescription=appointment_data.get('Prescription', 'N/A'),
                    status=appointment_data.get('Status', 'N/A')
                )
                # Construct appointment information string
                appointment_info_text = (
                    f"Patient name: {appointment.get_patient_name()}\n"
                    f"Doctor name: {appointment.get_doctor_name()}\n"
                    f"Type: {appointment.get_appointment_type()}\n"
                    f"Date: {appointment.get_date()}\n"
                    f"Time: {appointment.get_time()}\n"
                    f"Status: {appointment.get_status()}\n"
                )

                # Create a frame for each appointment
                frameAppointmentItem = CTkFrame(master=frameAppointmentList, bg_color="transparent",
                                                fg_color="transparent")
                frameAppointmentItem.grid(row=index, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

                # Add label for index number
                lblIndex = CTkLabel(master=frameAppointmentItem, text=f"{index}.", font=("Inter", 20, "bold"),
                                    text_color="#5D5D5D")
                lblIndex.grid(row=0, column=0, sticky="w", padx=(10, 20), pady=(10, 5))

                # Create a label to display appointment information
                lblAppointmentListInfo = CTkLabel(
                    master=frameAppointmentItem,
                    text=appointment_info_text,
                    width=800,
                    height=120,
                    corner_radius=10,
                    fg_color="white",
                    bg_color="transparent",
                    text_color="#5D5D5D",
                    font=("Inter", 15),
                    justify="left",
                    anchor="nw"
                )
                lblAppointmentListInfo.grid(row=0, column=1, sticky="w", padx=(0, 20), pady=(10, 5))

                # Bind the click event to lblAppointmentListInfo
                lblAppointmentListInfo.bind("<Button-1>",
                                            lambda e, appt=appointment,
                                                   cid=appointment.get_clinic_id(): appointment_details(
                                                filter_type, cid, appt))

                index += 1

                # Display frameAppointmentList and configure columns
        frameAppointmentList.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        frameAppointmentList.grid_columnconfigure(0, weight=1, minsize=200)
        frameAppointmentList.grid_columnconfigure(1, weight=1, minsize=400)

        # Display the image on the right side
        img_path = "C:/Users/michi/PycharmProjects/DCS2103_Aug2023/SE Project/Images/placeholder.jpg"
        ImgAppointmentList = Image.open(img_path)
        ImgAppointmentList = CTkImage(ImgAppointmentList, size=(400, 500))  # Adjust size as needed
        img_label = CTkLabel(master=frameAppointmentList, text="", image=ImgAppointmentList, bg_color="transparent")
        img_label.grid(row=1, column=2, rowspan=len(appointment_data_list) + 1, sticky="nsew", padx=(10, 20),
                       pady=(10, 5))

        # Display frameAppointment and hide other frames
        navBtnFrame.grid()

    except Exception as e:
        print(f"Error fetching appointment information: {e}")


def get_doctor_list(clinic_id):
    try:
        doctors_ref = db.collection('Doctors').where('ClinicId', '==', clinic_id)
        doctors_docs = doctors_ref.stream()
        all_doctors = {}

        for doctor in doctors_docs:
            doctor_data = doctor.to_dict()
            doctor_id = doctor.id
            doctor_name = doctor_data.get('Name')

            all_doctors[doctor_id] = doctor_name

        return all_doctors

    except Exception as e:
        print(f"Error searching doctors: {e}")
        return {}


def get_appointed_doctor(clinic_id):
    try:
        appointed_doctors_ref = db.collection('AppointmentDetails') \
            .where('ClinicId', '==', clinic_id) \
            .where('Status', 'in', ['Accepted', 'Pending'])

        appointed_doctors_docs = appointed_doctors_ref.stream()
        appointed_doctors = {}

        for doc in appointed_doctors_docs:
            doctor_data = doc.to_dict()
            doctor_id = doctor_data.get('DoctorId')
            appointed_time = str(doctor_data.get('DateTime'))

            if doctor_id and appointed_time:
                if doctor_id in appointed_doctors:

                    appointed_doctors[doctor_id].append(appointed_time)
                else:

                    appointed_doctors[doctor_id] = [appointed_time]

        return appointed_doctors

    except Exception as e:
        print(f"Error displaying appointment details: {e}")
        return {}


def search_doctor(clinic_id, appointment_date_time):
    try:
        all_doctors = get_doctor_list(clinic_id)
        appointed_doctors = get_appointed_doctor(clinic_id)
        # Create a temporary dictionary to filter out appointments based on appointment_date_time
        temp_doctors = {}
        for doctor_id, appointments in appointed_doctors.items():
            filtered_appointments = [dt for dt in appointments if dt != appointment_date_time]
            if filtered_appointments:
                temp_doctors[doctor_id] = filtered_appointments

        # Create available_doctors dictionary containing doctors with no appointments at appointment_date_time
        doctor_available = {doctor_id: name for doctor_id, name in all_doctors.items() if
                            doctor_id not in temp_doctors}

        # display each dictionary for testing
        print_dict_in_batches("All Doctors", all_doctors)
        print_dict_in_batches("Appointed Doctors", appointed_doctors)
        print_dict_in_batches(" Available Doctor", doctor_available)
        return doctor_available
    except Exception as e:
        print(f"Error searching doctors: {e}")
        return {}


def print_dict_in_batches(label, dictionary):
    print(label + ":")
    for key, value in dictionary.items():
        print(f"\t{key}: {value},")
    print("\n")


def appointment_details(filter_type, clinic_id, appointment):
    global selected_clinic_id
    global frameClinic
    global navBtnFrame
    global imgBtnBack
    global frameDoctor
    global frameAppointment
    global framePatient
    global frameEditDoctor
    global frameDeclineAppointment
    global frameHome

    try:
        # Fetch appointment date/time
        appointment_date_time = appointment.get_date_time()

        # Fetch available doctors for the given clinic and appointment date/time
        doctor_names_dic = search_doctor(clinic_id, appointment_date_time)
        print(doctor_names_dic)

        # Clear existing widgets in framePatient
        for widget in framePatient.winfo_children():
            widget.destroy()

        # Retrieve appointment details
        appointment_info_text = (
            f"ID: {appointment.get_appointment_id()}\n"
            f"Type: {appointment.get_appointment_type()}\n"
            f"Date: {appointment.get_date()}\n"
            f"Time: {appointment.get_time()}\n"
        )
        if appointment.get_appointment_type() == 'Home Visit':
            patient_info = (
                f"ID: {appointment.get_patient_id()}\n"
                f"Name: {appointment.get_patient_name()}\n"
                f"Phone No: {appointment.get_patient_phone()}\n"
                f"Medical Concern: {appointment.get_medical_concern()}\n"
            )
        else:
            patient_info = (
                f"ID: {appointment.get_patient_id()}\n"
                f"Name: {appointment.get_patient_name()}\n"
                f"Phone No: {appointment.get_patient_phone()}\n"
                f"Address: {appointment.get_patient_address()}\n"
                f"Medical Concern: {appointment.get_medical_concern()}\n"
            )

        doctor_info = (
            f"ID: {appointment.get_doctor_id()}\n"
            f"Name: {appointment.get_doctor_name()}\n"
        )

        status = appointment.get_status()

        # Determine the status color
        if status == "Pending":
            status_color = "#5271FF"
        elif status == "Rejected":
            status_color = "#5D5D5D"
        elif status == "Accepted":
            status_color = "red"
        else:
            status_color = "#5D5D5D"

        # Display appointment details
        current_row = 0

        btnBack = CTkButton(
            master=framePatient, text="", fg_color="transparent",
            image=CTkImage(imgBtnBack, size=(30, 30)),
            width=50, height=50, corner_radius=0,
            command=lambda: btnAppointment_Click(clinic_id)
        )
        btnBack.grid(row=current_row, column=0, padx=20, pady=(10, 5), sticky="w")

        current_row += 1

        lblPatient = CTkLabel(
            master=framePatient, text="Appointment Information:", width=550, height=0, corner_radius=0,
            text_color="#5D5D5D", font=("Inter", 20, "bold"), justify="left", anchor="w"
        )
        lblPatient.grid(row=current_row, column=0, padx=20, pady=0, sticky="w")

        current_row += 1

        lblPatientInfo = CTkLabel(
            master=framePatient, text=appointment_info_text, width=550, height=0, corner_radius=0,
            text_color="#5D5D5D", font=("Inter", 20), justify="left", anchor="w"
        )
        lblPatientInfo.grid(row=current_row, column=0, padx=20, pady=0, sticky="w")

        current_row += 1
        current_row += 1

        # Display patient information
        lblPatient = CTkLabel(
            master=framePatient, text="Patient Information:", width=550, height=0, corner_radius=0,
            text_color="#5D5D5D", font=("Inter", 20, "bold"), justify="left", anchor="w"
        )
        lblPatient.grid(row=current_row, column=0, padx=20, pady=0, sticky="w")

        current_row += 1

        lblPatientInfo = CTkLabel(
            master=framePatient, text=patient_info, width=550, height=0, corner_radius=0,
            text_color="#5D5D5D", font=("Inter", 20), justify="left", anchor="w"
        )
        lblPatientInfo.grid(row=current_row, column=0, padx=20, pady=0, sticky="w")

        current_row += 1

        # Display doctor information
        lblDoctor = CTkLabel(
            master=framePatient, text="Doctor Information:", width=550, height=0, corner_radius=0,
            text_color="#5D5D5D", font=("Inter", 20, "bold"), justify="left", anchor="w"
        )
        lblDoctor.grid(row=current_row, column=0, padx=20, pady=0, sticky="w")

        current_row += 1

        lblDoctorInfo = CTkLabel(
            master=framePatient, text=doctor_info, width=550, height=0, corner_radius=0,
            text_color="#5D5D5D", font=("Inter", 20), justify="left", anchor="w"
        )
        lblDoctorInfo.grid(row=current_row, column=0, padx=20, pady=0, sticky="w")

        current_row += 1

        if appointment.get_doctor_id() == '-':
            if not doctor_names_dic:
                lblNoDoctorsAvailable = CTkLabel(
                    master=framePatient, text="No doctors available for this date and time.", font=("Inter", 16),
                    text_color="red"
                )
                lblNoDoctorsAvailable.grid(row=current_row, column=0, padx=20, pady=(10, 5), sticky="w")
            else:
                lblChooseDoctor = CTkLabel(
                    master=framePatient, text="Choose doctor for patient:", font=("Inter", 20),
                    text_color="#5D5D5D"
                )
                lblChooseDoctor.grid(row=current_row, column=0, padx=20, pady=(10, 5), sticky="w")

                dropDownDoctors = CTkOptionMenu(
                    master=framePatient, values=list(doctor_names_dic.values()), fg_color="white",
                    dropdown_fg_color="white"
                )
                dropDownDoctors.grid(row=current_row + 1, column=0, padx=20, pady=(10, 5), sticky="w")

                btnApplyDoctor = CTkButton(
                    master=framePatient, text="Apply", fg_color="gray", font=("Inter", 20, "bold"),
                    corner_radius=20,
                    command=lambda: apply_doctor_selection(doctor_names_dic,
                                                           appointment, clinic_id, filter_type, dropDownDoctors.get())
                )
                btnApplyDoctor.grid(row=current_row + 1, column=0, padx=250, pady=(10, 5), sticky="w")

                current_row += 2

        # Display appointment status
        lblStatus = CTkLabel(
            master=framePatient, text=f"Status: {status}", width=550, height=0, corner_radius=0,
            text_color=status_color, font=("Inter", 20, "bold"), justify="left", anchor="w"
        )
        lblStatus.grid(row=current_row, column=0, padx=20, pady=0, sticky="w")

        current_row += 1

        # Spacer between Reject and Accept buttons
        spacer = CTkLabel(master=framePatient, text="", width=10, bg_color="transparent")
        spacer.grid(row=current_row, column=1, padx=10, pady=20, sticky="w")

        # Reject and Accept buttons
        btnReject = CTkButton(
            master=framePatient, text="Reject", fg_color="red", font=("Inter", 20, "bold"),
            corner_radius=20, command=lambda: reject_appointment(filter_type, appointment, clinic_id)
        )
        btnReject.grid(row=current_row, column=2, pady=20, padx=(0, 20), sticky="e")

        if appointment.get_doctor_id() != "-":
            btnAccept = CTkButton(
                master=framePatient, text="Accept", fg_color="#5271FF", font=("Inter", 20, "bold"),
                corner_radius=20, command=lambda: accept_appointment(filter_type, appointment, clinic_id)
            )
            btnAccept.grid(row=current_row, column=3, pady=20, padx=(0, 20), sticky="e")

        # Ensure framePatient and its contents are visible
        framePatient.grid()
        navBtnFrame.grid()
        frameDeclineAppointment.grid_remove()

    except Exception as e:
        print(f"Error displaying appointment details: {e}")


def apply_doctor_selection(doctor_names_dic, appointment, clinic_id, filter_type, selected_doctor):
    try:
        doctor_id = ""
        doctor_name = ""
        # Retrieve doctor ID and name based on the selected value
        for doctor_id, doctor_name in doctor_names_dic.items():
            if doctor_name == selected_doctor:
                break

        # Update the appointment with the selected doctor
        appointment_id = appointment.get_appointment_id()
        db.collection('AppointmentDetails').document(appointment_id).update({
            'DoctorId': doctor_id,
            'DoctorName': doctor_name
        })

        # Reload and display the updated patient details
        reload_patient_details(appointment_id, clinic_id, appointment.get_time(), filter_type)

    except Exception as e:
        print(f"Error applying doctor selection: {e}")


def reload_patient_details(appointment_id, clinic_id, time_format, filter_type):
    try:
        # Updated appointment details from Firestore
        appointment_doc = db.collection('AppointmentDetails').document(appointment_id).get()
        if appointment_doc.exists:
            appointment_data = appointment_doc.to_dict()
            appointment_data['AppointmentId'] = appointment_id

            patient_Id = appointment_data.get('PatientId')
            # Extract the date and time from the appointment data
            date, time = format_date_and_time(appointment_data.get('DateTime'))
            patient_name = get_patient_name(patient_Id)
            doctor_name = get_doctor_name(appointment_data.get('DoctorId'))
            clinic_name = get_clinic_name(appointment_data.get('ClinicId'))
            address = get_patient_address_from_database(patient_Id)

            # Create a new Appointment object with the updated data
            appointment = Appointment(
                appointment_id=appointment_id,
                appointment_type=appointment_data.get('AppointmentType', 'N/A'),
                clinic_id=appointment_data.get('ClinicId', 'N/A'),
                date_time=appointment_data.get('DateTime', 'N/A'),
                date=date,
                time=time,
                clinic_name=clinic_name,
                doctor_id=str(appointment_data.get('DoctorId', 'N/A')),  # Ensure DoctorId is a string
                doctor_name=doctor_name,
                medical_concern=appointment_data.get('MedicalConcern', 'N/A'),
                medical_doc=appointment_data.get('MedicalDocs', 'N/A'),
                patient_address=address,
                patient_id=patient_Id,
                patient_name=patient_name,
                prescription=appointment_data.get('Prescription', 'N/A'),
                status=appointment_data.get('Status', 'N/A')
            )
            print(f"{appointment_data.get('DoctorID')}")

            # Display the updated patient details in the UI
            appointment_details(filter_type, clinic_id, appointment)

    except Exception as e:
        print(f"Error reloading patient details: {e}")


def accept_appointment(filter_type, appointment, clinic_id):
    try:
        appointment_id = appointment.get_appointment_id()
        # Update the status of the appointment in Firestore
        update_appointment_status(appointment_id, "Accepted")
        print("Accepted")

        print("Clinic Approved")
        appointment_accepted(appointment)
        # Display a pop-up informing that the clinic has been approved
        messagebox.showinfo("Appointment acceptation success",
                            f"Patient {appointment.get_patient_name()}'s appointment has been accepted.\n"
                            f"An accepted notification email has been sent to {appointment.get_patient_name()}.")
        # Call the function to navigate back to the appointment list
        btnAppointment_Click(clinic_id)
    except Exception as e:
        print(f"Error approving clinic: {e}")


def appointment_accepted(appointment):
    global frameAppointment

    print("Send approve email.")

    # Clear existing widgets in frameAppointment (if using a GUI toolkit)
    for widget in frameAppointment.winfo_children():
        widget.destroy()

    sender = sender_email
    sender_password = sender_email_password
    recipient = get_patient_email(appointment.get_patient_id())

    appointment_type = appointment.get_appointment_type()

    if appointment_type == 'Home Visit':
        address = appointment.get_patient_address()
    else:
        clinic_id = appointment.get_clinic_id()
        clinic_ref = db.collection('Clinics').document(clinic_id)
        clinic_doc = clinic_ref.get()

        if clinic_doc.exists:
            clinic_data = clinic_doc.to_dict()
            address = clinic_data.get('Address', '-')
        else:
            address = '-'

    # Build the address line conditionally
    address_line = f"Address: {address}\n"

    # Construct the message with the address conditionally included
    message = (f"<!DOCTYPE html>"
               f"<html>"
               f"<body>"
               f"<p style='color:black;'>"
               f"Dear {appointment.get_patient_name()},<br><br>"
               f"Your appointment has been accepted.<br><br>"
               f"<b>Appointment details:</b><br>"
               f"Appointment ID: {appointment.get_appointment_id()}<br>"
               f"Clinic name: {appointment.get_clinic_name()}<br>"
               f"Doctor name: {appointment.get_doctor_name()}<br>"
               f"Date: {appointment.get_date()}<br>"
               f"Time: {appointment.get_time()}<br>"
               f"Appointment type: {appointment.get_appointment_type()}<br>"
               f"{address_line}"
               f"</p>"
               f"</body>"
               f"</html>")

    print(message)

    email = EmailMessage()
    email["From"] = sender
    email["To"] = recipient
    email["Subject"] = f"{appointment.get_clinic_name()} has accepted your request"
    email.add_alternative(message, subtype='html')

    # Send email using SMTP
    try:
        smtp = smtplib.SMTP("smtp-mail.outlook.com", port=587)
        smtp.starttls()
        smtp.login(sender, sender_password)
        smtp.sendmail(sender, recipient, email.as_string())
        smtp.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")


def reject_appointment(filter_type, appointment, clinic_id):
    global frameDeclineAppointment
    global frameAppointment
    global navBtnFrame
    global imgBtnBack

    print("reject appointment")
    try:
        frameDeclineAppointment.grid()
        frameAppointment.grid_remove()
        navBtnFrame.grid_remove()

        for widget in frameAppointment.winfo_children():
            widget.destroy()

        btnBack = CTkButton(
            master=frameDeclineAppointment, text="", fg_color="transparent",
            image=CTkImage(imgBtnBack, size=(30, 30)),
            width=50, height=50, corner_radius=0,
            command=lambda: appointment_details(filter_type, clinic_id, appointment)
        )
        btnBack.grid(row=0, column=0, padx=20, pady=(10, 5), sticky="w")

        # Label for decline reason
        lblDeclineClinic = CTkLabel(
            master=frameDeclineAppointment,
            text=f"Please choose the reason for declining {appointment.get_patient_name()}'s appointment?\n"
                 f"Date: {appointment.get_date()}\n"
                 f"Time: {appointment.get_time()}",
            font=("Inter", 20),
            text_color="#5D5D5D",
            justify="left"
        )
        lblDeclineClinic.grid(row=1, column=0, sticky="wn", pady=(10, 5), padx=(10, 0))

        # Variable to store the decline reason
        decline_reason = StringVar(value="Select decline reason")

        # Dropdown for decline reasons
        dropDecline = CTkOptionMenu(
            master=frameDeclineAppointment,
            values=["Select decline reason", "Doctor emergency leave",
                    "Unforeseen reason (water supply stops/ electric supply stop/system down)", "Public holiday"],
            fg_color="white",
            dropdown_fg_color="white",
            button_color="white",
            button_hover_color="white",
            width=206,
            height=59,
            anchor="center",
            corner_radius=20,
            font=("Inter", 20),
            text_color="#898989",
            variable=decline_reason,
        )
        dropDecline.grid(row=2, column=0, sticky="enw", padx=47, pady=20)

        # Submit button
        btnSubmit = CTkButton(
            master=frameDeclineAppointment,
            text="Submit",
            fg_color="#5271FF",
            font=("Inter", 20, "bold"),
            corner_radius=20,
            width=100,
            command=lambda: btnSubmit_Click(appointment, decline_reason.get(), filter_type, clinic_id)
            # Pass the selected value
        )
        btnSubmit.grid(row=3, column=0, pady=20, padx=(150, 150))

    except Exception as e:
        print(f"Error declining appointment: {e}")


import tkinter as tk


def btnSubmit_Click(appointment, reject_reason, filter_type, clinic_id):
    global frameDeclineAppointment

    # Check if reject_reason is "Select decline reason"
    if reject_reason == "Select decline reason":
        lblDeclineClinic = CTkLabel(
            master=frameDeclineAppointment,
            text=f"Please choose the reason for declining {appointment.get_patient_name()}'s appointment before submitting.",
            font=("Inter", 15),
            text_color="red"
        )
        lblDeclineClinic.grid(row=4, column=0, sticky="wn", pady=(10, 5), padx=(10, 0))
        return

    print(f"Submit button clicked for appointment: {appointment.get_patient_name()}")
    print(f"Reason for decline: {reject_reason}")

    try:
        appointment_id = appointment.get_appointment_id()
        clinic_id = appointment.get_clinic_id()

        # Update appointment status to "Rejected" in Firestore
        update_appointment_status(appointment_id, "Rejected")

        # Clear existing widgets in frameAppointment (if using a GUI toolkit)
        for widget in frameAppointment.winfo_children():
            widget.destroy()

        sender = sender_email
        sender_password = sender_email_password
        recipient = get_patient_email(appointment_id)

        # Example recipient (replace with actual recipient as needed)
        recipient1 = "p22014062@student.newinti.edu.my"

        if isinstance(reject_reason, tk.StringVar):
            reject_reason_lower = reject_reason.get().lower()
        else:
            reject_reason_lower = reject_reason.lower()

        message = (f"Dear {appointment.get_patient_name()},\n\n"
                   f"Your appointment has been rejected due to {reject_reason_lower}.\n\n"
                   f"Please select a new appointment date. Sorry for any inconvenience.")

        email = EmailMessage()
        email["From"] = sender
        email["To"] = recipient1
        email["Subject"] = f"{appointment.get_clinic_name()} has declined your appointment"
        email.set_content(message)

        smtp = smtplib.SMTP("smtp-mail.outlook.com", port=587)
        smtp.starttls()
        smtp.login(sender, sender_password)
        smtp.sendmail(sender, recipient1, email.as_string())
        smtp.quit()

        messagebox.showinfo("Appointment rejection success",
                            f"{appointment.get_patient_name()}'s appointment has been declined.\n"
                            f"A rejection notification has been sent to the patient's email.")

        btnAppointment_Click(clinic_id)

    except smtplib.SMTPException as e:
        print(f"Error sending email: {e}")
    except Exception as e:
        print(f"Error updating appointment in database: {e}")


def get_patient_email(patient_id):
    patient_doc = db.collection('Patients').document(patient_id).get()
    if patient_doc.exists:
        patient_data = patient_doc.to_dict()
        patient_email = patient_data.get('Email', 'N/A')
        print(f"\nPatient ID: {patient_id}")
        print(f"Patient email: {patient_email}\n")
        return patient_email
    else:
        return 'N/A'


def update_appointment_status(appointment_id, status):
    # Update the status in Firestore
    db.collection('AppointmentDetails').document(appointment_id).update({'Status': status})


# Function to get patient name from ID
def get_patientName(patient_id):
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
        doctor_name = doctor_data.get('Name', '-')
        # print(f"\nDoctor ID: {doctor_id}")
        # print(f"Doctor name: {doctor_name}\n")
        return doctor_name
    else:
        return '-'


def get_clinic_name(clinic_id):
    if clinic_id == 'N/A':
        return '-'

    clinic_ref = db.collection('Clinics').document(clinic_id)
    clinic_doc = clinic_ref.get()

    if clinic_doc.exists:
        clinic_data = clinic_doc.to_dict()
        clinic_name = clinic_data.get('Name', '-')
        # print(f"\nClinic ID: {clinic_id}")
        # print(f"Clinic name: {clinic_name}\n")
        return clinic_name
    else:
        return '-'


def get_unique_doctor_id():
    while True:
        doctor_id = generate_doctor_id()
        doctor_ref = db.collection('Doctors').document(doctor_id)
        if not doctor_ref.get().exists:
            print(f"\nNew doctor ID: {doctor_id}\n")
            return doctor_id


def generate_doctor_id():
    # Define the range of characters for the ID
    characters = string.ascii_letters + string.digits

    while True:
        # Generate a random ID with the range of 6
        doctor_id = 'D-' + ''.join(random.choices(characters, k=6))

        # Check if this ID already exists in the database
        doctor_ref = db.collection('Doctors').document(doctor_id)
        if not doctor_ref.get().exists:
            return doctor_id


def btnDoctor_Click(clinic_id):
    global selected_clinic_id
    global frameClinic
    global navBtnFrame
    global frameDoctor
    global frameAppointment
    global framePatient
    global frameEditDoctor
    global frameDeclineAppointment
    global frameHome

    # Fetching doctors for the given clinic ID
    doctors_ref = db.collection('Doctors').where('ClinicId', '==', clinic_id)
    docs = doctors_ref.stream()

    doctor_data_list = []
    for doc in docs:
        doctor_details = doc.to_dict()
        doctor_details['DoctorId'] = doc.id
        doctor_data_list.append(doctor_details)

    # Add an empty doctor entry for the 'Create Doctor' button
    doctor_data_list.append({})

    # Clear existing widgets in frameDoctor and frameEditDoctor
    for widget in frameDoctor.winfo_children():
        widget.destroy()

    for widget in frameEditDoctor.winfo_children():
        widget.destroy()

    # Configure grid columns for frameDoctor to expand dynamically
    for col in range(3):
        frameDoctor.grid_columnconfigure(col, weight=1)

    rowIndex = 2
    colIndex = 0
    found_doctors = False

    for doctor_details in doctor_data_list[:-1]:
        found_doctors = True

        doctor = Doctors(
            doctor_id=doctor_details.get('DoctorId', 'N/A'),
            address=doctor_details.get('Address', 'N/A'),
            clinic_id=clinic_id,
            email=doctor_details.get('Email', 'N/A'),
            image=doctor_details.get('Image', ''),
            language=doctor_details.get('Language', 'N/A'),
            name=doctor_details.get('Name', 'N/A'),
            phone_no=doctor_details.get('PhoneNo', 'N/A'),
            qualification=doctor_details.get('Qualification', 'N/A'),
            specialty=doctor_details.get('Specialty', 'N/A'),
            workdays=doctor_details.get('WorkDays', 'N/A')
        )

        doctor_info = (
            f"Name: {doctor.get_name()}\n"
            f"Email: {doctor.get_email()}\n"
            f"Phone: {doctor.get_phone_no()}\n"
            f"Specialty: {doctor.get_specialty()}\n"
            f"Language: {doctor.get_language()}\n"
            f"Work days: {doctor.get_workdays()}"
        )

        # Create the doctor information label
        lblDoctorInfo = CTkLabel(
            master=frameDoctor, width=300, height=150, corner_radius=10,
            fg_color="white", text_color="#5D5D5D", font=("Inter", 15), justify="left",
            anchor="nw", text=doctor_info, wraplength=380
        )
        lblDoctorInfo.grid(row=rowIndex, column=colIndex, sticky="nsew", padx=10, pady=(0, 20))

        lblDoctorInfo.bind(
            "<Button-1>",
            lambda event, data=doctor_details, clinic_id_param=clinic_id: doctor_details_click(data, clinic_id_param)
        )

        if doctor.get_image():
            image_path = doctor.get_image()
            blob = bucket.get_blob(image_path)
            if blob is not None:
                try:
                    arr = np.frombuffer(blob.download_as_string(), np.uint8)
                    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                    # Resize the image and convert to PIL Image
                    pil_img = Image.fromarray(img)
                    pil_img = pil_img.resize((200, 200), Image.LANCZOS)

                    # Add rounded corners to the image
                    pil_img = addRoundedCorners(pil_img, 10)

                    # Convert PIL Image to PhotoImage
                    photo_image = ImageTk.PhotoImage(pil_img)

                    # Configure label with image and text
                    lblDoctorInfo.configure(image=photo_image, compound='top', text=doctor_info)
                    lblDoctorInfo.image = photo_image
                except Exception as e:
                    print(f"Error decoding image for doctor: {e}")
            else:
                print(f"Blob not found for path: {image_path}")
        else:
            lblDoctorInfo.configure(text=doctor_info)

        colIndex += 1
        if colIndex >= 3:
            colIndex = 0
            rowIndex += 1

    # Load the image for creating a new doctor
    img_path = "C:/Users/michi/PycharmProjects/DCS2103_Aug2023/SE Project/Images/create doctor.jpg"
    imgCreateDoctor = Image.open(img_path)
    imgCreateDoctor = imgCreateDoctor.resize((150, 200), Image.LANCZOS)
    photo_image_create_doctor = ImageTk.PhotoImage(imgCreateDoctor)

    create_row = rowIndex
    create_col = colIndex
    if colIndex > 0:
        create_col -= 1

    lblCreateDoctor = CTkLabel(
        master=frameDoctor, image=photo_image_create_doctor, text="", width=50, height=100,
        fg_color="white", corner_radius=10
    )
    lblCreateDoctor.grid(row=create_row, column=create_col, sticky="nsew", padx=10, pady=(0, 20))
    lblCreateDoctor.bind("<Button-1>", lambda event, clinic_id_param=clinic_id: new_doctor(clinic_id_param))
    lblCreateDoctor.image = photo_image_create_doctor

    if not found_doctors:
        print("No doctors found for this clinic.")

    # Configure row weights for frameDoctor to expand dynamically
    for row in range(rowIndex + 1):
        frameDoctor.grid_rowconfigure(row, weight=1)

    frameDoctor.grid_remove()
    frameDoctor.grid()
    navBtnFrame.grid()
    frameAppointment.grid_remove()
    framePatient.grid_remove()
    frameClinic.grid_remove()
    frameEditDoctor.grid_remove()
    frameDeclineAppointment.grid_remove()
    frameEditDoctor.grid_remove()


def addRoundedCorners(image, corner_radius):
    mask = Image.new('L', image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([0, 0, *image.size], radius=corner_radius, fill=255)
    image = image.convert("RGBA")
    image.putalpha(mask)
    return image


# Crops and expands images to fit the target size while maintaining the aspect ratio
def cropImage(image, targetSize):
    targetWidth, targetHeight = targetSize

    # Calculate the aspect ratio of the image
    aspectRatio = image.width / image.height

    # Calculate the new size preserving the aspect ratio
    newWidth = targetWidth
    newHeight = int(newWidth / aspectRatio)

    # Check if the new height exceeds the label height
    if newHeight < targetHeight:
        newHeight = targetHeight
        newWidth = int(newHeight * aspectRatio)

    # Resize the image to fit within the label dimensions
    imageResized = image.resize((newWidth, newHeight), Image.LANCZOS)

    # Create a blank white canvas with the exact label size
    canvas = Image.new('RGB', (targetWidth, targetHeight), color='white')

    # Calculate the position to paste the resized image
    pasteX = (targetWidth - newWidth) // 2
    pasteY = targetHeight - newHeight  # Paste at the bottom

    # If the image height exceeds the label height, prevent cropping from the top
    if pasteY < 0:
        pasteY = 0

    # Paste the resized image onto the canvas
    canvas.paste(imageResized, (pasteX, pasteY))

    return canvas


def upload_doctor_image(file_path, doctor_id, label_status):
    global imageFile
    if file_path:
        file_extension = file_path.split('.')[-1]
        imageFile = f"Doctors/{doctor_id}.{file_extension}"

        bucket = storage.bucket()
        blob = bucket.blob(imageFile)

        try:
            blob.upload_from_filename(file_path)
            blob.make_public()
            print("Your file URL:", blob.public_url)

            label_status.configure(text="An image has been selected.", text_color="green")
            return imageFile  # Return the uploaded image path
        except Exception as e:
            print("Error uploading file:", e)
            label_status.configure(text="An image has not been selected.", text_color="red")
    else:
        print("No file selected for upload.")
        label_status.configure(text="No file selected for upload.", fg_color="red")

    return None


# Function for opening the file explorer window
def browseDoctorFiles(label_status, doctor_id):
    filename = filedialog.askopenfilename(title="Select a File",
                                          filetypes=(("PNG files", "*.png"),
                                                     ("JPG files", "*.jpg"),
                                                     ("JPEG files", "*.jpeg")))
    if filename:

        label_status.configure(text="Image selected", text_color="green")
        upload_doctor_image(filename, doctor_id, label_status)
    else:
        label_status.configure(text="No image selected", text_color="red")


def create_label_and_entry(master, text, row, entryDoctorId=None, is_image=False):
    label = CTkLabel(master=master, text=text, font=("Inter", 20), justify="left", anchor="w")
    label.grid(row=row, column=0, sticky="w", padx=10, pady=5)

    if is_image:
        lblImageStatus = CTkLabel(master=master, text="No file selected", font=("Inter", 15),
                                  justify="left", anchor="w")
        lblImageStatus.grid(row=row, column=1, padx=10, pady=5, sticky="w")
        btnUploadImage = CTkButton(master=master, text="Select Image", fg_color="gray",
                                   command=lambda: browseDoctorFiles(lblImageStatus, entryDoctorId))
        btnUploadImage.grid(row=row, column=2, padx=(5, 10), pady=5)
        return lblImageStatus
    else:
        entry = CTkEntry(master=master, width=300, height=30, font=("Inter", 20), border_width=0,
                         corner_radius=20)
        entry.grid(row=row, column=1, padx=(10, 5), pady=5)
        error_label = CTkLabel(master=master, text="", font=("Inter", 15), justify="left", anchor="w",
                               text_color="red")
        error_label.grid(row=row, column=2, sticky="w", padx=5)
        return entry, error_label


def new_doctor(clinic_Id):
    global selected_clinic_id
    global frameClinic
    global navBtnFrame
    global imgBtnBack
    global frameDoctor
    global frameAppointment
    global framePatient
    global frameEditDoctor
    global frameDeclineAppointment
    global frameHome

    print("Add new doctor")
    for widget in frameDoctor.winfo_children():
        widget.destroy()

    # Generate a unique doctor ID
    entryDoctorId = get_unique_doctor_id()
    entryClinicId = clinic_Id
    entryRegisterStatus = "Pending"
    row_index = 0

    def confirm_back_action():
        if messagebox.askyesno("Confirmation", "Are you sure you want to discard the new doctor information?"):
            btnDoctor_Click(clinic_Id)

    btnBack = CTkButton(
        master=frameEditDoctor, text="", fg_color="transparent",
        image=CTkImage(imgBtnBack, size=(30, 30)),
        width=50, height=50, corner_radius=0,
        command=lambda: confirm_back_action()  # Using lambda to pass function reference
    )
    btnBack.grid(row=row_index, column=0, padx=10, pady=(5, 5), sticky="w")

    row_index += 1
    entryName, lblErrorName = create_label_and_entry(frameEditDoctor, "Name:", row_index)
    row_index += 1

    lblImageStatus = create_label_and_entry(frameEditDoctor, "Image:", row_index, is_image=True,
                                            entryDoctorId=entryDoctorId)
    row_index += 1

    entryEmail, lblErrorEmail = create_label_and_entry(frameEditDoctor, "Email:", row_index)
    row_index += 1

    entryPhone, lblErrorPhone = create_label_and_entry(frameEditDoctor, "Phone No:", row_index)
    row_index += 1

    entryQualification, lblErrorQualification = create_label_and_entry(frameEditDoctor, "Qualification:", row_index)
    row_index += 1

    entrySpecialty, lblErrorSpecialty = create_label_and_entry(frameEditDoctor, "Specialty:", row_index)
    row_index += 1

    entryLanguage, lblErrorLanguage = create_label_and_entry(frameEditDoctor, "Language:", row_index)
    row_index += 1

    entryAddress, lblErrorAddress = create_label_and_entry(frameEditDoctor, "Address:", row_index)
    row_index += 1

    workdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    workday_vars = {day: BooleanVar() for day in workdays}

    labelWorkDays = CTkLabel(master=frameEditDoctor, text="Work days:", font=("Inter", 20), justify="left", anchor="w")
    labelWorkDays.grid(row=row_index, column=0, sticky="w", padx=10, pady=5)
    row_index += 1

    for i, day in enumerate(workdays):
        chk = CTkCheckBox(master=frameEditDoctor, text=day, variable=workday_vars[day], onvalue=True, offvalue=False)
        chk.grid(row=row_index, column=i % 2, sticky="w", padx=10, pady=5)
        if i % 2 == 1:
            row_index += 1

    if i % 2 == 0:
        row_index += 1

    # Add an empty column with flexible weight to push the Save button to the right
    frameEditDoctor.grid_columnconfigure(3, weight=1)

    btnSave = CTkButton(master=frameEditDoctor, text="Save", fg_color="#5271FF", font=("Inter", 20, "bold"),
                        corner_radius=20,
                        command=lambda: btnSaveNewDoctor_Click(entryDoctorId, entryClinicId, entryName, lblImageStatus,
                                                               entryEmail, entryPhone, entryQualification,
                                                               entrySpecialty,
                                                               entryLanguage, entryAddress,
                                                               lblErrorName, lblImageStatus, lblErrorEmail,
                                                               lblErrorPhone, lblErrorQualification, lblErrorSpecialty,
                                                               lblErrorLanguage,
                                                               lblErrorAddress, workday_vars))
    btnSave.grid(row=row_index, column=4, pady=10, padx=10, sticky='e')

    frameEditDoctor.grid()
    navBtnFrame.grid()
    frameDoctor.grid_remove()
    frameEditClinic.grid_remove()
    frameAppointment.grid_remove()
    frameDeclineAppointment.grid_remove()


def btnSaveNewDoctor_Click(entryDoctorId, entryClinicId, entryName, entryImage, entryEmail, entryPhone,
                           entryQualification,
                           entrySpecialty, entryLanguage, entryAddress, lblErrorName,
                           lblImageStatus, lblErrorEmail, lblErrorPhone, lblErrorQualification, lblErrorSpecialty,
                           lblErrorLanguage,
                           lblErrorAddress, workday_vars):
    global selected_clinic_id
    global frameClinic
    global navBtnFrame
    global imgBtnBack
    global frameDoctor
    global frameAppointment
    global framePatient
    global frameEditDoctor
    global frameDeclineAppointment
    global frameHome
    # Collect data from entries
    name = entryName.get()
    image_status = lblImageStatus.cget("text")

    email = entryEmail.get()
    phone = entryPhone.get()
    qualification = entryQualification.get()
    specialty = entrySpecialty.get()
    language = entryLanguage.get()
    address = entryAddress.get()

    # Initialize error state
    has_error = False

    # Clear previous error messages
    lblErrorName.configure(text="")
    lblImageStatus.configure(text="")
    lblErrorEmail.configure(text="")
    lblErrorPhone.configure(text="")
    lblErrorQualification.configure(text="")
    lblErrorSpecialty.configure(text="")
    lblErrorLanguage.configure(text="")
    lblErrorAddress.configure(text="")

    # Check for missing information
    if not name:
        lblErrorName.configure(text="Please enter doctor name.")
        has_error = True
    if image_status == "No file selected":
        lblImageStatus.configure(text="Please upload the doctor image.")
        has_error = True
    if not email:
        lblErrorEmail.configure(text="Please enter doctor email.")
        has_error = True
    if not phone:
        lblErrorPhone.configure(text="Please enter doctor phone No.")
        has_error = True
    if not qualification:
        lblErrorQualification.configure(text="Please enter doctor qualification.")
        has_error = True
    if not specialty:
        lblErrorSpecialty.configure(text="Please enter doctor specialty.")
        has_error = True
    if not language:
        lblErrorLanguage.configure(text="Please enter doctor available language.")
        has_error = True
    if not address:
        lblErrorAddress.configure(text="Please enter doctor home address.")
        has_error = True

    # If there is any error, return early
    if has_error:
        return

    # Get the selected work days as a comma-separated string
    selected_workdays = [day for day, var in workday_vars.items() if var.get()]
    workdays_str = ", ".join(selected_workdays)

    global imageFile
    try:
        # Save doctor data to Firestore
        doctor_data = {
            "DoctorId": entryDoctorId,
            "ClinicId": entryClinicId,
            "Name": name,
            "Image": imageFile,
            "Email": email,
            "PhoneNo": phone,
            "Qualification": qualification,
            "Specialty": specialty,
            "Language": language,
            "Address": address,
            "WorkDays": workdays_str
        }

        print(imageFile)

        # Save to Firestore
        doctor_ref = db.collection('Doctors').document(entryDoctorId)
        doctor_ref.set(doctor_data)

        print(f"Doctor {entryDoctorId} added successfully.")
        messagebox.showinfo("Success", f"Doctor {name} has been added successfully.")

        btnDoctor_Click(entryClinicId)

    except Exception as e:
        print(f"Error saving doctor: {e}")
        messagebox.showerror("Error", f"Failed to save doctor. Error: {e}")


def doctor_details_click(doctor_data, clinic_id):
    print("Doctor information has been clicked.")

    global selected_clinic_id
    selected_clinic_id = clinic_id

    for widget in frameDoctor.winfo_children():
        widget.destroy()

    btnBack = CTkButton(
        master=frameDoctor, text="", fg_color="transparent",
        image=CTkImage(imgBtnBack, size=(30, 30)),
        width=50, height=50, corner_radius=0,
        command=lambda: btnDoctor_Click(clinic_id)
    )
    btnBack.grid(row=0, column=0, padx=20, pady=(10, 5), sticky="w")

    doctor = Doctors(
        doctor_id=doctor_data.get('DoctorId', 'N/A'),
        address=doctor_data.get('Address', 'N/A'),
        clinic_id=clinic_id,
        email=doctor_data.get('Email', 'N/A'),
        image=doctor_data.get('Image', ''),
        language=doctor_data.get('Language', 'N/A'),
        name=doctor_data.get('Name', 'N/A'),
        phone_no=doctor_data.get('PhoneNo', 'N/A'),
        qualification=doctor_data.get('Qualification', 'N/A'),
        specialty=doctor_data.get('Specialty', 'N/A'),
        workdays=doctor_data.get('WorkDays', 'N/A')
    )

    doctor_info = (
        f"Doctor ID: {doctor.get_doctor_id()}\n"
        f"Name: {doctor.get_name()}\n"
        f"Email: {doctor.get_email()}\n"
        f"Phone: {doctor.get_phone_no()}\n"
        f"Specialty: {doctor.get_specialty()}\n"
        f"Qualification: {doctor.get_qualification()}\n"
        f"Workdays: {doctor.get_workdays()}\n"
        f"Language: {doctor.get_language()}\n"
        f"Address: {doctor.get_address()}\n"
    )

    lblDoctorDetails = CTkLabel(master=frameDoctor, text=doctor_info, width=100, height=0, corner_radius=0,
                                text_color="#5D5D5D", font=("Inter", 20), justify="left", anchor="w")
    lblDoctorDetails.grid(row=1, column=0, padx=20, pady=20, sticky="new", columnspan=2)

    # Load and display the doctor's image if available
    if doctor.get_image():
        image_path = doctor.get_image()
        # print(f"Fetching image from path: {image_path}")  # Debug print
        bucket = storage.bucket()
        blob = bucket.get_blob(image_path)
        if blob is not None:
            try:
                arr = np.frombuffer(blob.download_as_string(), np.uint8)
                img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                # Convert the numpy array to a PIL Image object
                pilImgDoctorIdv = Image.fromarray(img)
                pilImgDoctorIdv = cropImage(pilImgDoctorIdv, (350, 300))
                pilImgDoctorIdv = addRoundedCorners(pilImgDoctorIdv, 10)
                photo_image = ImageTk.PhotoImage(pilImgDoctorIdv)

                lblDoctorDetails.configure(image=photo_image, compound='top')
                lblDoctorDetails.image = photo_image
            except Exception as e:
                print(f"Error decoding image for doctor: {e}")
        else:
            print(f"Blob not found for path: {image_path}")

    btnEdit = CTkButton(master=frameDoctor, text="Edit", fg_color="#5271FF", font=("Inter", 20, "bold"),
                        corner_radius=20,
                        command=lambda: edit_doctor(doctor, doctor_data, doctor.get_doctor_id(), clinic_id), width=150)
    btnEdit.grid(row=2, column=3, pady=20, padx=(0, 20), sticky="e")

    frameDoctor.grid_rowconfigure(0, weight=1)
    frameDoctor.grid_columnconfigure(0, weight=1)

    frameDoctor.grid()
    navBtnFrame.grid()
    frameEditDoctor.grid_remove()
    frameEditClinic.grid_remove()
    frameAppointment.grid_remove()
    frameClinic.grid_remove()
    framePatient.grid_remove()
    frameDeclineAppointment.grid_remove()


selected_image_path = None


def confirm_back_action_edit(doctor, doctor_data, clinic_id):
    if messagebox.askyesno("Confirmation", f"Do you want to discard changes for doctor {doctor.get_name()}?"):
        doctor_details_click(doctor_data, clinic_id)


def edit_doctor(doctor, doctor_data, doctor_id, clinic_id):
    global selected_image_path
    global frameEditDoctor
    global frameDoctor
    global frameAppointment
    global navBtnFrame

    selected_image_path = doctor.get_image()

    print("Edit doctor information")
    frameEditDoctor.grid()
    navBtnFrame.grid()

    # Clear existing widgets in frameEditDoctor
    for widget in frameEditDoctor.winfo_children():
        widget.destroy()

    row_index = 0

    btnBack = CTkButton(
        master=frameEditDoctor, text="", fg_color="transparent",
        image=CTkImage(imgBtnBack, size=(30, 30)),
        width=50, height=50, corner_radius=0,
        command=lambda: confirm_back_action_edit(doctor, doctor_data, clinic_id)  # Updated to use the new function
    )
    btnBack.grid(row=row_index, column=0, padx=20, pady=(10, 5), sticky="w")

    row_index += 1

    lblDoctorId = CTkLabel(master=frameEditDoctor, text="Doctor ID:", font=("Inter", 20), justify="left", anchor="w")
    lblDoctorId.grid(row=row_index, column=0, sticky="w", padx=20, pady=10)
    lblDoctorIdValue = CTkLabel(master=frameEditDoctor, text=doctor.get_doctor_id(), font=("Inter", 20))
    lblDoctorIdValue.grid(row=row_index, column=1, padx=(0, 20), pady=10)
    row_index += 1

    lblName = CTkLabel(master=frameEditDoctor, text="Name:", font=("Inter", 20), justify="left", anchor="w")
    lblName.grid(row=row_index, column=0, sticky="w", padx=20, pady=10)
    entryName = CTkEntry(master=frameEditDoctor, font=("Inter", 20), width=300, border_width=0, corner_radius=50)
    entryName.insert(0, doctor.get_name())
    entryName.grid(row=row_index, column=1, padx=(0, 20), pady=10)
    row_index += 1

    lblImage = CTkLabel(master=frameEditDoctor, text="Image:", font=("Inter", 20), justify="left", anchor="w")
    lblImage.grid(row=row_index, column=0, sticky="w", padx=20, pady=10)

    lblImageStatus = CTkLabel(master=frameEditDoctor,
                              text="Image has been selected" if doctor.get_image() else "No file selected",
                              font=("Inter", 20))
    lblImageStatus.grid(row=row_index, column=1, padx=(0, 20), pady=10)

    btnUploadImage = CTkButton(master=frameEditDoctor, text="Select Image", fg_color="gray",
                               command=lambda: uploadDoctor_image(lblImageStatus, doctor, lblImageStatus))
    btnUploadImage.grid(row=row_index, column=1, padx=10, pady=10, sticky='e')

    row_index += 1

    lblEmail = CTkLabel(master=frameEditDoctor, text="Email:", font=("Inter", 20), justify="left", anchor="w")
    lblEmail.grid(row=row_index, column=0, sticky="w", padx=20, pady=10)
    entryEmail = CTkEntry(master=frameEditDoctor, font=("Inter", 20), width=300, border_width=0, corner_radius=50)
    entryEmail.insert(0, doctor.get_email())
    entryEmail.grid(row=row_index, column=1, padx=(0, 20), pady=10)

    row_index += 1

    lblPhone = CTkLabel(master=frameEditDoctor, text="Phone No:", font=("Inter", 20), justify="left", anchor="w")
    lblPhone.grid(row=row_index, column=0, sticky="w", padx=20, pady=10)
    entryPhone = CTkEntry(master=frameEditDoctor, font=("Inter", 20), width=300, border_width=0, corner_radius=50)
    entryPhone.insert(0, doctor.get_phone_no())
    entryPhone.grid(row=row_index, column=1, padx=(0, 20), pady=10)

    row_index += 1

    lblQualification = CTkLabel(master=frameEditDoctor, text="Qualification:", font=("Inter", 20), justify="left",
                                anchor="w")
    lblQualification.grid(row=row_index, column=0, sticky="w", padx=20, pady=10)
    entryQualification = CTkEntry(master=frameEditDoctor, font=("Inter", 20), width=300, border_width=0,
                                  corner_radius=50)
    entryQualification.insert(0, doctor.get_qualification())
    entryQualification.grid(row=row_index, column=1, padx=(0, 20), pady=10)

    row_index += 1

    lblLanguage = CTkLabel(master=frameEditDoctor, text="Language:", font=("Inter", 20), justify="left", anchor="w")
    lblLanguage.grid(row=row_index, column=0, sticky="w", padx=20, pady=10)
    entryLanguage = CTkEntry(master=frameEditDoctor, font=("Inter", 20), width=300, border_width=0, corner_radius=50)
    entryLanguage.insert(0, doctor.get_language())
    entryLanguage.grid(row=row_index, column=1, padx=(0, 20), pady=10)

    row_index += 1

    lblAddress = CTkLabel(master=frameEditDoctor, text="Address:", font=("Inter", 20), justify="left", anchor="w")
    lblAddress.grid(row=row_index, column=0, sticky="w", padx=20, pady=10)
    entryAddress = CTkEntry(master=frameEditDoctor, font=("Inter", 20), width=300, border_width=0, corner_radius=50)
    entryAddress.insert(0, doctor.get_address())
    entryAddress.grid(row=row_index, column=1, padx=(0, 20), pady=10)

    row_index += 1

    lblSpecialty = CTkLabel(master=frameEditDoctor, text="Specialty:", font=("Inter", 20), justify="left", anchor="w")
    lblSpecialty.grid(row=row_index, column=0, sticky="w", padx=20, pady=10)
    entrySpecialty = CTkEntry(master=frameEditDoctor, font=("Inter", 20), width=300, border_width=0, corner_radius=50)
    entrySpecialty.insert(0, doctor.get_specialty())
    entrySpecialty.grid(row=row_index, column=1, padx=(0, 20), pady=10)

    row_index += 1

    workdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    workday_vars = {day: BooleanVar(value=day in doctor.get_workdays().split(", ")) for day in workdays}

    labelWorkDays = CTkLabel(master=frameEditDoctor, text="Work days:", font=("Inter", 20), justify="left", anchor="w")
    labelWorkDays.grid(row=row_index, column=0, sticky="w", padx=20, pady=10)
    row_index += 1

    for i, day in enumerate(workdays):
        chk = CTkCheckBox(master=frameEditDoctor, text=day, variable=workday_vars[day], onvalue=True, offvalue=False)
        chk.grid(row=row_index, column=i % 2, sticky="w", padx=20, pady=5)
        if i % 2 == 1:
            row_index += 1

    if i % 2 == 0:
        row_index += 1

    # save and delete doctor controls
    btnDelete = CTkButton(master=frameEditDoctor, text="Delete", fg_color="red", font=("Inter", 20, "bold"),
                          corner_radius=20, command=lambda: btnDeleteDoctor_Click(doctor, selected_clinic_id))
    btnDelete.grid(row=row_index, column=2, padx=10, sticky="e")

    btnSave = CTkButton(master=frameEditDoctor, text="Save", fg_color="#5271FF", font=("Inter", 20, "bold"),
                        corner_radius=20,
                        command=lambda: btnSaveDoctor_Click(doctor, doctor_id, entryName, lblImageStatus,
                                                            entryEmail, entryPhone,
                                                            entryQualification, entryLanguage,
                                                            entryAddress, entrySpecialty,
                                                            workday_vars))
    btnSave.grid(row=row_index, column=3, padx=10, sticky="e")

    frameEditDoctor.grid_rowconfigure(row_index, weight=1)
    frameEditDoctor.grid_columnconfigure(1, weight=1)

    frameDoctor.grid_remove()
    frameAppointment.grid_remove()


def uploadDoctor_image(label_status, doctor, lblImageStatus):
    global selected_image_path
    filename = filedialog.askopenfilename(title="Select a File",
                                          filetypes=(("PNG files", "*.png"),
                                                     ("JPG files", "*.jpg"),
                                                     ("JPEG files", "*.jpeg")))
    if filename:
        selected_image_path = filename  # Update the selected image path
        label_status.configure(text="Image has been selected", text_color="green")
        # Update doctor's image and display
        new_image_url = upload_doctor_image(filename, doctor.get_doctor_id(), label_status)
        if new_image_url:
            doctor.set_image(new_image_url)  # Update doctor object with new image URL
    else:
        label_status.configure(text="No file selected for upload.", text_color="red")


def btnSaveDoctor_Click(doctor, doctor_id, entryName, lblImageStatus, entryEmail, entryPhone, entryQualification,
                        entryLanguage, entryAddress, entrySpecialty, workdays_vars):
    print("Update doctor information")

    # Extract data from UI components
    name = entryName.get()
    email = entryEmail.get()
    phone_no = entryPhone.get()
    qualification = entryQualification.get()
    language = entryLanguage.get()
    address = entryAddress.get()
    specialty = entrySpecialty.get()

    # Convert workdays_vars dictionary to a comma-separated string of selected days
    workdays = ", ".join([day for day, var in workdays_vars.items() if var.get()])

    global selected_image_path

    # Check if a new image has been selected
    if lblImageStatus.cget("text") == "An image has been selected.":
        # If an image has been selected, upload it and get the new image path
        imageFile = upload_doctor_image(selected_image_path, doctor_id, lblImageStatus)
    else:
        # If no new image is selected, use the existing image
        imageFile = doctor.get_image()

    # Prepare updated data dictionary
    updated_data = {
        'Name': name,
        'Image': imageFile,
        'Email': email,
        'PhoneNo': int(phone_no),
        'Qualification': qualification,
        'Language': language,
        'Address': address,
        'Specialty': specialty,
        'WorkDays': workdays
    }

    # Update the doctor data in Firestore
    doctor_ref = db.collection('Doctors').document(doctor_id)
    doctor_ref.update(updated_data)
    print(f"Doctor {doctor_id} updated successfully.")

    # Display the update confirmation popup
    messagebox.showinfo("Update Successful", "Doctor information has been updated successfully.")

    # Relocate to btnDoctor_Click and display frameDoctor
    btnDoctor_Click(selected_clinic_id)


def btnDeleteDoctor_Click(doctor, selected_clinic_id):
    # Display a warning box to confirm deletion
    confirmation = messagebox.askokcancel("Confirmation",
                                          f"Are you sure you want to delete {doctor.get_name()} doctor information?")

    if confirmation:
        try:
            # User clicked 'OK', proceed with deletion
            doctor_ref = db.collection('Doctors').document(doctor.get_doctor_id())
            doctor_ref.delete()
            print(f"Doctor {doctor.get_doctor_id()} deleted successfully.")
            btnDoctor_Click(selected_clinic_id)

        except Exception as e:
            print(f"An error occurred while deleting the doctor: {e}")
            messagebox.showerror("Error", f"Failed to delete doctor: {e}")
    else:
        # User clicked 'Cancel', navigate back to the list of doctors
        btnDoctor_Click(selected_clinic_id)


def clear_entry(event):
    event.widget.delete(0, "end")


def btnClinic_Click(clinic_id):
    global selected_clinic_id
    global frameClinic
    global navBtnFrame
    global frameDoctor
    global frameAppointment
    global framePatient
    global frameEditDoctor
    global frameDeclineAppointment
    global frameHome

    selected_clinic_id = clinic_id

    # Display and hide frames
    frameClinic.grid()
    navBtnFrame.grid()
    frameDoctor.grid_remove()
    frameAppointment.grid_remove()
    framePatient.grid_remove()
    frameEditDoctor.grid_remove()
    frameDeclineAppointment.grid_remove()

    # Clear existing widgets in frameClinic
    for widget in frameClinic.winfo_children():
        widget.destroy()

    try:
        clinic_doc = db.collection('Clinics').document(clinic_id).get()
        if clinic_doc.exists:
            clinic_data = clinic_doc.to_dict()

            # Create a Clinic object with the retrieved data
            clinic = Clinic(
                clinic_Id=clinic_id,
                name=clinic_data.get('Name', 'N/A'),
                image=clinic_data.get('Image', 'N/A'),  # Assuming 'Image' is the field name for image path
                address=clinic_data.get('Address', 'N/A'),
                email=clinic_data.get('Email', 'N/A'),
                phone_no=clinic_data.get('PhoneNo', 'N/A'),
                specialty=clinic_data.get('Specialty', 'N/A'),
                work_days=clinic_data.get('WorkDays', 'N/A'),
                start_hours=clinic_data.get('StartHours', 'N/A'),
                end_hours=clinic_data.get('EndHours', 'N/A'),
                start_break_hours=clinic_data.get('StartBreak', 'N/A'),
                end_break_hours=clinic_data.get('EndBreak', 'N/A'),
                description=clinic_data.get('Description', 'N/A')
            )

            # Configure grid to make it responsive
            for i in range(6):
                frameClinic.grid_columnconfigure(i, weight=1)

            row_index = 0

            # Fetch clinic image from Firestore if available
            if clinic.get_image():
                image_path = clinic.get_image()
                bucket = storage.bucket()
                blob = bucket.blob(image_path)
                if blob.exists():
                    try:
                        # Download the image as bytes and convert to an array
                        image_bytes = blob.download_as_bytes()
                        np_image = np.frombuffer(image_bytes, np.uint8)
                        img = cv2.imdecode(np_image, cv2.IMREAD_COLOR)
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                        # Convert to PIL Image
                        pil_img = Image.fromarray(img)
                        pil_img = pil_img.resize((200, 200), Image.LANCZOS)

                        # Add rounded corners to the image
                        pil_img = addRoundedCorners(pil_img, 10)

                        # Convert PIL Image to PhotoImage
                        clinic_image = ImageTk.PhotoImage(pil_img)

                        lbl_clinic_image = CTkLabel(
                            master=frameClinic, text="", image=clinic_image,
                            bg_color="transparent", width=200, height=150
                        )
                        lbl_clinic_image.image = clinic_image  # Keep reference
                        lbl_clinic_image.grid(row=row_index, column=0, columnspan=5, sticky="ew", padx=10, pady=0)

                    except Exception as e:
                        print(f"Error displaying clinic image: {e}")
                else:
                    print(f"Image blob does not exist for clinic_id: {clinic_id}")
            else:
                print(f"No valid image path found for clinic_id: {clinic_id}")

            # Display other clinic information
            clinic_info = (
                "Name: {}\n"
                "Clinic user ID: {}\n"
                "Specialty: {}\n"
                "Description: {}\n"
                "Phone No.: {}\n"
                "Working hours: {} - {}\n"
                "Break hours: {} - {}\n"
                "Workdays: {}\n"
                "Email address: {}\n"
                "Address: {}\n"
            ).format(
                clinic.get_name(),
                clinic.get_clinic_Id(),
                clinic.get_specialty(),
                clinic.get_description().replace(',', ',\n'),
                clinic.get_phone_no(),
                clinic.get_start_hours(),
                clinic.get_end_hours(),
                clinic.get_start_break_hours(),
                clinic.get_end_break_hours(),
                clinic.get_work_days(),
                clinic.get_email(),
                clinic.get_address()
            )
            row_index += 1

            btn_edit = CTkButton(
                master=frameClinic, text="Edit", fg_color="#5271FF", font=("Inter", 20, "bold"),
                corner_radius=20, width=10,
                command=lambda: btnEditClinic_click(clinic)
            )
            btn_edit.grid(row=row_index, column=2, pady=20, sticky="new")

            row_index += 1

            lbl_clinics = CTkLabel(
                master=frameClinic, text=clinic_info, width=550, height=0, corner_radius=0,
                fg_color="#DCC6FF", text_color="#5D5D5D", font=("Inter", 20), justify="left", anchor="w"
            )
            lbl_clinics.grid(row=row_index, column=0, columnspan=6, sticky="ew", padx=10, pady=0)

            row_index += 1

            # Ensure the parent frame has proper configuration to center its content
            frameHome.grid_columnconfigure(0, weight=1)
        else:
            print(f"No document found for clinic_id: {clinic_id}")
    except Exception as e:
        print(f"Error fetching clinic data: {e}")


def toggle_entries(var, start_work_hour, end_work_hour, start_break_hour, end_break_hour):
    state = 'normal' if var.get() == 1 else 'disabled'
    start_work_hour.configure(state=state)
    end_work_hour.configure(state=state)
    start_break_hour.configure(state=state)
    end_break_hour.configure(state=state)


def btnEditClinic_click(clinic):
    global selected_clinic_id
    global frameClinic
    global frameTimeTable
    global navBtnFrame

    print(f"Edit Clinic Button Clicked for clinic_id: {selected_clinic_id}")

    # Display the clinic frame and hide other frames
    frameClinic.grid()
    navBtnFrame.grid()
    frameTimeTable.grid_remove()  # Remove the frame first to clear existing widgets
    frameTimeTable.grid()

    # Clear existing widgets in frameClinic
    for widget in frameClinic.winfo_children():
        widget.destroy()

    try:
        # Configure grid columns for frameClinic
        for i in range(8):
            frameClinic.grid_columnconfigure(i, weight=1)

        row_index = 0

        btnBack = CTkButton(
            master=frameClinic, text="", fg_color="transparent",
            image=CTkImage(imgBtnBack, size=(30, 30)),
            width=50, height=50, corner_radius=0,
            command=lambda: confirm_back_clinic(selected_clinic_id)
        )
        btnBack.grid(row=row_index, column=0, padx=20, pady=(10, 5), sticky="w")

        row_index += 1

        # Entry fields for clinic information
        entryName = add_clinic_label_entry(row_index, "Name:", clinic.get_name())
        row_index += 1

        # Image Label, Status Label, and Upload Button
        lblImage = CTkLabel(master=frameClinic, text="Image:", font=("Inter", 20), justify="left", anchor="w")
        lblImage.grid(row=row_index, column=0, sticky="w", padx=20, pady=10)

        lblImageStatus = CTkLabel(master=frameClinic,
                                  text="Image has been selected" if clinic.get_image() else "No file selected",
                                  font=("Inter", 20))
        lblImageStatus.grid(row=row_index, column=1, padx=(130, 0), pady=10)

        btnUploadImage = CTkButton(master=frameClinic, text="Select Image", fg_color="gray",
                                   command=lambda: uploadClinic_image(lblImageStatus, clinic, lblImageStatus))
        btnUploadImage.grid(row=row_index, column=2, padx=20, pady=10)
        row_index += 1

        entryAddress = add_clinic_label_entry(row_index, "Address:", clinic.get_address())
        row_index += 1
        entryEmail = add_clinic_label_entry(row_index, "Email address:", clinic.get_email())
        row_index += 1
        entryPhone = add_clinic_label_entry(row_index, "Phone No.:", clinic.get_phone_no())
        row_index += 1
        entrySpecialty = add_clinic_label_entry(row_index, "Specialty:", clinic.get_specialty())
        row_index += 1
        entryDescription = add_clinic_label_entry(row_index, "Description:", clinic.get_description())
        row_index += 1

        # Dropdown lists for hours and minutes
        hours = [f"{i:02}" for i in range(1, 25)]
        minutes = [f"{i:02}" for i in range(0, 60, 5)]

        def add_time_selector(row_index, label_text, initial_time):
            label = CTkLabel(master=frameClinic, text=label_text, font=("Inter", 20), justify="left", anchor="w")
            label.grid(row=row_index, column=0, sticky="w", padx=20, pady=10)

            initial_hours, initial_minutes = initial_time.split(":")

            time_frame = CTkFrame(master=frameClinic, fg_color="transparent")
            time_frame.grid(row=row_index, column=1, columnspan=3, padx=(150, 0), pady=10, sticky="w")

            hours_combo = CTkComboBox(master=time_frame, values=hours, width=100)
            hours_combo.set(initial_hours)
            hours_combo.pack(side="left")

            colon_label = CTkLabel(master=time_frame, text=":", font=("Inter", 20))
            colon_label.pack(side="left")

            minutes_combo = CTkComboBox(master=time_frame, values=minutes, width=100)
            minutes_combo.set(initial_minutes)
            minutes_combo.pack(side="left")

            return hours_combo, minutes_combo

        # Entry fields for clinic work schedule
        startWorkHour, startWorkMinute = add_time_selector(row_index, "Start working hours:", clinic.get_start_hours())
        row_index += 1
        endWorkHour, endWorkMinute = add_time_selector(row_index, "End working hours:", clinic.get_end_hours())
        row_index += 1
        startBreakHour, startBreakMinute = add_time_selector(row_index, "Start break hours:",
                                                             clinic.get_start_break_hours())
        row_index += 1
        endBreakHour, endBreakMinute = add_time_selector(row_index, "End break hours:", clinic.get_end_break_hours())
        row_index += 1

        # Work days checkboxes
        workdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        workday_vars = {day: BooleanVar(value=day in clinic.get_work_days().split(", ")) for day in workdays}

        labelWorkDays = CTkLabel(master=frameClinic, text="Work days:", font=("Inter", 20), justify="left",
                                 anchor="w")
        labelWorkDays.grid(row=row_index, column=0, sticky="w", padx=20, pady=10)
        row_index += 1

        for i, day in enumerate(workdays):
            chk = CTkCheckBox(master=frameClinic, text=day, variable=workday_vars[day], onvalue=True,
                              offvalue=False)
            chk.grid(row=row_index, column=i % 2, sticky="w", padx=20, pady=5)
            if i % 2 == 1:
                row_index += 1

        if i % 2 == 0:
            row_index += 1

        # Save button
        btnSave = CTkButton(master=frameClinic, text="Save", fg_color="#5271FF", font=("Inter", 20, "bold"),
                            corner_radius=20,
                            command=lambda: btnSaveClinic_Click(
                                clinic.get_clinic_Id(),
                                entryName,
                                lblImageStatus,
                                entryAddress,
                                entryEmail,
                                entryPhone,
                                entrySpecialty,
                                entryDescription,
                                workday_vars,
                                f"{startWorkHour.get()}:{startWorkMinute.get()}",
                                f"{endWorkHour.get()}:{endWorkMinute.get()}",
                                f"{startBreakHour.get()}:{startBreakMinute.get()}",
                                f"{endBreakHour.get()}:{endBreakMinute.get()}"
                            ))
        btnSave.grid(row=row_index, column=5, pady=20, padx=(0, 20), sticky="e")

    except Exception as e:
        print("Error fetching clinic data:", str(e))


def btnSaveClinic_Click(clinic_id, entryName, lblImageStatus, entryAddress, entryEmail, entryPhone, entrySpecialty,
                        entryDescription, workday_vars, start_work_time, end_work_time, start_break_time,
                        end_break_time):
    global frameClinic

    # Handle image upload status
    if lblImageStatus.cget("text") == "Image has been selected":
        new_image_path = upload_clinic_image(selected_image_path, clinic_id, lblImageStatus)
    else:
        new_image_path = None

    try:
        # Prepare the work days
        work_days = ', '.join(day for day in workday_vars if workday_vars[day].get())

        # Fetch current clinic data from Firestore
        clinic_doc = db.collection('Clinics').document(clinic_id).get()
        if clinic_doc.exists:
            clinic_data = clinic_doc.to_dict()

            # Extract values from CTkEntry widgets
            updated_data = {
                'Name': entryName.get(),
                'Address': entryAddress.get(),
                'Email': entryEmail.get(),
                'PhoneNo': entryPhone.get(),
                'Specialty': entrySpecialty.get(),
                'Description': entryDescription.get(),
                'Image': new_image_path if new_image_path else clinic_data.get('Image'),
                'StartHours': start_work_time,
                'EndHours': end_work_time,
                'StartBreak': start_break_time,
                'EndBreak': end_break_time,
                'WorkDays': work_days
            }

            # Update only if there are changes in the data
            if any(value != clinic_data.get(key) for key, value in updated_data.items()):
                # Perform the Firestore update
                db.collection('Clinics').document(clinic_id).update(updated_data)
                print("Clinic data saved successfully")
            else:
                print("No changes detected. Data not updated for time table")

            # Clear existing widgets in the clinic frame
            for widget in frameClinic.winfo_children():
                widget.destroy()

            # Refresh the clinic information
            btnClinic_Click(clinic_id)

        else:
            print(f"No document found for clinic_id: {clinic_id}")

    except Exception as e:
        print(f"Error updating clinic data: {e}")


def confirm_back_clinic(clinic_id):
    if messagebox.askyesno("Confirmation", f"Do you want to discard changes for clinic information?"):
        btnClinic_Click(selected_clinic_id)


def add_clinic_label_entry(row_index, label_text, entry_text):
    lbl = CTkLabel(master=frameClinic, text=label_text, font=("Inter", 20), justify="left", anchor="w")
    lbl.grid(row=row_index, column=0, sticky="w", padx=20, pady=10)

    entry = CTkEntry(master=frameClinic, width=500, height=35, font=("Inter", 20), corner_radius=10)
    entry.insert(0, entry_text)
    entry.grid(row=row_index, column=1, columnspan=3, padx=(0, 20), pady=10)
    return entry


def delete_clinic_images(clinic_id):
    try:
        bucket = storage.bucket()
        blobs = bucket.list_blobs(prefix=f"Clinic/{clinic_id}")

        for blob in blobs:
            blob.delete()
            print(f"Deleted old image: {blob.name}")

    except Exception as e:
        print(f"Error deleting images: {e}")


def uploadClinic_image(label_status, clinic, lblImageStatus):
    global selected_image_path
    filename = filedialog.askopenfilename(title="Select a File",
                                          filetypes=(("PNG files", "*.png"),
                                                     ("JPG files", "*.jpg"),
                                                     ("JPEG files", "*.jpeg")))
    if filename:
        selected_image_path = filename
        label_status.configure(text="Image has been selected", text_color="green")
        # Update clinic's image and display
        current_image_url = clinic.get_image()
        new_image_path = upload_clinic_image(filename, clinic.get_clinic_Id(), label_status, current_image_url)
        if new_image_path:
            clinic.set_image(new_image_path)  # Update clinic object with new image path
    else:
        label_status.configure(text="No file selected for upload.", text_color="red")


def upload_clinic_image(file_path, clinic_id, label_status, current_image_url=None):
    global imageFile
    if file_path:
        file_extension = file_path.split('.')[-1]
        imageFile = f"Clinics/{clinic_id}.{file_extension}"

        bucket = storage.bucket()
        blob = bucket.blob(imageFile)

        try:
            blob.upload_from_filename(file_path)
            blob.make_public()
            print("Your file URL:", blob.public_url)

            label_status.configure(text="An image has been selected.", text_color="green")
            return imageFile  # Return the uploaded image path
        except Exception as e:
            print("Error uploading file:", e)
            label_status.configure(text="An image has not been selected.", text_color="red")
    else:
        print("No file selected for upload.")
        label_status.configure(text="No file selected for upload.", fg_color="red")

    return None


# Function for opening the file explorer window
def browseClinicFiles(label_status, doctor_id):
    filename = filedialog.askopenfilename(title="Select a File",
                                          filetypes=(("PNG files", "*.png"),
                                                     ("JPG files", "*.jpg"),
                                                     ("JPEG files", "*.jpeg")))
    if filename:

        label_status.configure(text="Image selected", text_color="green")
        upload_clinic_image(filename, doctor_id, label_status)
    else:
        label_status.configure(text="No image selected", text_color="red")


def create_ClinicPg(master):
    global frameDeclineAppointment
    global frameAppointment
    global navBtnFrame
    global imgBtnBack
    global frameClinic
    global frameTimeTable
    global frameDoctor
    global frameEditClinic
    global framePatient
    global frameEditDoctor
    global frameHome

    # Frames
    frameHome = CTkFrame(master=master, fg_color="#B5CAFF")
    frameHome.grid_columnconfigure(0, weight=1)
    frameHome.grid_rowconfigure(0, weight=0)

    # Create a frame for the toolbar and the label
    toolbar_label_frame = CTkFrame(master=frameHome, fg_color="transparent")
    toolbar_label_frame.grid(row=1, column=0, sticky="ew")
    toolbar_label_frame.grid_columnconfigure(0, weight=1)

    # Create a frame to hold the label and button
    navBtnFrame = CTkFrame(master=toolbar_label_frame, fg_color="transparent")
    navBtnFrame.grid(row=0, column=1, padx=(5, 0), pady=0)

    # Clinic View Label with blue background
    lblClinicView = CTkLabel(master=toolbar_label_frame, text="Clinic View", font=("Inter", 30, "bold"),
                             text_color="#5D5D5D")
    lblClinicView.grid(row=0, column=0, sticky="w", pady=(0, 5), padx=(0, 0))

    # Create a large frame below the navigation bar
    frameAppointment = CTkScrollableFrame(master=frameHome, fg_color="#FFF9BE", )  # Adjust color as needed
    frameAppointment.grid(row=2, column=0, sticky="nsew", pady=0)  # Use sticky="nsew" to fill height and width

    framePatient = CTkScrollableFrame(master=frameHome, fg_color="#FFF9BE", )  # Adjust color as needed
    framePatient.grid(row=2, column=0, sticky="nsew", pady=0)  # Use sticky="nsew" to fill height and width

    frameDoctor = CTkScrollableFrame(master=frameHome, fg_color="#C8FFD4", height=900,
                                     orientation="vertical", )  # Adjust color as needed
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

    frameButton = CTkScrollableFrame(master=frameEditClinic, fg_color="transparent")
    frameButton.grid(row=2, column=0, sticky="nsew")
    frameButton.grid_remove()

    frameSearchBar = CTkFrame(master=frameAppointment, fg_color="#FFF9BE", corner_radius=0)
    frameSearchBar.grid(row=1, column=0, sticky="ew")
    frameSearchBar.grid_columnconfigure(0, weight=1)

    frameDeclineAppointment = CTkScrollableFrame(master=frameHome, fg_color="#FFF9BE",
                                                 height=900)  # Adjust color as needed
    frameDeclineAppointment.grid(row=2, column=0, sticky="sew", pady=0)  # Fill the remaining space in the frame
    frameDeclineAppointment.grid_remove()

    btnAppointment_Click(ClinicId)
    document_name = "CAD DB"
    sheet_name = "AppointmentDetails"

    frameHome.grid_columnconfigure(0, weight=1)
    frameHome.grid_rowconfigure(2, weight=1)
    # Configure row and column weights to allow children to expand
    frameAppointment.grid_rowconfigure(0, weight=1)
    frameAppointment.grid_columnconfigure(2, weight=1)

    framePatient.grid_rowconfigure(0, weight=1)
    framePatient.grid_columnconfigure(2, weight=1)

    frameDoctor.grid_rowconfigure(0, weight=1)
    frameDoctor.grid_columnconfigure(0, weight=1)

    frameClinic.grid_columnconfigure(0, weight=1)
    frameClinic.grid_columnconfigure(0, weight=1)

    frameEditClinic.grid_rowconfigure(0, weight=1)
    frameEditClinic.grid_columnconfigure(0, weight=1)

    # Adding the Navigation Toolbar inside the toolbar_label_frame
    # Create a label for the image inside the frame
    imgBtnBack = Image.open("./SE Project/Images/back.png")
    imgBtnSchedule = Image.open("./SE Project/Images/schedule-blue.png")

    navBtnAppointment = CTkButton(master=navBtnFrame, text="Appointments", text_color="#5271FF",
                                  command=lambda: btnAppointment_Click(ClinicId),
                                  image=CTkImage(imgBtnSchedule, size=(40, 40)),
                                  fg_color="#FFF9BE", font=("Inter", 20, "bold"), width=50, height=50, corner_radius=0)

    # Place the button in the toolbar
    navBtnAppointment.grid(row=0, column=1, padx=0, pady=0)

    imgBtnDoctor = Image.open("./SE Project/Images/doctor-blue.png")

    # Create the button inside the frame
    navBtnDoctor = CTkButton(master=navBtnFrame, text="Doctors", text_color="#5271FF",
                             image=CTkImage(imgBtnDoctor, size=(30, 30)),
                             command=lambda: btnDoctor_Click(ClinicId),
                             fg_color="#C8FFD4", font=("Inter", 20, "bold"), width=50, height=50, corner_radius=0)

    # Place the button in the toolbar
    navBtnDoctor.grid(row=0, column=2, padx=0, pady=0)

    # Create the button with the image and label

    # Add the image to the button
    imgBtnClinic = Image.open("./SE Project/Images/clinic-blue.png")

    # Create the button with the image and label
    navBtnClinic = CTkButton(master=navBtnFrame, text="Clinic Settings", text_color="#5271FF",
                             command=lambda: btnClinic_Click(ClinicId),
                             image=CTkImage(imgBtnClinic, size=(30, 30)),
                             fg_color="#DCC6FF", font=("Inter", 20, "bold"), width=50, height=50, corner_radius=0)

    # Place the button in the toolbar
    navBtnClinic.grid(row=0, column=3, padx=0, pady=0)

    return frameHome
# Run the application
# app.mainloop()
