import numpy as np

from keras.models import Sequential, Model
from keras.layers import Dense, Embedding, Flatten, Input, Dropout, BatchNormalization, Input, Concatenate
from keras.optimizers import Adam

class TBP_AS_model():
    def __init__(self, vocs):
        n_features = len(vocs)

        input_features = [Input(shape=(1,)) for _ in range(n_features)]
        features = [Embedding(len(vocs[i]), min(32, len(vocs[i])))(f) for i,f in enumerate(input_features)]
        features = [Flatten()(f) for i,f in enumerate(features)]
        features = Concatenate()(features)

        input_shape = np.sum([min(32, len(vocs[i])) for i,f in enumerate(input_features)])

        model = Sequential()
        model.add(Dense(input_shape, input_shape=(input_shape,), activation='relu'))
        model.add(Dense(256, activation='relu'))
        model.add(BatchNormalization())
        model.add(Dropout(0.2))
        model.add(Dense(128, activation='relu'))
        model.add(BatchNormalization())
        model.add(Dropout(0.2))
        model.add(Dense(64, activation='relu'))
        model.add(BatchNormalization())
        model.add(Dropout(0.2))
        model.add(Dense(32, activation='relu'))
        model.add(BatchNormalization())
        model.add(Dropout(0.2))
        model.add(Dense(32, activation='relu'))
        model.add(BatchNormalization())
        model.add(Dropout(0.2))
        model.add(Dense(16, activation='relu'))
        model.add(BatchNormalization())
        model.add(Dropout(0.2))
        model.add(Dense(8, activation='relu'))
        model.add(BatchNormalization())

        output = model(features)
        
        transition = Dense(3, activation="tanh")(output)

        classifier =  Model(input_features, transition)

        losses = ['categorical_crossentropy']
        classifier.compile(loss=losses,
                    optimizer='adam',
                    metrics=['accuracy'])

        classifier.summary()
        self.classifier = classifier
