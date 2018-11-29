from keras.models import Sequential, Model
from keras.layers import Dense, Embedding, Input, Flatten
from keras.optimizers import Adam

class TBP_AS_model():
    def __init__(self, n_features, n_label):

        model = Sequential()
        model.add(Embedding(n_features, 128, input_shape=(n_features,)))
        model.add(Flatten())
        model.add(Dense(128))
        model.add(Dense(128))
        model.add(Dense(64))
        model.add(Dense(64))

        features = Input(shape=(n_features,))
        output = model(features)
        
        transition = Dense(3, activation="sigmoid")(output)
        label = Dense(n_label, activation="softmax")(output)
        
        self.classifier =  Model(features, [transition, label])
        
        optimizer = Adam(0.0002, 0.5)
        losses = ['binary_crossentropy', 'sparse_categorical_crossentropy']
        self.classifier.compile(loss=losses,
                    optimizer=optimizer,
                    metrics=['accuracy'])

        self.classifier.summary()
