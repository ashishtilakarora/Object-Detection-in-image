#classes and subclasses to import
import cv2
import numpy as np
import os
from os import listdir
from os.path import isfile, join,basename

#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
#subroutine to write rerults to a csv
def writecsv(color,shape):
    #open csv file in append mode
    filep = open(filename,'a')
    # create string data to write per image
    datastr = "," + color + "-" + shape
    #write to csv
    filep.write(datastr)
    filep.close()

def main(path):
#####################################################################################################

    #to extract the test image number
    n = basename(path)[len(basename(path))-5]

    img = cv2.imread(path,1)
    img2 = cv2.imread(path,1) 

    img2 = cv2.cvtColor(img2,cv2.COLOR_BGR2HSV)

    edges = cv2.Canny(img,100,200)

    features = [basename(path)]
    _,contours,hierarchy = cv2.findContours(edges,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
    
    for i in range(len(contours))[1:]:
        if hierarchy[0][i][3] >=0 :
            c=contours[i]
            shape = "unidentified"
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.04 * peri, True)

            cy1 = int( c[0][0][1]) 
            cx1 = int( c[0][0][0])
            
            M = cv2.moments(c)
            cx2 = int(M['m10']/M['m00'])
            cy2 = int(M['m01']/M['m00'])

            cy1 = int(cy1 + 0.1*(cy2-cy1))
            cx1 = int(cx1 + 0.1*(cx2-cx1))

            color = img2[cy1,cx1]
            
            if color[0]<=10: 
                color = "red"
            elif color[0]<=65 and color[0]>=55:
                color = "green"
            elif color[0]<=125 and color[0]>=115:
                color = "blue"

            if len(approx) == 3:
                shape = "triangle"
            elif len(approx) == 4:
                (x, y, w, h) = cv2.boundingRect(approx)
                ar = w / float(h)
                if ar >= 0.95 and ar <= 1.05:
                    shape = "square"
                else:
                    shape = "rectangle"
            elif len(approx) == 5:
                shape = "pentagon"
            else:
                shape = "circle"

            writecsv(color,shape)

            combo = [color + "-" + shape]

            features.append(combo)

            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img,color + "-" + shape,(cx1,cy1), font, 0.5,(0,0,0),1,cv2.LINE_AA)
            cv2.drawContours(img,contours,i,(0,0,0),2)
                
    fname = 'output' + n + '.png'
    """
    cv2.imshow("img",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    """
    cv2.imwrite(fname,img)
    return features
#####################################################################################################


#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
#main where the path is set for the directory containing the test images
if __name__ == "__main__":
    global filename 
    filename = '4103.csv'
    mypath = 'C:/Users/admin/Desktop/@shu/eyantra tasks/Set 4/Task 1A/Test Images/'
    #getting all files in the directory
    onlyfiles = [join(mypath, f) for f in listdir(mypath) if f.endswith(".png")]
    #iterate over each file in the directory
    for fp in onlyfiles:
        #Open the csv to write in append mode
        filep = open(filename,'a')
        #this csv will later be used to save processed data, thus write the file name of the image 
        filep.write(fp)
        #close the file so that it can be reopened again later
        filep.close()
        #process the image
        data = main(fp)
        print data
        #open the csv
        filep = open(filename,'a')
        #make a newline entry so that the next image data is written on a newline
        filep.write('\n')
        #close the file
        filep.close()
