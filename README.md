# Computação Visual
Material utilizado no curso EA979 - Intr. Computação Gráfica e Processamento de Imagem.
Os principais tópicos do curso são introduzidos na forma de tutoriais usando o Jupyter Notebook, com exemplos práticos em python. 


## Dependência:
    - numpy
    - matplotlib
    - jupyter and jupyter extentions

## Introdução ao Processamento de Imagens

1. [Overview](tutoriais/01_Processamento_Imagens.ipynb)

### Introdução às Imagens digitais
    
1. [Introdução ao NumPy](tutoriais/02_Aprendendo_Numpy.ipynb) 
2. [Manipulando imagens: abrir, salvar, visualizar, criar](tutoriais/03_Lendo_e_Visualizando_Imagens.ipynb)
3. [Geração de imagens sintéticas](tutoriais/04_Gerando_imagens_sinteticas.ipynb)

### Transformações radiométricas (ponto-a-ponto)

1. [Histograma da Imagem](tutoriais/05_Histograma_da_imagem.ipynb)
2. [Transformação de Intensidade](tutoriais/tutorial_ti_2.ipynb)
3. [Tutorial sobre equalização de histograma](tutoriais/tutorial_hist_eq_2.ipynb)
4. [Tutorial equalização de histograma por montagem de mosaico](tutoriais/tutorial_pehist_1.ipynb)
5. [Transformações em cores](tutoriais/06_Histograma_de_Imagens_Coloridas.ipynb)

### Transformações espaciais (vizinhança)

1. [Filtragem no domínio espacial](tutoriais/07_Filtragem_no_dominio_espacial.ipynb)
2. [Convolução como média ponderada de translações da imagem](tutoriais/tutorial_conv_3.ipynb)

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

## Introdução ao Computação Gráfica

### Introdução ao OpenGL

1. [Primeiro programa OpenGL](tutoriais/17_Primeiro_programa_OpenGL.ipynb)
2. [Configurando uma cor única para todos os vértices](tutoriais/18_Configurando_uma_cor_unica_para_todos_os_vertices.ipynb)
3. [Renderizando mais de um objeto](tutoriais/19_Renderizando_mais_de_um_objeto.ipynb)
4. [Animando as cores dos triângulos](tutoriais/20_Animando_as_cores_dos_triangulos.ipynb)
5. [Animando os vértice do triângulo](tutoriais/21_Animando_os_vertice_do_triangulo.ipynb)
6. [Ordem de renderização e teste de profundidade](tutoriais/22_Ordem_de_renderizacao_e_teste_de_profundidade.ipynb)
7. [Transparência](tutoriais/23_Transparencia.ipynb)
8. [Eventos de teclado](tutoriais/24_Eventos_do_teclado.ipynb)
9. [Descrevendo um modelo](tutoriais/25_Formas_de_especificar_um_modelo.ipynb)
10. [Esfera com wireframe (culling e teste de profundidade ativados)](tutoriais/26_Esfera_com_wireframe_culling_depth.ipynb)
11. [Transformações de modelo](tutoriais/27_Quadrado_com_transformacoes.ipynb)
12. [Carregando modelos de arquivos *.OBJ](tutoriais/28_Carregando_modelos_de_arquivos_OBJ.ipynb)
13. [Transformação de visão](tutoriais/29_Transformacao_visao.ipynb)
14. [Transformação de projeção ortogonal](tutoriais/30_Transformacao_projecao_ortogonal.ipynb)
15. [Transformação de projeção perspectiva](tutoriais/31_Transformacao_projecao_perspectiva.ipynb)
16. [Renderização com diferentes shader programs](tutoriais/32_Esferas_com_diferentes_shader_programs.ipynb)
17. [Terreno com esferas e fonte de luz pontual](tutoriais/33_Terreno_com_esferas_iluminacao_fonte_de_luz_pontual.ipynb)
18. [Terreno com esferas e fonte de luz direcional](tutoriais/34_Terreno_com_esferas_iluminacao_fonte_de_luz_direcional.ipynb)
19. [Terreno com esferas e fonte de luz spotlight](tutoriais/35_Terreno_com_esferas_iluminacao_fonte_de_luz_spotlight.ipynb)
20. [Terreno com esferas e multiplas fontes de luz](tutoriais/36_Terreno_com_esferas_iluminacao_multiplas_fontes_de_luz.ipynb)
21. [Renderizando uma textura por completo](tutoriais/37_Renderizando_uma_textura_por_completo.ipynb)
22. [Renderizando parte de uma textura](tutoriais/38_Renderizando_parte_de_uma_textura.ipynb)
23. [Renderizando sprites animados](tutoriais/39_Renderizando_sprites_animados.ipynb)
24. [Objetos com texturas](tutoriais/40_Objetos_com_texturas.ipynb)
25. [Objetos com texturas e height maps](tutoriais/41_Objetos_com_texturas_e_height_maps.ipynb)
26. [Usando iluminação e textura em modelos carregados de arquivos OBJ](tutoriais/42_Usando_iluminacao_e_textura_em_modelos_carregados_de_arquivos_OBJ.ipynb)
27. [Sistema_solar - final](tutoriais/43_Sistema_solar_final.ipynb)


