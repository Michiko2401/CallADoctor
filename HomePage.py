from customtkinter import *
import firebase_admin
from firebase_admin import credentials, storage
from firebase_admin import firestore
from PIL import Image, ImageDraw
import BookingHistory
import numpy as np
import cv2
import subprocess
from tkcalendar import Calendar
from datetime import datetime, timedelta
from tkinter import ttk
import pickle
from tkinter import messagebox
import random
import string
import hashlib

cred = credentials.Certificate("serviceAccountKey.json")
# Check if firebase_admin has been initialized
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {'storageBucket':'call-a-doctor-20a5d.appspot.com'})

db = firestore.client()

app = CTk()
app.geometry("1080x664")
set_appearance_mode("light")
style = ttk.Style(app)
style.theme_use("clam")

# Functions
# Adds corner radius to images
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

# Global variables
pageBookHis = None
pageClinicPg = None
pageDoctorPg = None
pageAdminPg = None

currentClinicData = None
currentDoctorData = None
clinicAptVisible = None
doctorAptVisible = None

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

def resetUi():
    currentUser, role = checkCurrentUser(pickleFile)

    if role == "Patient":
        btnBookHis.place(relx=0.51, rely=0.5, anchor="center")
    elif role == "Clinic":
        btnClinicPg.place(relx=0.5, rely=0.5, anchor="center")
    elif role == "Doctor":
        btnDoctorPg.place(relx=0.5, rely=0.5, anchor="center")
    elif role == "Admin":
        btnAdminPg.place(relx=0.5, rely=0.5, anchor="center")
    elif role == "Test":
        btnBookHis.place(relx=0.51, rely=0.4, anchor="center")
        btnClinicPg.place(relx=0.5, rely=0.5, anchor="center")
        btnDoctorPg.place(relx=0.5, rely=0.6, anchor="center")
        btnAdminPg.place(relx=0.5, rely=0.7, anchor="center")
    else:
        btnBookHis.place_forget()
        btnClinicPg.place_forget()
        btnDoctorPg.place_forget()
        btnAdminPg.place_forget()

    updateUi()
    app.grid_rowconfigure(0, weight=1)
    app.grid_rowconfigure(1, weight=0)
    frameHome.grid_forget()
    frameClinic.grid_forget()
    frameClinicBook.grid_forget()
    frameDoctorIndiv.grid_forget()
    frameProfile.grid_forget()
    frameProfileDetails.grid_forget()

    dropApTimeClinic.set("Select Time")
    dropApTimeClinic.configure(values=["Select Time"])
    dropApTimeDoctor.set("Select Time")
    dropApTimeDoctor.configure(values=["Select Time"])

    lblApUploadNoteClinic.configure(text="If there are multiple files, use a zip.")
    lblApUploadNoteDoctor.configure(text="If there are multiple files, use a zip.")

    tbApAddressClinic.delete("1.0", "end")
    tbApAddressDoctor.delete("1.0", "end")

    if currentUser != "":
        getAndUpdateUserAddress()
        deleteLeftoverMedicalDocs()

    # Reset the doctor frames to prevent overlaps of doctors from different clinics
    for widget in frameDoctors.winfo_children():
            if isinstance(widget, CTkLabel) and widget != lblTextClinicIndiv:
                widget.destroy()

    disableNonWorkdays(lblCalendarClinic)
    disableNonWorkdays(lblCalendarDoctor)

    # Close the pages from other .py files
    global pageBookHis
    if pageBookHis is not None:
        pageBookHis.grid_forget()  # Hide the page if it exists
        pageBookHis.destroy()  # Destroy the page to free up memory
        pageBookHis = None  # Reset the variable to None
    
    global pageClinicPg
    if pageClinicPg is not None:
        pageClinicPg.grid_forget()
        pageClinicPg.destroy()
        pageClinicPg = None

    global pageDoctorPg
    if pageDoctorPg is not None:
        pageDoctorPg.grid_forget()
        pageDoctorPg.destroy()
        pageDoctorPg = None

    global pageAdminPg
    if pageAdminPg is not None:
        pageAdminPg.grid_forget()
        pageAdminPg.destroy()
        pageAdminPg = None

# Function to expand the navigation bar
def btnMenu_Click():
    if btnHome.cget("text") == "":
        frameSideNav.configure(width=190)
        btnMenu.configure(text="                                        ", anchor="w")
        btnHome.configure(text="  Home Page               ", anchor="w")
        btnBookHis.configure(text="Booking History           ", anchor="w")
        btnClinicPg.configure(text="Clinic Management    ", anchor="w")
        btnDoctorPg.configure(text="  Doctor Appointments", anchor="w")
        btnAdminPg.configure(text=" Clinic Applications      ", anchor="w")
    else:
        frameSideNav.configure(width=80)
        btnMenu.configure(text="", anchor="center")
        btnHome.configure(text="", anchor="center")
        btnBookHis.configure(text="", anchor="center")
        btnClinicPg.configure(text="", anchor="center")
        btnDoctorPg.configure(text="", anchor="center")
        btnAdminPg.configure(text="", anchor="center")
    

# Function to switch to the home page
def btnHome_Click():
    resetUi()
    frameHome.grid(row=0, column=1, sticky="news")
    lblLogo.grid_forget()
    btnLogin2.grid_forget()

# Function to switch to the booking history page by calling a frame from BookingHistory.py
def btnBookHis_Click():
    resetUi()
    app.grid_rowconfigure(0, weight=0)
    app.grid_rowconfigure(1, weight=1)
    lblLogo.grid(row=0, column=1, sticky="ewn")
    btnLogin2.grid(row=0, column=1, sticky="ne", padx=16, pady=12)
    global pageBookHis
    if pageBookHis is None:
        pageBookHis = BookingHistory.create_BookHis(app)  # Call the create_BookHis function to get the frame
        pageBookHis.grid(row=1, column=1, sticky="news")
    else:
        pageBookHis.grid(row=1, column=1, sticky="news")  # Show the current page
    
def btnClinicPg_Click():
    resetUi()
    app.grid_rowconfigure(0, weight=0)
    app.grid_rowconfigure(1, weight=1)
    lblLogo.grid(row=0, column=1, sticky="ewn")
    btnLogin2.grid(row=0, column=1, sticky="ne", padx=16, pady=12)
    global pageClinicPg
    if pageClinicPg is None:
        import ClinicPageMe
        pageClinicPg = ClinicPageMe.create_ClinicPg(app)
        pageClinicPg.grid(row=1, column=1, sticky="news")
    else:
        pageClinicPg.grid(row=1, column=1, sticky="news")

def btnDoctorPg_Click():
    resetUi()
    app.grid_rowconfigure(0, weight=0)
    app.grid_rowconfigure(1, weight=1)
    lblLogo.grid(row=0, column=1, sticky="ewn")
    btnLogin2.grid(row=0, column=1, sticky="ne", padx=16, pady=12)
    global pageDoctorPg
    if pageDoctorPg is None:
        import DoctorPage
        pageDoctorPg = DoctorPage.create_DoctorPg(app)
        pageDoctorPg.grid(row=1, column=1, sticky="news")
    else:
        pageDoctorPg.grid(row=1, column=1, sticky="news")

def btnAdminPg_Click():
    resetUi()
    app.grid_rowconfigure(0, weight=0)
    app.grid_rowconfigure(1, weight=1)
    lblLogo.grid(row=0, column=1, sticky="ewn")
    btnLogin2.grid(row=0, column=1, sticky="ne", padx=16, pady=12)
    global pageAdminPg
    if pageAdminPg is None:
        import AdminPage
        pageAdminPg = AdminPage.create_AdminPg(app)
        pageAdminPg.grid(row=1, column=1, sticky="news")
    else:
        pageAdminPg.grid(row=1, column=1, sticky="news")

# Showcases the login feature
def btnLogin_Click():
    currentUser, role = checkCurrentUser(pickleFile)

    if currentUser == "":
        pythonExecutable = sys.executable
        subprocess.Popen([pythonExecutable, './SE Project/LoginRegister.py'])
    else:
        resetUi()
        lblLogo.grid_forget()
        btnLogin2.grid_forget()
        frameProfile.grid(row=0, column=1, sticky="news")
        generateProfileText()

def generateProfileText():
    currentUser, role = checkCurrentUser(pickleFile)
    if role == "Patient":
            frameProfileDetails.grid(row=0, column=0, columnspan=2, sticky="news")
            userDoc = db.collection("Patients").document(currentUser).get()
            if userDoc.exists:
                userData = userDoc.to_dict()
                email = userData.get("Email", "N/A")
                name = userData.get("Name", "N/A")
                phoneNo = userData.get("PhoneNo", "N/A")
                address = userData.get("Address", "N/A")
                
                lblUserEmailText.configure(text=email)
                lblUserPasswordText.configure(text="●"*8)
                lblUserNameText.configure(text=name)
                lblUserPhoneNoText.configure(text=phoneNo)
                lblUserAddressText.configure(text=address)

                tbUserEmail.delete(0, END)    
                tbUserName.delete(0, END)    
                tbUserPassword.delete(0, END)    
                tbUserNewPassword.delete(0, END)    
                tbUserPhoneNo.delete(0, END)    
                tbUserAddress.delete("1.0", "end-1c")

                tbUserEmail.insert(0, email)
                tbUserName.insert(0, name)
                tbUserPhoneNo.insert(0, phoneNo)
                tbUserAddress.insert("1.0", address)

                btnEditProfile.grid(row=1, column=1, sticky="e", padx=50, pady=50)
                btnLogout.grid(row=1, column=0, sticky="w", padx=50, pady=50)
    else:
        frameProfileDetails.grid_forget()
        btnLogout.grid(row=1, column=0, columnspan=2, padx=50, pady=50, sticky="ew", ipadx=20, ipady=20)
        btnEditProfile.grid_forget()

def btnBackProfile_Click():
    resetUi()
    frameHome.grid(row=0, column=1, sticky="news")

