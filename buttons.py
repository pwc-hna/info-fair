from Tkinter import *


# Here, we are creating our class, Window, and inheriting from the Frame
# class. Frame is a class from the tkinter module. (see Lib/tkinter/__init__)
class Window(Frame):

    # Define settings upon initialization. Here you can specify
    def __init__(self, master=None):
        
        # parameters that you want to send through the Frame class. 
        Frame.__init__(self, master)   

        #reference to the master widget, which is the tk window                 
        self.master = master

        #with that, we want to then run init_window, which doesn't yet exist
        self.init_window()

    #Creation of init_window
    def init_window(self):

        # changing the title of our master widget      
        self.master.title("GUI")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        # creating the start button instance
        self.startRecording = Button(self, text="Record",command=self.start_recording)
        # placing the button on my window
        self.startRecording.place(x=0, y=0)

        # creating the stop button instance
        self.stopRecording = Button(self, text="Stop",command=self.stop_recording)
        # placing the button on my window
        #stopRecording.place(x=0, y=0)


    def client_exit(self):
        exit()

    def start_recording(self):
        print "Started recording ..."
        self.startRecording['state'] = 'disabled'
        self.startRecording['text'] = 'Recording'
        self.stopRecording.place(x=100, y=0)
    
    def stop_recording(self):
        print "Stopped recording ..."
        self.client_exit()

# root window created. Here, that would be the only window, but
# you can later have windows within windows.
root = Tk()

root.geometry("150x50")

#creation of an instance
app = Window(root)

#mainloop 
root.mainloop()  