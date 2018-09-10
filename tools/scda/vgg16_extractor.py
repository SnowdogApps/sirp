from keras.applications import vgg16
from keras.models import Model


def get_extractor(layer='block5_conv3'):
    """Returns pretrained InceptionResNetV2 model from bottom
    to chosen layer (block5_conv3 by default).

    Args:
        layer (str): extractor output layer

    Returns:
        keras.Model
    """
    base_model = vgg16.VGG16(include_top=False)
    extractor = Model(inputs=base_model.inputs,
                      outputs=base_model.get_layer(layer).output)
    return extractor


def preprocess_input(*args, **kwargs):
    return vgg16.preprocess_input(*args, **kwargs)
