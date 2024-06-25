from customtkinter import *
import firebase_admin
from firebase_admin import credentials, storage
from firebase_admin import firestore
from tkinter import messagebox
from PIL import Image
import pickle
import webbrowser
from datetime import datetime, timedelta

cred = credentials.Certificate("serviceAccountKey.json")
# Check if firebase_admin has been initialized
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {'storageBucket':'call-a-doctor-20a5d.appspot.com'})

db = firestore.client()

# Global variable to store frameBookHis reference
frameBookHis = None
frameInitialPg = None
frameAppointmentList = None
lblApStatus = None
lblAppointmentId = None
frameAppointmentIndiv = None

pickleFile = 'userId.pkl'

def checkCurrentUser(pickleFile):
    if os.path.exists(pickleFile) and os.path.getsize(pickleFile) > 0:
        try:
            with open(pickleFile, 'rb') as f:
                pickledData = pickle.load(f)
                if pickledData is not None:
                    currentUser, role = map(str.strip, pickledData.split(','))
                else:
                    currentUser = ""
                    role = ""
        except (EOFError, pickle.UnpicklingError) as e:
            print(f"Error reading '{pickleFile}': {e}")
            currentUser = ""
            role = ""
    else:
        currentUser = ""
        role = ""
        print(f"'The pickle file {pickleFile}' does not exist or is empty.")

    return currentUser, role

def dropSearch_Filter(filter):
    global frameInitialPg
    currentUser, role = checkCurrentUser(pickleFile)
    
    if filter == "Any Time":
        appointmentsRef = db.collection('AppointmentDetails').where('PatientId', '==', currentUser)
    else:
        appointmentsRef = db.collection('AppointmentDetails').where('PatientId', '==', currentUser)
    
    displayAppointments(appointmentsRef)

def btnSearch_Click():
    print("Button Clicked")

# Function to display the list of appointments
def displayAppointments(appointmentsRef):
    global frameInitialPg
    global frameAppointmentList
    global lblApStatus
    global btnAppointment_Click

    docs = appointmentsRef.stream()

    # Prepare the data
    appointmentData = []
    for doc in docs:
        appointment = doc.to_dict()
        appointment['AppointmentId'] = doc.id
        appointmentData.append(appointment)

    rowIndex = 3
    
    # Display each appointment data
    for appointment in appointmentData:
        # Prepare appointment information

        status = appointment.get('Status', 'N/A')
        appointmentInfo = (
            f"{appointment['AppointmentId']}\n\n"
            f"Time: {appointment.get('DateTime', 'N/A')}\n"
            f"Type: {appointment.get('AppointmentType', 'N/A')}\n"
            f"Medical Concern: {appointment.get('MedicalConcern', 'N/A')}\n"
        )

        if status == "Completed":
            appointmentInfo += f"Prescription: {appointment.get('Prescription', 'N/A')}\n" 

        # Create a frame for each appointment
        frameAppointmentList = CTkFrame(master=frameInitialPg, bg_color="transparent", fg_color="transparent")
        frameAppointmentList.grid(row=rowIndex, column=0, sticky="new", padx=47, pady=10)
        frameAppointmentList.grid_columnconfigure(0, weight=1)

        # Add text label
        lblTextAppointment = CTkLabel(master=frameAppointmentList, text=appointmentInfo, height=150, corner_radius=20, 
                                      fg_color="white", bg_color="transparent", text_color="#5D5D5D", font=("Inter", 20), justify="left", anchor="w")
        lblTextAppointment.grid(row=0, column=0, sticky="ew")

        lblApStatus = CTkLabel(master=frameAppointmentList, text=status, fg_color="white", bg_color="transparent", 
                               text_color="#5D5D5D", font=("Inter", 20))
        lblApStatus.grid(row=0, column=0, sticky="e", padx=(0,20))
        
        if status == "Rejected":
            lblApStatus.configure(text_color="red")
        elif status == "Accepted":
            lblApStatus.configure(text_color="green")
        elif status == "Pending":
            lblApStatus.configure(text_color="orange")
        else:
            lblApStatus.configure(text_color="#5D5D5D")

        # Bind click event to the frame
        frameAppointmentList.bind("<Button-1>", lambda e, a=appointment: btnAppointment_Click(a))
        lblTextAppointment.bind("<Button-1>", lambda e, a=appointment: btnAppointment_Click(a))
        lblApStatus.bind("<Button-1>", lambda e, a=appointment: btnAppointment_Click(a))

        rowIndex += 1

def btnBack_Click():
    frameAppointmentIndiv.grid_forget()
    frameInitialPg.grid(row=0, column=0, sticky="news")

