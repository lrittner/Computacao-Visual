
# coding: utf-8

# # Function dftshift
# 
# ## Synopse
# 
# Shifts zero-frequency component to center of spectrum.
# 
# - **g = iafftshift(f)**
#     - **OUTPUT**
#         - **g**: Image.
#     - **INPUT**
#         - **f**: Image. n-dimensional.
# 
# ## Description
# 
# The origin (0,0) of the DFT is normally at top-left corner of the image. For visualization
# purposes, it is common to periodically translate the origin to the image center. This is
# particularlly interesting because of the complex conjugate simmetry of the DFT of a real function.
# Note that as the image can have even or odd sizes, to translate back the DFT from the center to
# the corner, there is another correspondent function: `idftshift`.

# In[1]:

import numpy as np
import sys
sys.path.append( '../master' )
from function import ptrans

def dftshift(f):
    return ptrans.ptrans(f, np.array(f.shape)//2)


# ## Examples

# In[1]:

testing = (__name__ == "__main__")

if testing:
    get_ipython().system(' jupyter nbconvert --to python dftshift.ipynb')
    import numpy as np
    import sys,os
    import matplotlib.image as mpimg
    ea979path = os.path.abspath('../../')
    if ea979path not in sys.path:
        sys.path.append(ea979path)
    import ea979.src as ia


# ### Example 1

# In[6]:

if testing:
    
    f = ia.circle([120,150],6,[60,75])
    F = ia.dft(f)
    Fs = ia.dftshift(F)
    ia.adshow(ia.dftview(F))
    ia.adshow(ia.dftview(Fs))


# In[7]:

if testing:
    
    F = np.array([[10+6j,20+5j,30+4j],
                  [40+3j,50+2j,60+1j]])
    Fs = ia.dftshift(F)
    print('Fs=\n',Fs)


# ## Equation
# 
# $$ \begin{matrix}
#     HS &=& H_{xo,yo} \\xo     &=& \lfloor W/2 \rfloor \\yo     &=& \lfloor H/2 \rfloor
# \end{matrix} $$

# ## See Also
# 
# - `iaptrans iaptrans` - Periodic translation
# - `iaifftshift iaifftshift` - Undoes the translation of iafftshift

# In[8]:

if testing:
    print('testing dftshift')
    print(repr(ia.dftshift(np.array([[10+6j,20+5j,30+4j],
                                     [40+3j,50+2j,60+1j]]))) == 
          repr(np.array([[ 60.+1.j,  40.+3.j,  50.+2.j],
                         [ 30.+4.j,  10.+6.j,  20.+5.j]])))


# ## Contributions
# 
# - André Luis da Costa, 1st semester 2011

# In[ ]:



