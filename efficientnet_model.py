import keras
import tensorflow as tf
from keras import backend as K
from keras import layers
from keras import models
from keras.utils.generic_utils import get_custom_objects
from training_metrics import recall_m, precision_m


class Swish(layers.Activation):
    def __init__(self, activation, **kwargs):
        super(Swish, self).__init__(activation, **kwargs)
        self.__name__ = 'swish'


def swish(x):
    """
    Swish function to use in Efficientnet model
    :param x: input
    :return: swish
    """
    return K.sigmoid(x) * x


def focal_loss(y_true, y_pred, gamma=2., alpha=.25):
    """
    Focal loss implementation
    :param y_true: true mask
    :param y_pred: prediction mask
    :param gamma:
    :param alpha:
    :return: focal loss
    """
    pt_1 = tf.where(tf.equal(y_true, 1), y_pred, tf.ones_like(y_pred))
    pt_0 = tf.where(tf.equal(y_true, 0), y_pred, tf.zeros_like(y_pred))
    return -K.sum(alpha * K.pow(1. - pt_1, gamma) * K.log(pt_1))-K.sum((1-alpha) * K.pow( pt_0, gamma) * K.log(1. - pt_0))


def build_efficientnet_model(efficientnet_path, img_size, num_classes=1, loss_name="binary_crossentropy", initial_learning_rate=0.001):
    """
    loads EfficientNet model and add Batch Normalization, Dropout and Dense layers
    :param efficientnet_path: path to efficientNet model
    :param img_size: Image size, for B0 use [224, 224, 3]
    :param num_classes: number of output classes, in our case num_classes=1
    :param loss_name: binary cross-entropy achieves good results, but you can explore other losses as well
    :return: compiled model with the additional layers
    """
    inputs = layers.Input(shape=(img_size, img_size, 3,))

    model = models.load_model(efficientnet_path, custom_objects=get_custom_objects().update({'swish': Swish(swish)}))

    for layer in model.layers[-10:]:
        if not isinstance(layer, layers.BatchNormalization):
            layer.trainable = True

    output = model(inputs)
    print(model.summary())

    x = layers.BatchNormalization()(output)

    top_dropout_rate = 0.2
    x = layers.Dropout(top_dropout_rate, name="top_dropout")(x)
    outputs = layers.Dense(num_classes, activation="sigmoid", name="pred")(x)

    model = keras.Model(inputs, outputs, name="EfficientNet")

    if loss_name == 'binary_crossentropy':
        loss = loss_name
    elif loss_name is 'focal':
        loss = focal_loss

    model.compile(
        optimizer=keras.optimizers.Adam(initial_learning_rate), loss=loss, metrics=['binary_accuracy', recall_m, precision_m]
    )
    return model