def btnLogout_Click():
    if os.path.exists(pickleFile) and os.path.getsize(pickleFile) > 0:
        with open(pickleFile, 'wb') as f:
            try:
                pickle.dump(None, f)
                print("Logging out...")
                print("User is no longer logged in, returning to home page.")
                resetUi()
                frameHome.grid(row=0, column=1, sticky="news")
            except EOFError:
                print(f"'{pickleFile}' is empty or corrupted.")
    else:
        print(f"'The pickle file {pickleFile}' does not exist or is empty.")

def btnEditProfile_Click():
    generateProfileText()

    btnEditProfile.grid_forget()
    btnLogout.grid_forget()
    lblUserEmailText.grid_forget()
    lblUserPasswordText.grid_forget()
    lblUserNameText.grid_forget()
    lblUserPhoneNoText.grid_forget()
    lblUserAddressText.grid_forget()

    btnEditProfileCancel.grid(row=7, column=0, sticky="w", padx=50, pady=50)
    btnEditProfileSave.grid(row=7, column=1, sticky="e", padx=50, pady=50)
    lblUserNewPassword.grid(row=3, column=0, sticky="new", padx=(10,0), pady=20)
    tbUserEmail.grid(row=1, column=1, sticky="new", pady=20)
    tbUserPassword.grid(row=2, column=1, sticky="new", pady=20)
    tbUserNewPassword.grid(row=3, column=1, sticky="new", pady=20)
    tbUserName.grid(row=4, column=1, sticky="new", pady=20)
    tbUserPhoneNo.grid(row=5, column=1, sticky="new", pady=20)
    tbUserAddress.grid(row=6, column=1, sticky="new", pady=20)

def btnEditProfileCancel_Click():
    btnEditProfile.grid(row=1, column=1, sticky="e", padx=50, pady=50)
    btnLogout.grid(row=1, column=0, sticky="w", padx=50, pady=50)
    lblUserEmailText.grid(row=1, column=1, sticky="new", pady=20)
    lblUserPasswordText.grid(row=2, column=1, sticky="new", pady=20)
    lblUserNameText.grid(row=4, column=1, sticky="new", pady=20)
    lblUserPhoneNoText.grid(row=5, column=1, sticky="new", pady=20)
    lblUserAddressText.grid(row=6, column=1, sticky="new", pady=20)

    btnEditProfileCancel.grid_forget()
    btnEditProfileSave.grid_forget()
    lblUserNewPassword.grid_forget()
    tbUserEmail.grid_forget()
    tbUserPassword.grid_forget()
    tbUserNewPassword.grid_forget()
    tbUserName.grid_forget()
    tbUserPhoneNo.grid_forget()
    tbUserAddress.grid_forget()

def btnEditProfileSave_Click():
    currentUser, role = checkCurrentUser(pickleFile)
    userEmail = tbUserEmail.get().strip()
    userPassword = tbUserPassword.get()
    userNewPassword = tbUserNewPassword.get()
    userName = tbUserName.get().strip()
    userPhoneNo = tbUserPhoneNo.get().strip()
    userAddress = tbUserAddress.get("1.0", "end-1c").strip()

    userDocRef = db.collection("Users").document(currentUser)  # Initialize userDocRef

    if userPassword and userNewPassword:
        if userPassword == "" or userNewPassword == "":
            messagebox.showerror("Error", "Please fill in both the current and new passwords.")
            return

        # Validate current password against stored hashed password in Firestore
        userDoc = userDocRef.get()

        if userDoc.exists:
            userData = userDoc.to_dict()
            storedHashedPassword = userData.get("Password", "")

            # Hash the user-provided current password and compare with stored hashed password
            if hashlib.sha256(userPassword.encode()).hexdigest() == storedHashedPassword:
                # Passwords match, continue with update
                hashedNewPassword = hashlib.sha256(userNewPassword.encode()).hexdigest()

                # Prepare update data
                updateData = {}
                if userEmail:
                    updateData["Email"] = userEmail
                if userName:
                    updateData["Name"] = userName
                if userPhoneNo:
                    updateData["PhoneNo"] = userPhoneNo
                if userAddress:
                    updateData["Address"] = userAddress
                if userNewPassword:
                    updateData["Password"] = hashedNewPassword

                # Update Firestore document if there are updates
                if updateData:
                    userDocRef.update(updateData)
                    messagebox.showinfo("Success", "Profile updated successfully.")
                else:
                    messagebox.showwarning("No Changes", "No fields were updated.")
            else:
                messagebox.showerror("Error", "Current password is incorrect.")
                return
    else:
        # Handle case where user does not want to update password
        # Prepare update data
        updateData = {}
        if userEmail:
            updateData["Email"] = userEmail
        if userName:
            updateData["Name"] = userName
        if userPhoneNo:
            updateData["PhoneNo"] = userPhoneNo
        if userAddress:
            updateData["Address"] = userAddress

        # Update Firestore document if there are updates
        if updateData:
            userDocRef.update(updateData)
            messagebox.showinfo("Success", "Profile updated successfully.")
        else:
            messagebox.showwarning("No Changes", "No fields were updated.")

    btnEditProfileCancel_Click()

# Function to display the list of clinics
# Global variable to store references to created frameClinicList instances
global clinicFrames
clinicFrames = []

# Function to display the list of clinics
def displayClinicList(filter, ref):
    global clinicFrames

    # Clear existing frames
    for frame in clinicFrames:
        frame.destroy()
    clinicFrames = []

    docs = ref.stream()

    # Prepare the data
    clinicData = []
    for doc in docs:
        clinic = doc.to_dict()
        
        if filter == "Doctors":
            clinic['DoctorId'] = doc.id
        else:
            clinic['ClinicId'] = doc.id
        clinicData.append(clinic)

    rowIndexClinics = 2

    # Display each clinic data
    for clinic in clinicData:
        doctor = clinic  # Assign clinic to doctor for consistent naming in lambda

        # Fetch image from Firestore
        imgClinicList = clinic.get('Image')

        if imgClinicList is not None:
            bucket = storage.bucket()
            blob = bucket.get_blob(imgClinicList)
            if blob is not None:
                arr = np.frombuffer(blob.download_as_string(), np.uint8)
                img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                # Convert the numpy array to a PIL Image object
                pilImgClinicList = Image.fromarray(img)
                if filter == "Doctors":
                    pilImgClinicList = cropImage(pilImgClinicList, (220, 150))
                pilImgClinicList = addRoundedCorners(pilImgClinicList, 20)
                ctkImgClinicList = CTkImage(pilImgClinicList, size=(220, 150))
            else:
                # Set a placeholder image
                print("There is no image for this clinic.")
                placeholderImg = Image.open("./SE Project/Images/bg.png")
                ctkImgClinicList = CTkImage(placeholderImg, size=(220, 150))

        if filter == "Doctors":
            clinicId = doctor.get('ClinicId', 'N/A')
    
            # Initialize clinicName
            clinicName = "N/A"
            
            if clinicId != 'N/A':
                # Fetch clinic name from Firestore using the clinicId
                clinicRef = db.collection('Clinics').document(clinicId)
                clinic = clinicRef.get().to_dict()
                
                if clinic:
                    clinicName = clinic.get('Name', 'N/A')
            
            # Format doctor information with clinic name
            doctorInfo = (
                f"{doctor.get('Name', 'N/A')}\n"
                f"Specialty: {doctor.get('Specialty', 'N/A')}\n"
                f"Languages: {doctor.get('Language', 'N/A')}\n"
                f"Work Days: {doctor.get('WorkDays', 'N/A')}\n"
                f"Clinic: {clinicName}\n"
            )
            displayInfo = doctorInfo

        else:
            clinicInfo = (
                f"{clinic.get('Name', 'N/A')}\n"
                f"Phone No: {clinic.get('PhoneNo', 'N/A')}\n"
                f"Address: {clinic.get('Address', 'N/A')}\n"
                f"Specialty: {clinic.get('Specialty', 'N/A')}\n"
                f"Open: {clinic.get('WorkDays', 'N/A')}\n"
            )
            displayInfo = clinicInfo

        # Create a frame for each clinic
        frameClinicList = CTkFrame(master=frameHome, bg_color="transparent", fg_color="transparent")
        frameClinicList.grid(row=rowIndexClinics, column=0, sticky="new", padx=47, pady=10)
        frameClinicList.grid_columnconfigure(0, weight=1)
        
        # Add image label
        lblImgClinicList = CTkLabel(master=frameClinicList, text="", image=ctkImgClinicList, bg_color="transparent", 
                                    width=220, height=150)
        lblImgClinicList.grid(row=1, column=0, sticky="w")

        # Add text label
        lblTextClinicList = CTkLabel(master=frameClinicList, text=displayInfo, height=150, corner_radius=20, fg_color="white", 
                                     bg_color="transparent", text_color="#5D5D5D", font=("Inter", 20), justify="left", 
                                     anchor="w")
        lblTextClinicList.grid(row=1, column=0, sticky="ew", padx=(220, 0))

        # Add behind label
        lblBehindClinicList = CTkLabel(master=frameClinicList, text="", fg_color="white", width=24, height=150)
        lblBehindClinicList.grid(row=1, column=0, sticky="w", padx=212)

        # Bind the click event to the frame and its labels
        if filter == "Doctors":
            frameClinicList.bind("<Button-1>", lambda e, doctor=doctor: btnDoctor_Click(doctor))
            lblImgClinicList.bind("<Button-1>", lambda e, doctor=doctor: btnDoctor_Click(doctor))
            lblTextClinicList.bind("<Button-1>", lambda e, doctor=doctor: btnDoctor_Click(doctor))
            lblBehindClinicList.bind("<Button-1>", lambda e, doctor=doctor: btnDoctor_Click(doctor))
        else:
            frameClinicList.bind("<Button-1>", lambda e, clinic=clinic: btnClinic_Click(clinic))
            lblImgClinicList.bind("<Button-1>", lambda e, clinic=clinic: btnClinic_Click(clinic))
            lblTextClinicList.bind("<Button-1>", lambda e, clinic=clinic: btnClinic_Click(clinic))
            lblBehindClinicList.bind("<Button-1>", lambda e, clinic=clinic: btnClinic_Click(clinic))

        # Store reference to the created frame
        clinicFrames.append(frameClinicList)

        rowIndexClinics += 1
        
def dropSearch_Filter(filter, searchTerm=""):
    if filter == "Doctors":
        doctorsRef = db.collection('Doctors')
        if searchTerm:
            nameQuery = db.collection('Doctors').where('Name', '>=', searchTerm).where('Name', '<=', searchTerm + '\uf8ff')
            emailQuery = db.collection('Doctors').where('Email', '>=', searchTerm).where('Email', '<=', searchTerm + '\uf8ff')
            phoneNoQuery = db.collection('Doctors').where('PhoneNo', '>=', searchTerm).where('PhoneNo', '<=', searchTerm + '\uf8ff')
            qualificationQuery = db.collection('Doctors').where('Qualification', '>=', searchTerm).where('Qualification', '<=', searchTerm + '\uf8ff')
            specialtyQuery = db.collection('Doctors').where('Specialty', '>=', searchTerm).where('Specialty', '<=', searchTerm + '\uf8ff')
            languageQuery = db.collection('Doctors').where('Language', '>=', searchTerm).where('Language', '<=', searchTerm + '\uf8ff')
            workDaysQuery = db.collection('Doctors').where('WorkDays', '>=', searchTerm).where('WorkDays', '<=', searchTerm + '\uf8ff')
            docs1 = nameQuery.stream()
            docs2 = emailQuery.stream()
            docs3 = phoneNoQuery.stream()
            docs4 = qualificationQuery.stream()
            docs5 = specialtyQuery.stream()
            docs6 = languageQuery.stream()
            docs7 = workDaysQuery.stream()
            if len(list(docs1)) > 0:
                doctorsRef = nameQuery
            elif len(list(docs2)) > 0:
                doctorsRef = emailQuery
            elif len(list(docs3)) > 0:
                doctorsRef = phoneNoQuery
            elif len(list(docs4)) > 0:
                doctorsRef = addressQuery
            elif len(list(docs5)) > 0:
                doctorsRef = specialtyQuery
            elif len(list(docs6)) > 0:
                doctorsRef = workDaysQuery
            elif len(list(docs7)) > 0:
                doctorsRef = workDaysQuery
            else:
                doctorsRef = nameQuery
                print("Data not found")
        ref = doctorsRef
    else:
        clinicsRef = db.collection('Clinics').where('AppStatus', '==', 'Approved')
        if searchTerm:
            nameQuery = db.collection('Clinics').where('Name', '>=', searchTerm).where('Name', '<=', searchTerm + '\uf8ff')
            emailQuery = db.collection('Clinics').where('Email', '>=', searchTerm).where('Email', '<=', searchTerm + '\uf8ff')
            phoneNoQuery = db.collection('Clinics').where('PhoneNo', '>=', searchTerm).where('PhoneNo', '<=', searchTerm + '\uf8ff')
            addressQuery = db.collection('Clinics').where('Address', '>=', searchTerm).where('Address', '<=', searchTerm + '\uf8ff')
            specialtyQuery = db.collection('Clinics').where('Specialty', '>=', searchTerm).where('Specialty', '<=', searchTerm + '\uf8ff')
            workDaysQuery = db.collection('Clinics').where('WorkDays', '>=', searchTerm).where('WorkDays', '<=', searchTerm + '\uf8ff')
            docs1 = nameQuery.stream()
            docs2 = emailQuery.stream()
            docs3 = phoneNoQuery.stream()
            docs4 = addressQuery.stream()
            docs5 = specialtyQuery.stream()
            docs6 = workDaysQuery.stream()
            if len(list(docs1)) > 0:
                clinicsRef = nameQuery
            elif len(list(docs2)) > 0:
                clinicsRef = emailQuery
            elif len(list(docs3)) > 0:
                clinicsRef = phoneNoQuery
            elif len(list(docs4)) > 0:
                clinicsRef = addressQuery
            elif len(list(docs5)) > 0:
                clinicsRef = specialtyQuery
            elif len(list(docs6)) > 0:
                clinicsRef = workDaysQuery
            else:
                clinicsRef = nameQuery
                print("Data not found")
        ref = clinicsRef

    displayClinicList(filter, ref)

# Function to handle the search button click
def btnSearch_Click():
    searchTerm = ""
    searchTerm = tbSearch.get().strip()
    filter = dropSearch.get() 
    print("Searching for '" + searchTerm + "' under " + filter)
    dropSearch_Filter(filter, searchTerm)

def getAndUpdateUserAddress():
    try:
        currentUser, role = checkCurrentUser(pickleFile)
        # Fetch document snapshot from Firestore
        docRef = db.collection('Patients').document(currentUser)
        doc = docRef.get()

        if doc.exists:
            # Get the 'Address' field from the document
            address = doc.to_dict().get('Address')

            # Update the text box with the retrieved address
            tbApAddressClinic.delete("1.0", "end")  # Clear existing text
            tbApAddressClinic.insert("1.0", address)  # Insert new address text
            tbApAddressDoctor.delete("1.0", "end")
            tbApAddressDoctor.insert("1.0", address) 

        else:
            # Handle case where document does not exist
            tbApAddressClinic.delete("1.0", "end")  # Clear existing text
            tbApAddressDoctor.delete("1.0", "end")  

    except Exception as e:
        print(f"Error fetching address: {e}")
        tbApAddressClinic.delete("1.0", "end")  # Clear existing text
        tbApAddressDoctor.delete("1.0", "end")

