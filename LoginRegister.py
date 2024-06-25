from customtkinter import *
import firebase_admin
from firebase_admin import credentials, storage
from firebase_admin import firestore
from tkinter import messagebox
from PIL import Image
import hashlib
import pickle
import string
import random

cred = credentials.Certificate("serviceAccountKey.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {'storageBucket': 'call-a-doctor-20a5d.appspot.com'})

db = firestore.client()

pickleFile = 'userId.pkl'
clinicId = ""
userId = ""
tbClinicStartHours = ""
tbClinicEndHours = ""
tbClinicStartBreak = ""
tbClinicEndBreak = ""

def btnLogin_Click():
    emailOrUserId = tbLoginEmailUID.get()
    password = tbLoginPassword.get()
    userData = None

    try:
        if '@' in emailOrUserId:
            collectionsToCheck = ['Patients', 'Clinics', 'Doctors']
            for collection in collectionsToCheck:
                userRef = db.collection(collection).where('Email', '==', emailOrUserId).limit(1).get()
                if userRef:
                    print("Email found.")
                    userId = userRef[0].id

                    userRef = db.collection('Users').document(userId).get()
                    if userRef.exists:
                        userData = userRef.to_dict()
                    else:
                        userData = None
                    break
                else:
                    print("Email not found.")
        else:
            userRef = db.collection("Users").document(emailOrUserId).get()
            if userRef.exists:
                print("ID found.")
                userData = userRef.to_dict()

    except Exception as e:
        messagebox.showerror("Error", f"Error retrieving user: {e}")
        return

    if userData:
        storedPassword = userData.get('Password')
        hashedEnteredPassword = hashlib.sha256(password.encode()).hexdigest()
        if hashedEnteredPassword == storedPassword:
            userId = userRef.id
            role = userData.get('Role')
            with open(pickleFile, 'wb') as f:
                pickle.dump(userId + ',' + role, f)
            messagebox.showinfo("Login Successful", "You may close this window.")
        else:
            with open(pickleFile, 'wb') as f:
                pickle.dump(None, f)
            messagebox.showerror("Login Failed", "Incorrect password. Please try again.")
    else:
        messagebox.showerror("Login Failed", "User not found. Please check your credentials.")

def generateUserId():
    global userId
    # Define the range of characters for the ID
    characters = string.ascii_letters + string.digits

    while True:
        # Generate a random ID with the range of 6
        userId = 'P-' + ''.join(random.choices(characters, k=6))

        # Check if this ID already exists in the database
        userRef = db.collection('Patients').document(userId)
        if not userRef.get().exists:
            return userId

def btnOpenClinicPg_Click():
    frameLogin.pack_forget()
    frameRegisterUser.pack_forget()
    frameRegisterClinic.pack(fill="both", expand=True)

def btnOpenUserPg_Click():
    frameLogin.pack_forget()
    frameRegisterUser.pack(fill="both", expand=True)
    frameRegisterClinic.pack_forget()

def generateClinicId():
    # Define the range of characters for the ID
    characters = string.ascii_letters + string.digits

    while True:
        # Generate a random ID with the range of 6
        clinicId = 'C-' + ''.join(random.choices(characters, k=6))

        # Check if this ID already exists in the database
        clinicRef = db.collection('Clinics').document(clinicId)
        if not clinicRef.get().exists:
            return clinicId

def btnRegisterUser_Click():
    try:
        global userId
        userId = generateUserId()

        email = tbClinicEmail.get()
        password = tbClinicPassword.get()
        name = tbClinicName.get()
        phoneNo = tbClinicPhoneNo.get()
        address = tbClinicAddress.get("1.0", "end-1c")

        # Validate if all required fields are filled
        if email and password and name and phoneNo and address:
            # Convert appointmentDate to a format suitable for Firestore (e.g., as a string)
            userData = {
                'Email': email,
                'Name': name,
                'PhoneNo': phoneNo,
                'Address': address,
            }
            
            # Add clinic data to Firestore
            db.collection('Patients').document(userId).set(userData)
            
            messagebox.showinfo("Registration Success", f"The account for {userId} been registered.\nYou may close this window.")
            btnBack_Click()
        else:
            messagebox.showwarning("Incomplete Information", "Please fill in all required fields.")
    except Exception as e:
        print(f"Error registering account: {e}")
        # messagebox.showerror("Error", "An error occurred while registering the account.")

def btnClinicRegister_Click():
    global tbClinicStartHours
    global tbClinicEndHours
    global tbClinicStartBreak
    global tbClinicEndBreak

    try:
        global clinicId
        clinicId = generateClinicId()

        email = tbClinicEmail.get()
        password = tbClinicPassword.get()
        name = tbClinicName.get()
        phoneNo = tbClinicPhoneNo.get()
        address = tbClinicAddress.get("1.0", "end-1c")
        specialty = tbClinicSpecialty.get()
        description = tbClinicDescription.get("1.0", "end-1c")
        image = "-"
        grdFile = "-"

        # Check if any 'temp-' files exist in Firebase Storage
        bucket = storage.bucket()
        blobs1 = bucket.list_blobs(prefix=f"tempImage-{clinicId}")
        for blob in blobs1:
            # Move the file to MedicalDocs with the new filename
            newFilename = f"Clinics/{clinicId}.{blob.name.split('.')[-1]}"  # Use the original file extension
            bucket.rename_blob(blob, newFilename)
            image = newFilename  # Set path in Firestore
            break 

        blobs2 = bucket.list_blobs(prefix=f"tempGRD-{clinicId}")
        for blob in blobs2:
            # Move the file to MedicalDocs with the new filename
            newFilename = f"GRDDocs/{clinicId}.{blob.name.split('.')[-1]}"  # Use the original file extension
            bucket.rename_blob(blob, newFilename)
            grdFile = newFilename  # Set path in Firestore
            break 

        # Validate if all required fields are filled
        if email and password and name and phoneNo and address and image and specialty and description and grdFile:
            # Get selected days and hours
            selectedDays = []
            startHours = {}
            endHours = {}
            startBreaks = {}
            endBreaks = {}

            # Check each day individually and update hours if selected
            if var1.get() == "Monday":
                selectedDays.append("Monday")
                startHours["Monday"] = tbClinicStartHours.get()
                endHours["Monday"] = tbClinicEndHours.get()
                startBreaks["Monday"] = tbClinicStartBreak.get()
                endBreaks["Monday"] = tbClinicEndBreak.get()

            if var2.get() == "Tuesday":
                selectedDays.append("Tuesday")
                startHours["Tuesday"] = tbClinicStartHours.get()
                endHours["Tuesday"] = tbClinicEndHours.get()
                startBreaks["Tuesday"] = tbClinicStartBreak.get()
                endBreaks["Tuesday"] = tbClinicEndBreak.get()

            if var3.get() == "Wednesday":
                selectedDays.append("Wednesday")
                startHours["Wednesday"] = tbClinicStartHours.get()
                endHours["Wednesday"] = tbClinicEndHours.get()
                startBreaks["Wednesday"] = tbClinicStartBreak.get()
                endBreaks["Wednesday"] = tbClinicEndBreak.get()

            if var4.get() == "Thursday":
                selectedDays.append("Thursday")
                startHours["Thursday"] = tbClinicStartHours.get()
                endHours["Thursday"] = tbClinicEndHours.get()
                startBreaks["Thursday"] = tbClinicStartBreak.get()
                endBreaks["Thursday"] = tbClinicEndBreak.get()

            if var5.get() == "Friday":
                selectedDays.append("Friday")
                startHours["Friday"] = tbClinicStartHours.get()
                endHours["Friday"] = tbClinicEndHours.get()
                startBreaks["Friday"] = tbClinicStartBreak.get()
                endBreaks["Friday"] = tbClinicEndBreak.get()

            if var6.get() == "Saturday":
                selectedDays.append("Saturday")
                startHours["Saturday"] = tbClinicStartHours.get()
                endHours["Saturday"] = tbClinicEndHours.get()
                startBreaks["Saturday"] = tbClinicStartBreak.get()
                endBreaks["Saturday"] = tbClinicEndBreak.get()

            if var7.get() == "Sunday":
                selectedDays.append("Sunday")
                startHours["Sunday"] = tbClinicStartHours.get()
                endHours["Sunday"] = tbClinicEndHours.get()
                startBreaks["Sunday"] = tbClinicStartBreak.get()
                endBreaks["Sunday"] = tbClinicEndBreak.get()

            # Convert lists to comma-separated strings
            workDays = ', '.join(selectedDays)
            startHoursStr = ', '.join(startHours.values())
            endHoursStr = ', '.join(endHours.values())
            startBreaksStr = ', '.join(startBreaks.values())
            endBreaksStr = ', '.join(endBreaks.values())

            # Convert appointmentDate to a format suitable for Firestore (e.g., as a string)
            clinicData = {
                'Email': email,
                'Name': name,
                'PhoneNo': phoneNo,
                'Address': address,
                'Image': image,
                'Specialty': specialty,
                'Description': description,
                'WorkDays': workDays,
                'StartHours': startHoursStr,
                'EndHours': endHoursStr,
                'StartBreak': startBreaksStr,
                'EndBreak': endBreaksStr,
                'GRDFile': grdFile,
                'AppStatus': 'Pending',
            }
            
            # Add clinic data to Firestore
            db.collection('Clinics').document(clinicId).set(clinicData)
            
            messagebox.showinfo("Submitted", f"Clinic account has been submitted for approval.\nAwait our email in the coming days to find out if it's been approved.")
            btnBack_Click()
        else:
            messagebox.showwarning("Incomplete Information", "Please fill in all required fields.")

    except Exception as e:
        print(f"Error registering account: {e}")
        messagebox.showerror("Error", "An error occurred while registering the account.")

# Function to update hours based on selected days
def updateHours():
    # Clear previous option menus
    for widget in frameHours.winfo_children():
        widget.destroy()

    # Check each day individually and update hours if selected
    selectedDays = []
    if var1.get() == "Monday":
        selectedDays.append("Monday")
    if var2.get() == "Tuesday":
        selectedDays.append("Tuesday")
    if var3.get() == "Wednesday":
        selectedDays.append("Wednesday")
    if var4.get() == "Thursday":
        selectedDays.append("Thursday")
    if var5.get() == "Friday":
        selectedDays.append("Friday")
    if var6.get() == "Saturday":
        selectedDays.append("Saturday")
    if var7.get() == "Sunday":
        selectedDays.append("Sunday")
    
    hours = [f"{h:02d}:{m:02d}" for h in range(24) for m in (0, 30)]

    for i, day in enumerate(selectedDays):
        lblDay = CTkLabel(master=frameHours, text=f"{day} Work Hours", font=("Inter", 15, "bold"),
                          text_color="#5D5D5D")
        lblDay.grid(row=i, column=0, padx=(10, 10), sticky="w", pady=(10, 10))

        startHourVar = StringVar(value="00:00")
        endHourVar = StringVar(value="23:00")
        breakStartVar = StringVar(value="12:00")
        breakEndVar = StringVar(value="13:00")

        dropClinicStartHours = CTkOptionMenu(master=frameHours, variable=startHourVar, values=hours)
        dropClinicEndHours = CTkOptionMenu(master=frameHours, variable=endHourVar, values=hours)
        dropClinicStartBreak = CTkOptionMenu(master=frameHours, variable=breakStartVar, values=hours)
        dropClinicEndBreak = CTkOptionMenu(master=frameHours, variable=breakEndVar, values=hours)
        
        dropClinicStartHours.grid(row=i, column=1, sticky="ew", padx=(10, 10), pady=(10, 10))
        dropClinicEndHours.grid(row=i, column=2, sticky="ew", padx=(10, 10), pady=(10, 10))
        lblDay = CTkLabel(master=frameHours, text=f"Break Hours", font=("Inter", 15, "bold"),
                          text_color="#5D5D5D")
        lblDay.grid(row=i, column=3, padx=(10, 10), sticky="w", pady=(10, 10))
        dropClinicStartBreak.grid(row=i, column=4, sticky="ew", padx=(10, 10), pady=(10, 10))
        dropClinicEndBreak.grid(row=i, column=5, sticky="ew", padx=(10, 10), pady=(10, 10))

def btnClinicImageUpload_Click():
    global clinicId

    filepath = filedialog.askopenfilename(title="Select a File")
    
    if filepath:
        # Generate the filename in the format temp-currentUser.extension
        filename = f"tempImage-{clinicId}.{os.path.splitext(filepath)[1][1:]}"
        
        try:      
            bucket = storage.bucket()
            # Upload the new file to Firebase Storage with temp-currentUser filename
            blob = bucket.blob(filename)
            blob.upload_from_filename(filepath)
            print(f"File {filename} uploaded successfully to Firebase Storage.")
            lblClinicImage.configure(text="Clinic Image - Set")
        
        except Exception as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", "An error occurred while uploading the file.")

def btnClinicGRDFileUpload_Click():
    global clinicId

    filepath = filedialog.askopenfilename(title="Select a File")
    
    if filepath:
        # Generate the filename in the format temp-currentUser.extension
        filename = f"tempGRD-{clinicId}.{os.path.splitext(filepath)[1][1:]}"
        
        try:      
            bucket = storage.bucket()
            # Upload the new file to Firebase Storage with temp-currentUser filename
            blob = bucket.blob(filename)
            blob.upload_from_filename(filepath)
            print(f"File {filename} uploaded successfully to Firebase Storage.")
            lblClinicGRDFile.configure(text="GRD File - Set")
            lblClinicImage.configure(text="")
        
        except Exception as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", "An error occurred while uploading the file.")

def btnBack_Click():
    frameLogin.pack(fill="both", expand=True)
    frameRegisterUser.pack_forget()
    frameRegisterClinic.pack_forget()

app = CTk()
app.geometry("1080x664")
set_appearance_mode("light")

#def create_LoginReg(master):
frameLoginReg = CTkFrame(master=app, fg_color="#91BBF1", corner_radius=0)
frameLoginReg.pack(fill="both", expand=True)

# Frames
frameLogin = CTkFrame(master=frameLoginReg, fg_color="#91BBF1", corner_radius=0)
frameLogin.pack(fill="both", expand=True)
frameLogin.grid_columnconfigure(0, weight=1)
frameLogin.grid_rowconfigure(0, weight=1)
frameLogin.grid_rowconfigure(1, weight=1)

frameRegisterBtns = CTkFrame(master=frameLogin, fg_color="transparent")
frameRegisterBtns.grid(row=2, column=0, sticky="nw", padx=(0,10))

frameRegisterUser = CTkScrollableFrame(master=frameLoginReg, fg_color="transparent", orientation="vertical", 
                                       scrollbar_button_color="white")
frameRegisterUser.grid_columnconfigure(0, weight=1)
frameRegisterUser.grid_columnconfigure(1, weight=1)
frameRegisterUser.grid_rowconfigure(0, weight=1)
frameRegisterUser.grid_rowconfigure(1, weight=1)
frameRegisterUser.grid_rowconfigure(2, weight=1)
frameRegisterUser.grid_rowconfigure(3, weight=1)

frameRegisterClinic = CTkScrollableFrame(master=frameLoginReg, fg_color="transparent", orientation="vertical", 
                                       scrollbar_button_color="white")
frameRegisterClinic.grid_columnconfigure(1, weight=1)
frameRegisterClinic.grid_rowconfigure(0, weight=1)
frameRegisterClinic.grid_rowconfigure(1, weight=1)
frameRegisterClinic.grid_rowconfigure(2, weight=1)
frameRegisterClinic.grid_rowconfigure(3, weight=1)

frameWorkDays = CTkFrame(master=frameRegisterClinic, fg_color="transparent")
frameWorkDays.grid(row=10, column=0, columnspan=2, sticky="new", padx=(75,50), pady=20)

frameHours = CTkFrame(master=frameRegisterClinic, fg_color="transparent")
frameHours.grid(row=12, column=0, columnspan=2, sticky="new", padx=(70,0), pady=20)

# Widgets for the login page
imgLblProfile = Image.open("./SE Project/Images/profile-user-white.png")
LblProfile = CTkLabel(master=frameLogin, text="", image=CTkImage(imgLblProfile, size=(200,200)), bg_color="transparent")
LblProfile.grid(row=0, rowspan=2, column=0, sticky="w", padx=(50,0), pady=(60,0))

lblLoginEmailUID = CTkLabel(master=frameLogin, text="Email / User ID", font=("Inter",38,"bold"), text_color="#5271FF", 
                            bg_color="transparent")
lblLoginEmailUID.grid(row=0, column=0, sticky="sw", padx=(325,0), pady=(100,30))

tbLoginEmailUID = CTkEntry(master=frameLogin, bg_color="transparent", border_width=0, corner_radius=20, width=400, height=50,
                           font=("Inter",24))
tbLoginEmailUID.grid(row=0, column=0, sticky="sew", padx=(620,50), pady=30)

lblLoginPassword = CTkLabel(master=frameLogin, text="Password", font=("Inter",38,"bold"), text_color="#5271FF", 
                            bg_color="transparent")
lblLoginPassword.grid(row=1, column=0, sticky="nw", padx=(325,0), pady=30)

tbLoginPassword = CTkEntry(master=frameLogin, bg_color="transparent", border_width=0, corner_radius=20, width=400, height=50,
                           font=("Inter",24), show="●")
tbLoginPassword.grid(row=1, column=0, sticky="new", padx=(620,50), pady=30)

btnLogin = CTkButton(master=frameLogin, text="Login", font=("Inter",30,"bold"), text_color="white", fg_color="#5271FF",
                    corner_radius=20, width=208, height=50, command=btnLogin_Click)
btnLogin.grid(row=2, column=0, sticky="ne", padx=(0,50))

lblRegisterText = CTkLabel(master=frameRegisterBtns, text="Don’t have an account?", font=("Inter", 20, "bold"), text_color="#5D5D5D")
lblRegisterText.grid(row=0, column=0, sticky="nw", padx=(50,0))

btnRegisterUser = CTkButton(master=frameRegisterBtns, text="Click here to Register as a User", font=("Inter",20,"bold","underline"), 
                        text_color="#5271FF", fg_color="transparent", command=btnOpenUserPg_Click)
btnRegisterUser.grid(row=1, column=0, sticky="nw", padx=(50,0))

btnRegisterClinic = CTkButton(master=frameRegisterBtns, text="Click here to Register as a Clinic", font=("Inter",20,"bold","underline"), 
                            text_color="#5271FF", fg_color="transparent", command=btnOpenClinicPg_Click)
btnRegisterClinic.grid(row=2, column=0, sticky="nw", padx=(50,0), pady=(0,200))

# Register page for patients
imgLblProfile = Image.open("./SE Project/Images/profile-user-blue.png")
LblProfile = CTkLabel(master=frameRegisterUser, text="", image=CTkImage(imgLblProfile, size=(157,157)), bg_color="transparent",
                      anchor="center")
LblProfile.grid(row=0, column=0, columnspan=2, sticky="new", padx=(50,0), pady=(60,20))

imgBtnBack = Image.open("./SE Project/Images/back.png")
btnBack = CTkButton(master=frameRegisterUser, text="", image=CTkImage(imgBtnBack, size=(25,25)), bg_color="transparent",
                      font=("Inter",20,"bold"), fg_color="transparent", command=btnBack_Click, width=0)
btnBack.grid(row=0, column=0, columnspan=2, sticky="nw", padx=(50,0), pady=(60,0))

lblRegEmail = CTkLabel(master=frameRegisterUser, text="Email Address", font=("Inter",24,"bold"), text_color="#5271FF", 
                       fg_color="transparent", anchor="w")
lblRegEmail.grid(row=1, column=0, sticky="new", padx=(200,20), pady=20)
tbRegEmail = CTkEntry(master=frameRegisterUser, corner_radius=20, font=("Inter",20), fg_color="white", border_width=0,
                      height=35)
tbRegEmail.grid(row=1, column=1, sticky="new", padx=(20,200), pady=20)

lblRegPassword = CTkLabel(master=frameRegisterUser, text="Password", font=("Inter",24,"bold"), text_color="#5271FF", 
                       fg_color="transparent", anchor="w")
lblRegPassword.grid(row=2, column=0, sticky="new", padx=(200,20), pady=20)
tbRegPassword = CTkEntry(master=frameRegisterUser, corner_radius=20, font=("Inter",20), fg_color="white", border_width=0,
                      height=35, show="●")
tbRegPassword.grid(row=2, column=1, sticky="new", padx=(20,200), pady=20)

lblRegName = CTkLabel(master=frameRegisterUser, text="Name", font=("Inter",24,"bold"), text_color="#5271FF", 
                       fg_color="transparent", anchor="w")
lblRegName.grid(row=3, column=0, sticky="new", padx=(200,20), pady=20)
tbRegName = CTkEntry(master=frameRegisterUser, corner_radius=20, font=("Inter",20), fg_color="white", border_width=0,
                      height=35)
tbRegName.grid(row=3, column=1, sticky="new", padx=(20,200), pady=20)

lblRegPhoneNo = CTkLabel(master=frameRegisterUser, text="Phone Number", font=("Inter",24,"bold"), text_color="#5271FF", 
                       fg_color="transparent", anchor="w")
lblRegPhoneNo.grid(row=4, column=0, sticky="new", padx=(200,20), pady=20)
tbRegPhoneNo = CTkEntry(master=frameRegisterUser, corner_radius=20, font=("Inter",20), fg_color="white", border_width=0,
                      height=35)
tbRegPhoneNo.grid(row=4, column=1, sticky="new", padx=(20,200), pady=20)

lblRegAddress = CTkLabel(master=frameRegisterUser, text="Home Address", font=("Inter",24,"bold"), text_color="#5271FF", 
                       fg_color="transparent", anchor="w")
lblRegAddress.grid(row=5, column=0, sticky="new", padx=(200,20), pady=20)
tbRegAddress = CTkTextbox(master=frameRegisterUser, corner_radius=20, font=("Inter",20), fg_color="white", border_width=0,
                      height=87)
tbRegAddress.grid(row=5, column=1, sticky="new", padx=(20,200), pady=20)

btnRegisterUser = CTkButton(master=frameRegisterUser, text="Register", text_color="white", font=("Inter",20,"bold"), height=35,
                            fg_color="#5271FF", corner_radius=20, bg_color="transparent", anchor="center", command=btnRegisterUser_Click())
btnRegisterUser.grid(row=9, column=0, columnspan=6, sticky="n", pady=20)

# Register page for clinics
btnBack = CTkButton(master=frameRegisterClinic, text="", image=CTkImage(imgBtnBack, size=(25,25)), bg_color="transparent",
                      font=("Inter",20,"bold"), fg_color="transparent", command=btnBack_Click, width=0)
btnBack.grid(row=0, column=0, columnspan=2, sticky="nw", padx=(50,0), pady=(60,0))

lblClinicEmail = CTkLabel(master=frameRegisterClinic, text="Clinic Email", font=("Inter",20,"bold"),
                          text_color="#5271FF",  anchor="w")
tbClinicEmail = CTkEntry(master=frameRegisterClinic, font=("Inter",20), border_width=0, corner_radius=20)
lblClinicEmail.grid(row=1, column=0, sticky="new", padx=(200,0), pady=20)
tbClinicEmail.grid(row=1, column=1, sticky="new", padx=(50,200), pady=20)

lblClinicPassword = CTkLabel(master=frameRegisterClinic, text="Password", font=("Inter",20,"bold"),
                          text_color="#5271FF", anchor="w")
tbClinicPassword = CTkEntry(master=frameRegisterClinic, font=("Inter",20), border_width=0, corner_radius=20)
lblClinicPassword.grid(row=2, column=0, sticky="new", padx=(200,0), pady=20)
tbClinicPassword.grid(row=2, column=1, sticky="new", padx=(50,200), pady=20)

lblClinicName = CTkLabel(master=frameRegisterClinic, text="Clinic Name", font=("Inter",20,"bold"),
                          text_color="#5271FF",  anchor="w")
tbClinicName = CTkEntry(master=frameRegisterClinic, font=("Inter",20), border_width=0, corner_radius=20)
lblClinicName.grid(row=3, column=0, sticky="new", padx=(200,0), pady=20)
tbClinicName.grid(row=3, column=1, sticky="new", padx=(50,200), pady=20)

lblClinicPhoneNo = CTkLabel(master=frameRegisterClinic, text="Clinic Phone No", font=("Inter",20,"bold"),
                          text_color="#5271FF",  anchor="w")
tbClinicPhoneNo = CTkEntry(master=frameRegisterClinic, font=("Inter",20), border_width=0, corner_radius=20)
lblClinicPhoneNo.grid(row=4, column=0, sticky="new", padx=(200,0), pady=20)
tbClinicPhoneNo.grid(row=4, column=1, sticky="new", padx=(50,200), pady=20)

lblClinicAddress = CTkLabel(master=frameRegisterClinic, text="Clinic Address", font=("Inter",20,"bold"),
                          text_color="#5271FF",  anchor="w")
tbClinicAddress = CTkTextbox(master=frameRegisterClinic, font=("Inter",20), border_width=0, corner_radius=20, height=87)
lblClinicAddress.grid(row=5, column=0, sticky="new", padx=(200,0), pady=20)
tbClinicAddress.grid(row=5, column=1, sticky="new", padx=(50,200), pady=20)

lblClinicImage = CTkLabel(master=frameRegisterClinic, text="Clinic Image - Not Set", font=("Inter",20,"bold"),
                          text_color="#5271FF",  anchor="w")
btnClinicImageUpload = CTkButton(master=frameRegisterClinic, text="Upload Image", font=("Inter",20,"bold"), border_width=0, 
                                 corner_radius=20, fg_color="#5271FF", command=btnClinicImageUpload_Click)
lblClinicImage.grid(row=6, column=0, sticky="new", padx=(200,0), pady=20)
btnClinicImageUpload.grid(row=6, column=1, sticky="new", padx=(50,200), pady=20)

lblClinicSpecialty = CTkLabel(master=frameRegisterClinic, text="Clinic Specialty", font=("Inter",20,"bold"),
                          text_color="#5271FF",  anchor="w")
tbClinicSpecialty = CTkEntry(master=frameRegisterClinic, font=("Inter",20), border_width=0, corner_radius=20)
lblClinicSpecialty.grid(row=7, column=0, sticky="new", padx=(200,0), pady=20)
tbClinicSpecialty.grid(row=7, column=1, sticky="new", padx=(50,200), pady=20)

lblClinicDescription = CTkLabel(master=frameRegisterClinic, text="Clinic Description", font=("Inter",20,"bold"),
                          text_color="#5271FF",  anchor="w")
tbClinicDescription = CTkTextbox(master=frameRegisterClinic, font=("Inter",20), border_width=0, corner_radius=20,
                                 height=87)
lblClinicDescription.grid(row=8, column=0, sticky="new", padx=(200,0), pady=20)
tbClinicDescription.grid(row=8, column=1, sticky="new", padx=(50,200), pady=20)

# List of checkbox labels
workDays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

lblClinicWorkDays = CTkLabel(master=frameRegisterClinic, text="Choose Opening Days", font=("Inter",20,"bold"),
                          text_color="#5271FF",  anchor="w")
lblClinicWorkDays.grid(row=9, column=0, sticky="new", padx=(200,0), pady=(20,5))

# Creating checkboxes for work days
var1 = StringVar(value="-")
var2 = StringVar(value="-")
var3 = StringVar(value="-")
var4 = StringVar(value="-")
var5 = StringVar(value="-")
var6 = StringVar(value="-")
var7 = StringVar(value="-")

cbWorkDays = CTkCheckBox(master=frameWorkDays, text="Monday", text_color="#5271FF", font=("Inter", 20),
                             border_color="white", fg_color="#5271FF", hover_color="#5271FF", onvalue="Monday",
                             variable=var1, command=updateHours)
cbWorkDays.grid(row=0, column=1, sticky="new", padx=(10, 10), pady=(0, 20))
cbWorkDays = CTkCheckBox(master=frameWorkDays, text="Tuesday", text_color="#5271FF", font=("Inter", 20),
                             border_color="white", fg_color="#5271FF", hover_color="#5271FF", onvalue="Tuesday",
                             variable=var2, command=updateHours)
cbWorkDays.grid(row=0, column=2, sticky="new", padx=(10, 10), pady=(0, 20))
cbWorkDays = CTkCheckBox(master=frameWorkDays, text="Wednesday", text_color="#5271FF", font=("Inter", 20),
                             border_color="white", fg_color="#5271FF", hover_color="#5271FF", onvalue="Wednesday",
                             variable=var3, command=updateHours)
cbWorkDays.grid(row=0, column=3, sticky="new", padx=(10, 10), pady=(0, 20))
cbWorkDays = CTkCheckBox(master=frameWorkDays, text="Thursday", text_color="#5271FF", font=("Inter", 20),
                             border_color="white", fg_color="#5271FF", hover_color="#5271FF", onvalue="Thursday",
                             variable=var4, command=updateHours)
cbWorkDays.grid(row=0, column=4, sticky="new", padx=(10, 10), pady=(0, 20))
cbWorkDays = CTkCheckBox(master=frameWorkDays, text="Friday", text_color="#5271FF", font=("Inter", 20),
                             border_color="white", fg_color="#5271FF", hover_color="#5271FF", onvalue="Friday",
                             variable=var5, command=updateHours)
cbWorkDays.grid(row=0, column=5, sticky="new", padx=(10, 10), pady=(0, 20))
cbWorkDays = CTkCheckBox(master=frameWorkDays, text="Saturday", text_color="#5271FF", font=("Inter", 20),
                             border_color="white", fg_color="#5271FF", hover_color="#5271FF", onvalue="Saturday",
                             variable=var6, command=updateHours)
cbWorkDays.grid(row=0, column=6, sticky="new", padx=(10, 10), pady=(0, 20))
cbWorkDays = CTkCheckBox(master=frameWorkDays, text="Sunday", text_color="#5271FF", font=("Inter", 20),
                             border_color="white", fg_color="#5271FF", hover_color="#5271FF", onvalue="Sunday",
                             variable=var7, command=updateHours)
cbWorkDays.grid(row=0, column=7, sticky="new", padx=(10, 10), pady=(0, 20))

lblClinicGRDFile = CTkLabel(master=frameRegisterClinic, text="GRD File - Not Set", 
                            font=("Inter",20,"bold"), text_color="#5271FF",  anchor="w")
btnClinicGRDFileUpload = CTkButton(master=frameRegisterClinic, text="Upload File", font=("Inter",20,"bold"), border_width=0, 
                                 corner_radius=20, fg_color="#5271FF", command=btnClinicGRDFileUpload_Click)
lblClinicGRDFile.grid(row=13, column=0, columnspan=2, sticky="new", padx=(200,0), pady=(20,0))
btnClinicGRDFileUpload.grid(row=13, column=1, columnspan=2, sticky="new", padx=(50,200), pady=(20,5))

btnClinicRegister = CTkButton(master=frameRegisterClinic, text="Register Clinic", corner_radius=20, font=("Inter",20,"bold"),
                              text_color="#5271FF", fg_color="white", command=btnClinicRegister_Click)
btnClinicRegister.grid(row=14, column=0, columnspan=2, sticky="ne", padx=(50,50), pady=(50,20))

app.mainloop()
