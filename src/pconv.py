
# coding: utf-8

# # pconv - Periodic convolution, kernel origin at array origin
# 
# ##Synopse
# 
# 1D, 2D or 3D Periodic convolution. (kernel origin at array origin)
# 
# - **g = pconv(f, h)**
# 
#   - **g**: Image. Output image. 
# 
#   - **f**: Image. Input image.
#   - **h**: Image. PSF (point spread function), or kernel. The origin is at the array origin.

# ## Description
# 
# Perform a 1D, 2D or 3D discrete periodic convolution. The kernel origin is at the origin of image h. 
# Both image and kernel are periodic with same period. Usually the kernel h is smaller than the image f, 
# so h is padded with zero until the size of f. Supports complex images.

# In[1]:

def pconv(f,h):
    import numpy as np

    h_ind=np.nonzero(h)
    f_ind=np.nonzero(f)
    if len(h_ind[0])>len(f_ind[0]):
        h,    f    = f,    h
        h_ind,f_ind= f_ind,h_ind

    gs = np.maximum(np.array(f.shape),np.array(h.shape))
    if (f.dtype == 'complex') or (h.dtype == 'complex'):
        g = np.zeros(gs,dtype='complex')
    else:
        g = np.zeros(gs)

    f1 = g.copy()
    f1[f_ind]=f[f_ind]      

    if f.ndim == 1:
        (W,) = gs
        col = np.arange(W)
        for cc in h_ind[0]:
            g[:] += f1[(col-cc)%W] * h[cc]

    elif f.ndim == 2:
        H,W = gs
        row,col = np.indices(gs)
        for rr,cc in np.transpose(h_ind):
            g[:] += f1[(row-rr)%H, (col-cc)%W] * h[rr,cc]

    else:
        Z,H,W = gs
        d,row,col = np.indices(gs)
        for dd,rr,cc in np.transpose(h_ind):
            g[:] += f1[(d-dd)%Z, (row-rr)%H, (col-cc)%W] * h[dd,rr,cc]
    return g


# ## Examples
# 

# In[1]:

testing = (__name__ == '__main__')
if testing:
    get_ipython().system(' jupyter nbconvert --to python pconv.ipynb')
    import numpy as np
    get_ipython().magic('matplotlib inline')
    import matplotlib.image as mpimg
    import matplotlib.pyplot as plt
    import sys,os
    ea979path = os.path.abspath('../../')
    if ea979path not in sys.path:
        sys.path.append(ea979path)
    import ea979.src as ia


# ## Numerical Example 1D

# In[2]:

if testing: 
    f = np.array([0,0,0,1,0,0,0,0,1])
    print("f:",f)

    h = np.array([1,2,3])
    print("h:",h)

    g1 = ia.pconv(f,h)
    g2 = ia.pconv(h,f)
    print("g1:",g1)
    print("g2:",g2)


# ## Numerical Example 2D

# In[4]:

if testing:
    f = np.array([[1,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0],
                  [0,0,0,1,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,1],
                  [0,0,0,0,0,0,0,0,0]])
    print("Image (f):")
    print(f)
    
    h = np.array([[1,2,3],
                  [4,5,6]])
    print("\n Image Kernel (h):")
    print(h)
    
    g1 = ia.pconv(f,h)
    print("Image Output (g1=f*h):")
    print(g1)
    
    g2 = ia.pconv(h,f)
    print("Image Output (g2=h*f):")
    print(g)


# ## Numerical Example 3D

# In[5]:

if testing:
    f = np.zeros((3,3,3))
    #f[0,1,1] = 1
    f[1,1,1] = 1
    #f[2,1,1] = 1
     
    print("\n Image Original (F): ")
    print(f)

    h = np.array([[[ 1,  2, 3 ],
                   [ 3,  4, 5 ], 
                   [ 5,  6, 7 ]],
                  [[ 8,  9, 10],
                   [11, 12, 13], 
                   [14, 15, 16]],
                  [[17, 18, 19],
                   [20, 21, 22], 
                   [23, 24, 25]]])
              
    print("\n Image Kernel (H): ")
    print(h)
    
    result = ia.pconv(f,h)
    print("\n Image Output - (G): ")
    print(result)


# ## Example with Image 2D

# In[6]:

if testing:
    f = mpimg.imread('../data/cameraman.tif')
    ia.adshow(f, title = 'a) - Original Image')
    h = np.array([[-1,-1,-1],
                  [ 0, 0, 0],
                  [ 1, 1, 1]])
    g = ia.pconv(f,h)
    print("\nPrewitt´s Mask")
    print(h)
    
    gn = ia.normalize(g, [0,255])
    ia.adshow(gn, title = 'b) Prewitt´s Mask filtering')

    ia.adshow(ia.normalize(abs(g)), title = 'c) absolute of Prewitt´s Mask filtering')


# ## Equation
# 
# $$ f(i) = f(i + kN), h(i)=h(i+kN)$$
# 
# $$    mod(i,N) = i - N \lfloor \frac{i}{N} \rfloor $$
# 
# $$    (f \ast_W h) (col) = \sum_{cc=0}^{W-1} f(mod(col-cc,W)) h(cc)$$
# 
# $$    (f \ast_{(H,W)} h) (row,col) = \sum_{rr=0}^{H-1} \sum_{cc=0}^{W-1} f(mod(row-rr,H), mod(col-cc,W)) h(rr,cc)$$
# 
# $$    (f \ast_{(Z,H,W)} h) (d,row,col) =  \sum_{dd=0}^{Z-1} \sum_{rr=0}^{H-1} \sum_{cc=0}^{W-1} f(mod(d-dd,Z), mod(row-rr,N), mod(col-cc,W)) h(dd,rr,cc)$$ 
#     

# ## See also
# 
# - [conv](conv.ipynb)  - 2D or 3D linear discrete convolution.
# - [ptrans](ptrans.ipynb)  - Periodic translation.
# - [convteo](../master/convteo.ipynb)  - Illustrate the convolution theorem.

# ## Contributions:
# 
# - Francislei J. Silva (set 2013)
# - Roberto M. Souza (set 2013)
