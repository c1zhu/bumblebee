import time, sys
from naoqi import ALModule
from naoqi import ALBroker
from naoqi import ALProxy

HumanGreeters = None
memory = None
pip = "192.168.1.4"
pport = 9559

class FaceReaction(ALModule):
    def __init__(self, name):
        ALModule.__init__(self, name)
        self.tts = ALProxy("ALTextToSpeech")

        global memory
        memory = ALProxy("ALMemory")
        memory.subsribeToEvent("FaceDetected", "HumanGreeters", "reactToFaces")

    def findFaceInfo(self, name):
        try:
            faceProxy = ALProxy("ALFaceDetection", pip, pport)
        except Exception, e:
            print "Error with creating faceProxy"
            print str(e)
            exit(1)

        period = 500
        faceProxy.subsribe("Test_Face", period, 0.0)
        memValue = "FaceDetected"
        global faceLabel

        try:
            memoryProxy = ALProxy("ALMemory", pip, pport)
        except Exception, e:
            print "Error with creating memoryProxy"
            print str(e)
            exit(1)

        for i in range(0, 20):
            time.sleep(0.5)
            val = memoryProxy.getData(memValue)

            if(val and isinstance(val, list) and len(val) >= 2):
                faceInfoArray = val[1]

                try:
                    for j in range(len(faceInfoArray)-1):
                        faceInfo = faceInfoArray[j]

                        faceExtraInfo = faceInfo[1]
                        faceLabel = faceExtraInfo[2]
                        return faceLabel
                except Exception, e:
                    print "faces detected, but it seems getData is invalid. ALValue ="
                    print val
                    print "Error msg %s" % (str(e))

            else:
                print"No face detected"

            faceProxy.unsubscribe("Test_Face")
            print "Detection terminated successfully"

    def reactToFaces(self, *_args):
        memory.unsubscribeToEvent("FaceDetected", "HumanGreeters")

        if findFaceInfo() == 'Chenlei':
            self.tts.say("Hello, Chenlei! How is it going?")
        elif findFaceInfo() == 'Ljina':
            self.tts.say("Hi, Ljina! How are you?")
        else:
            self.tts.say("Sorry I can't recognize you")

        memory.subsribeToEvent("FaceDetected", "HumanGreeters", "reactToFaces")

    def main():
        myBroker = ALBroker("myBroker", "0, 0, 0, 0", 0, pip, pport)
        global HumanGreeters
        HumanGreeters = FaceReaction("HumanGreeters")

    if __name__ == '__main__':
        main()