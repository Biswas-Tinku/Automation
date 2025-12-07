import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox
from tkinter import *
import pandas as pd
from datetime import datetime
import os
#import openpyxl

class AuditGUI:
    def __init__(self,parent):
        self.parent = parent
        self.parent.title("AWHG Payment RLA")
        self.parent.geometry('700x250')
        self.parent.configure(bg="light blue")
        self.parent.resizable(False,False)

        self.label_message = tk.Label(self.parent,text = "Load the report for Audit",bg="light blue")
        self.label_message.grid(column=0, row=0)
        
        self.frame1=tk.Frame(self.parent,borderwidth=5,width=700, height=50, background="light blue")
        self.frame1.grid(column=0, row=1)
        self.entry_file1 = tk.Entry(self.frame1,width=80)
        self.entry_file1.grid(column=0, row=1)
        self.frame4=tk.Frame(self.parent,borderwidth=5,width=60, height=50,background="light blue")
        self.frame4.grid(column=2, row=1)
        self.button_browse1 = tk.Button(self.frame4, text="Report 37.12",command=self.browse1, relief="raise", padx=5,pady=5,width=20,bg="light green")
        self.button_browse1.grid(column=2, row=1)

        self.frame2=tk.Frame(self.parent,borderwidth=3,width=700, height=50, bg="light blue")
        self.frame2.grid(column=0, row=3)
        self.entry_file2 = tk.Entry(self.frame2,width=80)
        self.entry_file2.grid(column=0, row=3)
        self.frame5=tk.Frame(self.parent,borderwidth=5,width=60, height=50,background="light blue")
        self.frame5.grid(column=2, row=3)
        self.button_browse2 = tk.Button(self.frame5, text="Report 31.08",command=self.browse2, relief="raise", padx=5,pady=5,width=20,bg="light green")
        self.button_browse2.grid(column=2, row=3)

        self.frame3=tk.Frame(self.parent,borderwidth=3,width=700, height=50, bg="light blue")
        self.frame3.grid(column=0, row=5)
        self.entry_file3 = tk.Entry(self.frame3,width=80)
        self.entry_file3.grid(column=0, row=5)
        self.frame6=tk.Frame(self.parent,borderwidth=5,width=60, height=50,background="light blue")
        self.frame6.grid(column=2, row=5)
        self.button_browse3 = tk.Button(self.frame6, text="Report 11.04",command=self.browse3, relief="raise", padx=5,pady=5,width=20,bg="light green")
        self.button_browse3.grid(column=2, row=5)

        self.frame7=tk.Frame(self.parent,borderwidth=5,width=380, height=50,background="light blue")
        self.frame7.grid(column=0, row=7)
        self.button_run = tk.Button(self.frame7, text="Run Audit",command=self.file, relief='raise', padx=5, pady=5, width=30, bg="light green")
        self.button_run.grid(column=0, row=7)

        self.frame8=tk.Frame(self.parent,borderwidth=5,width=380, height=50,background="light blue")
        self.frame8.grid(column=2, row=7)
        self.button_close = tk.Button(self.frame8, text="Close",command=self.terminate_app, relief='raise', padx=5, pady=5, width=20, bg="orange")
        self.button_close.grid(column=2, row=7)

    def browse1(self):
        path = fd.askopenfilename(title='37.12 Report')
        if path:
            self.entry_file1.delete(0, tk.END)
            self.entry_file1.insert(0, path)

    def browse2(self):
        path = fd.askopenfilename(title='31.08 Report')
        if path:
            self.entry_file2.delete(0, tk.END)
            self.entry_file2.insert(0, path)

    def browse3(self):
        path = fd.askopenfilename(title='11.04 Report')
        if path:
            self.entry_file3.delete(0, tk.END)
            self.entry_file3.insert(0, path)

    def file(self):
        file_Name1 = self.entry_file1.get()
        file_Name2 = self.entry_file2.get()
        file_Name3 = self.entry_file3.get()
        if file_Name1 == "":
            messagebox.showinfo("Information","Enter the file path for Report 37.12")
        elif file_Name2 == "":
            messagebox.showinfo("Information","Enter the file path for Report 31.08")
        elif file_Name3 == "":
            messagebox.showinfo("Information","Enter the file path for Report 11.04")
        else:
            self.run_cat(file_Name1, file_Name2, file_Name3)

    def terminate_app(self):
        self.parent.destroy()

    def run_cat(self,file_Name1, file_Name2, file_Name3):

        try:
            df = pd.read_excel(file_Name1, sheet_name = "page")
            PAR = pd.read_excel(file_Name2, sheet_name = "page", usecols=['Claim No'])
            Deposit= pd.read_excel(file_Name3, sheet_name="page", usecols =['Payment ID','Deposit Date'])
            PAR.drop_duplicates(inplace=True)
            PAR.rename(columns={'Claim No':'Pat_AR'}, inplace=True)
            Deposit.drop_duplicates(inplace=True)
            Acc_bal=df.groupby(by=['Claim No'])['Claim Balance'].sum()
            raw = df.merge(Acc_bal, how='left', on='Claim No')
            raw.rename(columns={'Claim Balance_y':'Acc_Balance'}, inplace=True)
            raw_Par = raw.merge(PAR, how="left", left_on="Claim No", right_on="Pat_AR")
            raw_Par_deposit = raw_Par.merge(Deposit,how="left", on = 'Payment ID')
            RAW = raw_Par_deposit
            def c (row):
                if (row['CPT Code'] == "99396") and (row["Claim Status"] == "PAT") and (row["Acc_Balance"] > 500) :
                    val = 'Rule 1-CPT 99396 Billed to patient'
                elif row['Reason Code'] in ['1','2','3'] and row["Claim Status"] == "44PA" \
                    and (row["Group Code"]=="PR" or row["Group Code"]=="HE"):
                    val = 'Rule 2-Incorrect Status code taken'
                elif (row['CPT Code'] in ['81002','81003']) and (row["Group Code"] in ["PI","OA","CO"]) \
                    and (row['CPT Balance'] in [30.00,15.00,3.45]) and (row['Denial Amount'] > 0.00):
                    val = 'Rule 3-Missed to adjust 81002/81003'
                elif row['CPT Code'] == "36416" and row["Contractual Adjustment"] == 15.00:
                    val = 'Rule 4-Incorrect adjustment done for CPT 36416'
                elif (row["Group Code"] in ["PI","OA","CO"]) and (row['Reason Code'] == "45") \
                    and (row['Payment'] > 0.00) and (row["Contractual Adjustment"] == 0.00):
                    val = "Rule 5-Missed to capture CO45 adjustment"
                elif row['Claim Charges'] == 0.00:
                    val = "Rule 6-Zero Charge claim"
                elif (row["Contractual Adjustment"] > 0.00) and (row['Reason Code'] == "186"):
                    val = "Rule 7-Incorrect adjustment on CO186"
                elif pd.notna(row['Pat_AR']) and (row["Claim Status"] == "PAT") and \
                    (row["Group Code"] in ["PI","OA","CO"]) and (row['Reason Code'] not in ['1','2','3','45','253']):
                    val="Rule 8-Balance incorrectly moved to Pat Bucket"
                elif pd.isna(row['Pat_AR']) and (row["Claim Status"] == "PAT") and \
                    (row["Secondary Payer Name"]!='Unknown') and (row["Acc_Balance"] > 0):
                    val="Rule 9-Incorrect status code taken"
                else:
                    val = ""
                return val
            RAW["Category"] = RAW.apply(c, axis=1)
            now = datetime.now()
            now_str = now.strftime('%Y-%m-%d-%H-%M')
            base_location = os.getcwd()
            output_path = base_location + "\\" + "Output_" + now_str + ".csv"
            RAW.to_csv(output_path, index=False)
            messagebox.showinfo("Success", f"Report saved successfully : {output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred: {str(e)}")

def main():
    root = tk.Tk()
    Audit = AuditGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
