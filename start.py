from tkinter import *
from handler.handler import *

def handleInput():
	if track_text.get() != '':
		response = downloadHandler(track_text.get())
		output_label.config(text=response)
		# output_label.config(text=getClienId())
	else:
		output_label.config(text='Erroor')

	

root = Tk()
root.title('Soundcloud downloader')
frame=Frame(root, width=610, height=190)
frame.pack()


track_text = StringVar()
track_label = Label(text="Soundcloud track url:")
track_label.place(x=60, y=20)
track_entry = Text(frame)
track_entry = Entry(root,textvariable=track_text)
track_entry.place(x=60, y=60, height=30, width=500)

output_label = Label(text="...")
output_label.place(x=60, y=150)

button1 = Button(frame, text="Get track",command=handleInput)
button1.place(x=60, y=110, height=30, width=100)


root.mainloop()

