# User-Defined-function-for-Spatial-Filtering-
I have written a function for spatial filtering which has the following syntax, with only 'f' and 'w' as mandatory input arguments, g=imfilter_rollno(f, w, filtering_mode, boundary_options, size_options) where 'f' is the input image, 'g' is the filtered result, and the other parameters are summarized below.
The filtering mode is specified as 'corr' for correlation (this is kept as default) or as 'conv' for convolution. The boundary options deal with the border-padding issue, and the size of the filter determines the size of the border. The size options are either 'same' (default) or 'full.' 

Aim: 
The output of the code written in Python (imfilter17110150) should be somewhat similar to that of the in-built function present in MATLAB (imfilter). 

First of all, RGB input image is converted into its grayscale form. Then, for any of the size options chosen, same boundary is applied to the input image (m ∗ n) such that the output image remains of the same size as the input image is. Here, I have considered only the square matrix kernel to make it less complicated. For a kernel matrix of size (2k+1), (2k) rows and columns are added to the input matrix. For obtaining diﬀerent boundary conditions, I took an array of dimension (m+2k)∗(n+2k) with all its elements equal to 0 named as 'padded_f.' Then, in the middle, skipping 2k rows and columns, the input matrix is placed, and the following operations are carried out for diﬀerent boundary options:

Boundary Options

• P : The value of P is padded at the boundaries. The default value taken is 0. 

• 'replicate' : The 1st row(1∗n), last row(1∗n), 1st column(m∗1) and last column(m ∗ 1) are stored in 4 diﬀerent variables: a,b,c, and d and then replicated 'k' times at the boundaries of the 'padded_f' matrix according to the kernel chosen. If the size of the kernel is 3 ∗ 3, each variable is replicated once to it. If the size of the kernel is 7 ∗ 7, each variable id replicated thrice to it. The four corners of the input matrix (each of size 1 ∗ 1) are also stored in diﬀerent variables e,g,h, and k and then, replicated at the corner boundaries of the 'padded_f' matrix according to the kernel matrix chosen. 

• 'symmetric' : The 1st row(k ∗ n), last row(k ∗ n), 1st column(m ∗ k) and last column (m ∗ k) are stored in four diﬀerent variables: top_row, bottom_row, left_column and right_column. The 1st two are ﬂipped horizontally and then replicated once at the boundaries of the 'padded_f' matrix according to the kernel chosen. Similarly, the last two are ﬂipped vertically and then replicated.The 4 corners of the input matrix each of size k ∗ k are also stored in 4 diﬀerent variables: top_left_corner, top_right_corner, bottom_left_corner and bottom_right_corner. All the four matrices are ﬂipped horizontally and vertically and then replicated k2 times at the corners of the boundaries at their respective locations. 

• 'circular' : (Treating the input image as a 2D periodic function) the boundary elements are filled with appropriate values. 

After applying desired boundary to the input image, the size of the obtained ’padded_f’ matrix is again changed depending upon the size option chosen.

Size Options 

• 'same' : No change needs to be done to the 'padded_f' matrix. 

• 'full' : Zeroes are padded at the boundaries of the 'padded_f' matrix, which therefore increases the rows and columns by '2k' where 'k' is the number of rows or columns present in the kernel matrix. 

Now, convolution or correlation is carried out on the 'padded_f' matrix, depending upon the filtering mode given by the user.

#Parameters Chosen 

• f: Input Image represented as 2D matrix

• w: filter, assumed to have equal number of rows and columns 

• g: Filtered output Image

• filtering_mode : can be either ’corr’ for correlation or ’conv’ for convolution 

• boundary_options : P, 'symmetric,' 'replicate,' 'circular' 

• size_options: 'same' or 'full' 

• row_f, column_f: number of rows, number of columns of the input image 

• row_w,column_w: number of rows and number of columns of the kernel, assuming the kernel to be a square matrix (row_w=column_w)

• padded_f: It is the input matrix after applying necessary boundary conditions. Convolution and correlation operations are performed on this matrix only.




 
 	
