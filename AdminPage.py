from tkinter import messagebox
from customtkinter import *
import customtkinter as ctk
import firebase_admin
from firebase_admin import credentials, storage
from firebase_admin import firestore
from PIL import Image, ImageDraw, ImageTk
import numpy as np
import cv2
from email.message import EmailMessage
import smtplib


class Clinic:
    def __init__(self, clinic_Id, address, app_status, description, email, end_break_hours, end_hours, GRD_status,
                 image, name, phone_no, specialty, start_break_hours, start_hours, work_days):
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
        self.__app_status = app_status
        self.__description = description
        self.__GRD_status = GRD_status

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

    def get_start_break_hours(self):
        return self.__start_break_hours

    def get_end_break_hours(self):
        return self.__end_break_hours

    def get_app_status(self):
        return self.__app_status

    def get_GRDStatus(self):
        return self.__GRD_status

    def get_description(self):
        return self.__description

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

    def set_app_status(self, app_status):
        self.__app_status = app_status

    def set_GRDStatus(self, GRD_status):
        self.__GRD_status = GRD_status

    def set_description(self, description):
        self.__description = description


cred = credentials.Certificate("serviceAccountKey.json")
# Check if firebase_admin has been initialized
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {'storageBucket': 'call-a-doctor-20a5d.appspot.com'})

db = firestore.client()

app = CTk()
app.geometry("1080x664")
# app.resizable(False, False)

set_appearance_mode("light")


def btnMenu_Click():
    print("Button Clicked")


pageBookHis = None


def btnHome_Click():
    print("Home button")


def btnBookHis_Click():
    print("Booking history")


def btnLogin_Click():
    print("Button Clicked")


def btnSearch_Click():
    print("Button Clicked")


# Function to get clinic information and display it
# Function to get clinic information and display it
def GetClinicInformation(filter_type, clinics_ref):
    # Fetch data from Firestore
    docs = clinics_ref.stream()

    # Prepare the data
    clinic_data_list = []
    for doc in docs:
        clinic_dict = doc.to_dict()
        clinic_dict['clinicId'] = doc.id
        clinic_data_list.append(clinic_dict)

    # Remove old clinic information widgets from frameHome
    for widget in frameClinicInfo.winfo_children():
        widget.destroy()

    row_index = 0

    # Fetch the Firebase Storage bucket
    bucket = storage.bucket()

    # Display each clinic data
    for clinic_info in clinic_data_list:
        clinic_id = clinic_info['clinicId']

        # Fetch clinic data from Firestore
        clinic_doc = db.collection('Clinics').document(clinic_id).get()
        if clinic_doc.exists:
            clinic_data = clinic_doc.to_dict()
            imgClinicList = clinic_data.get('Image')
            blob = bucket.get_blob(imgClinicList)
            if blob is not None:
                arr = np.frombuffer(blob.download_as_string(), np.uint8)
                img = cv2.imdecode(arr, cv2.IMREAD_COLOR)

                # Convert the numpy array to a PIL Image object
                pilImgClinicList = Image.fromarray(img)
                pilImgClinicList = add_rounded_corners(pilImgClinicList, 20)
                ctkImgClinicList = ctk.CTkImage(pilImgClinicList, size=(220, 150))
            else:
                # Placeholder image or handle missing image
                ctkImgClinicList = None

            # Create a Clinic instance
            clinic_instance = Clinic(
                clinic_Id=clinic_id,
                address=clinic_data.get('Address', 'N/A'),
                app_status=clinic_data.get('AppStatus', 'N/A'),
                description=clinic_data.get('Description', 'N/A'),
                email=clinic_data.get('Email', 'N/A'),
                end_break_hours=clinic_data.get('EndBreak', 'N/A'),
                end_hours=clinic_data.get('EndHours', 'N/A'),
                GRD_status=clinic_data.get('GRDStatus', 'N/A'),
                image=ctkImgClinicList,
                name=clinic_data.get('Name', 'N/A'),
                phone_no=clinic_data.get('PhoneNo', 'N/A'),
                specialty=clinic_data.get('Specialty', 'N/A'),
                start_break_hours=clinic_data.get('StartBreak', 'N/A'),
                start_hours=clinic_data.get('StartHours', 'N/A'),
                work_days=clinic_data.get('WorkDays', 'N/A')
            )

            # Create a frame for each clinic
            frameClinicList = ctk.CTkFrame(master=frameClinicInfo, bg_color="transparent", fg_color="transparent")
            frameClinicList.grid(row=row_index, column=0, sticky="new", padx=47, pady=10)
            frameClinicList.grid_columnconfigure(0, weight=1)

            # Add image label
            lblImageClinicList = ctk.CTkLabel(master=frameClinicList, text="", image=clinic_instance.get_image(),
                                              bg_color="transparent", width=220, height=150)
            lblImageClinicList.grid(row=0, column=0, sticky="w")

            # Prepare clinic information string
            clinic_info_text = (
                f"Name: {clinic_instance.get_name()}\n"
                f"Clinic user ID: {clinic_instance.get_clinic_Id()}\n"
                f"Specialty: {clinic_instance.get_specialty()}\n"
                f"Phone number: {clinic_instance.get_phone_no()}\n"
                f"Email address: {clinic_instance.get_email()}\n"
                f"Address: {clinic_instance.get_address()}\n"
            )

            # Add text label
            lblTextClinicList = ctk.CTkLabel(master=frameClinicList, text=clinic_info_text, height=150,
                                             corner_radius=20, fg_color="white", bg_color="transparent",
                                             text_color="#5D5D5D", font=("Inter", 20), justify="left", anchor="w")
            lblTextClinicList.grid(row=0, column=0, sticky="ew", padx=(220, 0))

            # Add behind label
            lblBehindClinicList = ctk.CTkLabel(master=frameClinicList, text="", fg_color="white", width=20, height=150)
            lblBehindClinicList.grid(row=0, column=0, sticky="w", padx=213)

            # Link btnClinic_Click function to clinic button
            frameClinicList.bind("<Button-1>", lambda e, clinic=clinic_instance: btnClinic_Click(filter_type, clinic))
            lblImageClinicList.bind("<Button-1>",
                                    lambda e, clinic=clinic_instance: btnClinic_Click(filter_type, clinic))
            lblTextClinicList.bind("<Button-1>", lambda e, clinic=clinic_instance: btnClinic_Click(filter_type, clinic))
            lblBehindClinicList.bind("<Button-1>",
                                     lambda e, clinic=clinic_instance: btnClinic_Click(filter_type, clinic))

            row_index += 1
            frameClinicList.grid()
            frameClinicTimeTable.grid_remove()
            DeclineClinic.grid_remove()


def btn_navigate_clinic_list(filter_type):
    toolbar_label_frame.grid()
    frameClinic.grid_remove()
    frameClinicTimeTable.grid_remove()
    frameHome.pack(fill="both", expand=True)  # Use pack instead of grid

    # Call your function to repopulate the clinic information frame
    on_filter_change(filter_type)


def btnClinic_Click(filter_type, clinic):
    toolbar_label_frame.grid()
    frameClinic.grid()
    frameClinicTimeTable.grid()

    toolbar_label_frame.grid_remove()
    for widget in frameClinicInfo.winfo_children():
        widget.destroy()

    print("Display clinic list")

    row_index = 0

    try:
        clinic_name = (
            f"{clinic.get_name()}\n"
        )
        clinic_info = (
            f"ID: {clinic.get_clinic_Id()}\n"
            f"Phone number: {clinic.get_phone_no()}\n"
            f"Email address: {clinic.get_email()}\n"
            f"Specialty: {clinic.get_specialty()}\n"
            f"Address: {clinic.get_address()}\n"
            f"Description: {clinic.get_description()}\n"
            f"GRD status: {clinic.get_GRDStatus()}\n"

        )

        app_status = clinic.get_app_status()
        display_app_status = f"App status: {app_status}"

        # Determine the text color based on the value of app_status
        if app_status == "Pending":
            status_color = "#5271FF"  # Blue color
        elif app_status == "Decline":
            status_color = "black"  # Black color
        elif app_status == "Approved":
            status_color = "red"  # Red color
        else:
            status_color = None

        imgBtnBack = Image.open("C:/Users/michi/PycharmProjects/DCS2103_Aug2023/SE Project/Images/back-button.png")

        # Create the button inside the frame
        BtnBack = CTkButton(
            master=frameClinic,
            text="",  # Set text to an empty string
            image=CTkImage(imgBtnBack, size=(30, 30)),  # Assuming imgBtnBack is the image for the button
            command=lambda: btn_navigate_clinic_list(filter_type),  # Change the command to navigate back
            fg_color="transparent", font=("Inter", 20), width=50, height=50, corner_radius=0
        )
        BtnBack.grid(row=0, column=0, padx=(10, 0), pady=10, sticky="w")

        row_index += 1

        # Display the clinic image if available

        lbl_clinic_name = CTkLabel(
            master=frameClinic, text=clinic_name, width=550, height=0, corner_radius=0,
            fg_color="transparent", text_color="#5D5D5D", font=("Inter", 30, "bold"), justify="left", anchor="w"
        )
        lbl_clinic_name.grid(row=row_index, column=0, sticky="ew", padx=10, pady=0)

        row_index += 1

        clinic_image = clinic.get_image()
        if clinic_image is not None:
            lbl_clinic_image = CTkLabel(
                master=frameClinic, text="", image=clinic_image,
                bg_color="transparent", width=220, height=150
            )
            lbl_clinic_image.grid(row=row_index, column=0, columnspan=6, sticky="ew", padx=10, pady=0)
            row_index += 1

        lbl_clinics = CTkLabel(
            master=frameClinic, text=clinic_info, corner_radius=0, width=550, height=0,
            fg_color="transparent", text_color="#5D5D5D", font=("Inter", 20), justify="left", anchor="w"
        )
        lbl_clinics.grid(row=row_index, column=0, sticky="ew", padx=10, pady=0)

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
                master=frameClinicTimeTable, text=header, width=100, height=0, corner_radius=0,
                fg_color="#5271FF", text_color="white", font=("Inter", 15), justify="center"
            )
            header_label.grid(row=row_index, column=col_index, padx=5, pady=5, sticky="ew")

        row_index += 1

        # Display working hours information
        for i in range(len(work_days)):
            day_label = CTkLabel(
                master=frameClinicTimeTable, text=work_days[i], width=100, height=0, corner_radius=0,
                fg_color="transparent", text_color="#5D5D5D", font=("Inter", 15), justify="center"
            )
            day_label.grid(row=row_index, column=0, padx=5, pady=5, sticky="ew")

            start_hour_label = CTkLabel(
                master=frameClinicTimeTable, text=start_hours[i], width=100, height=0, corner_radius=0,
                fg_color="transparent", text_color="#5D5D5D", font=("Inter", 15), justify="center"
            )
            start_hour_label.grid(row=row_index, column=1, padx=5, pady=5, sticky="ew")

            end_hour_label = CTkLabel(
                master=frameClinicTimeTable, text=end_hours[i], width=100, height=0, corner_radius=0,
                fg_color="transparent", text_color="#5D5D5D", font=("Inter", 15), justify="center"
            )
            end_hour_label.grid(row=row_index, column=2, padx=5, pady=5, sticky="ew")

            start_break_label = CTkLabel(
                master=frameClinicTimeTable, text=start_breaks[i], width=100, height=0, corner_radius=0,
                fg_color="transparent", text_color="#5D5D5D", font=("Inter", 15), justify="center"
            )
            start_break_label.grid(row=row_index, column=3, padx=5, pady=5, sticky="ew")

            end_break_label = CTkLabel(
                master=frameClinicTimeTable, text=end_breaks[i], width=100, height=0, corner_radius=0,
                fg_color="transparent", text_color="#5D5D5D", font=("Inter", 15), justify="center"
            )
            end_break_label.grid(row=row_index, column=4, padx=5, pady=5, sticky="ew")

            row_index += 1

        lblAppStatus = CTkLabel(
            master=frameClinic,
            text=display_app_status,
            width=550,
            height=0,
            corner_radius=0,
            fg_color="transparent",
            text_color=status_color,
            font=("Inter", 20),
            justify="left",
            anchor="w"
        )
        lblAppStatus.grid(row=row_index, column=0, sticky="ew", padx=10, pady=0)

        row_index += 1

        btnReject = CTkButton(master=frameClinic, text="Decline", fg_color="red", font=("Inter", 20, "bold"),
                              corner_radius=20, command=lambda: decline_clinic(filter_type, clinic))
        btnReject.grid(row=row_index, column=1, pady=20, sticky="e")

        btnAccept = CTkButton(master=frameClinic, text="Accept", fg_color="#5271FF", font=("Inter", 20, "bold"),
                              corner_radius=20, command=lambda: approve_clinic(filter_type, clinic))
        btnAccept.grid(row=row_index, column=2, pady=20, padx=(0, 20), sticky="e")

        # Ensure the parent frame has proper configuration to center its content
        frameClinic.grid_columnconfigure(0, weight=1)
    except Exception as e:
        print(f"Error fetching clinic data: {e}")