# Function to open an individual clinic's page
def btnClinic_Click(clinic):
    global currentClinicData
    currentClinicData = clinic

    updateUi()
    frameHome.grid_forget()
    frameClinic.grid(row=0, column=1, sticky="news")
    lblLogo.grid(row=0, column=1, sticky="ewn")
    btnLogin2.grid(row=0, column=1, sticky="ne", padx=16, pady=12)

    clinicPageId = clinic['ClinicId']
    clinicInfo = (
        f"{clinic.get('Name', 'N/A')}\n"
        f"Phone No: {clinic.get('PhoneNo', 'N/A')}\n"
        f"Address: {clinic.get('Address', 'N/A')}\n"
        f"Specialty: {clinic.get('Specialty', 'N/A')}\n"
        f"About: {clinic.get('Description', 'N/A')}\n"
        f"Open: {clinic.get('WorkDays', 'N/A')}\n"
    )

    # Fetch image from Firestore
    imgClinic = clinic.get('Image')
    bucket = storage.bucket()
    blob = bucket.get_blob(imgClinic)
    if blob is not None:
        arr = np.frombuffer(blob.download_as_string(), np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert from BGR to RGB

        # Convert the numpy array to a PIL Image object
        pilImgClinic = Image.fromarray(img)
        pilImgClinic = addRoundedCorners(pilImgClinic, 20)
        ctkImgClinic = CTkImage(pilImgClinic, size=(270, 200))
    else:
        # Set a placeholder image
        print("There is no image for this clinic.")
        placeholderImg = Image.open("./SE Project/Images/bg.png")
        ctkImgClinic = CTkImage(placeholderImg, size=(220, 150))

    lblImgClinicIndiv.configure(image=ctkImgClinic)
    lblTextClinicIndiv.configure(text=clinicInfo)

    # Fetch data from Firestore via ClinicId
    doctorsRef = db.collection('Doctors').where('ClinicId', '==', clinicPageId)
    docs = doctorsRef.stream()

    global currentDoctorData
    # Prepare the data
    doctorData = []
    for doc in docs:
        doctor = doc.to_dict()
        doctor['DoctorId'] = doc.id
        doctorData.append(doctor)

    currentDoctorData = doctor

    # Display each doctor data in a grid with 3 columns per row
    colIndexDocs = 0
    rowIndexDocs = 0 

    # Check if there are any doctors for the clinic
    if doctorData:  # If doctorData is not empty
        # Loop through each doctor
        for doctor in doctorData:
            if clinicPageId.startswith("C-"):
                # Extract doctor information
                doctorInfo = (
                    f"\n"
                    f"{doctor.get('Name', 'N/A')}\n"
                    f"Specialty: {doctor.get('Specialty', 'N/A')}\n"
                )
                # Split languages by commas
                languages = doctor.get('Language', 'N/A').split(', ')
                workDays = doctor.get('WorkDays', 'N/A').split(', ')

                # Join languages with new lines after every two segments
                languagesText = '\n                    '.join(', '.join(languages[i:i+2]) for i in range(0, len(languages), 2))
                workDaysText = '\n                    '.join(', '.join(workDays[i:i+2]) for i in range(0, len(workDays), 2))
                
                doctorInfo += f"Languages: {languagesText}\n" f"Work Days: {workDaysText}\n"

                imgDoctorList = doctor.get('Image')

                bucket = storage.bucket()
                blob = bucket.get_blob(imgDoctorList)
                if blob is not None:
                    try:
                        arr = np.frombuffer(blob.download_as_string(), np.uint8)
                        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert from BGR to RGB

                        # Convert the numpy array to a PIL Image object
                        pilImgDoctorList = Image.fromarray(img)
                        pilImgDoctorList = cropImage(pilImgDoctorList, (200, 200))
                        # pilImgDoctors = addRoundedCorners(pilImgDoctors, 20)
                        ctkImgDoctorList = CTkImage(pilImgDoctorList, size=(200, 200))
                    except Exception as e:
                        print(f"Error decoding image for doctor: {e}")
                        ctkImgDoctorList = None
                else:
                    print(f"Blob not found for path: {imgDoctorList}")  # Debug print
                    # Set a placeholder image
                    placeholderImg = Image.open("./SE Project/Images/bg.png")
                    ctkImgDoctorList = CTkImage(placeholderImg, size=(220, 150))

                # Create a label for the doctor image
                lblImgDoctorList = CTkLabel(master=frameDoctors, text="", image=ctkImgDoctorList, height=200, corner_radius=20, fg_color="white")
                lblImgDoctorList.grid(row=rowIndexDocs, column=colIndexDocs, sticky="new", padx=10)

                # Create a label for the doctor information
                lblTextDoctorList = CTkLabel(master=frameDoctors, text=doctorInfo, height=100, corner_radius=20, fg_color="white",
                                         text_color="#5D5D5D", font=("Inter", 15), justify="left", anchor="w")
                lblTextDoctorList.grid(row=rowIndexDocs, column=colIndexDocs, sticky="news", padx=10, pady=(180, 20))

                lblBehindDoctorList = CTkLabel(master=frameDoctors, text="", fg_color="white", height=20)
                lblBehindDoctorList.grid(row=rowIndexDocs, column=colIndexDocs, sticky="new", padx=10, pady=(180,0))

                # Bind the click event to the label
                lblImgDoctorList.bind("<Button-1>", lambda e, doctor=doctor: btnDoctor_Click(doctor))
                lblTextDoctorList.bind("<Button-1>", lambda e, doctor=doctor: btnDoctor_Click(doctor))
                lblBehindDoctorList.bind("<Button-1>", lambda e, doctor=doctor: btnDoctor_Click(doctor))

                # Increment column index
                colIndexDocs += 1
                if colIndexDocs >= 3:  # Reset column index and move to the next row after 3 columns
                    colIndexDocs = 0
                    rowIndexDocs += 2  # Increment by 2 to account for image and info rows
    else:  # If doctorData is empty
        print("There is no doctor data")
        # Clear any existing doctor labels
        for widget in frameDoctors.winfo_children():
            if isinstance(widget, CTkLabel) and widget != lblTextClinicIndiv:
                widget.destroy()

# Function to open individual doctor's page
def btnDoctor_Click(doctor):
    resetUi()

    global currentDoctorData
    global clinicAptVisible
    global doctorAptVisible
    
    currentDoctorData = doctor
    print(doctor)
    clinicAptVisible = False
    doctorAptVisible = True

    frameDoctorIndiv.grid(row=0, column=1, sticky="news")
    lblLogo.grid(row=0, column=1, sticky="ewn")
    btnLogin2.grid(row=0, column=1, sticky="ne", padx=16, pady=12)
    
    print(f"Doctor clicked: {doctor.get('Name')}")

    imgDoctors = doctor.get('Image')

    bucket = storage.bucket()
    blob = bucket.get_blob(imgDoctors)
    if blob is not None:
        try:
            arr = np.frombuffer(blob.download_as_string(), np.uint8)
            img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert from BGR to RGB

            # Convert the numpy array to a PIL Image object
            pilImgDoctorIndiv = Image.fromarray(img)
            pilImgDoctorIndiv = cropImage(pilImgDoctorIndiv, (250, 200))
            pilImgDoctorIndiv = addRoundedCorners(pilImgDoctorIndiv, 20)
            ctkImgDoctorIndiv = CTkImage(pilImgDoctorIndiv, size=(250, 200))
        except Exception as e:
            print(f"Error decoding image for doctor: {e}")
            ctkImgDoctorIndiv = None
    else:
        print(f"Blob not found for path: {imgDoctors}")  # Debug print
        # Placeholder image or handle missing image
        placeholderImg = Image.open("./SE Project/Images/bg.png")
        ctkImgDoctorIndiv = CTkImage(placeholderImg, size=(220, 150))

    clinicId = doctor.get('ClinicId', 'N/A')
    
    # Initialize clinicName
    clinicName = "N/A"
    
    if clinicId != 'N/A':
        # Fetch clinic name from Firestore using the clinicId
        clinicRef = db.collection('Clinics').document(clinicId)
        clinic = clinicRef.get().to_dict()
        
        if clinic:
            clinicName = clinic.get('Name', 'N/A')
    
    # Format doctor information with clinic name
    doctorInfo = (
        f"{doctor.get('Name', 'N/A')}\n"
        f"Phone No: {doctor.get('PhoneNo', 'N/A')}\n"
        f"Qualification: {doctor.get('Qualification', 'N/A')}\n"
        f"Specialty: {doctor.get('Specialty', 'N/A')}\n"
        f"Languages: {doctor.get('Language', 'N/A')}\n"
        f"Work Days: {doctor.get('WorkDays', 'N/A')}\n"
        f"Clinic: {clinicName}\n"
    )

    lblImgDoctorIndiv.configure(image=ctkImgDoctorIndiv)
    lblTextDoctorIndiv.configure(text=doctorInfo)

def disableNonWorkdays(calendar):
    global currentClinicData
    global currentDoctorData
    global clinicAptVisible
    global doctorAptVisible
    
    if clinicAptVisible == True or doctorAptVisible == True:
        generateAppointmentTimes()
    
    updateUi()

    if currentClinicData is not None:
        # Fetch workdays from the current data
        if doctorAptVisible == True:
            workdaysString = currentDoctorData.get('WorkDays', '')
        else:
            workdaysString = currentClinicData.get('WorkDays', '')
        
        # Split workdays string into a list and clean up extra spaces
        workdays = [day.strip().lower() for day in workdaysString.split(',') if day.strip()]
        
        # List of weekdays
        weekdays = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

        # Disable days not in workdays
        for i in range(6):
            for j in range(7):
                if weekdays[j] not in workdays:
                    calendar._calendar[i][j].state(['disabled'])

        # Check if the selected date is disabled and deselect it if necessary
        selectedDate = calendar.selection_get()
        if selectedDate:
            selectedWeekday = selectedDate.strftime("%A").lower()
            if selectedWeekday not in workdays:
                calendar.selection_set(None)
                print("Invalid date.")

    # Bind updateCalendar to the month changed events
    calendar.bind("<<CalendarMonthChanged>>", lambda event: disableNonWorkdays(calendar))
    calendar.bind("<<CalendarSelected>>", lambda event: disableNonWorkdays(calendar))

def btnSearchDoc_Click():
    print("Button Clicked")

# Function to return to the home page from the individual clinic's page
def btnBackClinicIndiv_Click():
    frameClinic.grid_forget()
    for widget in frameDoctors.winfo_children():
            if isinstance(widget, CTkLabel) and widget != lblTextClinicIndiv:
                widget.destroy()
    frameHome.grid(row=0, column=1, sticky="news")
    lblLogo.grid_forget()
    btnLogin2.grid_forget()

def btnBackClinicBook_Click():
    global currentClinicData
    btnClinic_Click(currentClinicData)
    frameClinicBook.grid_forget()

def btnBackDoctorIndiv_Click():
    filter = dropSearch.get()
    if filter == "Clinics":
        global currentClinicData
        btnClinic_Click(currentClinicData)
        frameDoctorIndiv.grid_forget()
    else:
        resetUi()
        frameHome.grid(row=0, column=1, sticky="news")
    frameDoctorIndiv.grid_forget()
    
def btnApTypeVisit_Click():
    radioVar.set(0)

def btnApTypeWalkIn_Click():
    radioVar.set(1)

def deleteLeftoverMedicalDocs():
    currentUser, role = checkCurrentUser(pickleFile)

    # Initialize Firebase Storage bucket
    bucket = storage.bucket()
    
    # List objects with the temp- prefix and the id from currentUser (to delete existing temporary user files)
    blobs = list(bucket.list_blobs(prefix="temp-" + currentUser))
    
    # Delete each existing blob with temp- prefix
    for blob in blobs:
        blob.delete()
        print(f"Existing file {blob.name} deleted from Firebase Storage.")

# Function to handle the medical document(s) upload for booking appointments
def btnApUpload_Click():
    currentUser, role = checkCurrentUser(pickleFile)
    filepath = filedialog.askopenfilename(title="Select a File")
    
    if filepath:
        # Generate the filename in the format temp-currentUser.extension
        filename = f"temp-{currentUser}.{os.path.splitext(filepath)[1][1:]}"
        
        try:      
            deleteLeftoverMedicalDocs()
            
            bucket = storage.bucket()
            # Upload the new file to Firebase Storage with temp-currentUser filename
            blob = bucket.blob(filename)
            blob.upload_from_filename(filepath)
            print(f"File {filename} uploaded successfully to Firebase Storage.")
            lblApUploadNoteClinic.configure(text="Your file has been uploaded.")
            lblApUploadNoteDoctor.configure(text="Your file has been uploaded.")
        
        except Exception as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", "An error occurred while uploading the file.")

def btnClinicBook_Click():
    resetUi()
    global currentClinicData
    global currentDoctorData
    global clinicAptVisible
    global doctorAptVisible

    clinicAptVisible = True
    doctorAptVisible = False

    # Ensure currentClinicData is a dictionary
    if isinstance(currentClinicData, dict):
        clinicName = currentClinicData.get("Name", "")
    else:
        clinicName = ""

    frameClinicBook.grid(row=0, column=1, sticky="news")
    lblClinicBook.configure(text="Book an appointment with " + clinicName)

def generateAppointmentTimes():
    global doctorAptVisible

    # Get the selected date from the calendar
    if doctorAptVisible:
        selectedDate = lblCalendarDoctor.selection_get()
        calendar = lblCalendarDoctor  # Assuming lblCalendarDoctor is a Calendar widget
        doctorId = currentDoctorData.get('DoctorId')
    else:
        selectedDate = lblCalendarClinic.selection_get()
        calendar = lblCalendarClinic  # Assuming lblCalendarClinic is a Calendar widget
        doctorId = None  # Adjust if needed for clinic mode

    if not selectedDate:
        return

    # Fetch existing appointments for the doctor on the selected date
    existingAppointments = []
    if doctorId:
        # Convert selectedDate to the format expected in Firestore ('YYYY-MM-DD')
        selectedDateString = selectedDate.strftime("%Y-%m-%d")
        
        # Query appointments where DoctorId matches and DateTime starts with selectedDateString
        appointments_ref = db.collection('AppointmentDetails').where('DoctorId', '==', doctorId).where('DateTime', '>=', f"{selectedDateString},").where('DateTime', '<', f"{selectedDateString},\uf8ff")
        
        existingAppointments = [appointment.to_dict() for appointment in appointments_ref.stream() if appointment.get('Status') in ['Pending', 'Accepted']]

    # Get clinic workdays and hours
    if doctorAptVisible:
        workDays = [day.strip() for day in currentDoctorData.get('WorkDays', '').lower().split(',')]
    else:
        workDays = [day.strip() for day in currentClinicData.get('WorkDays', '').lower().split(',')]
    startHours = [hour.strip() for hour in currentClinicData.get('StartHours', '').split(',')]
    endHours = [hour.strip() for hour in currentClinicData.get('EndHours', '').split(',')]

    # print(f"Work days: {workDays}")
    # print(f"Start hours: {startHours}")
    # print(f"End hours: {endHours}")

    # Initialize the list of times
    times = []

    # Check if the selected weekday is in the workdays
    weekdayName = selectedDate.strftime("%A").lower()
    if weekdayName in workDays:
        index = workDays.index(weekdayName)
        startHour = int(startHours[index][:2])
        startMinute = int(startHours[index][2:])
        endHour = int(endHours[index][:2])
        endMinute = int(endHours[index][2:])

        # print(f"Start time: {startHour:02d}:{startMinute:02d}, End time: {endHour:02d}:{endMinute:02d}")

        # Generate times from start_hour to end_hour
        currentTime = startHour * 60 + startMinute
        endTime = endHour * 60 + endMinute

        while currentTime < endTime:
            currentHour = currentTime // 60
            currentMinute = currentTime % 60

            # Format current time
            timeStr = f"{currentHour:02d}:{currentMinute:02d}"

            # Check if the current time slot is available
            isAvailable = True
            for appointment in existingAppointments:
                appointmentDateTime = appointment.get('DateTime', '')
                if appointmentDateTime.endswith(timeStr):
                    isAvailable = False
                    break
            
            if isAvailable:
                times.append(timeStr)

            currentTime += 60  # Increment by one hour

    # print(f"Generated times: {times}")        

    if doctorAptVisible:
        # Populate the drop times with the generated times
        dropApTimeDoctor.configure(values=times if times else ["Select Time"])
        dropApTimeDoctor.set("Select Time")
    else:
        dropApTimeClinic.configure(values=times if times else ["Select Time"])
        dropApTimeClinic.set("Select Time")

    # Highlight fully booked dates in the calendar
    def highlightFullDates():
        calendar.calevent_remove('all', 'full')  # Remove previous 'full' tags
        calendar.tag_config('full', background='red')
        
        for appointment in existingAppointments:
            appointmentDateTime = appointment.get('DateTime', '')
            appointmentDate, appointmentTime = appointmentDateTime.split(', ')
            appointmentDate = datetime.strptime(appointmentDate, "%Y-%m-%d")
            
            # Check if the date is fully booked
            appointmentDay = appointmentDate.strftime("%A").lower()
            if appointmentDay in workDays:
                index = workDays.index(appointmentDay)
                startHour = int(startHours[index][:2])
                endHour = int(endHours[index][:2])
                
                # Calculate total slots in the day
                totalSlots = (endHour - startHour) * 60 // 60
                
                # Check if all slots are booked
                bookedSlots = [appt for appt in existingAppointments if appt.get('DateTime', '').startswith(appointmentDate.strftime("%Y-%m-%d"))]
                if len(bookedSlots) >= totalSlots:
                    calendar.calevent_create(appointmentDate, 'Fully Booked', 'full')
                    messagebox.showinfo("Appointments Full", "Appointments are full on this day. Please pick another date.")
                    return
                    
    highlightFullDates()

def dropApTimeClinic_Click(selected_value):
    # Check if the selected value in dropApTimeClinic is "Select Time"
    if selected_value == "Select Time":
        messagebox.showinfo("Select Date", "Please select a date first.")
    else:
        generateAppointmentTimes()
        dropApTimeClinic.set(selected_value)

def dropApTimeDoctor_Click(selected_value):
    if selected_value == "Select Time":
        messagebox.showinfo("Select Date", "Please select a date first.")
    else:
        generateAppointmentTimes()
        dropApTimeDoctor.set(selected_value)

def generateAppointmentId():
    # Define the range of characters for the ID
    characters = string.ascii_letters + string.digits

    while True:
        # Generate a random ID with the range of 6
        apId = 'A-' + ''.join(random.choices(characters, k=6))

        # Check if this ID already exists in the database
        apRef = db.collection('AppointmentDetails').document(apId)
        if not apRef.get().exists:
            return apId

def btnProceed_Click():
    global currentClinicData
    global currentDoctorData
    global doctorAptVisible

    # Check if the user is a patient or has the appropriate role
    currentUser, role = checkCurrentUser(pickleFile)

    if currentUser == "":
        messagebox.showinfo("Log In!", "You must log in to proceed.")
        return

    if currentUser.startswith("P-") or role == "Patient":
        try:
            # Get clinicId and other appointment details from textboxes and calendar
            appointmentId = generateAppointmentId()
            clinicId = currentClinicData.get('ClinicId')
            patientId = currentUser
            if doctorAptVisible:
                doctorId = currentDoctorData.get('DoctorId')
                appointmentDate = lblCalendarDoctor.selection_get()
                appointmentTime = dropApTimeDoctor.get()
                if radioVar.get() == 0:
                    appointmentType = "Home Visit"
                elif radioVar.get() == 1:
                    appointmentType = "Walk In"
                else:
                    appointmentType = None
                appointmentAddress = tbApAddressDoctor.get("1.0", "end-1c")
                appointmentMedicalConcern = tbApConcernDoctor.get("1.0", "end-1c")
            else:
                doctorId = "-"
                appointmentDate = lblCalendarClinic.selection_get()
                appointmentTime = dropApTimeClinic.get()
                if radioVar.get() == 0:
                    appointmentType = "Home Visit"
                elif radioVar.get() == 1:
                    appointmentType = "Walk In"
                else:
                    appointmentType = None
                appointmentAddress = tbApAddressClinic.get("1.0", "end-1c")
                appointmentMedicalConcern = tbApConcernClinic.get("1.0", "end-1c")
            
            if appointmentTime == "Select Time":
                appointmentTime = None

            # Combine date and time into a datetime string
            if appointmentDate and appointmentTime:
                appointmentDateTime = appointmentDate.strftime("%Y-%m-%d") + ", " + appointmentTime
            else:
                appointmentDateTime = None
            
            # Check if any 'temp-' user files exist in Firebase Storage
            bucket = storage.bucket()
            blobs = bucket.list_blobs(prefix=f"temp-{currentUser}")
            for blob in blobs:
                # Move the file to MedicalDocs with the new filename
                newFilename = f"MedicalDocs/{appointmentId}.{blob.name.split('.')[-1]}"  # Use the original file extension
                bucket.rename_blob(blob, newFilename)
                appointmentMedicalDoc = newFilename  # Set path in Firestore
                break  # Assuming you only want to move one file, remove this line if you want to move all

            # If no 'temp-' files were found, set appointmentMedicalDoc to "-"
            else:
                appointmentMedicalDoc = "-"

            # Validate if all required fields are filled
            if appointmentDateTime and appointmentType and appointmentAddress and appointmentMedicalConcern:
                # Convert appointmentDate to a format suitable for Firestore (e.g., as a string)
                appointmentData = {
                    'PatientId': patientId,
                    'ClinicId': clinicId,
                    'DoctorId': doctorId,
                    'AppointmentType': appointmentType,
                    'PatientAddress': appointmentAddress,
                    'MedicalConcern': appointmentMedicalConcern,
                    'MedicalDocs': appointmentMedicalDoc,
                    'DateTime': appointmentDateTime,
                    'Prescription': '-',
                    'Status': 'Pending'
                }
                
                # Add appointment data to Firestore
                db.collection('AppointmentDetails').document(appointmentId).set(appointmentData)
                
                messagebox.showinfo("Appointment Created", f"Appointment has been successfully made!\nID: {appointmentId}")
                dropApTimeClinic.set("Select Time")
                dropApTimeClinic.configure(values=["Select Time"])
                dropApTimeDoctor.set("Select Time")
                dropApTimeDoctor.configure(values=["Select Time"])
                lblApUploadNoteClinic.configure(text="If there are multiple files, use a zip.")
                lblApUploadNoteDoctor.configure(text="If there are multiple files, use a zip.")
            else:
                messagebox.showwarning("Incomplete Information", "Please fill in all required fields.")

        except Exception as e:
            print(f"Error creating appointment: {e}")
            messagebox.showerror("Error", "An error occurred while creating the appointment.")
    
    elif currentUser != "":
        messagebox.showinfo("Invalid Account", "Please log in with a normal account to proceed.")
    else:
        btnLogin_Click()

# App configurations
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1)

