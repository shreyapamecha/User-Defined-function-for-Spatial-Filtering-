#--------------------
#f represents the input image
#w represents the filter
#g represents the output image
#filtering_mode can be either 'corr' for correlation and 'conv' for convolution
#boundary_options: 0 for pad
#size_options can be 'same' or 'full'
#--------------------

#importing libraries
import cv2
import numpy as np
import matplotlib.pyplot as plt
import time

start_time=time.time();

def imfilter_17110150(f,w,filtering_mode,boundary_options=0,size_options='same'):
    P=boundary_options; #local variable
    #print(w)
    row_f=len(f); #number of rows in input image
    column_f=len(f[0]); #number of columns in the output image

    row_w=len(w); #number of rows in the filter
    column_w=len(w[0]);#for a square matrix filter, number of rows = number of columns

    #padding for both correlation and convolution
    offset_value=int(((row_w)-1)/2); #offset value for 3*3 filter is '1': for 5*5 filter is '2': offset value for 7*7 filter is '3'
    #print(offset_value)
    rows=row_f+(2*offset_value); #number of rows of the image after padding zeros to the boundary
    columns=column_f+(2*offset_value); #number of columns of the image after padding zeros to the boundary

    #different boundary_options: 'circular', 'symmetric', 'replicate', 'defaut'
    #correlation or convolution are done on this matrix ('padded_f')
    #circular: the size of the image is extended by treating the image as one period a 2-D periodic function
    if boundary_options=='circular':
        padded_f=np.zeros((rows,columns));
        #print('rows',rows,'columns',columns)
        #initially, padded_f was a matrix with all the elements equal to zero, operations has been done on it so that boundaries change according to the user input
        padded_f[offset_value:row_f+offset_value,offset_value:column_f+offset_value]=f #'f' matrix is there in the middle of the 'padded_f'
        #for boundary
        padded_f[0:offset_value,offset_value:columns-offset_value]=np.array(f)[row_f-offset_value:row_f,0:column_f] #for replicating the last row, considering a 3*3 kernel matrix
        padded_f[rows-offset_value:rows,offset_value:columns-offset_value]=np.array(f)[0:offset_value,0:column_f] #for replicating the 1st row, considering a 3*3 kernel matrix
        padded_f[offset_value:rows-offset_value,0:offset_value]=np.array(f)[0:row_f,column_f-offset_value:column_f] #for replicating the last column, considering a 3*3 kernel matrix 
        padded_f[offset_value:rows-offset_value,columns-offset_value:columns]=np.array(f)[0:row_f,0:offset_value] #for replicating the 1st column, considering a 3*3 kernel matrix
        padded_f[0:offset_value,0:offset_value]=np.array(f)[row_f-offset_value:row_f,column_f-offset_value:column_f] #for replicating the bottom right corner, considering a 3*3 kernel matrix
        padded_f[0:offset_value,columns-offset_value:columns]=np.array(f)[row_f-offset_value:row_f,0:offset_value] #for replicating the bottom left corner, considering a 3*3 kernel matrix
        padded_f[rows-offset_value:rows,0:offset_value]=np.array(f)[0:offset_value,column_f-offset_value:column_f] #for replicating the top right corner, considering a 3*3 kernel matrix
        padded_f[rows-offset_value:rows,columns-offset_value:columns]=np.array(f)[0:offset_value,0:offset_value] #for replicating the top left corner, considering a 3*3 kernel matrix
        #print(padded_f)

    #symmetric: the size of the image is extended mirror-reflecting it across its border
    elif boundary_options=='symmetric':
        padded_f=np.zeros((rows,columns)); #initializing a matrix with all the elements equal to 0
        #print('rows',rows,'columns',columns)
        padded_f[offset_value:row_f+offset_value,offset_value:column_f+offset_value]=f
        
        top_row=np.array(f)[0:offset_value,0:column_f]
        bottom_row=np.array(f)[row_f-offset_value:row_f,0:column_f]
        #for horizonal flip of the top row (mirror-reflection along horizontal axis)
        top_row_replica=top_row;
        top_row=np.zeros((len(top_row_replica),len(top_row_replica[0])))
        for i in range(len(top_row_replica)):
            top_row[i]=top_row_replica[len(top_row_replica)-1-i]
        #print(top_row_replica,'top_row_replica',top_row,'top_row')
        #for horizontal flip of the last row (mirror-reflection along horizontal axis)
        bottom_row_replica=bottom_row;
        bottom_row=np.zeros((len(bottom_row_replica),len(bottom_row_replica[0])))
        for i in range(len(bottom_row_replica)):
            bottom_row[i]=bottom_row_replica[len(bottom_row_replica)-1-i]
        #for top and bottom rows after applying symmetric boundary options
        padded_f[0:offset_value,offset_value:columns-offset_value]=top_row
        padded_f[rows-offset_value:rows,offset_value:columns-offset_value]=bottom_row

        left_column=np.array(f)[0:row_f,0:offset_value]
        right_column=np.array(f)[0:row_f,column_f-offset_value:column_f]
        #for vertical flip of the leftmost column (mirror-reflection along vertical axis)
        left_column_replica=np.array(left_column);
        left_column=np.array(np.zeros((len(left_column_replica),len(left_column_replica[0]))))
        for i in range(len(left_column_replica[0])):
            left_column[:,i]=left_column_replica[:,len(left_column_replica[0])-1-i]
        #print(left_column_replica,'left_column_replica',left_column,'left_column')
        #for vertical flip of the rightmost column (mirror-reflection along vertical axis) 
        right_column_replica=np.array(right_column);
        right_column=np.array(np.zeros((len(right_column_replica),len(right_column_replica[0]))))
        for i in range(len(right_column_replica[0])):
            right_column[:,i]=right_column_replica[:,len(right_column_replica[0])-1-i]
        #print(right_column_replica,'right_column_replica',right_column,'right_column')
        padded_f[offset_value:rows-offset_value,0:offset_value]=left_column
        padded_f[offset_value:rows-offset_value,columns-offset_value:columns]=right_column

        #for both horizontal and vertical flips of the corner matrices (reflection along both the axes)
        top_left_corner=np.array(f)[0:offset_value,0:offset_value]
        top_right_corner=np.array(f)[0:offset_value,column_f-offset_value:column_f]
        bottom_left_corner=np.array(f)[row_f-offset_value:row_f,0:offset_value]
        bottom_right_corner=np.array(f)[row_f-offset_value:row_f,column_f-offset_value:column_f]
        top_left_corner_replica=top_left_corner;
        top_right_corner_replica=top_right_corner;
        bottom_left_corner_replica=bottom_left_corner;
        bottom_right_corner_replica=bottom_right_corner;
        top_left_corner=np.array(np.zeros((len(top_left_corner_replica),len(top_left_corner_replica[0]))))
        top_right_corner=np.array(np.zeros((len(top_right_corner_replica),len(top_right_corner_replica[0]))))
        bottom_left_corner=np.array(np.zeros((len(bottom_left_corner_replica),len(bottom_left_corner_replica[0]))))
        bottom_right_corner=np.array(np.zeros((len(bottom_right_corner_replica),len(bottom_right_corner_replica[0]))))
        #for top left corner
        for i in range(len(top_left_corner_replica)):
            for j in range(len(top_left_corner_replica[0])):
                s=abs(len(top_left_corner_replica)-1-i);
                t=abs(len(top_left_corner_replica[0])-1-j);
                top_left_corner[i][j]=top_left_corner_replica[s][t]
        #for top right corner
        for i in range(len(top_right_corner_replica)):
            for j in range(len(top_right_corner_replica[0])):
                s=abs(len(top_right_corner_replica)-1-i);
                t=abs(len(top_right_corner_replica[0])-1-j);
                top_right_corner[i][j]=top_right_corner_replica[s][t]
        #for bottom left corner
        for i in range(len(bottom_left_corner_replica)):
            for j in range(len(bottom_left_corner_replica[0])):
                s=abs(len(bottom_left_corner_replica)-1-i);
                t=abs(len(bottom_left_corner_replica[0])-1-j);
                bottom_left_corner[i][j]=bottom_left_corner_replica[s][t]
        #for bottom right corner
        for i in range(len(bottom_right_corner_replica)):
            for j in range(len(bottom_right_corner_replica[0])):
                s=abs(len(bottom_right_corner_replica)-1-i);
                t=abs(len(bottom_right_corner_replica[0])-1-j);

        padded_f[0:offset_value,0:offset_value]=top_left_corner
        padded_f[0:offset_value,columns-offset_value:columns]=top_right_corner;
        padded_f[rows-offset_value:rows,0:offset_value]=bottom_left_corner;
        padded_f[rows-offset_value:rows,columns-offset_value:columns]=bottom_right_corner;
        #print(padded_f)

    #replicate: the size of the image is extended by replicating the values in its outer border
    elif boundary_options=='replicate':
        padded_f=np.zeros((rows,columns)); #initializing a matrix with all the elements equal to 0
        #print('rows',rows,'columns',columns)
        padded_f[offset_value:row_f+offset_value,offset_value:column_f+offset_value]=f

        a=np.array(f)[0];
        b=np.array(f)[row_f-1];
        c=np.array(f)[:,0:1];
        d=np.array(f)[:,column_f-1:column_f];
        for i in range(offset_value):
            padded_f[i:i+1,offset_value:column_f+offset_value]=a #for 1st row
            j=rows-i-1
            padded_f[j:j+1,offset_value:column_f+offset_value]=b # for last row
            padded_f[offset_value:row_f+offset_value,i:i+1]=c
            j=columns-i-1
            padded_f[offset_value:row_f+offset_value,j:j+1]=d

        e=f[0][0]
        g=f[0][column_f-1]
        h=f[row_f-1][0]
        k=f[row_f-1][column_f-1]
        for i in range(offset_value):
            for j in range(offset_value):
                padded_f[i:i+1,j:j+1]=e #top left
                padded_f[i:i+1,columns-j-1:columns-j]=g #top right
                padded_f[rows-i-1:rows-i,j:j+1]=h #bottom left
                padded_f[rows-i-1:rows-i,columns-j-1:columns-j]=k #bottom right
        #print(padded_f)
             
    else:
        #This is just padding 0 or P at the boundary and further performing correlation or convolution on it
        padded_f=np.full((rows,columns),P); #a matrix with 'rows' rows and 'columns' columns in which value of all the elements is zero 
        #print(padded_f)
    
        padded_f[offset_value:row_f+offset_value,offset_value:column_f+offset_value]=f #matrix of the image obtained after padding on which operations would be performed 
        #print(padded_f)


    #inverting the filter matrix for convolution
    w_change=w;
    #print(w_change)
    if (filtering_mode == 'conv'): 
        w=np.zeros((row_w,column_w));
        for i in range(row_w):
            for j in range(column_w):
                s=abs(row_w-1-i);
                t=abs(column_w-1-j);
                w[i][j]=w_change[s][t]
        
    
    #size_options: 'same' and 'full'
    #for 'full' size_options, extra zeros are being padded to the 'padded_f' matrix before carrying out correlation or convolution
    if size_options=='full':
        more_pad_f=np.zeros((row_f+(4*offset_value),column_f+(4*offset_value)))
        more_pad_f[offset_value:rows+offset_value,offset_value:columns+offset_value]=padded_f
        g=np.zeros((row_f+(2*offset_value), column_f+(2*offset_value))) #this is the output matrix, currenlty with 'zero' pixel values

        
        for i in range(rows):
            for j in range(columns):
                for k in range(row_w):
                    for l in range(column_w):
                        g[i][j]+=w[k][l]*more_pad_f[i+k][j+l]

                g[i][j]=round(g[i][j]);

                if (g[i][j]<0):
                    g[i][j]=0;
                if (g[i][j]>255):
                    g[i][j]=255; 

        
    else:
        g=np.zeros((row_f,column_f)); #this is the output matrix, currenlty with 'zero' pixel values
        for i in range(row_f):
            for j in range(column_f):
                for k in range(row_w):
                    for l in range(column_w):
                        g[i][j]+=w[k][l]*padded_f[i+k][j+l]

                g[i][j]=round(g[i][j]);

                if (g[i][j]<0):
                    g[i][j]=0;
                if (g[i][j]>255):
                    g[i][j]=255;
        
    

    #print(g)            
    return g

