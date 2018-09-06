from keras.applications import inception_resnet_v2
from keras.models import Model


def get_extractor(layer='conv_7b'):
    """Returns pretrained InceptionResNetV2 model from bottom
    to choosen layer (conv_7b by default).
    
    Returns:
        keras.Model
    """
    base_model = inception_resnet_v2.InceptionResNetV2(include_top=False)
    extractor = Model(inputs=base_model.inputs,
                      outputs=base_model.get_layer(layer).output)
    return extractor


def preprocess_input(*args, **kwargs):
    return inception_resnet_v2.preprocess_input(*args, **kwargs)