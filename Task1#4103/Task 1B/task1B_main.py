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
def writecsv(color,shape,size,count):
    #open csv file in append mode
    filep = open(filename,'a')
    # create string data to write per image
    datastr = "," + color + "-" + shape + "-" + size + "-" + count
    #write to csv
    filep.write(datastr)

def main(path):
#####################################################################################################
    color = ""
    size = ""
    shape = ""
    n = 0
    features = []
    colors = []
    sizes = []
    counts = []
    shapes = []


    j = basename(path)[len(basename(path))-5]
    k = 0
    
    img = cv2.imread(path,1)
    img1 = cv2.imread(path,1)
    img2 = cv2.imread(path,1) 

    img2 = cv2.cvtColor(img2,cv2.COLOR_BGR2HSV)

    edges = cv2.Canny(img,100,200)

    
    _,contours,hierarchy = cv2.findContours(edges,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)

    #address of sample images 
    addr = "C:/Users/admin/Desktop/Set 4/Task 1B/Test Images/Sample Images/"

    for i in range(len(contours))[1:]:
         if hierarchy[0][i][3] >=0 :
             
            cv2.drawContours(img1,contours,i,(0,0,0),2)
            c = contours[i]
            xy = tuple(c[0][0])
            
            cy1 = int( c[0][0][1]) 
            cx1 = int( c[0][0][0])
            
            shape = "unidentified"

            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.04 * peri, True)

            
            M = cv2.moments(c)
            cx2 = int(M['m10']/M['m00'])
            cy2 = int(M['m01']/M['m00'])

            cy1 = int(cy1 + 0.1*(cy2-cy1))
            cx1 = int(cx1 + 0.1*(cx2-cx1))
     
            color = img2[cy1,cx1]

            if color[0]<=10: 
                color = "red"
            elif color[0]<=20:
                color = "orange"
            elif color[0]<=35:
                color = "yellow"
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

            area = cv2.contourArea(c)

            sname1 = "Sample_" + shape + "_small.png"
            sname2 = "Sample_" + shape + "_large.png"

            simg1 = cv2.imread(join(addr,sname1),1)
            simg2 = cv2.imread(join(addr,sname2),1)

            simg1_gray = cv2.cvtColor(simg1,cv2.COLOR_BGR2GRAY)
            _,thresh1 = cv2.threshold(simg1_gray,230,255,cv2.THRESH_BINARY)

            simg2_gray = cv2.cvtColor(simg2,cv2.COLOR_BGR2GRAY)
            _,thresh2 = cv2.threshold(simg2_gray,230,255,cv2.THRESH_BINARY)
            
            _,cntrs1,_ = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            _,cntrs2,_ = cv2.findContours(thresh2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

            area1 = cv2.contourArea(cntrs1[1])
            area2 = cv2.contourArea(cntrs2[1])

            if area <= area1:
                size = "small"

            elif area >= area2:
                size = "large"

            else :
                size = "medium"

            colors.append(color)
            sizes.append(size)
            shapes.append(shape)

            k = k+1
            
            combo = [color + "-" + shape + "-" + size]
            features.append(combo)
            
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img1, color + "-" + shape + "-" + size, (cx1,cy1), font, 0.5, (0,0,0), 1, cv2.LINE_AA)
            
    f=[]
    
    for x in range(k):
        f.append(0)

    extrafeatures = []
    extrafeatures.append(basename(path))
    
    for x in range(k):
        if f[x] == 0:
            n=1;
            f[x] = 1
            for y in range(k)[x+1:]:
                if features[x] == features[y]:
                    f[y] = 1
                    n=n+1;
            
            combo = [features[x][0] + "-" + str(n)]
            extrafeatures.append(combo)
            writecsv(colors[x],shapes[x],sizes[x],str(n))

    fname = 'output' + j + '.png'

    """
    cv2.imshow("img",img1)  
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    """
    cv2.imwrite(fname,img1)
    return extrafeatures


        

#####################################################################################################


#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
#main where the path is set for the directory containing the test images
if __name__ == "__main__":
    global filename 
    filename = '4103.csv'
    mypath = 'C:/Users/admin/Desktop/Set 4/Task 1B/Test Images/'
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
