
# coding: utf-8

# # Function normalize
# 
# ## Synopse
# 
# Normalize the pixels values between the specified range.
# 
# - **g = normalize(f, range)**
# 
#   - **g**: Output: ndmage, same type as f. If range==[0,255], dtype is set to 'uint8'
#   - **f**: Input: ndimage.
#   - **range**: Input: vector with two elements, minimum and maximum values in the output image, respectively.
# 
# ## Description
# 
# Normalize the input image f. The minimum value of f is assigned to the minimum desired value and the 
# maximum value of f, to the maximum desired value. The minimum and maximum desired values are given by the 
# parameter range. The data type of the normalized image is the same data type of input image, unless the
# range is [0,255], in which case the dtype is set to 'uint8'.
# 
# 

# In[1]:

import numpy as np

def normalize(f, range=[0,255]):

    f = np.asarray(f)
    range = np.asarray(range)
    if f.dtype.char in ['D', 'F']:
        raise Exception('error: cannot normalize complex data')
    faux = np.ravel(f).astype(float)
    minimum = faux.min()
    maximum = faux.max()
    lower = range[0]
    upper = range[1]
    if upper == lower:
        g = np.ones(f.shape) * maximum
    if minimum == maximum:
        g = np.ones(f.shape) * (upper + lower) / 2.
    else:
        g = (faux-minimum)*(upper-lower) / (maximum-minimum) + lower
    g = g.reshape(f.shape)

    if f.dtype == np.uint8:
        if upper > 255: 
            raise Exception('normalize: warning, upper valuer larger than 255. Cannot fit in uint8 image')
    if lower == 0 and upper == 255:
        g = g.astype(np.uint8)
    else:
        g = g.astype(f.dtype) # set data type of result the same as the input image
    return g


# ## Examples

# In[1]:

testing = (__name__ == "__main__")

if testing:
    import numpy as np
    import sys,os
    ea979path = os.path.abspath('../../')
    if ea979path not in sys.path:
        sys.path.append(ea979path)
    import ea979.src as ia


# ### Example 1

# In[2]:

if testing:
    f = np.array([100., 500., 1000.])
    g1 = ia.normalize(f, [0,255])
    print(g1)


# In[3]:

if testing:
    g2 = ia.normalize(f, [-1,1])
    print(g2)


# In[4]:

if testing:
    g3 = ia.normalize(f, [0,1])
    print(g3)


# In[5]:

if testing:
    #
    f = np.array([-100., 0., 100.])
    g4 = ia.normalize(f, [0,255])
    print(g4)
    g5 = ia.normalize(f, [-1,1])
    print(g5)
    g6 = ia.normalize(f, [-0.5,0.5])
    print(g6)
    #
    f = np.arange(10).astype('uint8')
    g7 = ia.normalize(f)
    print(g7)
    #
    f = np.array([1,1,1])
    g8 = ia.normalize(f)
    print(g8)


# ## Equation
# 
# $$    g = f|_{gmin}^{gmax}$$  
# $$    g(p) = \frac{g_{max} - g_{min}}{f_{max}-f_{min}} (f(p) - f_{min}) + g_{min}  $$

# ## See Also
# 
# * `iaimginfo` - Print image size and pixel data type information
# * `iait` - Illustrate the contrast transform function
# 
# ## References
# 
# * [Wikipedia - Normalization](http://en.wikipedia.org/wiki/Normalization_(image_processing))
# 
# ## Contributions
# 
# - Marcos Fernandes, course IA368S, 1st semester 2013

# In[7]:

if testing:
    print('testing normalize')
    print(repr(ia.normalize(np.array([-100., 0., 100.]), [0,255])) == repr(np.array([   0. ,  127.5,  255. ])))


# In[ ]:



