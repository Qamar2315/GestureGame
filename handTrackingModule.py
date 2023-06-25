import mediapipe as mp
import cv2 
import time

# self.mode=mode
# self.maxHands=maxHands
# #self.modelComplex = modelComplexity
# self.detectionCon=detectionCon
# self.trackCon=trackCon

class handDetector():
    def __init__(self):
        # self.mode=mode
        # self.maxHands=maxHands
        # #self.modelComplex = modelComplexity
        # self.detectionCon=detectionCon
        # self.trackCon=trackCon
        self.mpHands=mp.solutions.hands
        self.hands= self.mpHands.Hands()
        self.mpDraw=mp.solutions.drawing_utils
    def findHands(self,img,draw):
        imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results=self.hands.process(imgRGB)
        hands= self.results.multi_hand_landmarks
        if self.results.multi_hand_landmarks:
            for handles in self.results.multi_hand_landmarks:
                if(draw):
                    self.mpDraw.draw_landmarks(img,handles,self.mpHands.HAND_CONNECTIONS)
        return img,hands
    
    def findPosition(self,img,handNo=0,draw=True):
        lnList=[]
        if self.results.multi_hand_landmarks:
            myHand =self.results.multi_hand_landmarks[handNo]
            for id,ln in enumerate(myHand.landmark):
                h,w,c=img.shape
                cx,cy=int(ln.x * w),int(ln.y*h)
                #print(id,cx,cy)
                lnList.append((id,cx,cy))
                if draw:
                    cv2.circle(img,(cx,cy),5,(255,0,240),cv2.FILLED)
        return lnList    
        
            

def main():
    detector= handDetector()
    cap= cv2.VideoCapture(0)
    pTime=0
    cTime=0   
    while True:
        success,img=  cap.read()
        img=detector.findHands(img,True)
        lnList=detector.findPosition(img)
        if len(lnList) !=0:
            cv2.circle(img,(lnList[4][1],lnList[4][2]),30,(255,0,240),cv2.FILLED)
        cTime=time.time()
        fps=1/(cTime-pTime)
        pTime=cTime
        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,255),3)    
        cv2.imshow("image",img)
        cv2.waitKey(1)

if __name__== "__main__":
    main()
