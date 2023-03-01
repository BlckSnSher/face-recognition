from tkinter import *
from pathlib import Path


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets/frame2")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class AddStudentWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Add Student")
        self.master.configure(bg="#FFFFFF")

        # Create a frame for the content
        self.frame = Frame(self.master, bg="#FFFFFF")
        self.frame.pack(fill=BOTH, expand=True)

        # Create a canvas for the image
        self.canvas = Canvas(self.frame, bg="#FFFFFF")
        self.canvas.grid(row=0, column=0, columnspan=2, sticky=N+S+E+W)

        self.image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(
            0, 0, anchor=NW, image=self.image_image_1)

        # Create a label and entry for each input field
        fields = ["First Name", "Last Name", "Email", "Phone", "Address", "City", "State", "Zip"]

        for i, field in enumerate(fields):
            label = Label(self.frame, text=field, bg="#FFFFFF", font=("OpenSans Bold", 16))
            label.grid(row=i+1, column=0, padx=10, pady=10, sticky=W)

            entry = Entry(self.frame, bd=0, bg="#FFFFFF", fg="#000716", font=("OpenSans Bold", 16))
            entry.grid(row=i+1, column=1, padx=10, pady=10, sticky=W + E)

        # Create the submit button
        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        self.button_1 = Button(
            self.frame,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.submit,
            relief="flat",
            cursor="hand2"
        )
        self.button_1.grid(row=len(fields)+1, column=0, columnspan=2, pady=10)

        # Set grid weights to make the canvas resize with the window
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

        # Bind the canvas to resize with the window
        self.canvas.bind("<Configure>", self.resize_image)

    def resize_image(self, event):
        # Resize the canvas and image to fill the window
        self.canvas.config(width=event.width, height=event.height)
        self.canvas.itemconfig(self.image_1, image=self.image_image_1.subsample(int(event.width / 2)))

    def submit(self):
        # TODO: Implement submit functionality
        pass


if __name__ == "__main__":
    root = Tk()
    root.resizable(True, True)
    window = AddStudentWindow(root)
    root.mainloop()
