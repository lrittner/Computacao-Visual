
# coding: utf-8

# # Function mosaic

# ## Synopse
# 
# Create a 2D visualization of a 3D image.
# 
# - **g = mosaic(f,N,s)**
# 
#   - **g**: Image. Mosaic of 2D images.
# 
#   - **f**: Image. 3D image.
#   - **N**: Integer. Number of image columns in mosaic.
#   - **s**: Float. Default: 1.0. Scale factor.

# ## Description
# 
# This function puts the slices of a 3D image side-by-side on a mosaic (2D image). The objective is to provide basic 3D visualization.

# In[8]:

import numpy as np
import scipy.misc

def mosaic(f,N,s=1.0):
    f = np.asarray(f)
    d,h,w = f.shape
    N = int(N)
    nLines = int(np.ceil(float(d)/N))
    nCells = int(nLines*N)
 
    # Add black slices to match the exact number of mosaic cells
    fullf = np.resize(f, (nCells,h,w))
    fullf[d:nCells,:,:] = 0

    Y,X = np.indices((nLines*h,N*w))
    Pts = np.array([
            (np.floor(Y/h)*N + np.floor(X/w)).ravel(),
            np.mod(Y,h).ravel(),
            np.mod(X,w).ravel() ]).astype(int).reshape((3,int(nLines*h),int(N*w)))
    g = fullf[Pts[0],Pts[1],Pts[2]]
    if (s != 1.0):
        #g = scipy.ndimage.interpolation.zoom(g,s,order=5)
        g = scipy.misc.imresize(g,s,interp='bilinear')
    return g


# ## Examples

# In[1]:

testing = (__name__ == "__main__")
if testing:
    get_ipython().system(' jupyter nbconvert --to python mosaic.ipynb')
    import sys
    import os
    import numpy as np
    ea979path = os.path.abspath('../../')
    if ea979path not in sys.path:
        sys.path.append(ea979path)
    import ea979.src as ia


# ### Example 1

# In[4]:

if testing:
    t = np.arange(60)
    t.shape = (5,3,4)

    print('Original 3D image:\n', t, '\n\n')

    for i in range(1,7):
        g = ia.mosaic(t,i)
        print('Mosaic with %d image column(s):\n' % i)
        print(g)
        print()

    for i in range(1,7):
        g = ia.mosaic(t,i,0.8)
        print('Mosaic with %d image column(s):\n' % i)
        print(g)
        print()


# ### Example 2

# In[5]:

if testing:
    d,r,c = np.indices((5,3,4))
    t = ((r + c)%2) >0

    for i in range(1,7):
       g = ia.mosaic(t,i,0.8)
       print('Mosaic with %d image column(s):\n' % i)
       print(g)
       print()


# ## Equation
# 
# Each element of the original 3D image $(x_{0},y_{0},z_{0})$ is mapped to an element on the destination 2D image (mosaic) $(x_{d},y_{d})$ by the equations.
# 
# $$ \begin{matrix}
#     x_{0} &=& x_{d} &mod& w \\
#     y_{0} &=& y_{d} &mod& h \\
#     z_{0} &=& \lfloor \frac{y_{d}}{h} \rfloor N + \lfloor \frac{x_{d}}{w} \rfloor
#     \end{matrix} $$
#     
# were $N$ is the number of image columns in mosaic, $w$ is the original image width and $h$ is the original image height.

# In[ ]:



