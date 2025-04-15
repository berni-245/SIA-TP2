# TP2 SIA - Algoritmos Genéticos

## Introducción

Trabajo práctico para la materia de Sistemas de Inteligencia Artificial en el ITBA. Se buscó implementar un generador de imágenes utilizando algoritmos genéticos. 
Se implementaron los métodos de selección de padres: **Elite**, **Ruleta**, **Universal**, **Boltzmann**, **Ranking**, **Torneo Estatocástico**, **Torneo Probabilístico**.
Para la cruza se implementó el método de **cruza en dos puntos** y **cruza uniforme**.
Para la mutación se implementó **mutación uniforme** y **mutación completa**.
Para los saltos generacionales se implementó **salto generacional tradicional** y **salto generacional sesgo joven**.

Para el **fitness** se implementó dos opciones:
- **fitness euclideano**, la diferencia euclideana entre dos imágenes con píxeles RGBA.
- **fitness delta_D**, aplica una diferencia perceptualmente más acorde al ojo humana con píxeles LAB.

Este fue el [Enunciado](docs/Enunciado%20TP2.pdf)

### Requisitos

- Python3 (La aplicación se probó en la versión de Python 3.11.*)
- pip3
- [pipenv](https://pypi.org/project/pipenv)

### Instalación

En caso de no tener python, descargarlo desde la [página oficial](https://www.python.org/downloads/release/python-3119/)

Utilizando pip (o pip3 en mac/linux) instalar la dependencia de **pipenv**:

```sh
pip install pipenv
```

Parado en la carpeta del proyecto ejecutar:

```sh
pipenv install
```

para instalar las dependencias necesarias en el ambiente virtual.

## Configuración
Se puede cambiar la configuración con la que se corre el algoritmo desde el [`config.json`](configs/config.json).
Las opciones presentes son:
- `selection_algorithm`: elite / roulette / universal / boltzmann / ranking / deterministic_tournament / probabilistic_tournament
- `crossover_algorith`: two_point / uniform
- `mutation_algorithm`: uniform / complete
- `gen_jump_algorithm`: traditional / young_bias
- `population_amount`: La población en cada generación, es un número **entero**
- `generated_child_amount`: La cantidad de hijos en cada generación, es un número **entero**
- `max_gen_count`: La cantidad máxima de generaciones en el algoritmo, es un número **entero**
- `min_fitness_goal`: La probabilidad mínina de fitness aceptable, es un número **real** entre [0, 1]
- `use_delta_D`: Un valor **booleano** para decidir que fitness usar, **true** para *delta_D* y **false** para *euclidean*

## Ejecución

Para correr el algoritmo genético se utiliza el siguiente comando:

```sh
pipenv run python main.py -i <image> -s <shape_count>
```

Donde **\<image>** es la imagen a recrear y **\<shape_count>** la cantidad de figuras a utilizar.

Se guardará la imagen generada en la carpeta [`generated`](generated).

Para abrir el Google Colab donde se realizaron las pruebas ir al siguiente [link](https://colab.research.google.com/drive/1o7iFwWaf3erb6Umz-UKPTcTTTLl2phjj?usp=sharing).