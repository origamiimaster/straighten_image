from PIL import Image
import numpy as np


# a is points in original plane, b is points in perspective shifted plane.  
def find_my_transform_matrix_yay(a, b): 
    matrix = []
    for (x1, y1), (x2, y2) in zip(a, b):
        matrix.extend([
            [x1, y1, 1, 0, 0, 0, -x2 * x1, -x2 * y1],
            [0, 0, 0, x1, y1, 1, -y2 * x1, -y2 * y1]
        ])
    A = np.matrix(matrix)
    B = np.array(b).reshape(8)
    after = np.dot(np.linalg.inv(A.T * A) * A.T, B)
    return np.array(after).reshape(8)
    return np.append(np.array(after).reshape(8), 1).reshape(3, 3)


def do_transform(img, a, b):
    width, height = img.size
    transform_matrix = find_my_transform_matrix_yay(b, a)
    print(transform_matrix)
    m = -0.5

    img.transform((width, height), Image.PERSPECTIVE, transform_matrix).show()
    # img.transform(img.size, Image.AFFINE, )

if __name__ == "__main__":
    print(find_my_transform_matrix_yay(((0, 0), (1, 0), (0, 1), (1, 1)), ((1, 0), (0, 1), (1, 1), (0, 0))))
    (9332, 6850)
    a = (0, 0), (9332, 0), (0, 6850), (9332, 6850)
    b = (-279, -120), (9332 + 120, -432), (0, 6850 + 380), (9332 + 348, 6850)
    img = Image.open("uploads/B1989-1992_05_10.jpeg", 'r')
    print(img.size)
    do_transform(img, a, b)
