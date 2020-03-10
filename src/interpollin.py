
# coding: utf-8

# # Function iainterpollin
# 
# ## Synopse
# 
# Perform linear interpolation
# 
# - **v = iainterpollin(f, pts)**
#     - **f:** 1D, 2D or 3D image to be interpolated
#     - **pts:** array DxN with the points to interpolate (one in each column)
#     - **v:** array of the interpolated values
#     
# 
# For each cell the following equation needs to be solved:
# 
# 1D: $ v = a + bx $
# 
# 2D: $ v = a + bx + cy + exy $
# 
# 3D: $ v = a + bx + cy + dz + exy + fxz + gyz + hxyz $
# 
# where $x, y$ and $z$ are the fractional part of the coordinate.
#     

# In[1]:

import numpy as np

def interpollin(f, pts):
    # f - one, two or three dimention array
    # pts - array of points to interpolate:
    # throws IndexError if there are indices out of range in pts
    #from iainterpollin import iainterpollin1D, iainterpollin2D, iainterpollin3D
    f = f.astype(float)
    if f.ndim == 1:
        return interpollin1D(f, np.ravel(pts))
    if f.ndim == 2:
        return interpollin2D(f, pts)
    if f.ndim == 3:
        return interpollin3D(f, pts)


# In[2]:

def interpollin1D(f, pts):
    # f - one dimention array
    # pts - array of points to interpolate:
    # throws IndexError if there are indices out of range in pts
    import numpy as np

    # integer indices
    ipts = np.floor(pts).astype(int)

    # fractional indices
    fpts = pts - ipts

    # workaround for the case some index equals the last valid index
    fpts[ipts>=f.shape[0]-1] += 1
    ipts[ipts>=f.shape[0]-1] -= 1

    I = ipts.copy()
    Ix = ipts.copy()+1

    a = f[I]
    b = f[Ix] - a

    return a + b*fpts


# In[3]:

def interpollin2D(f, pts):
    # f - bi-dimentional image
    # pts - array (2xN) of points to interpolate:
    # throws IndexError if there are indices out of range in pts
    # let's consider x the first and y the second dimention
    import numpy as np

    # integer indices
    ipts = np.floor(pts).astype(int)

    # fractional indices
    fpts = pts - ipts

    # workaround for the case some index equals the last valid index in the respective dimension
    fpts[0][ipts[0]>=f.shape[0]-1] += 1
    ipts[0][ipts[0]>=f.shape[0]-1] -= 1
    fpts[1][ipts[1]>=f.shape[1]-1] += 1
    ipts[1][ipts[1]>=f.shape[1]-1] -= 1

    I = ipts.copy()
    Ix = ipts.copy()
    Ix[0] += 1
    Iy = ipts.copy()
    Iy[1] += 1
    Ixy = Ix.copy()
    Ixy[1] += 1

    a = f[I[0], I[1]]
    b = f[Ix[0], Ix[1]] - a
    c = f[Iy[0], Iy[1]] - a
    e = f[Ixy[0], Ixy[1]] - a - b - c

    return a + b*fpts[0] + c*fpts[1] + e*fpts[0]*fpts[1]


# In[4]:

def interpollin3D(ff, pts):
    # ff - tri dimentional image
    # pts - array (3xN) of points to interpolate:
    # throws IndexError if there are indices out of range in pts
    # let's consider x the first dimension, y the second and z the third
    import numpy as np

    # integer indices
    ipts = np.floor(pts).astype(int)

    # fractional indices
    fpts = pts - ipts

    # workaround for the case some index equals the last valid index in the respective dimension
    fpts[0][ipts[0]>=ff.shape[0]-1] += 1
    ipts[0][ipts[0]>=ff.shape[0]-1] -= 1
    fpts[1][ipts[1]>=ff.shape[1]-1] += 1
    ipts[1][ipts[1]>=ff.shape[1]-1] -= 1
    fpts[2][ipts[2]>=ff.shape[2]-1] += 1
    ipts[2][ipts[2]>=ff.shape[2]-1] -= 1

    I = ipts.copy()
    Ix = ipts.copy()
    Ix[0] += 1
    Iy = ipts.copy()
    Iy[1] += 1
    Iz = ipts.copy()
    Iz[2] += 1
    Ixy = Ix.copy()
    Ixy[1] += 1
    Ixz = Ix.copy()
    Ixz[2] += 1
    Iyz = Iy.copy()
    Iyz[2] += 1
    Ixyz = Ixy.copy()
    Ixyz[2] += 1

    a = ff[I[0], I[1], I[2]]
    b = ff[Ix[0], Ix[1], Ix[2]] - a
    c = ff[Iy[0], Iy[1], Iy[2]] - a
    d = ff[Iz[0], Iz[1], Iz[2]] - a
    e = ff[Ixy[0], Ixy[1], Ixy[2]] - a - b - c
    f = ff[Ixz[0], Ixz[1], Ixz[2]] - a - b - d
    g = ff[Iyz[0], Iyz[1], Iyz[2]] - a - c - d
    h = ff[Ixyz[0], Ixyz[1], Ixyz[2]] - a - b - c - d - e - f - g

    return a + b*fpts[0] + c*fpts[1] + d*fpts[2] + e*fpts[0]*fpts[1] +                f*fpts[0]*fpts[2] + g*fpts[1]*fpts[2] + h*fpts[0]*fpts[1]*fpts[2]


# ## Example

# In[1]:

testing = (__name__ == "__main__")
if testing:
    get_ipython().system(' jupyter nbconvert --to python interpollin.ipynb')
    import numpy as np
    import sys,os
    ea979path = os.path.abspath('../../')
    if ea979path not in sys.path:
        sys.path.append(ea979path)
    import ea979.src as ia


# In[2]:

if testing:
    print("1D interpolation")
    Im = np.array([1, 7, 10, 5, 3, 0, -5, 6])
    points = np.array([1.5, 2.1, 2.5, 2.9, 0.1])
    print("Im= ", Im)
    print("points= ", points)
    print("Interpol vaules= ", ia.interpollin(Im, points))
    print("\n")

    print("2D interpolation")
    Im = np.arange(0, 9)
    Im.shape = (3, 3)
    print("Im=\n", Im)
    points = np.array([[0, 0.5, 0,   0.5, 1.5, 2],
                       [0, 0,   0.5, 0.5, 1.5, 2]])
    print("points=\n", points)
    print("Interpol vaules= ", ia.interpollin(Im, points))
    print("\n")

    print("3D interpolation")
    Im = np.arange(0, 27)
    Im.shape = (3, 3, 3)
    print("Im=\n", Im)
    points = np.array([[0, 0.5, 0,   0, 0.5, 0.5, 2],
                       [0, 0,   0.5, 0, 0.5, 0.5, 2],
                       [0, 0,   0,   0.5, 0, 0.5, 2]])
    print("points=\n", points)
    print("Interpol vaules= ", ia.interpollin(Im, points))


# ## See Also
# 
# - `iaffine3` - 3D affine geometric transform
# - `iainterpolclosest` - Interpolate closest

# In[ ]:



