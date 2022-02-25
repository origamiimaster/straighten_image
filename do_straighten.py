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
    return img.transform((width, height), Image.PERSPECTIVE, transform_matrix)

def make_straight(client_string):
    dash_count = 0
    
    for i in range(len(client_string)):
        if dash_count == 4:
            image_name = client_string[i:]
            break        
        
        if client_string[i] == '-':
            dash_count += 1
        
    corners = client_string.split('-') # Example: 62&66-376&75-67&330-374&324-
    # image_name = corners[-1] 
    corners = corners[:4]
    print(corners)
    corners = [(int(c.split("&")[0]), int(c.split("&")[1])) for c in corners]
    # Determine which corner is most likely to correspond to which other one, rearranging in order top left, top right, bottom right, bottom left.  
    corners.sort(key=lambda k: k[0]**2 + k[1]**2)
    corners[1:] = sorted(corners[1:], key=lambda k: (400 - k[0])**2 + (k[1])**2)
    corners[2:] = sorted(corners[2:], key=lambda k: (400 - k[0])**2 + (400 - k[1])**2)
    
    # Apply a shift to get back to the original image size:
    img = Image.open('uploads/' + image_name)
    width, height = img.size
    thumbnail_height = 400
    thumbnail_width = thumbnail_height * width // height



    for i in range(4):
        corners[i] = (int(corners[i][0] * width / thumbnail_width), int(corners[i][1] * height / thumbnail_height))
    b = ((0, 0), (width, 0), (width, height), (0, height))
    corners[0] = (-1 * corners[0][0], -1 * corners[0][1])
    corners[1] = (width + (width - corners[1][0]), -1 * corners[1][1])
    corners[2] = (width + (width - corners[2][0]), height + (height - corners[2][1]))
    corners[3] = (-1 * corners[3][0], height + (height - corners[3][1]))

    # a = (0, 0), (9332, 0), (0, 6850), (9332, 6850)
    # b = (-279, -120), (9332 + 120, -432), (0, 6850 + 380), (9332 + 348, 6850)
    print(b)
    print(corners)
    print(width)
    print(height)
    return do_transform(img, b, corners), image_name






if __name__ == "__main__":
    print(find_my_transform_matrix_yay(((0, 0), (1, 0), (0, 1), (1, 1)), ((1, 0), (0, 1), (1, 1), (0, 0))))
    (9332, 6850)
    a = (0, 0), (9332, 0), (0, 6850), (9332, 6850)
    b = (-279, -120), (9332 + 120, -432), (0, 6850 + 380), (9332 + 348, 6850)
    img = Image.open("uploads/B1989-1992_05_10.jpeg", 'r')
    print(img.size)
    do_transform(img, a, b)
