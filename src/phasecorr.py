
# coding: utf-8

# # Function phasecorr

# ## Synopse

# Computes the phase correlation of two images.
# 
# - **g = phasecorr(f,h)**
#     - **OUTPUT**
#         - **g**: Image. Phase correlation map.
#     - **INPUT**
#         - **f**: Image. n-dimensional.
#         - **h**: Image. n-dimensional.

# ## Description

# Computes the phase correlation of two n-dimensional images. Notice that the input images must have
# the same dimension and size. The output is an image with same dimension and size of the input image.
# This output image is a phase correlation map were the point of maximum value corresponds to the
# translation between the input images.
#         

# In[2]:

import numpy as np
def phasecorr(f,h):
    F = np.fft.fftn(f)
    H = np.fft.fftn(h)
    T = F * np.conjugate(H)
    R = T/np.abs(T)
    g = np.fft.ifftn(R)
    return g.real


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
    
    get_ipython().magic('matplotlib inline')
    import matplotlib.image as mpimg


# ### Example 1

# Show that the point of maximum correlation for two equal images is the origin.
#         
#     

# In[4]:

if testing:
    # 2D example
    f1 = mpimg.imread("../data/cameraman.tif")
    noise = np.random.rand(f1.shape[0],f1.shape[1])
    f2 = ia.normalize(ia.ptrans(f1,(-1,50)) + 300 * noise)
    g1 = ia.phasecorr(f1,f2)
    i = np.argmax(g1)
    row,col = np.unravel_index(i,g1.shape)
    v = g1[row,col]
    print(np.array(f1.shape) - np.array((row,col)))


# In[ ]:

if testing:
    print('max at:(%d, %d)' % (row,col))

    ia.adshow(ia.normalize(f1), "input image")
    ia.adshow(ia.normalize(f2), "input image")
    ia.adshow(ia.normalize(g1), "Correlation peak at (%d,%d) with %d" % (row,col,v))


# ### Exemplo 3

# Show how to perform Template Matching using phase correlation.

# In[ ]:

if testing:
    # 2D example
    w1 = f1[27:69,83:147]
    
    h3 = np.zeros_like(f1)
    h3[:w1.shape[0],:w1.shape[1]] = w1
    noise = np.random.rand(h3.shape[0],h3.shape[1])
    h3 = ia.normalize(h3 + 100 * noise)

    h3 = ia.ptrans(h3, - np.array(w1.shape, dtype=int)//2)
    
    g9 = ia.phasecorr(f1,h3)
    
    p3 = np.unravel_index(np.argmax(g9), g9.shape)
    g11 = ia.ptrans(h3,p3)
    
    ia.adshow(ia.normalize(f1), "Original 2D image - Cameraman")
    ia.adshow(ia.normalize(w1), "2D Template")
    ia.adshow(ia.normalize(h3), "2D Template same size as f1")
    ia.adshow(ia.normalize(g9), "Cameraman - Correlation peak: %s"%str(p3))
    ia.adshow(ia.normalize((g11*2.+f1)/3.), "Template translated mixed with original image")


# ## Equation

# We calculate the discrete Fourier transform of the input images $f$ and $h$:
# 
# $$    F = \mathcal{F}(f); $$
# 
# $$    H = \mathcal{F}(h). $$
# 
# Next, the following equation compute $R$
# 
# $$    R = \dfrac{F H^*}{|F H^*|}. $$
#     
# Finally, the result is given by applying the inverse discrete Fourier transform to $R$
# 
# $$    g = \mathcal{F}^{-1}(R). $$
# 
# The displacement (not implemented in this function) can be obtained by:
# 
# $$ (row, col) = arg max\{g\} $$

# ## See also

# - `ia636:iadft iadft` -- Discrete Fourier Transform.
# - `ia636:iaidft iaidft` -- Inverse Discrete Fourier Transform.
# - `ia636:iaptrans iaptrans` -- Periodic translation.
# - `ia636:iamosaic iamosaic` -- Creates a mosaic of images from the input volume (3D).
# - `ia636:iacorrdemo iacorrdemo` -- Illustrate the Template Matching technique.

# ## References

# - E. De Castro and C. Morandi "Registration of Translated and Rotated Images Using Finite Fourier Transforms", IEEE Transactions on pattern analysis and machine intelligence, Sept. 1987.

# ## Contributions

# - André Luis da Costa, 1st semester 2011
