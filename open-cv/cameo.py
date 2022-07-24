import cv2
import numpy as np
import time

class CaptureManager(object):

    def __init__(self,capture,previewWindowManager=None,shouldMirrorPreview=False):

        self.previewWindowManager = previewWindowManager
        self.shouldMirrorPreview = shouldMirrorPreview
        self._capture = capture
        self._channel = 0
        self._enteredFrame = False
        self._frame = None
        self._imageFilename = None
        self._videoFilename = None
        self._videoEncoding = None
        self._videoWriter = None

        self._startTime = None
        self._framesElapsed = 0
        self._fpsEstimate = None
    #1被property修饰的方法只有一个参数，self 2.它必须要有返回值
    @property
    def channel(self):
        return self._channel
    @channel.setter
    def channel(self,value):
        if self._channel != value:
            self._channel = value
            self._frame = None

    @property
    def frame(self):
        if self._enteredFrame and self._frame is None:
            _,self._frame = self._capture.retrieve()
        return self._frame
    @property
    def isWritingImage(self):
        return self._imageFilename is not None
    @property
    def isWritingVideo(self):
            return  self._videoFilename is not None

    def enterFrame(self):

        assert  not self._enteredFrame,\
            'previous enterFrame() had no matching exitFrame()'
        if self._capture is not None:
            self._enteredFrame = self._capture.grab()

    def exitFrame(self):
        if self.frame is None:
            self._enteredFrame = False
            return
        if self._framesElapsed == 0:
            self._startTime = time.time()
        else :
            timeElapsed  = time.time()-self._startTime
            self._fpsEstimate = self._framesElapsed/timeElapsed
        self._framesElapsed += 1

        if self.previewWindowManager is not None:
            if self.shouldMirrorPreview:
                mirroredFrame = np.fliplr(self._frame).copy()

                #加美白
                # value = 18
                # mirroredFrame = cv2.bilateralFilter(mirroredFrame,value,value*2,value/2)
                #过滤某通道颜色
                mirroredFrame[:,:,1] = 0
                self.previewWindowManager.show(mirroredFrame)
            else:
                self.previewWindowManager.show(self._frame)

        if self.isWritingImage :
            cv2.imwrite(self._imageFilename,self._frame)
            self._imageFilename = None

        self._writeVideoFrame()
        self._frame = None
        self._enteredFrame = False

    def writeImage(self,filename):
        self._imageFilename = filename

    def startWritingVideo(self,filename,encoding=cv2.VideoWriter_fourcc('I','4','2','0')):
        self.flag = 111
        self._videoFilename = filename
        self._videoEncoding = encoding

    def stopWritingvideo(self):
        self._videoFilename = None
        self._videoEncoding = None
        self._videoWriter = None

    def _writeVideoFrame(self):
        if not self.isWritingVideo:
            return
        if self._videoWriter is None:   #构建一次cv2.VideoWriter
            fps = int(self._capture.get(cv2.CAP_PROP_FPS))
            if fps == 30: #从摄像头读取图像，预估fps
                if self._framesElapsed<20:
                    return
                else:
                    fps = self._fpsEstimate
                    print('预估FPS：',fps)
            #如果再放外一层，每次调用—videoWriter都会赋值size和构造self._videoWriter，这是不期望的。
            #只需测到预估FPS后构造一次self._videoWriter，后续调用之后执行self._videoWriter.write
            size = (int(self._capture.get(cv2.CAP_PROP_FRAME_WIDTH))),(int(self._capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            self._videoWriter = cv2.VideoWriter(self._videoFilename,self._videoEncoding,fps,size)
        #重点BUG 20帧之后写入 不在if self._videoWriter is None之内写入图片数据
        self._videoWriter.write(self._frame)


class WindowManager(object):

    def __init__(self, windowname,keypresscallback=None):

        self.keypresscallback = keypresscallback
        self._windowname = windowname
        self._iswindowcreated = False

    @property
    def iswindowcreated(self):
        return self._iswindowcreated
    
    def createdwindow(self):
        cv2.namedWindow(self._windowname)
        self._iswindowcreated = True

    def show(self,frame):
        cv2.imshow(self._windowname,frame)

    def destroyWindow(self):
        cv2.destroyWindow(self._windowname)
        self._iswindowcreated = False

    def processEvents(self):
        keycode = cv2.waitKey(80)
        if self.keypresscallback is not None and keycode != -1:
            keycode &= 0xFF
            self.keypresscallback(keycode)

class Cameo:

    def __init__(self):

        self._windowManager = WindowManager('Cameo',self.onKeypress)
        self._captureManager = CaptureManager(cv2.VideoCapture('baidu.gif'),self._windowManager,True)

    def run(self):
        self._windowManager.createdwindow()
        while self._windowManager.iswindowcreated :
            self._captureManager.enterFrame()
            frame = self._captureManager.frame
        # TODO: Filter the frame (Chapter 3)

            self._captureManager.exitFrame()
            self._windowManager.processEvents()

    #监听到键盘事件 调用该函数执行相应操作
    def onKeypress(self,keycode):
        if keycode == 32:
            self._captureManager.writeImage('screenshot.png')

        elif keycode == 9:
            if not self._captureManager.isWritingVideo:
                self._captureManager.startWritingVideo('screen.avi')
            else:
                self._captureManager.stopWritingvideo()

        elif keycode == 27:
            self._windowManager.destroyWindow()


if __name__ == '__main__':
    Cameo().run()





