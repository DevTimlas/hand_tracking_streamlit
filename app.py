import cv2
import numpy as np
import av
import mediapipe as mp
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

def process(image):
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
    return cv2.flip(image, 1)


RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

class VideoProcessor:
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")

        img = process(img)

        return av.VideoFrame.from_ndarray(img, format="bgr24")

webrtc_streamer(key="example",
			rtc_configuration={"iceServers":[

				{"urls":"stun:openrelay.metered.ca:80",},

				{"urls":"turn:openrelay.metered.ca:80",
				"username":"openrelayproject",
				"credential":"openrelayproject",},

				{"urls":"turn:openrelay.metered.ca:443",
				"username":"openrelayproject",
				"credential":"openrelayproject",},

				{"urls":"turn:openrelay.metered.ca:443?transport=tcp",
				"username":"openrelayproject",
				"credential":"openrelayproject",},],},

			video_processor_factory=VideoProcessor,
			media_stream_constraints={"video":True, "audio":False})