# Frames
frameSideNav = CTkFrame(master=app, fg_color="#5271FF", corner_radius=0, width=80)
frameSideNav.grid(row=0, rowspan=2, column=0, sticky="nws")

frameProfile = CTkScrollableFrame(master=app, fg_color="#B5CAFF", bg_color="transparent", corner_radius=0, 
                                  orientation="vertical", scrollbar_button_color="white")
frameProfile.grid_forget()
frameProfile.grid_columnconfigure(0, weight=1)
frameProfile.grid_columnconfigure(1, weight=1)
frameProfile.grid_rowconfigure(0, weight=1)
frameProfile.grid_rowconfigure(1, weight=1)

frameProfileDetails = CTkFrame(master=frameProfile, fg_color="transparent", bg_color="transparent", corner_radius=0)
frameProfileDetails.grid_forget()
frameProfileDetails.grid_columnconfigure(0, weight=1)
frameProfileDetails.grid_columnconfigure(1, weight=1)
frameProfileDetails.grid_rowconfigure(0, weight=1)
frameProfileDetails.grid_rowconfigure(1, weight=1)
frameProfileDetails.grid_rowconfigure(2, weight=1)
frameProfileDetails.grid_rowconfigure(3, weight=1)
frameProfileDetails.grid_rowconfigure(4, weight=1)
frameProfileDetails.grid_rowconfigure(5, weight=1)
frameProfileDetails.grid_rowconfigure(6, weight=1)
frameProfileDetails.grid_rowconfigure(7, weight=1)

