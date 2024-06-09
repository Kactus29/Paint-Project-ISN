import tkinter as tk

class ZoomableCanvas(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.scale_factor = 1.0
        self.bind("<MouseWheel>", self.zoom)
        self.config(scrollregion=self.bbox("all"))  # Set scroll region to fit all items

        # Create scrollbars
        self.v_scrollbar = tk.Scrollbar(master, orient="vertical", command=self.yview)
        self.h_scrollbar = tk.Scrollbar(master, orient="horizontal", command=self.xview)

        # Associate scrollbars with canvas
        self.config(yscrollcommand=self.v_scrollbar.set)
        self.config(xscrollcommand=self.h_scrollbar.set)

        # Pack the scrollbars
        self.v_scrollbar.pack(side="right", fill="y")
        self.h_scrollbar.pack(side="bottom", fill="x")



    def zoom(self, event):
        # Get the coordinates of the mouse pointer
        x_center = self.canvasx(event.x)
        y_center = self.canvasy(event.y)

        # Zoom in or out depending on the direction of the mouse wheel
        if event.delta > 0:
            zoom_scale = 1.1  # Increase scale by 50%
            self.scale_factor *= zoom_scale
        else:
            # if self.scale_factor * 0.5 <= 1.0:
            #     zoom_scale = 1.0 / self.scale_factor
            #     self.scale_factor = 1.0
            # else:
            zoom_scale = 0.9  # Decrease scale by 50%
            self.scale_factor *= zoom_scale

        # Rescale all items on the canvas
        self.scale("all", x_center, y_center, zoom_scale, zoom_scale)

        # Adjust scroll region after zooming
        self.config(scrollregion=self.bbox("all"))

    def start_scroll(self, event):
        self.scan_mark(event.x, event.y)

    def scroll(self, event):
        self.scan_dragto(event.x, event.y, gain=1)
        # self.limit_scroll()

    def limit_scroll(self):
        bbox = self.bbox("all")
        if bbox:
            x0, y0, x1, y1 = bbox
            self.update_idletasks()  # Ensure the canvas is updated before limiting
            current_x = self.canvasx(0)
            current_y = self.canvasy(0)
            max_x = x1 - self.winfo_width()
            max_y = y1 - self.winfo_height()

            if current_x < x0:
                self.xview_moveto(x0 / self.bbox("all")[2])
            elif current_x > max_x:
                self.xview_moveto(max_x / self.bbox("all")[2])

            if current_y < y0:
                self.yview_moveto(y0 / self.bbox("all")[3])
            elif current_y > max_y:
                self.yview_moveto(max_y / self.bbox("all")[3])