def approve_clinic(filter_type, clinic):
    try:
        clinic_id = clinic.get_clinic_Id()
        db.collection('Clinics').document(clinic_id).update({'AppStatus': 'Approved'})
        print("Clinic Approved")
        ApproveMail(clinic)
        # Display a pop-up informing that the clinic has been approved
        messagebox.showinfo("Clinic Approved",
                            f"The clinic {clinic.get_name()} has been approved.\nApproved clinic email has been sent")
        btn_navigate_clinic_list(filter_type)
    except Exception as e:
        print(f"Error approving clinic: {e}")


def ApproveMail(clinic):
    print("Send approve email. ")
    for widget in frameClinicInfo.winfo_children():
        widget.destroy()

    sender = "CallADoctor2024@outlook.com"
    recipient = clinic.get_email()
    print(recipient)
    message = (f"Dear {clinic.get_name()},\n"
               f"Your request has been approved. ")
    print(message)

    email = EmailMessage()
    email["From"] = sender
    email["To"] = recipient
    email["Subject"] = "Approved clinic request for CallDoctor"
    email.set_content(message)

    smtp = smtplib.SMTP("smtp-mail.outlook.com", port=587)
    smtp.starttls()
    smtp.login(sender, "P7EMtmk8Vw3Y")
    smtp.sendmail(sender, recipient, email.as_string())
    smtp.quit()


def decline_clinic(filter_type, clinic):
    try:
        # Hide other frames
        frameClinic.grid_remove()
        frameClinicTimeTable.grid_remove()
        toolbar_label_frame.grid_remove()
        DeclineClinic.grid()

        for widget in DeclineClinic.winfo_children():
            widget.destroy()

        # Label for decline reason
        lblClinicView = CTkLabel(
            master=DeclineClinic,
            text=f"What is the reason for declining {clinic.get_name()}?",
            font=("Inter", 30),
            text_color="black"
        )
        lblClinicView.grid(row=0, column=0, sticky="w", pady=(0, 5), padx=(0, 0))

        # Variable to store the decline reason
        decline_reason = StringVar(value="Select decline reason")

        # Dropdown for decline reasons
        dropDecline = CTkOptionMenu(
            master=DeclineClinic,
            values=["Select decline reason", "Outstanding payment", "Clinic already exists in system.", "Blacklisted"],
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
            variable=decline_reason,  # Bind the variable
        )
        dropDecline.grid(row=1, column=0, sticky="nw", padx=47, pady=40)

        # Submit button
        btnSubmit = CTkButton(
            master=DeclineClinic,
            text="Submit",
            fg_color="#5271FF",  # Blue color
            font=("Inter", 20, "bold"),
            corner_radius=20,
            width=100,  # Set a smaller width
            command=lambda: btnSubmit_Click(clinic, decline_reason.get(), filter_type)  # Pass the selected value
        )
        btnSubmit.grid(row=2, column=0, pady=20)

        # Center the button by setting padx to auto
        btnSubmit.grid(row=2, column=0, pady=20, padx=(150, 150))

    except Exception as e:
        print(f"Error declining clinic: {e}")