frameHome = CTkScrollableFrame(master=app, fg_color="#B5CAFF", corner_radius=0, orientation="vertical", 
                                 scrollbar_button_color="white")
frameHome.grid(row=0, column=1, sticky="news")
frameHome.grid_columnconfigure(0, weight=1)
frameHome.grid_rowconfigure(0, weight=1)

frameClinic = CTkScrollableFrame(master=app, fg_color="#B5CAFF", corner_radius=0, orientation="vertical", 
                                 scrollbar_button_color="white")
frameClinic.grid_forget()
frameClinic.grid_columnconfigure(0, weight=1)
frameClinic.grid_columnconfigure(1, weight=1)
frameClinic.grid_rowconfigure(0, weight=1)

frameDoctors = CTkFrame(master=frameClinic, bg_color="transparent", fg_color="transparent")
frameDoctors.grid(row=4, column=0, columnspan=3, sticky="new", padx=47)
frameDoctors.grid_columnconfigure(0, weight=1)
frameDoctors.grid_columnconfigure(1, weight=1)
frameDoctors.grid_columnconfigure(2, weight=1)
frameDoctors.grid_rowconfigure(0, weight=1)

frameDoctorIndiv = CTkScrollableFrame(master=app, fg_color="#B5CAFF", corner_radius=0, orientation="vertical", 
                                      scrollbar_button_color="white")
frameDoctorIndiv.grid_forget()
frameDoctorIndiv.grid_columnconfigure(0, weight=1)
frameDoctorIndiv.grid_columnconfigure(1, weight=1)
frameDoctorIndiv.grid_rowconfigure(0, weight=1)
frameDoctorIndiv.grid_rowconfigure(1, weight=1)
frameDoctorIndiv.grid_rowconfigure(2, weight=1)

frameClinicBook = CTkScrollableFrame(master=app, fg_color="#B5CAFF", corner_radius=0, orientation="vertical", 
                                      scrollbar_button_color="white")
frameClinicBook.grid_forget()
frameClinicBook.grid_columnconfigure(0, weight=1)
frameClinicBook.grid_columnconfigure(1, weight=1)
frameClinicBook.grid_rowconfigure(0, weight=1)

frameCalendarClinic = CTkFrame(master=frameClinicBook, bg_color="transparent", fg_color="#5271FF", corner_radius=20)
frameCalendarClinic.grid(row=5, column=0, sticky="news", padx=(22,17), pady=(20,100))

frameCalendarDoctor = CTkFrame(master=frameDoctorIndiv, bg_color="transparent", fg_color="#5271FF", corner_radius=20)
frameCalendarDoctor.grid(row=3, column=0, columnspan=1, sticky="news", padx=(22,17), pady=(20,100))

frameAppointmentClinic = CTkFrame(master=frameClinicBook, bg_color="transparent", fg_color="transparent")
frameAppointmentClinic.grid(row=5, column=1, sticky="new", padx=(0,17), pady=(20,20))
frameAppointmentClinic.grid_columnconfigure(0, weight=1)
frameAppointmentClinic.grid_rowconfigure(0, weight=1)
frameAppointmentClinic.grid_rowconfigure(1, weight=1)
frameAppointmentClinic.grid_rowconfigure(2, weight=1)
frameAppointmentClinic.grid_rowconfigure(3, weight=1)
frameAppointmentClinic.grid_rowconfigure(4, weight=1)

frameAppointmentDoctor = CTkFrame(master=frameDoctorIndiv, bg_color="transparent", fg_color="transparent")
frameAppointmentDoctor.grid(row=3, column=1, sticky="new", padx=(0,17), pady=20)
frameAppointmentDoctor.grid_columnconfigure(0, weight=1)
frameAppointmentDoctor.grid_rowconfigure(0, weight=1)
frameAppointmentDoctor.grid_rowconfigure(1, weight=1)
frameAppointmentDoctor.grid_rowconfigure(2, weight=1)
frameAppointmentDoctor.grid_rowconfigure(3, weight=1)
frameAppointmentDoctor.grid_rowconfigure(4, weight=1)

# Shared Images
imgBtnBack = Image.open("./SE Project/Images/back.png")
imgBtnSearch = Image.open("./SE Project/Images/search.png")
imgLogo = Image.open("./SE Project/Images/logo.png")

# Side navigation bar widgets
imgBtnMenu = Image.open("./SE Project/Images/menu.png")
btnMenu = CTkButton(master=frameSideNav, text="", image=CTkImage(imgBtnMenu, size=(45,35)), 
                    fg_color="transparent", command=btnMenu_Click)
btnMenu.place(relx=0.5, rely=0.06, anchor="center")

imgBtnHome = Image.open("./SE Project/Images/home-icon-white.png")
btnHome = CTkButton(master=frameSideNav, text="", image=CTkImage(imgBtnHome, size=(50,50)), font=("Inter",12),
                    fg_color="transparent", command=btnHome_Click)
btnHome.place(relx=0.5, rely=0.3, anchor="center")

imgBtnBookHis = Image.open("./SE Project/Images/booking-history-white.png")
btnBookHis = CTkButton(master=frameSideNav, text="", image=CTkImage(imgBtnBookHis, size=(60,60)), font=("Inter",12),
                       fg_color="transparent", command=btnBookHis_Click)

imgBtnClinicPg = Image.open("./SE Project/Images/clinic-white.png")
btnClinicPg = CTkButton(master=frameSideNav, text="", image=CTkImage(imgBtnClinicPg, size=(58,58)), font=("Inter",12),
                       fg_color="transparent", command=btnClinicPg_Click)

imgBtnDoctorPg = Image.open("./SE Project/Images/doctor-white.png")
btnDoctorPg = CTkButton(master=frameSideNav, text="", image=CTkImage(imgBtnDoctorPg, size=(48,48)), font=("Inter",12),
                       fg_color="transparent", command=btnDoctorPg_Click)

imgBtnAdmin = Image.open("./SE Project/Images/admin.png")
btnAdminPg = CTkButton(master=frameSideNav, text="", image=CTkImage(imgBtnAdmin, size=(50,50)), font=("Inter",12),
                       fg_color="transparent", command=btnAdminPg_Click)

# Logo for home page
lblHomeLogo = CTkLabel(master=frameHome, text="", bg_color="white", image=CTkImage(imgLogo, size=(453,198)))
lblHomeLogo.grid(row=0, column=0, sticky="ewn")

# Smaller logo for the rest of the pages
lblLogo = CTkLabel(master=app, text="", bg_color="white", image=CTkImage(imgLogo, size=(180, 80)), anchor="w")

# Login buttons
imgBtnLogin = Image.open("./SE Project/Images/profile-user-blue.png")
btnLogin1 = CTkButton(master=frameHome, text="", image=CTkImage(imgBtnLogin, size=(50,50)), text_color="#5271FF", font=("Inter",18),
                     fg_color="white", corner_radius=0, anchor="w", width=50, command=btnLogin_Click, compound=RIGHT)
btnLogin1.grid(row=0, column=0, sticky="ne", pady=12)

btnLogin2 = CTkButton(master=app, text="", image=CTkImage(imgBtnLogin, size=(50,50)), text_color="#5271FF", font=("Inter",18),
                     fg_color="white", corner_radius=0, anchor="w", width=50, command=btnLogin_Click, compound=RIGHT)

def updateUi():
    currentUser, role = checkCurrentUser(pickleFile)
    if currentUser != "":
        # Update UI elements for logged-in state
        btnLogin1.configure(text=currentUser)
        btnLogin2.configure(text=currentUser)
    else:
        btnLogin1.configure(text="")
        btnLogin2.configure(text="")

# Widgets in frameProfileDetails which is only available to Patients
btnBackProfile = CTkButton(master=frameProfileDetails, text="", image=CTkImage(imgBtnBack, size=(25,25)), fg_color="transparent",
                           bg_color="transparent", width=0, command=btnBackProfile_Click)
btnBackProfile.grid(row=0, column=0, sticky="nw", pady=20)

imgLblProfile = Image.open("./SE Project/Images/profile-user-blue.png")
LblProfile = CTkLabel(master=frameProfileDetails, text="", image=CTkImage(imgLblProfile, size=(157,157)), bg_color="transparent")
LblProfile.grid(row=0, column=0, columnspan=2, sticky="new", padx=(50,0), pady=(60,20))

lblUserEmail = CTkLabel(master=frameProfileDetails, text="Email Address", font=("Inter",24,"bold"), text_color="#5271FF", 
                       fg_color="transparent", anchor="w")
lblUserEmail.grid(row=1, column=0, sticky="new", padx=(10,0), pady=20)
lblUserEmailText = CTkLabel(master=frameProfileDetails, text="", font=("Inter",24), text_color="white", 
                       fg_color="transparent", anchor="w")
lblUserEmailText.grid(row=1, column=1, sticky="new", pady=20)
tbUserEmail = CTkEntry(master=frameProfileDetails, corner_radius=20, font=("Inter",20), fg_color="white", border_width=0,
                      height=35)

lblUserPassword = CTkLabel(master=frameProfileDetails, text="Password", font=("Inter",24,"bold"), text_color="#5271FF", 
                       fg_color="transparent", anchor="w")
lblUserPassword.grid(row=2, column=0, sticky="new", padx=(10,0), pady=20)
lblUserPasswordText = CTkLabel(master=frameProfileDetails, text="", font=("Inter",24), text_color="white", 
                       fg_color="transparent", anchor="w")
lblUserPasswordText.grid(row=2, column=1, sticky="new", pady=20)
tbUserPassword = CTkEntry(master=frameProfileDetails, corner_radius=20, font=("Inter",20), fg_color="white", border_width=0,
                      height=35, show="●")

lblUserNewPassword = CTkLabel(master=frameProfileDetails, text="New Password", font=("Inter",24,"bold"), text_color="#5271FF", 
                       fg_color="transparent", anchor="w")
tbUserNewPassword = CTkEntry(master=frameProfileDetails, corner_radius=20, font=("Inter",20), fg_color="white", border_width=0,
                      height=35, show="●")

