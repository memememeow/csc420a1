# Q6 a)
import numpy as np
import scipy.linalg as sp
import cv2 as cv
import a1q4


# Q6 a)
# This function adds uniformly dis- tributed random noises on a given image.
# The input includes: a grayscale image I, the magnitude of random noises m.
# The output is the image with noises.
def AddRandNoise(I, m):
    noise = np.random.uniform(-1 * m, m, I.shape)
    return I + noise


# Q6 c)
# This function adds salt-and-pepper noises on a given image.
# The input includes: a grayscale image I, the density of noises d.
# The output is the image with noises.
def AddSaltAndPepperNoise(I, d):
    result = np.copy(I)
    salt_coord = [np.random.randint(0, i - 1, int(I.shape[0] * I.shape[1] * d / 2)) for i in I.shape]
    pepper_coord = [np.random.randint(0, i - 1, int(I.shape[0] * I.shape[1] * d / 2)) for i in I.shape]
    result[salt_coord] = 1
    result[pepper_coord] = 0

    # for i in range(I.shape[0]):
    #     for j in range(I.shape[1]):
    #         if np.random.random() < d:
    #             result[i, j] = 0 if np.random.random() < 0.5 else 1
    return result


if __name__ == '__main__':
    # Q6 a)
    img = cv.imread('../gray.jpg', 0).astype(np.float) / 255.0
    result_rand = np.clip(AddRandNoise(img, 0.05) * 255, 0, 255)
    cv.imwrite("../results/q6a_randNoiseImg.jpg", result_rand)

    # Q6 b)
    blur_filter = cv.getGaussianKernel(5, 5) * cv.getGaussianKernel(5, 5).T
    blur_result = a1q4.MyConvolution(result_rand, blur_filter, "same")
    cv.imwrite("../results/q6b_blurRandNoiseImg.jpg", blur_result)

    # Q6 c)
    img = cv.imread('../gray.jpg', 0).astype(np.float) / 255.0
    result_salt_and_pepper = np.clip(AddSaltAndPepperNoise(img, 0.05) * 255, 0, 255)
    cv.imwrite("../results/q6c_SaltAndPepperNoiseImg.jpg", result_salt_and_pepper)

    # Q6 d)
    # with method used in Q6 b)
    blur_filter = cv.getGaussianKernel(5, 5) * cv.getGaussianKernel(5, 5).T
    blur_result_salt_and_pepper = a1q4.MyConvolution(result_salt_and_pepper, blur_filter, "same")
    cv.imwrite("../results/q6d_blurSaltAndPepperNoiseImg.jpg", blur_result_salt_and_pepper)
    # with median filter
    median_result_salt_and_pepper = cv.medianBlur(result_salt_and_pepper.astype(np.uint8), 3)
    cv.imwrite("../results/q6d_medianSaltAndPepperNoiseImg.jpg", median_result_salt_and_pepper)

    # Q6 e)
    img = cv.imread('../color.jpg').astype(np.float) / 255.0
    color_result = np.zeros(img.shape)
    color_result[:, :, 0] = np.clip(AddSaltAndPepperNoise(img[:, :, 0], 0.05) * 255, 0, 255)
    color_result[:, :, 1] = np.clip(AddSaltAndPepperNoise(img[:, :, 1], 0.05) * 255, 0, 255)
    color_result[:, :, 2] = np.clip(AddSaltAndPepperNoise(img[:, :, 2], 0.05) * 255, 0, 255)
    cv.imwrite("../results/q6e_ColorSaltAndPepperNoiseImg.jpg", color_result)
    # with median filter separately on each channel
    median_color_result = np.zeros(img.shape)
    median_color_result[:, :, 0] = cv.medianBlur(color_result[:, :, 0].astype(np.uint8), 3)
    median_color_result[:, :, 1] = cv.medianBlur(color_result[:, :, 1].astype(np.uint8), 3)
    median_color_result[:, :, 2] = cv.medianBlur(color_result[:, :, 2].astype(np.uint8), 3)
    cv.imwrite("../results/q6e_medianColor1ChannelImg.jpg", median_color_result)
    # with median filter on 3-channel together
    median_color_result = cv.medianBlur(color_result.astype(np.uint8), 5)
    cv.imwrite("../results/q6e_medianColor3ChannelImg.jpg", median_color_result)