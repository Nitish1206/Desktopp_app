import xml.etree.ElementTree as ET
import cv2
import numpy as np


def load_binary_annotations(annotations_path, annotation_type):
    """
    Parse annotations according to annotation type
    :param annotations_path: path to annotation file
    :param annotation_type: type of annotation
    :return: binary annotations list according to annotation type
    """
    try:
        annotations = []
        tree = ET.parse(annotations_path)
        root = tree.getroot()
        for image in root.findall('image'):
            annotations = append_annotation(annotations, image, annotation_type)
    except:
        print('no annotation file ' + annotations_path)
        return None
    return annotations


def append_annotation(annotations, image, annotation_type):
    """
    Parse annotation of an image according to annotation type
    :param annotations: annotations list to update
    :param image: image annotation in xml
    :param annotation_type: type of annotation
    :return: updated annotations list
    """
    long_names = ['Rt long', 'Lt Long', 'Lt long']
    short_names = ['Rt short', 'Lt short']
    lt_long_names = ['Lt Long', 'Lt long']
    rt_long_names = ['Rt long']
    lt_short_names = ['Lt short']
    rt_short_names = ['Rt short']

    box = image.find('box')
    if box is not None:
        if annotation_type == 'all':
            annotations.append(1)
        elif annotation_type == 'long':
            append_if_in_list(annotations, box, long_names)
        elif annotation_type == 'short':
            append_if_in_list(annotations, box, short_names)
        elif annotation_type == 'lt_long':
            append_if_in_list(annotations, box, lt_long_names)
        elif annotation_type == 'rt_long':
            append_if_in_list(annotations, box, rt_long_names)
        elif annotation_type == 'lt_short':
            append_if_in_list(annotations, box, lt_short_names)
        elif annotation_type == 'rt_short':
            append_if_in_list(annotations, box, rt_short_names)
        else:
            annotations.append(0)
    else:
        annotations.append(0)
    return annotations


def append_if_in_list(annotations, box, names):
    """
    Append to annotations list 1 if the attribute in names list, 0 otherwise
    :param annotations: annotations list to update
    :param box: box
    :param names: names of annotations
    :return: updated annotations list
    """
    if (box.attrib['label'] in names):
        annotations.append(1)
    else:
        annotations.append(0)


def load_video_data(video_path):
    """
    Load images in the video
    :param video_path: path to video
    :return: video images
    """
    video_images = []
    vidcap = cv2.VideoCapture(video_path)
    success, image = vidcap.read()
    while success:
        video_images.append(image)
        success,image = vidcap.read()

    return video_images


def pad_to_size(img, size):
    """
    Pad img with zeros from both sides to specified size
    :param img: image to pad
    :param size: target size
    :return: padded image and delta of the padding
    """
    img_size = img.shape
    if(list(img_size)==size):
        return img, [0,0]
    padded = np.zeros(size, dtype=float)
    x_delta = int(np.ceil((size[0]-img_size[0])/2))
    y_delta = int(np.ceil((size[1]-img_size[1])/2))
    padded[x_delta:(x_delta+img_size[0]), y_delta:(y_delta+img_size[1]),:] = img

    return padded, [x_delta, y_delta]








