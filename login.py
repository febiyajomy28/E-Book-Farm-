import streamlit as st
import re
from utils import nav_page

if 'validasi' not in st.session_state:
    st.session_state.validasi = False
if 'username' not in st.session_state:
    st.session_state.username = False


def user_validation(user):
    to_pass = "^[a-z0-9A-Z]+[\.]?[a-zA-Z0-9]+[@]\w+[.]\w{2,3}$"
    result_1 = re.search(to_pass , user)
    if user and len(user) >= 4 and user.isalnum():
        st.session_state.validasi = True
        st.session_state.username = user

        return True
    else:   
        return False

def password_validation(password):
    to_pass = "^.(?=.[a-z])(?=.[A-Z])(?=.[0-9])(?=.[!@#$%^&_+-])(?=.{5,16}).*$"
    result_2 = re.findall(to_pass , password)
    if password and len(password) >= 6 and any(c.isupper() for c in password) and any(c.islower() for c in password) and any(c.isdigit() for c in password):
        return True
    else:
        return False
    
def user_checking(user, password):
    with open("user_information.txt", "r") as data:
        for line in data:
            user_data = line.split()
            if len(user_data) == 2 and user_data[0] == user and user_data[1] == password:
                return True
    return False  

def new_registration(user,password):
    with open("user_information.txt","a") as data:
        data.write(f'{user} {password}\n')


def forgot():
    global user
    with open("user_information.txt","r") as user_:
        for line in user_:
            INFO = line.split()
            if INFO[0]==user:
                password =  (line.split()[1:][0])
                return password
                break
if not st.session_state.validasi:
        
    st.title("Farm E-BOOK FARM")
    menu = ["Login","New Registration","Forgot Password","Logout"]
    choice = st.selectbox("MENU",menu)


    if choice=="Login":
        user = st.text_input("USER-ID")
        password = st.text_input("PASSWORD", type = "password")
        login = st.button("LOGIN")
        if (user):
            if user_validation(user)==True:
                if(password):
                    if password_validation(password)==True:
                        if user_checking(user,password)==True:
                            if (login):
                                st.success("Berhasil Masuk")
                                st.balloons()
                        else:
                            st.error(" ID USER Tidak Terdaftar,Silahkan Mencoba lagi")


                    else:
                        st.warning("password Salah")
                        st.error("Forgot Your Pasword")

            else:
                st.warning("user id yang anda masukkan salah")
    elif choice == "Logout":
     
        choice = "Login"
    elif choice == "New Registration":
        user = st.text_input("Masukkan USER-ID")
        st.info("*USER-ID gunakan unique name dan Angka")

        password = st.text_input("Masukkan Pasword Baru Anda", type="password")
        st.info("*PASSWORD harus maksimal 3 karakter, angka dua digit, satu huruf besar, dan huruf kecil")

        confirm_password = st.text_input("Konfirmasi Password", type="password")

        stay = st.button("Login")

        st.write(f"User input: {user}")
        if user:
            st.write("Validating user...")
            if user_validation(user):
                st.write("User is valid")
                if password:
                    st.write("Validating password...")
                    if password_validation(password):
                        st.write("Password is valid")
                        new_registration(user, password)
                        if confirm_password:
                            if confirm_password == password:
                                st.success("Registered Sukses")
                                if stay:
                                    st.success("Selamat Datang " + user + "..!")
                                    # Include relevant code for cookies
                                    st.subheader("SELAMAT DATANG, AKUN ANDA SEKARANG SUDAH TERSIMPAN")
                                    st.balloons()
                                else:
                                    st.subheader("LIFE IS TOO SHORT, HAVE COOKIES AND ENJOY")
                            else:
                                st.error("Konfirmasi Password Tidak Cocok")
                    else:
                        st.error("Please enter a valid PASSWORD")
                else:
                    st.error("Please enter a valid PASSWORD")
            


    elif choice=="Forgot Password":
        user = st.text_input("Masukkan USER-ID")
        GET = st.button("GET Password")
        if (user):
            if user_validation(user)==True:
                if (GET):
                    if forgot():
                        st.success("Makanya Jangan Lupa, Pasword Kamu Adalah"+ forgot())
            else:
                st.error("USER-ID Tidak ditemukan silahkan Membuat USE-ID baru")
else :
    st.write("Anda Sudah Login")
    if st.button("Logout"):
        st.session_state.validasi = False
        st.session_state.username = None
        st.write("Logout Berhasil")     
        st.rerun()
        
        