# Example on_submit_click function to handle the button click event
def btnSubmit_Click(clinic, decline_reason, filter_type):
    # Check if the decline reason is not selected or is the default "Select decline reason"
    if decline_reason == "Select decline reason":
        messagebox.showerror("Invalid Selection", "Please select a valid reason for declining the clinic.")
        return  # Exit the function early

    # Implement the actions to be taken when the submit button is clicked
    print(f"Submit button clicked for clinic: {clinic.get_name()}")
    print(f"Reason for decline: {decline_reason}")

    try:
        clinic_id = clinic.get_clinic_Id()
        db.collection('Clinics').document(clinic_id).update({
            'AppStatus': 'Decline',
            'DeclineReason': decline_reason  # Add the decline reason
        })
        print("Clinic status and decline reason updated in the database.")

        print("Send decline email. ")
        for widget in frameClinicInfo.winfo_children():
            widget.destroy()

        sender = "CallADoctor2024@outlook.com"
        recipient = clinic.get_email()
        print(recipient)
        message = (f"Dear {clinic.get_name()},\n"
                   f"Your request has been decline.\nDue to {decline_reason}")
        print(message)

        email = EmailMessage()
        email["From"] = sender
        email["To"] = recipient
        email["Subject"] = "Decline clinic request for CallDoctor"
        email.set_content(message)

        smtp = smtplib.SMTP("smtp-mail.outlook.com", port=587)
        smtp.starttls()
        smtp.login(sender, "P7EMtmk8Vw3Y")
        smtp.sendmail(sender, recipient, email.as_string())
        smtp.quit()

        messagebox.showinfo("Clinic Declined",
                            f"The clinic {clinic.get_name()} has been declined.\nA decline email has been sent.")
        btn_navigate_clinic_list(filter_type)


    except Exception as e:
        print(f"Error updating clinic in database: {e}")


def on_filter_change(filter_type):
    if filter_type == "Pending":
        clinics_ref = db.collection('Clinics').where('AppStatus', '==', 'Pending')
    elif filter_type == "Accept":
        clinics_ref = db.collection('Clinics').where('AppStatus', '==', 'Approved')
    elif filter_type == "Decline":
        clinics_ref = db.collection('Clinics').where('AppStatus', '==', 'Decline')
    elif filter_type == "All":
        clinics_ref = db.collection('Clinics')  # No filter for all clinics
    else:
        clinics_ref = db.collection('Clinics')  # Default to all clinics if value is unexpected
    GetClinicInformation(filter_type, clinics_ref)


# Frames
frameSideNav = CTkFrame(master=app, fg_color="#5271FF", corner_radius=0, width=80)
frameSideNav.pack(side="left", fill="y")

frameHome = CTkFrame(master=app, fg_color="#B5CAFF", corner_radius=0)
frameHome.pack(fill="both", expand=True)
frameHome.grid_columnconfigure(0, weight=1)
frameHome.grid_rowconfigure(2, weight=1)

toolbar_label_frame = CTkFrame(master=frameHome, fg_color="transparent")
toolbar_label_frame.grid(row=1, column=0, sticky="ew")
toolbar_label_frame.grid_columnconfigure(0, weight=1)

frameClinicInfo = CTkScrollableFrame(master=frameHome, fg_color="#B5CAFF", corner_radius=0, orientation="vertical",
                                     scrollbar_button_color="white")
frameClinicInfo.grid(row=2, column=0, sticky="nsew")
frameClinicInfo.grid_columnconfigure(0, weight=1)

frameClinic = CTkScrollableFrame(master=frameHome, width=800, fg_color="transparent")  # Adjust color as needed
frameClinic.grid(row=2, column=0, sticky="nsew")
frameClinic.grid_remove()  # Fill the remaining space in the frame

frameClinicTimeTable = CTkFrame(master=frameClinic, width=800, fg_color="transparent")  # Adjust color as needed
frameClinicTimeTable.grid(row=5, column=0, sticky="nsew")
frameClinicTimeTable.grid_remove()

DeclineClinic = CTkScrollableFrame(master=frameHome, fg_color="#C8FFD4", height=900)  # Adjust color as needed
DeclineClinic.grid(row=2, column=0, sticky="sew", pady=0)  # Fill the remaining space in the frame
DeclineClinic.grid_remove()

frameMail = CTkFrame(master=frameClinic, width=800, fg_color="green")
frameMail.grid(row=5, column=0, sticky="nsew")
frameMail.grid_remove()

# Side Navigation Bar
imgBtnMenu = Image.open("C:/Users/michi/PycharmProjects/DCS2103_Aug2023/SE Project/Images/menu.png")
btnMenu = CTkButton(master=frameSideNav, text="", image=CTkImage(imgBtnMenu, size=(30, 30)), fg_color="#5271FF",
                    command=btnMenu_Click)
btnMenu.place(relx=0.5, rely=0.06, anchor="center")

imgBtnHome = Image.open("C:/Users/michi/PycharmProjects/DCS2103_Aug2023/SE Project/Images/home-icon-white.png")
btnHome = CTkButton(master=frameSideNav, text="", image=CTkImage(imgBtnHome, size=(50, 50)), fg_color="transparent",
                    command=btnHome_Click)
btnHome.place(relx=0.5, rely=0.3, anchor="center")

imgBtnBookHis = Image.open("C:/Users/michi/PycharmProjects/DCS2103_Aug2023/SE Project/Images/booking-history-white.png")
BtnBookHis = CTkButton(master=frameSideNav, text="", image=CTkImage(imgBtnBookHis, size=(60, 60)),
                       fg_color="transparent", command=btnBookHis_Click)
BtnBookHis.place(relx=0.5, rely=0.5, anchor="center")

# Logo
imgHomeLogo = Image.open("C:/Users/michi/PycharmProjects/DCS2103_Aug2023/SE Project/Images/logo.png")
lblHomeLogo = CTkLabel(master=frameHome, text="", bg_color="white", image=CTkImage(imgHomeLogo, size=(453, 198)))
lblHomeLogo.grid(row=0, column=0, sticky="ewn")

# Login Button
imgBtnLogin = Image.open("C:/Users/michi/PycharmProjects/DCS2103_Aug2023/SE Project/Images/profile-user-blue.png")
BtnLogin = CTkButton(master=frameHome, text="", image=CTkImage(imgBtnLogin, size=(50, 50)), fg_color="white",
                     corner_radius=0, anchor="e", width=50, command=btnLogin_Click)
BtnLogin.grid(row=0, column=0, sticky="ne")

# Search Bar
lblClinicView = CTkLabel(master=toolbar_label_frame, text="Admin View", font=("Inter", 30), text_color="black")
lblClinicView.grid(row=0, column=0, sticky="w", pady=(0, 5), padx=(0, 0))

dropSearch = CTkOptionMenu(master=toolbar_label_frame, values=["Pending", "Accept", "Decline", "All"], fg_color="white",
                           dropdown_fg_color="white", button_color="white", button_hover_color="white", width=206,
                           height=59, anchor="center", corner_radius=20, font=("Inter", 20), text_color="#898989",
                           command=on_filter_change)
dropSearch.set("Pending")  # Set default value to "Pending"
dropSearch.grid(row=1, column=0, sticky="nw", padx=47, pady=40)

tbSearch = CTkEntry(master=toolbar_label_frame, fg_color="white", width=700, height=59, corner_radius=20,
                    font=("Inter", 15),
                    text_color="black", border_width=0)
tbSearch.grid(row=1, column=0, sticky="new", padx=(238, 47), pady=40)

lblBehindSearch = CTkLabel(master=toolbar_label_frame, text="|", font=("Inter", 28), text_color="#5271FF",
                           bg_color="white",
                           width=18, height=59)
lblBehindSearch.grid(row=1, column=0, sticky="nw", padx=237, pady=40)

imgBtnSearch = Image.open("C:/Users/michi/PycharmProjects/DCS2103_Aug2023/SE Project/Images/search.png")
BtnSearch = CTkButton(master=toolbar_label_frame, text="", image=CTkImage(imgBtnSearch, size=(25, 25)),
                      fg_color="white",
                      corner_radius=0, anchor="center", width=25, command=btnSearch_Click)
BtnSearch.grid(row=1, column=0, sticky="ne", padx=60, pady=55)


def add_rounded_corners(image, corner_radius):
    mask = Image.new('L', image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([0, 0, *image.size], radius=corner_radius, fill=255)
    image = image.convert("RGBA")
    image.putalpha(mask)
    return image


# Initial call to populate the frame with "Pending" clinics
on_filter_change("Pending")

app.mainloop()
