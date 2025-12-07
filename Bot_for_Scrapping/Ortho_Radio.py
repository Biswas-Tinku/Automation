import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText  # ScrolledText for scrollable text area
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
import math
from datetime import datetime, timedelta
import time

class LoginGUI:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Radiology Order Download")
        self.parent.geometry('800x400')

        self.login_frame = tk.Frame(parent, width=400, height=400)
        self.login_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.output_frame = tk.Frame(parent, width=400, height=400, bg='lightgray')
        self.output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.label_message = tk.Label(self.login_frame, text="Use the Modmed Credentials to login:", width=50, pady=5, relief="raised")
        self.label_message.pack()
        self.label_message = tk.Label(self.login_frame, text="The number of days should be numeric value only.", width=50, pady=5, relief="raised")
        self.label_message.pack()

        self.label_username = tk.Label(self.login_frame, text="Username:", width=50, pady=5)
        self.label_username.pack()
        self.entry_username = tk.Entry(self.login_frame)
        self.entry_username.pack()

        self.label_password = tk.Label(self.login_frame, text="Password:", width=50, pady=5)
        self.label_password.pack()
        self.entry_password = tk.Entry(self.login_frame, show="*")
        self.entry_password.pack()

        self.label_day_count = tk.Label(self.login_frame, text="No of days to Download:", width=50, pady=5)
        self.label_day_count.pack()
        self.entry_day_count = tk.Entry(self.login_frame)
        self.entry_day_count.pack()


        self.button_login = tk.Button(self.login_frame, text="Download", command=self.login, relief='raise', padx=5, pady=5)
        self.button_login.pack()

        self.text_output = ScrolledText(self.output_frame, wrap=tk.WORD, width=80, height=20)
        self.text_output.pack(pady=10)

        self.button_close = tk.Button(self.output_frame, text="Close", command=self.terminate_app, relief='raise', padx=5, pady=5)
        self.button_close.pack()

    def print_to_textbox(self, message):
            self.text_output.insert(tk.END, message + "\n")
            self.text_output.see(tk.END)  # Scroll to the end of the text widget
            self.parent.update_idletasks()  # Update the GUI to show the latest message

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        count_day = self.entry_day_count.get()
        if username == "" or password == "":
            messagebox.showinfo("Login", "Please enter both username and password to run the program")
        else:
            pass
        if count_day == "":
            messagebox.showinfo("Count of days", "Please enter valid count of days in numbers")
        else:
            self.login_frame.pack_forget()  # Hide login frame
            self.run_scraping(username, password, count_day)

    def terminate_app(self):
        self.parent.destroy()

    def run_scraping(self, username, password,count_day):
        url = 'https://orthony.ema.md/ema/app/OrderLog.action#/'
        options = Options()
        options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)
        driver = webdriver.Chrome(options=options)
        driver.get(url)

        try:
            time.sleep(3)
            button = driver.find_element(By.CLASS_NAME, "btn-primary")
            button.click()
            self.print_to_textbox("Provider button selected")
            #----------------------------------------------------------#
            time.sleep(3)
            user_elem = driver.find_element(By.CLASS_NAME, "login-input-username")
            user_elem.send_keys(username)
            password_elem = driver.find_element(By.CLASS_NAME, "login-input-password")
            password_elem.send_keys(password)
            login_btn = driver.find_element(By.CLASS_NAME, "btn-primary")
            login_btn.click()
            #----------------------------------------------------------#
            time.sleep(30)
            order = driver.find_element(By.ID, "orderLogMenuNavTab")
            order.click()
            self.print_to_textbox('Web page login successful')
            self.print_to_textbox("Order option in EPM selected")
            #----------------------------------------------------------#
            time.sleep(30)
            driver.find_element(By.CLASS_NAME, "btn-primary").click()
            self.print_to_textbox("Filter button is selected")
            #----------------------------------------------------------#
            time.sleep(3)
            driver.find_element(By.CSS_SELECTOR, "button[data-identifier='clearFilterButton']").click()
            self.print_to_textbox("Resetting all filters successful")
            #----------------------------------------------------------#
            time.sleep(30)
            driver.find_element(By.CLASS_NAME, "btn-primary").click()
            time.sleep(2)
            driver.find_element(By.XPATH, '//*[contains(text(),"Open")]').click()
            time.sleep(1)
            S = driver.find_elements(By.ID, 'selectAllCheckbox')
            S[0].click()
            time.sleep(1)
            driver.find_element(By.XPATH, '//*[contains(text(),"In Progress")]').click()
            time.sleep(1)
            #driver.find_element(By.XPATH, '//*[contains(text(),"Closed")]').click()
            #time.sleep(1)
            driver.find_element(By.XPATH, f'//span[@class="ng-binding" and contains(text(),"Radiology")]').click()
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "input[type='radio'][value='None']").click()
            self.print_to_textbox("Selecting all options successful")
            #----------------------------------------------------------#
            today = pd.to_datetime("today").to_pydatetime()

            to_date = today-timedelta(days=int(count_day))
            to_day = int(to_date.strftime('%d'))
            to_month = int(to_date.strftime('%m'))

            from_date= today
            from_day = int(today.strftime('%d'))
            from_month = int(today.strftime("%m"))
            #----------------------------------------------------------#
            date_picker=driver.find_elements(By.CLASS_NAME,"input-group-addon")
            date_picker[0].click()

            if (to_month == from_month):
                pass
            else:
                driver.find_element(By.XPATH,"//button[@class='btn btn-default btn-sm pull-left uib-left']").click()
            driver.find_element(By.XPATH, f'//span[@class="ng-binding" and contains(text(),"{to_day}")]').click() # changed
            self.print_to_textbox('From date selected')

            date_picker[1].click()
            driver.find_element(By.XPATH, f'//span[@class="ng-binding" and contains(text(),"{from_day}")]').click() # changed
            self.print_to_textbox('To date selected')
            #----------------------------------------------------------#
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "button[data-identifier='applyFilterButton']").click()
            self.print_to_textbox("All filters reapply successful")
            time.sleep(30)

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            totalCount = soup.find("div", class_="padding-bottom-15 baseMargin").text
            record_count = int(re.search(r'\d+', totalCount).group())
            if record_count > 10:
                larg_view = driver.find_element(By.XPATH, '//*[@id="orderLogApp"]/ui-view/order-log/div/div[3]/div/div[1]/div/div/div/button[4]')
                larg_view.click()
                time.sleep(20)
                self.print_to_textbox("Report view expanded")
            else:
                self.print_to_textbox("Total record count is 10 or less")

            counter = math.ceil(int(re.search(r'\d+', totalCount).group()) / 100)
            self.print_to_textbox(f"\n{totalCount}")
            self.print_to_textbox(f'Total number of pages to download: {counter}')

            DF = []
            for i in range(0, counter):
                time.sleep(10)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                page = []
                page.append(soup.find("div", class_='ng-scope').text.strip())
                self.print_to_textbox(f'Capturing page: {i+1}')

                matches = re.search(r'\bStatus\b', page[0])
                Textcount = matches.end()
                textexc = Textcount + 29
                page[0] = page[0][textexc:]
                page.insert(0, "\n\n")
                list = [''.join(page)]
                list1 = [line.split('\n') for line in list[0].split("(Edited)") if line]
                df = pd.DataFrame(list1)
                DF.append(df)

                if record_count > 100:
                    driver.find_element(By.CLASS_NAME, "pager-next").click()
                else:
                    pass

            #driver.close()

            Raw = pd.concat(DF)
            cols = [8, 13, 17, 20, 27, 29, 36, 53, 54, 55, 56, 57, 59]
            Final = Raw[cols]

            name = {8: 'Order_Date', 13: 'Patient_Name', 17: 'Date_of_Birth', 20: 'MRN',
                    27: 'Payer', 29: 'Order_Number', 36: 'Order_Name', 53: 'Provider',
                    54: 'Facility', 55: 'Perform_At', 56: 'Due_Date', 57: 'Scheduled_Date',
                    59: 'Status'}
            Final = Final.copy()
            Final.rename(columns=name, inplace=True)
            Final = Final[(Final['Date_of_Birth'] != 'Previous') & (Final['Patient_Name'] != '100')]
            Final = Final[(Final['Scheduled_Date'] == '')]
            Final['Order_Date'] = pd.to_datetime(Final['Order_Date'])
            Final['Status'].astype(str)

            now = datetime.now()
            now_str = now.strftime('%Y-%m-%d--%H-%M')
            #base_location = r"C:\Users\tinku.biswas\Downloads\Modmedscrapauto\Radio"
            base_location = os.getcwd()
            output_path = base_location + "\\" + now_str + ".csv"
            Final.to_csv(output_path, index=False)
            self.print_to_textbox(f"The output file is saved in : {output_path}")

        except Exception as e:
            self.print_to_textbox(f"Error occurred: {str(e)}")

        finally:
            driver.quit()
            # self.parent.destroy()

def main():
    root = tk.Tk()
    login_gui = LoginGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
