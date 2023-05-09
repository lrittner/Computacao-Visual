
# coding: utf-8

# # Function circle
# 
# ## Synopse
# 
# This function creates a binary circle image.
# 
# - **g = circle(s, r, c)**
# 
#     - **g**:output: circle image.
#     - **s**:input: Image. [rows cols], output image dimensions.
#     - **r**:input: Double. radius.
#     - **c**:input: Image. [row0 col0], center of the circle.
#     

# In[18]:

import numpy as np
def circle(s, r, c):
    
    rows, cols = s[0], s[1]
    rr0,  cc0  = c[0], c[1]
    rr, cc = np.meshgrid(range(rows), range(cols), indexing='ij')
    g = (rr - rr0)**2 + (cc - cc0)**2 <= r**2
    return g


# ## Description
# 
# Creates a binary image with dimensions given by s, radius given by r and center given by c. The pixels inside the circle are one and outside zero.

# ## Equation
# 
# $$ g(x,y) = (x-x_c)^2 + (y-y_c)^2 \leq r^2 $$

# ## Examples

# In[1]:

testing = (__name__ == "__main__")
if testing:
    get_ipython().system(' jupyter nbconvert --to python circle.ipynb')
    import numpy as np
    import sys,os
    ea979path = os.path.abspath('../../')
    if ea979path not in sys.path:
        sys.path.append(ea979path)
    import ea979.src as ia


# ## Showing a numerical example

# In[2]:

if testing:
    F = ia.circle([5,7], 2, [2,3])
    print (F.astype(np.uint8))


# ## Printing the generated image

# In[4]:

if testing:
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg
    get_ipython().magic('matplotlib inline')
    f = ia.circle([200,300], 90, [100,150])
    ia.adshow(f,'circle')


# ## Contributions
# 
# Luis Antonio Prado, 1st semester 2017
