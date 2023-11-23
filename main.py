import PyPDF2
import pyttsx3
from tkinter import filedialog
from tkinter import *
from os import remove

class Root(Tk):
    def __init__(self):
        self.engine = pyttsx3.init()
        super(Root, self).__init__()
        self.title("Pdf_to_text_to_speech")
        self.minsize(500, 500)
        self.maxsize(500, 500)
        self.text_box = Text(self)
        self.text_box.pack()

        left_frame = Frame(self)
        left_frame.pack(side=LEFT)

        self.rate_of_speech = Label(left_frame, text="rate of speech")
        self.rate_of_speech.pack(side=TOP)

        self.rate_slider = Scale(left_frame, from_=50, to=300, orient=HORIZONTAL)
        self.rate_slider.set(120)
        self.rate_slider.pack(side=TOP)

        right_frame = Frame(self)
        right_frame.pack(side=RIGHT)

        self.button = Button(right_frame, text="Run Text to speech", command=self.text_to_speech)
        self.button.pack(side=TOP)
        self.fem_voice = 0
        self.check = Checkbutton(right_frame, text='Female voice:', onvalue=1, offvalue=0, command=self.print_selection)
        self.check.pack(side=TOP)

        mid_frame = Frame(self)
        mid_frame.pack()

        self.new_button = Button(mid_frame, text="import text from pdf", command=self.import_pdf)
        self.new_button.pack(pady=40)

    def print_selection(self):
        if self.fem_voice == 0:
            self.fem_voice = 1
        else:
            self.fem_voice = 0

    def text_to_speech(self):

        """ RATE"""
        rate = self.engine.getProperty('rate')   # getting details of current speaking rate
        self.engine.setProperty('rate', self.rate_slider.get())     # setting up new voice rate

        """VOICE"""
        voices = self.engine.getProperty('voices')       # getting details of current voice

        self.engine.setProperty('voice', voices[self.fem_voice].id)   # changing index, changes voices. 1 for female

        self.engine.say(self.text_box.get(index1="1.0", index2=END))

        self.engine.runAndWait()

        self.engine.stop()

    def import_pdf(self):
        conv_pdf = filedialog.askopenfilename(initialdir="/", title="Select A File", filetypes=(("pdf files", "*.pdf"),
                                                                                                ("all files", "*.*")))

        if conv_pdf == "":
            pass

        else:
            pdf_reader = PyPDF2.PdfReader(conv_pdf)

            page = pdf_reader.pages[0]

            text = page.extract_text()

            with open('pdf_content.txt', 'w') as info:
                info.write(text)

            with open('pdf_content.txt') as info:
                self.text_box.insert(END, " ".join(line.strip() for line in info))

            try:
                remove('pdf_content.txt')
            except FileNotFoundError:
                pass




root = Root()

root.mainloop()

