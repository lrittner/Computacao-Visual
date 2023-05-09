
# coding: utf-8

# # Function rectangle

# ## Synopse
# Create a binary rectangle image.
# 
# - **g = rectangle(s, r, c) **
# 
#     - **g**: Image.
#     - **s**: Image. [rows cols], output image dimensions.
#     - **r**: Double. [rrows ccols], rectangle image dimensions.
#     - **c**: Image. [row0 col0], center of the rectangle.

# ## Description
# Creates a binary image with dimensions given by s, rectangle dimensions given by r and center given by c. The pixels inside the rectangle are one and outside zero.

# In[1]:

import numpy as np

def rectangle(s, r, c):

    rows,  cols  = s[0], s[1]
    rrows, rcols = r[0], r[1]
    rr0,   cc0   = c[0], c[1]
    rr, cc = np.meshgrid(np.arange(rows), np.arange(cols), indexing='ij')

    min_row, max_row = rr0-rrows//2, rr0+rrows//2
    min_col, max_col = cc0-rcols//2, cc0+rcols//2

    g1 = (min_row <= rr) & (max_row > rr)
    g2 = (min_col <= cc) & (max_col > cc)

    g = g1 & g2
    return g


# ## Examples

# In[2]:

testing = (__name__ == "__main__")
if testing:
    get_ipython().system(' jupyter nbconvert --to python rectangle.ipynb')
    import numpy as np
    import sys,os
    ea979path = os.path.abspath('../../')
    if ea979path not in sys.path:
        sys.path.append(ea979path)
    import ea979.src as ia


# ### Example 1

# In[2]:

if testing:
    F = ia.rectangle([7,9], [3,2], [3,4])
    print(F)


# - **Example 2**

# In[3]:

if testing:
    F = ia.rectangle([200,300], [90,120], [70,120])
    ia.adshow(ia.normalize(F))


# ## Equation
# 
# \begin{equation}
#   g(x,y)=\begin{cases}
#     1, & \text{if } x_\text{min} \leq x < x_\text{max} \text{ and } y_\text{min} \leq y < y_\text{max}.\\
#     0, & \text{otherwise}.
#   \end{cases}
# \end{equation}

# ## Contributions
# 
# Lucas de Vasconcellos Teixeira, 1st semester 2017
