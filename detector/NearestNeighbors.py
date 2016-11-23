from models import Image, Classification
import numpy as np

class LoadData:

    @class_method
    def load_queryset(image_object):
        
        lista_classifications = list()

        for i in image_object.classification.values():
            lista_classifications.append(i['classification'])


        #possiveis imagens (
        # Query de todas as imagens que possuem alguma classificacao igual a imagem upada)
        p_images = Image.objects.filter(
                                classification__classification__in=lista_classifications)

        p_images = list(set(p_images)) # Faz a lista ficar com valores unicos.

        image_list = list()

        lista_classifications = list()

        for i in image_object.classification.values():
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


        distancias = dict()

        #Transforma a lista de tuplas em um dicionario onde 
        # a key e o id do ImageObject e o value é uma lista das possibilidades
        for key, value in lista_mais_provaveis:
            distancias.setdefault(key,[]).append(value)


        #Faz a soma das possibilidades
        for key, value in distancias.iteritems():
            distancias[key] = sum(value)

        





class NearestNeighbors:

    def __init__(self, K=10, Xtr=[], images_path='Photos/', img_files=[], labels=np.empty(0)):
        # Setting defaults
        self.K = K
        self.Xtr = Xtr
        self.images_path = images_path
        self.img_files = img_files
        self.labels = labels

    def setXtr(self, Xtr):
        """ X is N x D where each row is an example."""
        # the nearest neighbor classifier simply remembers all the training data
        self.Xtr = Xtr
        
    def setK(self, K):
        """ K is the number of samples to be retrieved for each query."""
        self.K = K

    def setImagesPath(self,images_path):
        self.images_path = images_path
        
    def setFilesList(self,img_files):
        self.img_files = img_files

    def setLabels(self,labels):
        self.labels = labels
        
    def predict(self, x):
        """ x is a test (query) sample vector of 1 x D dimensions """
    
        # Compare x with the training (dataset) vectors
        # using the L1 distance (sum of absolute value differences)

        # p = 1.
        # distances = np.power(np.sum(np.power(np.abs(X-x),p), axis = 1), 1./p)
        distances = np.sum(np.abs(self.Xtr-x), axis = 1)
        # distances = 1-np.dot(X,x)
    
        # plt.figure(figsize=(15, 3))
        # plt.plot(distances)
        # print np.argsort(distances)
        return np.argsort(distances) # returns an array of indices of of the samples, sorted by how similar they are to x.

    def retrieve(self, x):
        # The next 3 lines are for debugging purposes:
        plt.figure(figsize=(5, 1))
        plt.plot(x)
        plt.title('Query vector')

        nearest_neighbours = self.predict(x)

        for n in range(self.K):
            idx = nearest_neighbours[n]
        
            # predictions = zip(self.Xtr[idx][top_inds], labels[top_inds]) # showing only labels (skipping the index)
            # for p in predictions:
            #     print p
            
            ## 
            # In the block below, instead of just showing the image in Jupyter notebook,
            # you can create a website showing results.
            image =  misc.imread(os.path.join(self.images_path, self.img_files[idx]))
            plt.figure()
            plt.imshow(image)
            plt.axis('off')
            if self.labels.shape[0]==0:
                plt.title('im. idx=%d' % idx)
            else: # Show top label in the title, if possible:
                top_inds = self.Xtr[idx].argsort()[::-1][:5]
                plt.title('%s   im. idx=%d' % (labels[top_inds[0]][10:], idx))
                
            # The next 3 lines are for debugging purposes:
            plt.figure(figsize=(5, 1))
            plt.plot(self.Xtr[idx])       
            plt.title('Vector of the element ranked %d' % n)