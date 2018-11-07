import numpy as np
import cv2
import enum
import threading
import FrameSaver

WHITE_TIMEOUT = 0.2
BLACK_TIMEOUT = 0.1
SHOW_TIMEOUT = 5

basepath =  "X:\\public_html\\deepdream\\gen\\"
baseURL = "http://dtpl.ehb.be/~davy.van.belle/deepdream/gen/"
 
class Borg:
    _shared_state = {}
    def __init__(self):
        self.__dict__ = self._shared_state      

class State(Borg):
    RUN = 1
    TAKEPIC = 2
    WHITE = 3
    BLACK = 4
    RESET = 5
    DREAM = 6
    SHOW = 7
    WAIT = 8
    EXIT = 9
    FULLSCREEN = 10
        
    def __init__(self):
        Borg.__init__(self)
        self.state = self.RUN
        self.prev_state = self.RESET
        print("Init State object")
        
    def __str__(self): return repr(self) + str(self.state )
    
    def get_state(self): return self.state
    
    def set_state(self,s): 
        self.prev_state = self.state
        self.state = s
        
    def get_previous_state(self): return self.prev_state


def init_camera(cam):
    cap = cv2.VideoCapture(cam)
    if not cap.isOpened:   #Check if succeeded to connect to the camera
       print ("Cam open failed")
       
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,10000)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,10000)
    return cap
    
    
def make_window(name):
    cv2.destroyWindow(name)
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(name, cv2.WND_PROP_AUTOSIZE, cv2.WINDOW_AUTOSIZE)
     

def make_fullscreen(name,f):
    #make_window(name)
    if (f):
        print("Switching to fullscreen")
        cv2.setWindowProperty(name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.setWindowProperty(name, cv2.WND_PROP_AUTOSIZE, cv2.WINDOW_AUTOSIZE)
        return True
    else:
        print("Switching to normal screen")
        cv2.setWindowProperty(name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(name, cv2.WND_PROP_AUTOSIZE, cv2.WINDOW_AUTOSIZE)
        return False

        
def text_overlay(text,color,frame):
    font = cv2.FONT_HERSHEY_TRIPLEX
    textScale = 1
    textThickness = 2

    textSize = cv2.getTextSize(text, font, textScale, textThickness)[0]
           
    textX = int((frame.shape[1] - textSize[0]) / 2)
    textY = int((frame.shape[0] - textSize[1]))
    
    cv2.putText(frame,text,(textX,textY), font, textScale,color,textThickness,cv2.LINE_AA)
    
    return frame

def get_new_frame(cap):
    ret, t_f = cap.read()
    return t_f
    
def read_user_input(state):
    key = cv2.waitKey(1)
    if key == ord('q'):
        state.set_state(State.EXIT)
        
    elif (key == ord('p') and (state.get_state() == State.RUN)):
        state.set_state(State.TAKEPIC)
        
    elif (key == ord('p') and (state.get_state() == State.WAIT)):
        state.set_state(State.RESET)
        
    elif key == ord('f'):
        state.set_state(State.FULLSCREEN)
    
    return state
    
    
def render_dream(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    
def callback_white():
    State().set_state(State.BLACK)
    
    
def callback_black():
    State().set_state(State.DREAM)
    
def callback_show():
    State().set_state(State.RESET)
    

def main():
   
    view_finder = "Viewfinder"
     
    active = True
    fullscreen = True
    
    cap_dev = init_camera(0)
    make_window(view_finder)
    make_fullscreen(view_finder,fullscreen)
    
    state = State()
    print(state)
    
    picture = 0
    
    height = int(cap_dev.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cap_dev.get(cv2.CAP_PROP_FRAME_WIDTH))

    while(active):
        
        state = read_user_input(state)
            
        s = state.get_state()   
        
        if (s == State.RUN):
            frame = get_new_frame(cap_dev)
            frame = text_overlay("Smile & push the button",(255,255,255),frame)
        
        elif (s == State.TAKEPIC):
            print("Take a picture")
            picture = get_new_frame(cap_dev)
            state.set_state(State.WHITE)
        
        elif (s == State.WHITE):
            print("Make it white")
            frame[:] = (255,255,255)
            threading.Timer(WHITE_TIMEOUT, callback_white).start()
            state.set_state(State.WAIT)
        
        elif (s == State.BLACK):
            print("Paint it black")
            frame[:] = (0,0,0)
            threading.Timer(BLACK_TIMEOUT, callback_black).start()
            state.set_state(State.WAIT)
        
        elif (s == State.RESET):
            print("Resetting")
            state.set_state(State.RUN)
        
        elif (s == State.SHOW):
            print("Show")
            frame = picture
            #threading.Timer(SHOW_TIMEOUT, callback_show).start()
            state.set_state(State.WAIT)
        
        elif (s == State.DREAM):
            print("Dream")
            picture = render_dream(picture)
            filename = FrameSaver.rand_filename('.png',6)
            path = basepath + filename
            URL = baseURL + filename
            FrameSaver.save_frame(picture,path)
            qr = FrameSaver.make_qrcode(URL)
            picture = text_overlay(filename,(255,255,255),picture)
            picture = FrameSaver.qr_overlay(picture,qr)
            state.set_state(State.SHOW)
                       
        elif (s == State.WAIT):
            #print("Wait for it ....")
            nop = 1
            
        elif (s ==State.FULLSCREEN):
            fullscreen = make_fullscreen(view_finder,not fullscreen)
            state.set_state(state.get_previous_state())    
        
        elif (s == State.EXIT):
            active = False
        
        #print(s)    
    
        if cv2.getWindowProperty(view_finder,1) == -1 :
            print("Window closed")
            make_window(view_finder)
            make_fullscreen(view_finder,fullscreen)
        
        #Finaly show the frame
        cv2.imshow(view_finder,frame)
          
  
    # When everything done, release the capture
    cap_dev.release()
    cv2.destroyAllWindows()
    
if __name__=="__main__":
   main()