lblUserName = CTkLabel(master=frameProfileDetails, text="Name", font=("Inter",24,"bold"), text_color="#5271FF", 
                       fg_color="transparent", anchor="w")
lblUserName.grid(row=4, column=0, sticky="new", padx=(10,0), pady=20)
lblUserNameText = CTkLabel(master=frameProfileDetails, text="", font=("Inter",24), text_color="white", 
                       fg_color="transparent", anchor="w")
lblUserNameText.grid(row=4, column=1, sticky="new",pady=20)
tbUserName = CTkEntry(master=frameProfileDetails, corner_radius=20, font=("Inter",20), fg_color="white", border_width=0,
                      height=35)

lblUserPhoneNo = CTkLabel(master=frameProfileDetails, text="Phone Number", font=("Inter",24,"bold"), text_color="#5271FF", 
                       fg_color="transparent", anchor="w")
lblUserPhoneNo.grid(row=5, column=0, sticky="new", padx=(10,0), pady=20)
lblUserPhoneNoText = CTkLabel(master=frameProfileDetails, text="", font=("Inter",24), text_color="white", 
                       fg_color="transparent", anchor="w")
lblUserPhoneNoText.grid(row=5, column=1, sticky="new", pady=20)
tbUserPhoneNo = CTkEntry(master=frameProfileDetails, corner_radius=20, font=("Inter",20), fg_color="white", border_width=0,
                      height=35)

lblUserAddress = CTkLabel(master=frameProfileDetails, text="Home Address", font=("Inter",24,"bold"), text_color="#5271FF", 
                       fg_color="transparent", anchor="w")
lblUserAddress.grid(row=6, column=0, sticky="new", padx=(10,0), pady=20)
lblUserAddressText = CTkLabel(master=frameProfileDetails, text="", font=("Inter",24), text_color="white", 
                       fg_color="transparent", anchor="w")
lblUserAddressText.grid(row=6, column=1, sticky="new", pady=20)
tbUserAddress = CTkTextbox(master=frameProfileDetails, corner_radius=20, font=("Inter",20), fg_color="white", border_width=0,
                      height=87)

# Logout button available for all roles
btnLogout = CTkButton(master=frameProfile, text="Logout", font=("Inter",20,"bold"), corner_radius=20, fg_color="red",
                      command=btnLogout_Click)
btnLogout.grid(row=1, column=0, sticky="w", padx=50, pady=50)

btnEditProfile = CTkButton(master=frameProfile, text="Edit", font=("Inter",20,"bold"), corner_radius=20, fg_color="#5271FF",
                      command=btnEditProfile_Click)
btnEditProfile.grid(row=1, column=1, sticky="e",padx=50, pady=50)

btnEditProfileCancel = CTkButton(master=frameProfile, text="Cancel", font=("Inter",20,"bold"), corner_radius=20, fg_color="red",
                      command=btnEditProfileCancel_Click)
btnEditProfileSave = CTkButton(master=frameProfile, text="Save", font=("Inter",20,"bold"), corner_radius=20, fg_color="#5271FF",
                      command=btnEditProfileSave_Click)

# Call the function upon app load
updateUi()

# Searh bar on home page
dropSearch = CTkOptionMenu(master=frameHome, values=["Clinics", "Doctors"], fg_color="white", dropdown_fg_color="white",
                         button_color="white", button_hover_color="white", width=206, height=59, anchor="center",
                         corner_radius=20, font=("Inter",20), text_color="#898989", command=dropSearch_Filter)
dropSearch.grid(row=1, column=0, sticky="nw", padx=47, pady=40)

tbSearch = CTkEntry(master=frameHome, fg_color="white", width=700, height=59, corner_radius=20, font=("Inter",20), 
                      text_color="black", border_width=0)
tbSearch.grid(row=1, column=0, sticky="new", padx=(238,47), pady=40)

lblBehindSearch = CTkLabel(master=frameHome, text="|", font=("Inter",28), text_color="#5271FF", bg_color="white", width=18, 
                             height=59)
lblBehindSearch.grid(row=1, column=0, sticky="nw", padx=236, pady=40)

btnSearch = CTkButton(master=frameHome, text="", image=CTkImage(imgBtnSearch, size=(25,25)), 
                     fg_color="white", corner_radius=0, anchor="center", width=25, command=btnSearch_Click)
btnSearch.grid(row=1, column=0, sticky="ne", padx=60, pady=55)

# Individual clinic's page setup
btnBackClinicIndiv = CTkButton(master=frameClinic, text="", image=CTkImage(imgBtnBack, size=(25,25)), width=25,
                               fg_color="transparent", command=btnBackClinicIndiv_Click)
btnBackClinicIndiv.grid(row=1, column=0, columnspan=3, padx=10, pady=(110,0), sticky="nw")

# Labels to display the clinic info in frameClinic
lblImgClinicIndiv = CTkLabel(master=frameClinic, text="", bg_color="transparent", width=220, height=200)
lblImgClinicIndiv.grid(row=2, column=0, columnspan=3, sticky="nw", padx=12, pady=30)

lblTextClinicIndiv = CTkLabel(master=frameClinic, text="", height=200, corner_radius=20, fg_color="white", 
                                text_color="#5D5D5D", font=("Inter", 20), justify="left", anchor="w")
lblTextClinicIndiv.grid(row=2, column=0, columnspan=3, sticky="new", padx=(282,10), pady=30)

lblBehindClinicIndiv = CTkLabel(master=frameClinic, text="", fg_color="white", width=23, height=200)
lblBehindClinicIndiv.grid(row=2, column=0, sticky="w", padx=274, pady=20)

# Booking button for individual clinic
btnClinicBook = CTkButton(master=frameClinic, text="Book Appointment", corner_radius=20, font=("Inter",20,"bold"), 
                          text_color="white", bg_color="white", fg_color="#5271FF", command=btnClinicBook_Click)
btnClinicBook.grid(row=2, column=0, columnspan=3, sticky="se", padx=(0, 20), pady=(0,38))

# Searh Bar for doctors
dropSearchDoc = CTkOptionMenu(master=frameClinic, values=["Specialty", "S1", "S2", "etc"], fg_color="white", 
                              dropdown_fg_color="white", button_color="white", button_hover_color="white", width=206, 
                              height=59, anchor="center", corner_radius=20, font=("Inter",20), text_color="#898989")
dropSearchDoc.grid(row=3, column=0, columnspan=3, sticky="nw", padx=47, pady=30)

tbSearchDoc = CTkEntry(master=frameClinic, fg_color="white", width=700, height=59, corner_radius=20, font=("Inter",15), 
                      text_color="black", border_width=0)
tbSearchDoc.grid(row=3, column=0, columnspan=3, sticky="new", padx=(238,47), pady=30)

lblBehindSearchDoc = CTkLabel(master=frameClinic, text="|", font=("Inter",28), text_color="#5271FF", bg_color="white", width=18, 
                             height=59)
lblBehindSearchDoc.grid(row=3, column=0, columnspan=3, sticky="nw", padx=237, pady=30)

btnSearchDoc = CTkButton(master=frameClinic, text="", image=CTkImage(imgBtnSearch, size=(25,25)), 
                     fg_color="white", corner_radius=0, anchor="center", width=25, command=btnSearchDoc_Click)
btnSearchDoc.grid(row=3, column=0, columnspan=2, sticky="ne", padx=59, pady=45)

# Individual doctor's page
imgBtnBackDoctorIndiv = CTkButton(master=frameDoctorIndiv, text="", image=CTkImage(imgBtnBack, size=(25,25)), width=25,
                               fg_color="transparent", command=btnBackDoctorIndiv_Click)
imgBtnBackDoctorIndiv.grid(row=1, column=0, columnspan=3, padx=10, pady=(110,0), sticky="nw")

lblImgDoctorIndiv = CTkLabel(master=frameDoctorIndiv, text="", bg_color="transparent", width=255,
                                 height=200, corner_radius=20)
lblImgDoctorIndiv.grid(row=2, column=0, columnspan=2, sticky="nw", pady=30)

lblTextDoctorIndiv = CTkLabel(master=frameDoctorIndiv, text="", height=200, corner_radius=20, fg_color="white", 
                                text_color="#5D5D5D", font=("Inter", 20), justify="left", anchor="w")
lblTextDoctorIndiv.grid(row=2, column=0, columnspan=2, sticky="new", padx=(272,10), pady=30)

lblBehindDoctorIndiv = CTkLabel(master=frameDoctorIndiv, text="", fg_color="white", width=33, height=200)
lblBehindDoctorIndiv.grid(row=2, column=0, columnspan=2, sticky="w", padx=255, pady=20)

# Widgets to get appointment details
btnBackClinicBook = CTkButton(master=frameClinicBook, text="", image=CTkImage(imgBtnBack, size=(25,25)),
                              command=btnBackClinicBook_Click, fg_color="transparent", width=0)
btnBackClinicBook.grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(100,10))

lblClinicBook = CTkLabel(master=frameClinicBook, text="", font=("Inter",34,"bold"), text_color="#5271FF")
lblClinicBook.grid(row=1, column=0, columnspan=2, sticky="w", padx=20, pady=10)

imglblLineClinicBook = Image.open("./SE Project/Images/line.png")
lblLineClinicBook = CTkLabel(master=frameClinicBook, text="", image=CTkImage(imglblLineClinicBook, size=(800,1)), bg_color="transparent")
lblLineClinicBook.grid(row=2, column=0, columnspan=2, sticky="ew", padx=100, pady=5)

# Calendar setups
lblCalendarClinic = Calendar(master=frameCalendarClinic, font=("Inter", 45), background="#5271FF", selectbackground="#5271FF", 
                        headersbackground="#B5CAFF", headersforeground="white", normalforeground="#5D5D5D",
                        weekendbackground="white", othermonthforeground="#BDBDBD", othermonthbackground="white", 
                        othermonthweforeground="#BDBDBD", othermonthwebackground="white", borderwidth=3, bordercolor="white", 
                        showweeknumbers=False, firstweekday="sunday", selectmode='day', mindate=datetime.now(), 
                        disabledbackground="#5271FF", maxdate=datetime.now()+timedelta(days=365), 
                        date_pattern='yyyy-mm-dd')
