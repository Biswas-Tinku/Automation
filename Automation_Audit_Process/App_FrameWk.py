import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox
from tkinter import *
class AuditGUI:
    def __init__(self,parent):
        self.parent = parent
        self.parent.title("AWHG Payment RLA")
        self.parent.geometry('700x250')
        self.parent.configure(bg="light blue")
        self.parent.resizable(False,False)

        self.label_message = tk.Label(self.parent,text = "Load the report for Audit",bg="light blue")
        self.label_message.grid(column=0, row=0)
        #self.label_message.pack
        
        self.frame1=tk.Frame(self.parent,borderwidth=5,width=700, height=50, background="light blue")
        self.frame1.grid(column=0, row=1)
        self.entry_file1 = tk.Entry(self.frame1,width=80)
        self.entry_file1.grid(column=0, row=1)
        
        self.frame4=tk.Frame(self.parent,borderwidth=5,width=60, height=50,background="light blue")
        self.frame4.grid(column=2, row=1)
        self.button_browse1 = tk.Button(self.frame4, text="Report 37.12", relief="raise", padx=5,pady=5,width=20,bg="light green")
        self.button_browse1.grid(column=2, row=1)

        self.frame2=tk.Frame(self.parent,borderwidth=3,width=700, height=50, bg="light blue")
        self.frame2.grid(column=0, row=3)
        self.entry_file2 = tk.Entry(self.frame2,width=80)
        self.entry_file2.grid(column=0, row=3)

        self.frame5=tk.Frame(self.parent,borderwidth=5,width=60, height=50,background="light blue")
        self.frame5.grid(column=2, row=3)
        self.button_browse2 = tk.Button(self.frame5, text="Report 31.08", relief="raise", padx=5,pady=5,width=20,bg="light green")
        self.button_browse2.grid(column=2, row=3)

        self.frame3=tk.Frame(self.parent,borderwidth=3,width=700, height=50, bg="light blue")
        self.frame3.grid(column=0, row=5)
        self.entry_file3 = tk.Entry(self.frame3,width=80)
        self.entry_file3.grid(column=0, row=5)
        
        self.frame6=tk.Frame(self.parent,borderwidth=5,width=60, height=50,background="light blue")
        self.frame6.grid(column=2, row=5)
        self.button_browse3 = tk.Button(self.frame6, text="Report 11.04", relief="raise", padx=5,pady=5,width=20,bg="light green")
        self.button_browse3.grid(column=2, row=5)
    
        self.frame7=tk.Frame(self.parent,borderwidth=5,width=380, height=50,background="light blue")
        self.frame7.grid(column=0, row=7)
        self.button_run = tk.Button(self.frame7, text="Run Audit", relief='raise', padx=5, pady=5, width=30, bg="light green")
        self.button_run.grid(column=0, row=7)
        
        self.frame8=tk.Frame(self.parent,borderwidth=5,width=380, height=50,background="light blue")
        self.frame8.grid(column=2, row=7)
        self.button_close = tk.Button(self.frame8, text="Close", relief='raise', padx=5, pady=5, width=20, bg="orange")
        self.button_close.grid(column=2, row=7)


def main():
    root = tk.Tk()
    Audit = AuditGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
