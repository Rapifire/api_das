# -*- coding: utf-8 -*-
from detector.models import Image, Classification
import numpy as np
import scipy

class LoadData():

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




        print "--------TIRA TEIMA--------------"
        print image_list
        print len(image_list)
        print "--------------------------------"
        image_list = list(set(image_list))
        print "--------TIRA TEIMA2--------------"
        print image_list
        print len(image_list)
        print "--------------------------------"
        print "--------TIRA TEIMA3 - lista_classifications--------------"
        print lista_classifications
        print len(image_list)
        print "--------------------------------"

        # print p_images

        lista_mais_provaveis = list()
        similaridade = 0

        for i in image_list:
            for a in lista_classifications:
                if(a[0] == i[1]):
                    distancia = 0
                    # distancia = np.abs(i[2]-a[1])
                    # distancia = scipy.spatial.distance.euclidean(i[2],a[1])
                    distancia = np.linalg.norm(i[2]-a[1])
                    lista_mais_provaveis.append((i[0],distancia))


        distancias = dict()
        #Transforma a lista de tuplas em um dicionario onde 
        # a key e o id do ImageObject e o value e uma lista das possibilidades
        for key, value in lista_mais_provaveis:
            distancias.setdefault(key,[]).append(value)


        #Faz a soma das possibilidades
        for key, value in distancias.iteritems():
            distancias[key] = sum(value)


        # print "----- list classification ----------"
        # print lista_classifications

        print "------Distancias------"
        print sorted(distancias.items(), key=lambda value:value[1])
        return distancias