lblCalendarClinic.pack(fill="both", expand=True, padx=20, pady=20)
lblCalendarClinic.selection_set(None)

lblCalendarDoctor = Calendar(master=frameCalendarDoctor, font=("Inter", 45), background="#5271FF", selectbackground="#5271FF", 
                        headersbackground="#B5CAFF", headersforeground="white", normalforeground="#5D5D5D",
                        weekendbackground="white", othermonthforeground="#BDBDBD", othermonthbackground="white", 
                        othermonthweforeground="#BDBDBD", othermonthwebackground="white", borderwidth=3, bordercolor="white", 
                        showweeknumbers=False, firstweekday="sunday", selectmode='day', mindate=datetime.now(), 
                        disabledbackground="#5271FF", maxdate=datetime.now()+timedelta(days=365), 
                        date_pattern='yyyy-mm-dd')
lblCalendarDoctor.pack(fill="both", expand=True, padx=20, pady=20)
lblCalendarDoctor.selection_set(None)

# Clinic appointment details
dropApTimeClinic = CTkOptionMenu(master=frameAppointmentClinic, values=["Select Time"], fg_color="white", dropdown_fg_color="white",
                         button_color="white", button_hover_color="white", height=30, corner_radius=20, 
                         font=("Inter",20), text_color="#898989", anchor="center", command=dropApTimeClinic_Click)
dropApTimeClinic.grid(row=0, column=0, columnspan=2, sticky="new")

lblTextApTypeClinic = CTkLabel(master=frameAppointmentClinic, text="Appointment Type", font=("Inter", 24, "bold"), text_color="#5271FF",
                         anchor="w", justify="left")
lblTextApTypeClinic.grid(row=1, column=0, columnspan=2, sticky="new", pady=(20,10))

radioVar = IntVar(value=0)
btnApTypeVisitClinic = CTkRadioButton(master=frameAppointmentClinic, text="Doctor Home Visit", text_color="#5D5D5D", font=("Inter",20),
                                border_color="white", radiobutton_width=20, radiobutton_height=20, hover_color="#5271FF",
                                border_width_checked=8, border_width_unchecked=10, fg_color="#5271FF", variable= radioVar,
                                value=0, command=btnApTypeVisit_Click)
btnApTypeVisitClinic.grid(row=2, column=0, sticky="new")
btnApTypeWalkInClinic = CTkRadioButton(master=frameAppointmentClinic, text="Walk In", text_color="#5D5D5D", font=("Inter",20),
                                border_color="white", radiobutton_width=20, radiobutton_height=20, hover_color="#5271FF",
                                border_width_checked=8, border_width_unchecked=10, fg_color="#5271FF", variable= radioVar,
                                value=1, command=btnApTypeWalkIn_Click)
btnApTypeWalkInClinic.grid(row=2, column=1, sticky="new")

lblTextApAddressClinic = CTkLabel(master=frameAppointmentClinic, text="Address", font=("Inter", 24, "bold"), text_color="#5271FF",
                         anchor="w", justify="left")
lblTextApAddressClinic.grid(row=3, column=0, columnspan=2, sticky="new", pady=(30,10))

tbApAddressClinic = CTkTextbox(master=frameAppointmentClinic, corner_radius=20, height=132, font=("Inter",20), scrollbar_button_color="#5271FF",
                         wrap="word")
tbApAddressClinic.grid(row=4, column=0, columnspan=2, sticky="new")

lblTextApConcernClinic = CTkLabel(master=frameAppointmentClinic, text="Medical Concern", font=("Inter", 24, "bold"), text_color="#5271FF",
                         anchor="w", justify="left")
lblTextApConcernClinic.grid(row=5, column=0, columnspan=2, sticky="new", pady=(30,10))

tbApConcernClinic = CTkTextbox(master=frameAppointmentClinic, corner_radius=20, height=90, font=("Inter",20), scrollbar_button_color="#5271FF",
                         wrap="word")
tbApConcernClinic.grid(row=6, column=0, columnspan=2, sticky="new")

imgBtnApUploadClinic = Image.open("./SE Project/Images/upload.png")
btnApUploadClinic = CTkButton(master=frameAppointmentClinic, image=CTkImage(imgBtnApUploadClinic, size=(20,20)), text="Related Medical Document(s)",
                        font=("Inter",20,"bold"), text_color="#5271FF", fg_color="white", anchor="center", 
                        corner_radius=20, command=btnApUpload_Click)
btnApUploadClinic.grid(row=7, column=0, columnspan=1, sticky="nw", pady=30)

lblApUploadTextClinic = CTkLabel(master=frameAppointmentClinic, text="", font=("Inter",18,"bold"), text_color="#5271FF")
lblApUploadTextClinic.grid(row=7, column=1, columnspan=1, sticky="nw", pady=30)

lblApUploadNoteClinic = CTkLabel(master=frameAppointmentClinic, text="*If there are multiple files, use a zip.", 
                                 font=("Inter", 12, "italic"), text_color="#5271FF",
                         anchor="w", justify="left")
lblApUploadNoteClinic.grid(row=7, column=0, columnspan=2, sticky="nw", pady=(60,0))

btnProceedClinic = CTkButton(master=frameAppointmentClinic, text="Proceed", font=("Inter",20,"bold"), text_color="white", fg_color="#5271FF", 
                    anchor="center", corner_radius=20, command=btnProceed_Click)
btnProceedClinic.grid(row=8, column=0, columnspan=2, sticky="ne", pady=40)

# Doctor appointment details
dropApTimeDoctor = CTkOptionMenu(master=frameAppointmentDoctor, values=["Select Time"], fg_color="white", dropdown_fg_color="white",
                         button_color="white", button_hover_color="white", height=30, corner_radius=20, 
                         font=("Inter",20), text_color="#898989", anchor="center", command=dropApTimeDoctor_Click)
dropApTimeDoctor.grid(row=0, column=0, columnspan=2, sticky="new")

lblTextApTypeDoctor = CTkLabel(master=frameAppointmentDoctor, text="Appointment Type", font=("Inter", 24, "bold"), text_color="#5271FF",
                         anchor="w", justify="left")
lblTextApTypeDoctor.grid(row=1, column=0, columnspan=2, sticky="new", pady=(20,10))

btnApTypeVisitDoctor = CTkRadioButton(master=frameAppointmentDoctor, text="Doctor Home Visit", text_color="#5D5D5D", font=("Inter",20),
                                border_color="white", radiobutton_width=20, radiobutton_height=20, hover_color="#5271FF",
                                border_width_checked=8, border_width_unchecked=10, fg_color="#5271FF", variable= radioVar,
                                value=0, command=btnApTypeVisit_Click)
btnApTypeVisitDoctor.grid(row=2, column=0, sticky="new")
btnApTypeWalkInDoctor = CTkRadioButton(master=frameAppointmentDoctor, text="Walk In", text_color="#5D5D5D", font=("Inter",20),
                                border_color="white", radiobutton_width=20, radiobutton_height=20, hover_color="#5271FF",
                                border_width_checked=8, border_width_unchecked=10, fg_color="#5271FF", variable= radioVar,
                                value=1, command=btnApTypeWalkIn_Click)
btnApTypeWalkInDoctor.grid(row=2, column=1, sticky="new")

lblTextApAddressDoctor = CTkLabel(master=frameAppointmentDoctor, text="Address", font=("Inter", 24, "bold"), text_color="#5271FF",
                         anchor="w", justify="left")
lblTextApAddressDoctor.grid(row=3, column=0, columnspan=2, sticky="new", pady=(30,10))

tbApAddressDoctor = CTkTextbox(master=frameAppointmentDoctor, corner_radius=20, height=132, font=("Inter",20), scrollbar_button_color="#5271FF",
                         wrap="word")
tbApAddressDoctor.grid(row=4, column=0, columnspan=2, sticky="new")

lblTextApConcernDoctor = CTkLabel(master=frameAppointmentDoctor, text="Medical Concern", font=("Inter", 24, "bold"), text_color="#5271FF",
                         anchor="w", justify="left")
lblTextApConcernDoctor.grid(row=5, column=0, columnspan=2, sticky="new", pady=(30,10))

tbApConcernDoctor = CTkTextbox(master=frameAppointmentDoctor, corner_radius=20, height=90, font=("Inter",20), scrollbar_button_color="#5271FF",
                         wrap="word")
tbApConcernDoctor.grid(row=6, column=0, columnspan=2, sticky="new")

imgBtnApUploadDoctor = Image.open("./SE Project/Images/upload.png")
btnApUploadDoctor = CTkButton(master=frameAppointmentDoctor, image=CTkImage(imgBtnApUploadDoctor, size=(20,20)), text="Related Medical Document(s)",
                        font=("Inter",20,"bold"), text_color="#5271FF", fg_color="white", anchor="center", 
                        corner_radius=20, command=btnApUpload_Click)
btnApUploadDoctor.grid(row=7, column=0, columnspan=2, sticky="nw", pady=30)

lblApUploadNoteDoctor = CTkLabel(master=frameAppointmentDoctor, text="*If there are multiple files, use a zip.", font=("Inter", 12, "italic"), text_color="#5271FF",
                         anchor="w", justify="left")
lblApUploadNoteDoctor.grid(row=7, column=0, columnspan=2, sticky="nw", pady=(60,0))

btnProceedDoctor = CTkButton(master=frameAppointmentDoctor, text="Proceed", font=("Inter",20,"bold"), text_color="white", fg_color="#5271FF", 
                    anchor="center", corner_radius=20, command=btnProceed_Click)
btnProceedDoctor.grid(row=8, column=0, columnspan=2, sticky="ne", pady=40)

# Initialise the home page on run
resetUi()
frameHome.grid(row=0, column=1, sticky="news")
# Initialise the clinic list
dropSearch_Filter("Clinics","")

app.mainloop()