def btnCancelAppointment_Click():
    global frameInitialPg
    global frameAppointmentIndiv
    global lblAppointmentId
    
    # Ask for confirmation
    response = messagebox.askyesno("Cancel Appointment", "Are you sure you want to cancel this appointment?")
    
    if response:  # If user clicked 'Yes'
        try:
            # Proceed with cancellation logic
            # Retrieve the text from the label
            appointmentText = lblAppointmentId.cget("text")

            # Remove "Appointment Id:" and strip whitespace
            appointmentId = appointmentText.replace("Appointment Id:", "").strip()
            
            db.collection('AppointmentDetails').document(appointmentId).update({"Status": "Cancelled"})
            messagebox.showinfo("Cancelled", "The appointment has been cancelled successfully.")
            # Refresh the appointment list and return to initial page
            frameAppointmentIndiv.grid_forget()
            frameInitialPg.grid(row=0, column=0, sticky="news")
            dropSearch_Filter("Any Time")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while cancelling the appointment: {e}")
    else:
        # User clicked 'No', do nothing
        pass

# Function to open the document in a web browser.
def openDocument(medicalDocs):
    bucket = storage.bucket()
    try:
        # Get the download URL for the document from Firebase Storage
        blob = bucket.blob(medicalDocs)

        # Set expiry time for the URL (e.g., 1 day from now)
        expiryTime = datetime.now() + timedelta(days=1)
        downloadUrl = blob.generateSignedUrl(expiration=expiryTime)

        # Open the document in the default web browser
        webbrowser.open(downloadUrl)
    
    except Exception as e:
        print(f"Error opening document: {e}")

