import copy

from keras.preprocessing import image
import numpy as np
from sklearn.preprocessing import normalize
from skimage.transform import resize
from skimage.measure import label


def load_img(img_path, size=None):
    """Loads image and optionally resize it.
    
    Args:
        img_path (str): path to image
        resize (int): target image size
    
    Returns:
        np.ndarray
    """
    if size:
        img = image.load_img(img_path, target_size=(size, size))
    else:
        img = image.load_img(img_path)   
    img = image.img_to_array(img)
    return img


def extract_features(extractor, img, preprocess):
    """Preprocess image and extracts activations
    
    Args:
        extractor (Model): extracting features model
        img (np.ndarray): image
    
    Returns:
        np.ndarray
    """
    img = preprocess(copy.copy(img))
    img = np.expand_dims(img, axis=0)
    activations = extractor.predict(img)[0,:,:,:]
    return activations


def aggregate(activations):
    """Returns aggregation map and its threshold.
    
    Adds up the obtained activation tensor through
    the depth direction and calculates mean of all
    values of aggregation map as threshold to decide
    which positions localize objects.
    
    Args:
        activations (np.ndarray): activations
    
    Returns:
        np.ndarray, float
    """
    aggregation_map = activations.sum(2)
    threshold = aggregation_map.mean()
    return aggregation_map, threshold


def label_mask(mask):
    """Label connected regions of mask and remove
    background label.
    
    Args:
        mask(np.ndarray): mask map
    
    Returns:
        np.ndarray, np.ndarray, np.ndarray
    """
    labeled_mask = label(mask, connectivity=1)
    unique, counts = np.unique(labeled_mask, return_counts=True)
    if unique[0] == 0:
        unique = unique[1:]
        counts = counts[1:]
    return unique, counts, labeled_mask


def get_mask(aggregation_map, threshold):
    """Creates mask map from aggregation map for values
    higher than threshold. Then chooses the largest connected
    component of the mask map.
    
    Args:
        aggregation_map (np.ndarray): aggregation map
        threshold (float): threshold value for mask map
    
    Returns:
        np.ndarray
    """
    mask = (aggregation_map > threshold).astype(float)
    unique, counts, labeled_mask = label_mask(mask)
    mask = (labeled_mask == unique[counts.argmax()])
    return mask

def select_descriptors(activations, mask=None):
    """Selects descriptors from all activations using mask, if mask is not
    provided all descriptors will be returned.
    
    Args:
        activations (np.ndarray): activations
        mask (np.ndarray): mask map
    Returns:
        np.ndarray
    """
    if mask is None:
        mask = np.ones(activations.shape)
    else:
        mask = np.stack([mask]*activations.shape[2], axis=2)
    descriptors = np.multiply(activations, mask)
    
    return descriptors


def aggregate_descriptors(activations, mask=None):
    """Aggregates descriptors using “avg&maxPool and
    normalize them using L2
    Args:
        activations (np.ndarray): activations
        mask (np.ndarray): mask map
    Returns:
        np.ndarray
    """
    descriptors = select_descriptors(activations, mask)
    avgpool = np.mean(descriptors, axis=(0,1))
    maxpool = np.max(descriptors, axis=(0,1))
    pool = np.concatenate((avgpool, maxpool))
    l2norm = normalize(pool.reshape(1,-1), norm='l2')
    l2norm = np.squeeze(l2norm)
    return l2norm


def mask_image(mask, img):
    mask = resize(mask, (img.shape[0], img.shape[1]), order=3, preserve_range=True)
    mask = np.stack((mask, mask, mask), axis=2)
    masked_image = img*mask
    return masked_image