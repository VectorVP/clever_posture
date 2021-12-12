from flask import Flask, render_template, Response
import cv2
import mediapipe as mp


STATIC_FOLDER = 'templates/assets'
app = Flask(__name__, static_folder=STATIC_FOLDER)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/survey')
def survey():
    return render_template('survey.html')


def gen_frames():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n' 
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def gen_frames_pipe():
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_pose = mp.solutions.pose
    camera = cv2.VideoCapture(0)

    while True:
        success, image = camera.read()
        if not success:
            break
        else:
            with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = pose.process(image)
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                mp_drawing.draw_landmarks(
                    image,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

                ret, buffer = cv2.imencode('.jpg', image)
                frame = buffer.tobytes()
                yield (b'--frame\r\n' 
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/processing')
def video_feed():
    # return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    return Response(gen_frames_pipe(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/stream')
def stream():
    return render_template('stream.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
