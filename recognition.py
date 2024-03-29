import face_recognition
import os, sys
import cv2
import numpy as np  
import math
import os
import time


#window

def slic(sting,s1,s2):
    return(sting[sting.find(s1)+1 : sting.find(s2)])
#run

# Helper
def face_confidence(face_distance,str_convert=True, face_match_threshold=0.6):
    range = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + '%'
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        if str_convert == True:
            return str(round(value, 2)) + '%'
        else: 
            return round(value, 2)
            




class FaceRecognition:
    face_locations = []
    face_encodings = []
    face_names = []
    known_face_encodings = []
    known_face_names = []
    process_current_frame = True

    def __init__(self):
        self.encode_faces()

    def encode_faces(self):
        for image in os.listdir('faces'):
            face_image = face_recognition.load_image_file(f"faces/{image}")
            face_encoding = face_recognition.face_encodings(face_image)[0]

            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(image)
        print(self.known_face_names)

    def run_recognition(self):
        video_capture = cv2.VideoCapture(0)

        if not video_capture.isOpened():
            sys.exit('Video source not found...')

        while True:
            ret, frame = video_capture.read()

            # Only process every other frame of video to save time
            if self.process_current_frame:
                # Resize frame of video to 1/4 size for faster face recognition processing
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

                # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                rgb_small_frame = small_frame[:, :, ::-1]

                # Find all the faces and face encodings in the current frame of video
                self.face_locations = face_recognition.face_locations(rgb_small_frame)
                self.face_encodings = face_recognition.face_encodings(small_frame, self.face_locations)

                self.face_names = []
                for face_encoding in self.face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    name = "Unknown"
                    confidence = '???'

                    # Calculate the shortest distance to face
                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)

                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index]
                        confidence = face_confidence(face_distances[best_match_index])
                        confidence_n = face_confidence(face_distances[best_match_index],False)

                        self.confid = face_confidence(face_distances[best_match_index])

                            
                    try:
                        if confidence_n < 88:
                            name = "Unknown"
                            confidence = '???'
                    except:
                        pass

                    self.face_names.append(f'{name} ({confidence})')
                    open('file.txt', 'w').close()
                    counts = time.strftime("%H:%M:%S")
                    try:
                        with open("data.txt", 'r') as file:
                            var = file.read()
                            file.close()
                        zafr = (f"<{counts}>|{confidence}/{name}..")
                        if var == zafr:
                            pass
                        else:
                            name = name.split(".")[0]
                            with open("data.txt", "w") as file:
                                file.write(f"<{counts}>|{confidence}/{name}..")
                                file.close()
                            with open("file.txt", "a") as file:
                                file.write(f"<{counts}>|{confidence}/{name}..")
                                file.close()
                                
                    except:
                        name = name.split(".")[0]
                        with open("data.txt", "w") as file:
                                file.write(f"<{counts}>|{confidence}/{name}..")
                                file.close()
                
                    


            self.process_current_frame = not self.process_current_frame

            # Display the results
            for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Create the frame with the name
                cv2.rectangle(frame, (left, top), (right, bottom), (225, 102, 0), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

            # Display the resulting image
            cv2.imshow('Face Recognition', frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) == ord('q'):
                break
    def get_value(self):
        return self.confidence

        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    fr = FaceRecognition()
    fr.run_recognition()
