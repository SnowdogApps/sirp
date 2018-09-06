from keras.applications import inception_v3
from keras.models import Model


def get_extractor(layer='mixed10'):
    """Returns pretrained InceptionResNetV2 model from bottom
    to conv_7b layer.
    
    Returns:
        keras.Model
    """
    base_model = inception_v3.InceptionV3(include_top=False)
    extractor = Model(inputs=base_model.inputs,
                      outputs=base_model.get_layer(layer).output)
    return extractor


def preprocess_input(*args, **kwargs):
    return inception_v3.preprocess_input(*args, **kwargs)