from flask import Flask, render_template, Response, g
import cv2

app = Flask("webcam_streaming")

global started
started = False

camera = cv2.VideoCapture(0)

def gen_frames():
    global started
    if not started:
        return
    while True:
        success, frame = camera.read()
        if success and started:
            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame, 1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass


@app.route('/start_stop_camera', methods=['POST'])
def start_stop_webcam():
    global started, camera
    started = not started
    if not started:
        camera.release()
        cv2.destroyAllWindows()
    else:
        camera = cv2.VideoCapture(0)
    return render_template('index.html')

@app.route('/camera')
def camera():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run()

camera.release()
cv2.destroyAllWindows()
