import cv2
import numpy as np

#img = cv2.imread('./golden_gate.jpg')

def transform(img, net=cv2.dnn.readNetFromTorch('models/eccv16/composition_vii.t7')):
    h, w, c = img.shape
    img = cv2.resize(img, dsize=(500, int(h / w * 500)))
    # (325, 500, 3)

    MEAN_VALUE = [103.939, 116.779, 123.680]
    blob = cv2.dnn.blobFromImage(img, mean=MEAN_VALUE)

    # (1, 3, 325, 500)
    net.setInput(blob)
    output = net.forward()

    output = output.squeeze().transpose((1, 2, 0))
    output += MEAN_VALUE

    output = np.clip(output, 0, 255)
    output = output.astype('uint8')

    return output