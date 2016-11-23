# -*- coding: utf-8 -*-
from detector.models import Image, Classification
import numpy as np

class LoadData:

    @classmethod
    def find_images(cls,image_url):
        
        lista_classifications = list()

        image = Image.objects.get(url=image_url)

        for i in image.classification.values():
            lista_classifications.append(i['classification'])


        #possiveis imagens (
        # Query de todas as imagens que possuem alguma classificacao igual a imagem upada)
        p_images = Image.objects.filter(
                                classification__classification__in=lista_classifications)

        p_images = list(set(p_images)) # Faz a lista ficar com valores unicos.

        image_list = list()

        lista_classifications = list()

        for i in image.classification.values():
            lista_classifications.append((i['classification'],i['percentage']))

        for image in p_images:
            for value in image.classification.values():
                image_list.append((image.id,value['classification'],value['percentage']))


        lista_mais_provaveis = list()
        similaridade = 0

        for i in image_list:
            for a in lista_classifications:
                if(a[0] == i[1]):
                    distancia = 0
                    distancia = np.abs(i[2]-a[1])
                    lista_mais_provaveis.append((i[0],distancia))



        lista_mais_provaveis = sorted(lista_mais_provaveis,key=lambda similarity:similarity[1])
        
        print lista_mais_provaveis

        distancias = dict()
        #Transforma a lista de tuplas em um dicionario onde 
        # a key eh o id do ImageObject e o value e uma lista das possibilidades
        for key, value in lista_mais_provaveis:
            distancias.setdefault(key,[]).append(value)


        #Faz a soma das possibilidades
        for key, value in distancias.iteritems():
            distancias[key] = sum(value)
            print distancias[key]

        return distancias
