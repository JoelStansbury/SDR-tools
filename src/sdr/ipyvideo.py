from ipywidgets import HBox, Image
from io import BytesIO
import PIL

class Video(HBox):
    def __init__(self, arr=None):
        """
        Initialize an ArrayImage widget for displaying numpy arrays as images.
        To load a new image use the ``show_frame`` function
        Parameters
        ----------
        (Optional) arr: numpy.array()
            Must be of type np.uint8 and suitable shape for a PIL Image
        
        Joel Stansbury
        7/17/2022
        """
        super().__init__()
        self.out = Image()
        self.children = [self.out]
        self.record = False
        self.imgs = []

        if arr is not None:
            self.show_frame(arr)
    
    def show_frame(self, arr):
        """
        Load a new image
        Parameters
        ----------
        arr: numpy.array()
            Must be of type np.uint8 and suitable shape for a PIL Image
        """
        h, w, *_ = arr.shape
        arr = arr.copy()
        arr -= arr.min()
        arr = (arr * 255 / arr.max())
        arr = arr.astype("uint8")

        self.layout = {"width":f"{w+20}px", "height":f"{h+20}px"}

        pil = PIL.Image.fromarray(arr)
        if self.record:
            self.imgs.append(pil)
        
        f = BytesIO()
        pil.save(f, "png")

        self.out.value=f.getvalue()
        self.out.width=w
        self.out.height=h
        self.out.format="png"
    
    def save(self, fname, duration=50, loop=0, flush=True, **kwargs):
        """
        Saves the stack of recorded frames as a gif

        Parameters
        ----------
        ```
            duration: int  # time in miliseconds to spend on each frame
            loop: int  # number of times to loop, 0 will loop forever (default=0)
            flush: bool  # clear stack for next recording 
            **kwargs: dict  # any other options for PIL.Image.save
        ```
        """
        assert self.imgs, "No images to save... Set `self.record=True` to start recording"
        self.imgs[0].save(fname, save_all=True, append_images=self.imgs[1:], duration=duration, loop=loop, **kwargs)
        if flush:
            self.imgs = []