# Tutoriais básicos sobre Jupyter, Python, NumPy, Matplotlib, Proc. Imagens

Uma série de pequenos tutoriais básicos do Python e principalmente do NumPy, com aplicação à processamento de imagens.

## Python

- [Python I - Tipos de variáveis](tutoriais/tutorial_python_1_1.ipynb)
- [Python III - Declaração de funções](tutoriais/tutorial_python_1_3.ipynb)

## NumPy

- [Chessboard](master/function/chess.ipynb) - Motivação sobre programação matricial NumPy versus programação com laço explícito
- [Rampa_solucoes](master/misc/Rampa_solucoes.ipynb) 
- [one_hot](master/function/one_hot.ipynb) - Codificação one-hot, duas soluções
- [NumPy - Introdução ao ndarray](tutoriais/tutorial_numpy_1_1.ipynb)
- [Matplotlib](tutoriais/tutorial_matplotlib.ipynb)    
- [NumPy - Formatando array para impressão](tutoriais/tutorial_numpy_1_11.ipynb) 
- [NumPy - Fatiamento array unidimensional](tutoriais/tutorial_numpy_1_2.ipynb)
- [NumPy - Fatiamento em duas dimensões](tutoriais/tutorial_numpy_1_3.ipynb)
- [NumPy - Cópia Rasa e Profunda](tutoriais/tutorial_numpy_1_4.ipynb)
- [NumPy - Array Strides](master/misc/Array-strides.ipynb)
- [NumPy - Redução de eixo](tutoriais/tutorial_numpy_1_5a.ipynb)

- [NumPy - Uso do tile](tutoriais/tutorial_numpy_1_8.ipynb)
- [NumPy - Uso do resize](tutoriais/tutorial_numpy_1_9.ipynb)
- [NumPy - Uso do clip](tutoriais/tutorial_numpy_1_10.ipynb) 

## Revisão - Cálculo, Álgebra

- [Revisão de Números Complexos](master/misc/Revisao_NumerosComplexos.ipynb )

## Processamento de Imagens

- [Imagens - Representação, Leitura e Visualização](tutoriais/tutorial_img_ds.ipynb) 
- [Proc Imagens com Fatiamento](tutoriais/tutorial_1_imagens.ipynb)     
- [NumPy - Indices e meshgrid para gerar imagens sintéticas](tutoriais/tutorial_numpy_1_7.ipynb)
- [Histograma e Estatística](tutoriais/tutorial_hist__stat_2.ipynb) 
- [Transformação de Intensidade](tutoriais/tutorial_ti_2.ipynb)
- [Equalização de histograma](tutoriais/tutorial_hist_eq_2.ipynb)
- [Equalização por ordenação dos pixels](tutoriais/tutorial_pehist_1.ipynb)
- [Especificação de histograma por ordenação dos pixels](tutoriais/tutorial_pehist_2.ipynb)
- [Ajuste interativo de contraste](tutoriais/tutorial_contraste_iterativo_2.ipynb)
- [Convolução](tutoriais/tutorial_conv_3.ipynb)
- [Propriedades da convolução](tutoriais/tutorial_convprop_3.ipynb)

- Propriedades da DFT
- [Propriedade da escala (expansão) da DFT](master/function/dftscaleproperty.ipynb)
- [Interpolação na expansão (análise no domínio da frequência](master/function/magnify.ipynb)
- [Transforma Discreta de Wavelets](master/function/wavelets.ipynb)

## Links úteis

- [Jupyter Notebook - documentação](http://jupyter-notebook.readthedocs.io/en/latest/notebook.html)
- [Jupyter notebook - tips and tricks](https://www.dataquest.io/blog/jupyter-notebook-tips-tricks-shortcuts/)
