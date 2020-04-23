import numpy as np
import scipy.linalg as sp
import cv2 as cv


# Q4 a)
# Helper to compute correlation in valid mode
def valid_correlation(image, h):
    m, n = image.shape[0], image.shape[1]
    r, c = h.shape[0], h.shape[1]
    result = np.zeros((m - r + 1, n - c + 1))
    for i in range(result.shape[0]):
        for j in range(result.shape[1]):
            patch = image[i: i + r, j: j + c].reshape(-1)
            result[i, j] = np.dot(h.reshape(-1), patch)
    return np.clip(result, 0, 255)


# This function implement the correlation operation of an image and a filter.
# The function outputs the filtering results J. The output must match what is specified by mode.
# Function takes three parameter:
#  img: a grayscale image
#  h: a filter
#  mode: could be 'valid', 'same' or 'full', otherwise return None
def MyCorrelation(I, h, mode):
    if I is None or h is None:
        return

    m, n = I.shape[0], I.shape[1]
    r, c = h.shape[0], h.shape[1]
    if mode is "valid":
        return valid_correlation(I, h)
    elif mode is "same":
        padding_target = np.zeros((m + r - 1, n + c - 1))
        padding_target[(r // 2):((r // 2) + m), (c // 2):((c // 2) + n)] = I
        return valid_correlation(padding_target, h)
    elif mode is "full":
        padding_target = np.zeros((m + 2 * r - 2, n + 2 * c - 2))
        padding_target[(r - 1):(r - 1 + m), (c - 1):(c - 1 + n)] = I
        return valid_correlation(padding_target, h)
    else:
        return


# Q4 b)
# This function implement the convolution operation of an image and a filter.
# The function outputs the filtering results J. The output must match what is specified by mode.
# Function takes three parameter:
#  img: a grayscale image
#  h: a filter
#  mode: could be 'valid', 'same' or 'full', otherwise return None
def MyConvolution(I, h, mode):
    return MyCorrelation(I, h[::-1, ::-1], mode)


# Q4 c)
# Blur background to make the photo into portrait mode
def to_portrait_mode(target, mask):
    blur_filter = cv.getGaussianKernel(10, 20) * cv.getGaussianKernel(10, 20).T
    blur_background = np.zeros(target.shape)
    blur_background[:, :, 0] = MyConvolution(target[:, :, 0], blur_filter, "same")
    blur_background[:, :, 1] = MyConvolution(target[:, :, 1], blur_filter, "same")
    blur_background[:, :, 2] = MyConvolution(target[:, :, 2], blur_filter, "same")

    comp_img = blur_background * (1 - mask.astype(np.float) / 255.0) + target * (mask.astype(np.float) / 255.0)
    return comp_img


if __name__ == '__main__':
    img = cv.imread('../gray.jpg', 0)

    # Test for Q4 a)
    blur = cv.getGaussianKernel(5, 10) * cv.getGaussianKernel(5, 10).T
    fullImg = MyCorrelation(img, blur, "full")
    sameImg = MyCorrelation(img, blur, "same")
    validImg = MyCorrelation(img, blur, "valid")

    cv.imwrite("../results/q4a_fullModeImg.jpg", fullImg)
    cv.imwrite("../results/q4a_sameModeImg.jpg", sameImg)
    cv.imwrite("../results/q4a_validModeImg.jpg", validImg)

    # Test for Q4 b)
    blur = cv.getGaussianKernel(5, 10) * cv.getGaussianKernel(5, 10).T
    fullImg = MyConvolution(img, blur, "full")
    sameImg = MyConvolution(img, blur, "same")
    validImg = MyConvolution(img, blur, "valid")

    cv.imwrite("../results/q4b_fullModeImg.jpg", fullImg)
    cv.imwrite("../results/q4b_sameModeImg.jpg", sameImg)
    cv.imwrite("../results/q4b_validModeImg.jpg", validImg)

    # Test for Q4 c)
    target_img = cv.imread('../portrait.jpg')
    mask_img = cv.imread('../mask.jpg')
    result = to_portrait_mode(target_img, mask_img)
    cv.imwrite("../results/q4c.jpg", result)
