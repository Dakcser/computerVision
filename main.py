import cv2
import numpy as np
import dlib

def main():

    #open default camera
    cap = cv2.VideoCapture(0)

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    landmarkCoordinates = {}

    while True:

        _, frame = cap.read()
        # grey scale format, requires less processing. Video should be well illuminated
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        for face in faces:

            x1 = face.left()
            y1 = face.top()
            x2 = face.right()
            y2 = face.bottom()

            #draw a box around the face by using coordinates, colour of rectangle = green, thickness = 3
            #cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255, 0), 3)

            landmarks = predictor(gray, face)



            #Map landmarks to coordinates in the matrix
            for n in range(48, 60):
                x = landmarks.part(n).x
                y = landmarks.part(n).y

                coordinate = (x, y)
                landmarkCoordinates[n] = coordinate

                cv2.circle(frame, (x, y), 2, (255, 0, 0), -1)


        distance = calculateDistance(landmarkCoordinates)
        print("Distance is: {}".format(distance))

        cv2.imshow("Frame", frame)

        #Stops closing the window, as long as program is running
        key = cv2.waitKey(1)
        if key == 27:
            break

def calculateDistance(data):

    points = []

    #print(data)

    for n in range(3):

        index = n + 50
        coord1 = data[index]
        index = 58 - n
        coord2 = data[index]

        '''
        print("------")
        print(coord1)
        print(coord2)
        '''

        x = coord2[0]-coord1[0]
        y = coord2[1]-coord1[1]
        xy = (np.power(x, 2) + np.power(y, 2))
        delta = np.sqrt(xy)

        points.append(delta)

    distance = (points[0]+points[1]+points[2])/3

    #print(points)

    return distance



if __name__ == "__main__":
    main()