def create_BookHis(master):
    global frameBookHis
    global frameInitialPg
    global frameAppointmentList
    global lblApStatus
    global lblAppointmentId
    global frameAppointmentIndiv
    global btnAppointment_Click
    
    # Frames
    frameBookHis = CTkFrame(master=master, fg_color="#B5CAFF", corner_radius=0)
    frameBookHis.grid_columnconfigure(0, weight=1)
    frameBookHis.grid_rowconfigure(0, weight=1)

    frameInitialPg = CTkScrollableFrame(master=frameBookHis, fg_color="#B5CAFF", corner_radius=0, orientation="vertical", 
                                    scrollbar_button_color="white")
    frameInitialPg.grid(row=0, column=0, sticky="news")
    frameInitialPg.grid_columnconfigure(0, weight=1)
    frameInitialPg.grid_rowconfigure(0, weight=1)

    frameAppointmentIndiv = CTkScrollableFrame(master=frameBookHis, fg_color="#B5CAFF", corner_radius=0, orientation="vertical", 
                                    scrollbar_button_color="white")
    frameAppointmentIndiv.grid_columnconfigure(0, weight=1)
    frameAppointmentIndiv.grid_rowconfigure(0, weight=1)

    # Search Bar
    dropSearch = CTkOptionMenu(master=frameInitialPg, values=["Any Time", "Last Week", "Last Month"], fg_color="white", dropdown_fg_color="white",
                            button_color="white", button_hover_color="white", width=206, height=59, anchor="center",
                            corner_radius=20, font=("Inter",20), text_color="#898989", command=dropSearch_Filter)
    dropSearch.grid(row=0, column=0, sticky="nw", padx=47, pady=40)

    tbSearch = CTkEntry(master=frameInitialPg, fg_color="white", width=700, height=59, corner_radius=20, font=("Inter",15), 
                        text_color="black", border_width=0)
    tbSearch.grid(row=0, column=0, sticky="new", padx=(238,47), pady=40)

    lblBehindSearch = CTkLabel(master=frameInitialPg, text="|", font=("Inter",28), text_color="#5271FF", bg_color="white", width=18, 
                                height=59)
    lblBehindSearch.grid(row=0, column=0, sticky="nw", padx=237, pady=40)

    imgBtnSearch = Image.open("./SE Project/Images/search.png")
    BtnSearch = CTkButton(master=frameInitialPg, text="", image=CTkImage(imgBtnSearch, size=(25,25)), 
                        fg_color="white", corner_radius=0, anchor="center", width=25, command=btnSearch_Click)
    BtnSearch.grid(row=0, column=0, sticky="ne", padx=60, pady=55)  

    lblBookHisText = CTkLabel(master=frameInitialPg, text="Booking History", font=("Inter",30,"bold"), text_color="#5271FF",
                              bg_color="transparent", fg_color="transparent")
    lblBookHisText.grid(row=1, column=0, sticky="ew")

    imglblLineBookHis = Image.open("./SE Project/Images/line.png")
    lblLineBookHis = CTkLabel(master=frameInitialPg, text="", image=CTkImage(imglblLineBookHis, size=(800,1)), bg_color="transparent")
    lblLineBookHis.grid(row=2, column=0, columnspan=2, sticky="ew", padx=100, pady=5)

    def btnAppointment_Click(appointment):
        print(f"Appointment clicked: {appointment['AppointmentId']}")

        frameInitialPg.grid_forget()
        frameAppointmentIndiv.grid(row=0, column=0, sticky="news")

        # Fetch data from the referenced collections
        patientId = appointment.get('PatientId')
        clinicId = appointment.get('ClinicId')
        doctorId = appointment.get('DoctorId')

        patientDoc = db.collection('Patients').document(patientId).get()
        clinicDoc = db.collection('Clinics').document(clinicId).get()
        doctorDoc = db.collection('Doctors').document(doctorId).get()

        if patientDoc.exists:
            patientData = patientDoc.to_dict()
        else:
            patientData = {}

        if clinicDoc.exists:
            clinicData = clinicDoc.to_dict()
        else:
            clinicData = {}

        if doctorDoc.exists:
            doctorData = doctorDoc.to_dict()
        else:
            doctorData = {}

        # Populate the clicked on appointment's details frame with the retrieved data
        lblAppointmentId.configure(text=f"Appointment Id: {appointment.get('AppointmentId', 'N/A')}")
        lblAppointmentType.configure(text=f"Type: {appointment.get('AppointmentType', 'N/A')}")
        lblAppointmentDateTime.configure(text="Date & Time: "+appointment.get('DateTime', 'N/A'))
        lblMedicalConcern.configure(text="Medical Concern: "+appointment.get('MedicalConcern', 'N/A'))
        medicalDocs = appointment.get('MedicalDocs', 'N/A')
         # Check if medicalDocs is a valid path in Firebase Storage
        if medicalDocs.startswith("MedicalDocs/"):
            # Create a button to view the document
            btnMedicalDocs = CTkButton(master=frameAppointmentIndiv, text="View Related Document(s)", font=("Inter",20,"bold"),
                                    fg_color="#5271FF",command=lambda: openDocument(medicalDocs), anchor="w")
            btnMedicalDocs.grid(row=11, column=0, sticky="w", padx=50)
        else:
            # Display medicalDocs as plain text
            lblMedicalDocs.configure(text=f"Medical Documents: {medicalDocs}")
        lblPrescription.configure(text="Prescription: "+appointment.get('Prescription', 'N/A'))

        status = appointment.get('Status', 'N/A')
        lblStatus.configure(text="Status: "+status)

        if status == "Pending":
            btnCancelAppointment.grid(row=17, column=0, sticky="e", padx=50, pady=30)
        else:
            btnCancelAppointment.grid_forget()

        lblPatientName.configure(text="Name: "+patientData.get('Name', 'N/A'))
        lblPatientPhone.configure(text=f"Phone No: {patientData.get('PhoneNo', 'N/A')}")
        lblPatientAddress.configure(text="Address: "+patientData.get('Address', 'N/A'))

        lblClinicName.configure(text="Clinic: "+clinicData.get('Name', 'N/A'))

        lblDoctorName.configure(text="Name: "+doctorData.get('Name', 'N/A'))
        lblDoctorSpecialty.configure(text="Specialty: "+doctorData.get('Specialty', 'N/A'))
        lblDoctorPhone.configure(text=f"Phone No: {doctorData.get('PhoneNo', 'N/A')}")

    # Widgets for the individual appointment page
    imgBtnBack = Image.open("./SE Project/Images/back.png")
    btnBack = CTkButton(master=frameAppointmentIndiv, text="", image=CTkImage(imgBtnBack, size=(25,25)), corner_radius=20,
                         fg_color="transparent", width=0, command=btnBack_Click)
    btnBack.grid(row=0, column=0, sticky="nw", pady=20)

    # Appointment information
    lblAppointmentInfo = CTkLabel(master=frameAppointmentIndiv, text="Appointment Information:", font=("Inter",20,"bold"), 
                                  text_color="#5271FF", fg_color="transparent", anchor="w")
    lblAppointmentInfo.grid(row=1, column=0, sticky="we", padx=50, pady=(20,0))

    lblAppointmentId = CTkLabel(master=frameAppointmentIndiv, text="", font=("Inter",20), text_color="#5D5D5D",
                              fg_color="transparent", anchor="w")
    lblAppointmentId.grid(row=2, column=0, sticky="we", padx=50)
    
    lblAppointmentType = CTkLabel(master=frameAppointmentIndiv, text="", font=("Inter",20), text_color="#5D5D5D",
                              fg_color="transparent", anchor="w")
    lblAppointmentType.grid(row=3, column=0, sticky="we", padx=50)
    
    lblAppointmentDateTime = CTkLabel(master=frameAppointmentIndiv, text="", font=("Inter",20), text_color="#5D5D5D",
                              fg_color="transparent", anchor="w")
    lblAppointmentDateTime.grid(row=4, column=0, sticky="we", padx=50)

    lblClinicName = CTkLabel(master=frameAppointmentIndiv, text="", font=("Inter",20), text_color="#5D5D5D",
                              fg_color="transparent", anchor="w")
    lblClinicName.grid(row=5, column=0, sticky="we", padx=50)

    # Patient Information
    lblPatientInfo = CTkLabel(master=frameAppointmentIndiv, text="Patient Information:", font=("Inter",20, "bold"), 
                              text_color="#5271FF", fg_color="transparent", anchor="w")
    lblPatientInfo.grid(row=6, column=0, sticky="we", padx=50, pady=(20,0))

    lblPatientName = CTkLabel(master=frameAppointmentIndiv, text="", font=("Inter",20), text_color="#5D5D5D",
                              fg_color="transparent", anchor="w")
    lblPatientName.grid(row=7, column=0, sticky="we", padx=50)

    lblPatientPhone = CTkLabel(master=frameAppointmentIndiv, text="", font=("Inter",20), text_color="#5D5D5D",
                              fg_color="transparent", anchor="w")
    lblPatientPhone.grid(row=8, column=0, sticky="we", padx=50)

    lblPatientAddress = CTkLabel(master=frameAppointmentIndiv, text="", font=("Inter",20), text_color="#5D5D5D",
                              fg_color="transparent", anchor="w")
    lblPatientAddress.grid(row=9, column=0, sticky="we", padx=50)

    lblMedicalConcern = CTkLabel(master=frameAppointmentIndiv, text="", font=("Inter",20), text_color="#5D5D5D",
                              fg_color="transparent", anchor="w")
    lblMedicalConcern.grid(row=10, column=0, sticky="we", padx=50)
    
    lblMedicalDocs = CTkLabel(master=frameAppointmentIndiv, text="", font=("Inter",20), text_color="#5D5D5D",
                              fg_color="transparent", anchor="w")
    lblMedicalDocs.grid(row=11, column=0, sticky="we", padx=50)

    # Doctor Information
    lblDoctorInfo = CTkLabel(master=frameAppointmentIndiv, text="Doctor Information:", font=("Inter",20,"bold"), 
                             text_color="#5271FF", fg_color="transparent", anchor="w")
    lblDoctorInfo.grid(row=12, column=0, sticky="we", padx=50, pady=(20,0))
    lblDoctorName = CTkLabel(master=frameAppointmentIndiv, text="", font=("Inter",20), text_color="#5D5D5D",
                              fg_color="transparent", anchor="w")
    lblDoctorName.grid(row=13, column=0, sticky="we", padx=50)

    lblDoctorSpecialty = CTkLabel(master=frameAppointmentIndiv, text="", font=("Inter",20), text_color="#5D5D5D",
                              fg_color="transparent", anchor="w")
    lblDoctorSpecialty.grid(row=14, column=0, sticky="we", padx=50)

    lblDoctorPhone = CTkLabel(master=frameAppointmentIndiv, text="", font=("Inter",20), text_color="#5D5D5D",
                              fg_color="transparent", anchor="w")
    lblDoctorPhone.grid(row=15, column=0, sticky="we", padx=50)
    
    lblPrescription = CTkLabel(master=frameAppointmentIndiv, text="", font=("Inter",20), text_color="#5D5D5D",
                              fg_color="transparent", anchor="w")
    lblPrescription.grid(row=16, column=0, sticky="we", padx=50)

    # Status
    lblStatus = CTkLabel(master=frameAppointmentIndiv, text="", font=("Inter",20,"bold"), text_color="#5271FF",
                              fg_color="transparent", anchor="w")
    lblStatus.grid(row=17, column=0, sticky="we", padx=50, pady=30)
    
    # Button to cancel the appointment
    btnCancelAppointment = CTkButton(master=frameAppointmentIndiv, text="Cancel Appointment", font=("Inter",20,"bold"), 
                                     text_color="#5271FF", fg_color="white", anchor="e", corner_radius=20,
                                     command=btnCancelAppointment_Click)
    btnCancelAppointment.grid_forget()

    dropSearch_Filter("Any Time")
    
    return frameBookHis