#------ASSUMPTIONS-------
#The filter will always be a square matrix with size greater than or equal to (3*3)
#    
#------------------------

if __name__ == '__main__':
    
    path_to_image = 'C:\\Users\\ympam\\Downloads\\image2.jpg';
    f=cv2.imread(path_to_image,cv2.IMREAD_GRAYSCALE); #array of an input image which is to be filtered
    P=50; #this is for the boundary options; image is extended by padding the value P, here the default value is 0
    #------------- for varying the filter size (uncomment the one which is to be used)
    w = np.array([[1,0,-1],
                  [2,0,-2],
                  [1,0,-1]]); #a 3*3 filter
    #-------------
    #w = np.array([[1/25,1/25,1/25,1/25,1/25],
    #              [1/25,1/25,1/25,1/25,1/25],
    #              [1/25,1/25,1/25,1/25,1/25],
    #              [1/25,1/25,1/25,1/25,1/25],
    #              [1/25,1/25,1/25,1/25,1/25]]); #a 5*5 filter: a low-pass filter
    #-------------
    #w = np.array([[0,0,0,5/1068,0,0,0],
    #              [0,5/1068,18/1068,32/1068,18/1068,5/1068,0],
    #              [0,18/1068,64/1068,100/1068,64/1068,18/1068,0],
    #              [5/1068,32/1068,100/1068,100/1068,100/1068,32/1068,5/1068],
    #              [0,18/1068,64/1068,100/1068,64/1068,18/1068,0],
    #              [0,5/1068,18/1068,32/1068,18/1068,5/1068,0],
    #              [0,0,0,5/1068,0,0,0]]); #a 7*7 filter, here processing time is a bit higher
    #------------
    
    filtering_mode='corr' # 2 options: 'corr' for correlation and 'conv' for convolution
    boundary_options='circular'
    size_options='full'
    #Now, calling the function imfilter
    g=imfilter_17110150(f,w,filtering_mode,boundary_options,size_options);

    #cv2.imshow('Filtered_Image', g)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    fig=plt.figure()
    ax1=fig.add_subplot(2,1,1)
    ax1.imshow(f, cmap='gray')
    ax2=fig.add_subplot(2,1,2)
    plt.imshow(g, cmap='gray')
    plt.show()

    print('%s seconds'%(time.time()-start_time))
    


