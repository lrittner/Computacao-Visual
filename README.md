# Computação Visual
Material utilizado no curso EA979 - Intr. Computação Gráfica e Processamento de Imagem.
Os principais tópicos do curso são introduzidos na forma de tutoriais usando o Jupyter Notebook, com exemplos práticos em python. 


## Dependência:
    - numpy
    - matplotlib
    - jupyter and jupyter extentions

## Conteúdo do curso

[Introdução ao Processamento de Imagens (overview)](tutoriais/01_Processamento_Imagens.ipynb)
### 1. Introdução às Imagens digitais

1. [Introdução ao NumPy](tutoriais/02_Aprendendo_Numpy.ipynb) 
2. [Manipulando imagens: abrir, salvar, visualizar, criar](tutoriais/03_Lendo_e_Visualizando_Imagens.ipynb)
3. [Geração de imagens sintéticas](tutoriais/04_Gerando_imagens_sinteticas.ipynb)

### 2. Transformações radiométricas (ponto-a-ponto)

1. [Histograma da Imagem](tutoriais/05_Histograma_da_imagem.ipynb)
2. [Transformações em cores](tutoriais/06_Histograma_de_Imagens_Coloridas.ipynb)

### Transformações espaciais (vizinhança)

1. [Filtragem no domínio espacial](tutoriais/07_Filtragem_no_dominio_espacial.ipynb)

### Transformações no domínio da frequência - Transformada de Fourier

1. [Geração de ondas senoidais 1D e 2D](tutoriais/08_Ondas_senoidais.ipynb)
2. [Translação periódica](tutoriais/09_Translacao_periodica.ipynb)
3. [Propriedades da DFT](tutoriais/10_A_transformada_discreta_de_Fourier_DFT.ipynb)
4. [Teorema da Convolução](tutoriais/11_Teorema_da_Convolucao.ipynb)
5. [Filtros em frequência](tutoriais/12_Filtros_em_frequencia.ipynb)

### Segmentação

1. [Segmentação por Otsu](tutoriais/14_Segmentacao_por_Otsu.ipynb)
2. [Exemplo de segmentação por Watershed](tutoriais/15_Exemplo_de_Segmentacao_por_Watershed.ipynb)
3. [Comparando Otsu e Watershed](tutoriais/16_Comparando_Otsu_e_Watershed.ipynb)


## Lessons
- [chess](master/chess.ipynb) - Illustrate the many ways to create an image of a chess like template
- [gengaussian](master/gengaussian.ipynb) - Illustrate the generation of d-dimensional Gaussian image
- [corrdemo](master/corrdemo.ipynb) - Illustrate the Template Matching technique
- [dftscaleproperty](master/dftscaleproperty.ipynb) - Illustrate the scale property of the Discrete Fourier Transform.
- [magnify](master/magnify.ipynb) - Illustrate the interpolation of magnified images

## Geometric Manipulations
- [affine](src/affine.ipynb) - Affine transform. Supports 3D but no interpolation.
- [polar](src/polar.ipynb) - Cartesian to polar coordinate transformation.
- [ptrans](src/ptrans.ipynb) - Periodic translation.

## Image Filtering
- [conv](src/conv.ipynb) - 2D or 3D convolution.
- [pconv](src/pconv.ipynb) - 2D or 3D periodic convolution (kernel origin at center of kernel).

## Image Information and Manipulation
- [meshgrid](src/meshgrid.ipynb) - Create two 2-D matrices of indexes.

## Image Transformation
- [hadamard](src/hadamard.ipynb) - Hadamard Transform.
- [hadamardmatrix](src/hadamardmatrix.ipynb) - Kernel matrix for the Hadamard Transform.
- [ihadamard](src/ihadamard.ipynb) - Inverse Hadamard Transform.
- [pca](src/pca.ipynb) - Principal Component Analysis

## Measurements
- histogram - Image histogram.

## Image Creation
- [ellipse](src/ellipse.ipynb) - Generate a 2D ellipse, rectangle or diamond image.
- [log](src/log.ipynb) - Laplacian of Gaussian image.
- [comb](src/comb.ipynb) - Create a grid of impulses image.

## Image Matching
- [phaseorr](src/phasecorr.ipynb) - Phase correlation
