from flask import Flask, render_template
import cv2

app = Flask("webcam_streaming")

started = False
camera = cv2.VideoCapture(0) # let's check here if you have a camera. Maybe select the camera?

def gen_frames():
    while True:
        success, frame = camera.read() 
        if success and started:
            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass
        else:
            pass

@app.route('/start_stop', methods=['POST'])
def start_stop_webcam():
    started = !started
    if not started:
        camera.release()
        cv2.destroyAllWindows()
    else:
        camera = cv2.VideoCapture(0)
    return Response({})

@app.route('/camera')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')
