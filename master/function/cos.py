
# coding: utf-8

# # Table of Contents
#  <p><div class="lev1 toc-item"><a href="#Function-cos" data-toc-modified-id="Function-cos-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Function cos</a></div><div class="lev2 toc-item"><a href="#Synopse" data-toc-modified-id="Synopse-11"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>Synopse</a></div><div class="lev2 toc-item"><a href="#Description" data-toc-modified-id="Description-12"><span class="toc-item-num">1.2&nbsp;&nbsp;</span>Description</a></div><div class="lev2 toc-item"><a href="#Examples" data-toc-modified-id="Examples-13"><span class="toc-item-num">1.3&nbsp;&nbsp;</span>Examples</a></div><div class="lev3 toc-item"><a href="#Example-1" data-toc-modified-id="Example-1-131"><span class="toc-item-num">1.3.1&nbsp;&nbsp;</span>Example 1</a></div><div class="lev2 toc-item"><a href="#Equation" data-toc-modified-id="Equation-14"><span class="toc-item-num">1.4&nbsp;&nbsp;</span>Equation</a></div><div class="lev2 toc-item"><a href="#See-Also" data-toc-modified-id="See-Also-15"><span class="toc-item-num">1.5&nbsp;&nbsp;</span>See Also</a></div>

# # Function cos
# 
# ## Synopse
# 
# Create a cosine wave image.
# 
# - **f = iacos(s, t, theta, phi)**
# 
#   - **f**: Image. 
# 
# 
#   - **s**: Image. size: [rows cols].
#   - **t**: Image. Period: in pixels.
#   - **theta**: Double. spatial direction of the wave, in radians. 0 is a wave on the horizontal direction.
#   - **phi**: Double. Phase

# In[2]:

import numpy as np

def cos(s, t, theta, phi):
    r, c = np.indices(s)
    tc = t / np.cos(theta)
    tr = t / np.sin(theta)
    f = np.cos(2*np.pi*(r/tr + c/tc) + phi)
    return f


# ## Description
# 
# Generate a cosine wave image of size s with amplitude 1, period T, phase phi and wave direction of theta. The output image is a double array.

# ## Examples

# In[1]:

testing = (__name__ == "__main__")
if testing:
    get_ipython().system(' jupyter nbconvert --to python cos.ipynb')
    import numpy as np
    import sys,os
    ea979path = os.path.abspath('../../')
    if ea979path not in sys.path:
        sys.path.append(ea979path)
    import ea979.src as ia


# ### Example 1

# In[2]:

if testing:

    f = ia.cos([128,256], 100, np.pi/3, 0)
    ia.adshow(ia.normalize(f, [0,255]))


# ## Equation
# 
# $$ \begin{matrix}
#     f(r,c) & = & cos( 2\pi (\frac{1}{T_r}r + \frac{1}{T_c}c) + \phi) \\
#     f(r,c) & = & cos( 2\pi (\frac{v}{H}r + \frac{u}{W}c) + \phi) \\
#     T_r    & = & \frac{T}{sin(\theta)} \\
#     T_c    & = & \frac{T}{cos(\theta)} \\
#     u   & = & \frac{W}{T_c} \\
#     v   & = & \frac{H}{T_r}
# \end{matrix} $$
# 
# - $\theta$ is the direction of the cosine wave.
# - $T$ is the wave period, in number of pixels.
# - $T_r$ and $T_c$ are the period or wave length in the vertical and horizontal directions, respectively, in number of pixels.
# - $H$ and $W$ are the number of image rows and columns, respectively. 
# - $v$ and $u$ are the normalized frequency in the horizontal and vertical directions, respectively, in cycles per image dimension.

# ## See Also
# 
# - `iacosdemo iacosdemo` -- Illustrate discrete cosine wave and its DFT showing its periodic nature.

# In[3]:

if testing:
    print('testing cos')
    print(repr(np.floor(0.5 + 127*(ia.cos([7,10], 3, np.pi/4, 0)+1))) == repr(np.array(
          [[ 254.,  138.,    2.,   93.,  246.,  182.,   18.,   52.,  223.,  219.],
           [ 138.,    2.,   93.,  246.,  182.,   18.,   52.,  223.,  219.,   48.],
           [   2.,   93.,  246.,  182.,   18.,   52.,  223.,  219.,   48.,   21.],
           [  93.,  246.,  182.,   18.,   52.,  223.,  219.,   48.,   21.,  187.],
           [ 246.,  182.,   18.,   52.,  223.,  219.,   48.,   21.,  187.,  244.],
           [ 182.,   18.,   52.,  223.,  219.,   48.,   21.,  187.,  244.,   88.],
           [  18.,   52.,  223.,  219.,   48.,   21.,  187.,  244.,   88.,    3.]])))


# In[ ]:



