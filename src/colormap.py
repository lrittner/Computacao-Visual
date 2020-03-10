
# coding: utf-8

# # Function colormap
# 
# ## Synopse
# 
# Create a colormap table.
# 
# - **ct = colormap(type='gray')**
# 
#   - **ct**: Image. 
# 
#   - **type**: String. Type of the colormap. Options: 'gray', 'hsv', 'hot', 'cool', 'bone','copper', 'pink'.

# In[1]:

def colormap(type='gray'):

    if type == 'gray':
        ct = np.transpose(np.resize(np.arange(256).astype(np.uint8), (3,256)))
    elif type == 'hsv':
        h = np.arange(256)/255.
        s = np.ones(256)
        v = np.ones(256)
        m = np.array(list(map(colorsys.hsv_to_rgb, h, s, v)))
        ct = ia898.src.normalize(np.reshape(m, (256,3)), [0,255]).astype(np.uint8)
    elif type == 'hot':
        n = 256//3 
        n1 = np.arange(1,n+1)/n
        n2 = np.ones(256-n)
        r = np.concatenate((n1, n2), 0).reshape(256,1)
        g = np.concatenate((np.zeros(n), np.arange(1,n+1)/n, np.ones(256-2*n)), 0).reshape(256,1)
        b = np.concatenate((np.zeros(2*n), np.arange(1,256-2*n+1)/(256-2*n)), 0).reshape(256,1)
        ct = ia898.src.normalize(np.concatenate((r,g,b), 1), [0,255]).astype(np.uint8)
    elif type == 'cool':
        r = (np.arange(256)/255.)[:,np.newaxis]
        ct = ia898.src.normalize(np.concatenate((r, 1-r, np.ones((256,1))), 1), [0,255]).astype(np.uint8)
    elif type == 'bone':
        ct = ia898.src.normalize((7. * colormap('gray') + colormap('hot')[:,::-1]) / 8., [0,255]).astype(np.uint8)
    elif type == 'copper':
        cg = colormap('gray')/255.
        fac = np.dot(cg, [[1.25,0,0],[0,0.7812,0],[0,0,0.4975]])
        aux = np.minimum(1, fac)
        ct = ia898.src.normalize(aux).astype(np.uint8)
    elif type == 'pink':
        ct = ia898.src.normalize(np.sqrt((2.*colormap('gray') + colormap('hot')) / 3), [0,255]).astype(np.uint8)
    else:
        ct = np.zeros((256,3))
    return ct


# ## Description
# 
# Create pseudo colormap tables.

# ## Examples

# In[1]:

testing = (__name__ == "__main__")
if testing:
    get_ipython().system(' jupyter nbconvert --to python colormap.ipynb')
    import numpy as np
    import sys,os
    ea979path = os.path.abspath('../../')
    if ea979path not in sys.path:
        sys.path.append(ea979path)
    import ea979.src as ia
    get_ipython().magic('matplotlib inline')
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg


# ### Example 1

# In[3]:

if testing:
    tables = [ 'gray', 'hsv', 'hot', 'cool', 'copper','pink','bone']
    r,f = np.indices((10,256), 'uint8')
    ia.adshow(f, 'gray scale')

    for table in tables:
        cm = ia.colormap(table)
        g = ia.applylut(f, cm)
        g = g.astype('uint8')
        if len(g.shape)==3:
            g = g.transpose(1,2,0)
        ia.adshow(g, table)
        


# ### Example 2
# 
# Plotting the colormap table

# In[4]:

if testing:
    for table in tables:
        Tc = ia.colormap(table)
        plt.plot(Tc[:,0])
        plt.plot(Tc[:,1])
        plt.plot(Tc[:,2])
        plt.title(table)
        plt.show()


# ### Example 3
# 
# With image

# In[5]:

if testing:
    nb = ia.nbshow(3)
    f = mpimg.imread('../data/retina.tif')
    for table in tables:
        Tc = ia.colormap(table)
        g = ia.applylut(f,Tc).astype('uint8')
        if len(g.shape)==3:
            g = g.transpose(1,2,0)
        nb.nbshow(g, table)
    nb.nbshow()


# ## See Also
# 
# - [ia636:applylut](applylut.ipynb) Lookup Table application
# 
# ## References
# 
# - [Wikipedia HSL and HSV](http://en.wikipedia.org/wiki/HSL_and_HSV)

# In[6]:

if testing:
    print('testing gray')
    print(repr(ia.colormap('gray')[0::51]) == repr(np.array(
          [[  0,   0,   0],
           [ 51,  51,  51],
           [102, 102, 102],
           [153, 153, 153],
           [204, 204, 204],
           [255, 255, 255]],np.uint8)))


# In[7]:

if testing:
    print('testing hsv')
    print(repr(ia.colormap('hsv')[0::51]) == repr(np.array(
          [[255,   0,   0],
           [203, 255,   0],
           [  0, 255, 102],
           [  0, 102, 255],
           [204,   0, 255],
           [255,   0,   0]],np.uint8)))


# In[9]:

if testing:
    print('testing hot')
    print(repr(ia.colormap('hot')[0::51]) == repr(np.array(
          [[  3,   0,   0],
           [156,   0,   0],
           [255,  54,   0],
           [255, 207,   0],
           [255, 255, 103],
           [255, 255, 255]],np.uint8)))


# In[10]:

if testing:
    print('testing cool')
    print(repr(ia.colormap('cool')[0::51]) == repr(np.array(
          [[  0, 255, 255],
           [ 51, 204, 255],
           [102, 153, 255],
           [153, 102, 255],
           [204,  50, 255],
           [255,   0, 255]],np.uint8)))


# In[11]:

if testing:
    print('testing bone')
    print(repr(ia.colormap('bone')[0::51]) == repr(np.array(
          [[  0,   0,   0],
           [ 44,  44,  64],
           [ 89,  96, 121],
           [133, 159, 165],
           [191, 210, 210],
           [255, 255, 255]],np.uint8)))


# In[12]:

if testing:
    print('testing copper')
    print(repr(ia.colormap('copper')[0::51]) == repr(np.array(
          [[  0,   0,   0],
           [ 63,  39,  25],
           [127,  79,  50],
           [191, 119,  76],
           [255, 159, 101],
           [255, 199, 126]],np.uint8)))
    print('testing pink')
    print(repr(ia.colormap('pink')[0::51]) == repr(np.array(
          [[ 15,   0,   0],
           [148,  93,  93],
           [197, 148, 131],
           [218, 208, 161],
           [237, 237, 208],
           [255, 255, 255]],'uint8')))


# In[ ]:




# In[ ]:



