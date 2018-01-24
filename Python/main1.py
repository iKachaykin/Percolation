from PIL import Image as img
import numpy as np
import numpy.random as rand


# Percolation numerical simulation
# Вычислительный эксперимент перколяции
# More info about percolation you can find here: https://en.wikipedia.org/wiki/Percolation_theory
# Больше информации здесь: https://en.wikipedia.org/wiki/Percolation_theory

# Function which take two vectors: left and right, and return True, if they are equal, and False - otherwise
# Функция, принимающая два вектора: left и right, и, возвращающая True, если они равны, и False - в противном случае
def component_equal(left, right):
    if len(left) != len(right):
        return False
    for l, r in zip(left, right):
        if l != r:
            return False
    return True


# Function creating img_number images which contain only white and tree_color_RGB pixels which associated with trees
# Функция, создающая картинки, что содержат только лишь пиксели двух цветов, ассоциируемые с деревьями
# More info you can find here: Ricard V. Sole, "Phase transitions", p. 53-62
# Больше информации вы можете найти здесь: Ricard V. Sole, "Phase transitions", стр. 53-62
def create_forest_images(img_number, img_width, img_height, first_prob, last_prob, tree_color_RGB=(0, 255, 0)):
    p = np.linspace(first_prob, last_prob, img_number)
    for i in range(img_number):
        image = img.new("RGB", (img_width, img_height), (255, 255, 255))
        for x in range(img_width):
            for y in range(img_height):
                ksi = rand.rand()
                if ksi < p[i]:
                    image.putpixel((x, y), tree_color_RGB)
        image.save(str(i + 1) + ".png")


# Function which burned well-defined trees in "forest"
# Функция, поджигающая вполне определенные деревья в "лесу"
def burn_forest(img_number, initial_burned_trees, fire_prob=1.0):
    for i in range(img_number):
        forest_image = img.open(str(i + 1) + ".png")
        burned_forest_image = forest_image.copy()
        pixels = np.array(burned_forest_image)
        burned_forest_matrix = np.zeros(pixels.shape[:2])
        for x in range(pixels.shape[1]):
            for y in range(pixels.shape[0]):
                if not component_equal(pixels[y, x], (255, 255, 255)):
                    burned_forest_matrix[y, x] = 1
        x, y, count = 0, pixels.shape[0] - 1, 0
        while count < initial_burned_trees:
            if burned_forest_matrix[y, x] == 1:
                burned_forest_matrix[y, x] = -1
                count += 1
            x += 1
            if x >= burned_forest_matrix.shape[1]:
                x = 0
                y -= 1
        while len(np.argwhere(burned_forest_matrix == -1)) != 0:
            y, x = tuple(np.argwhere(burned_forest_matrix == -1)[len(np.argwhere(burned_forest_matrix == -1)) - 1])
            burned_forest_matrix[y, x] = -2
            if y + 1 < burned_forest_matrix.shape[0] and burned_forest_matrix[y + 1, x] == 1:
                burned_forest_matrix[y + 1, x] = -1
            if y - 1 >= 0 and burned_forest_matrix[y - 1, x] == 1:
                burned_forest_matrix[y - 1, x] = -1
            if x + 1 < burned_forest_matrix.shape[1] and burned_forest_matrix[y, x + 1] == 1:
                burned_forest_matrix[y, x + 1] = -1
            if x - 1 >= 0 and burned_forest_matrix[y, x - 1] == 1:
                burned_forest_matrix[y, x - 1] = -1
        for x in range(pixels.shape[1]):
            for y in range(pixels.shape[0]):
                if burned_forest_matrix[y, x] == -2:
                    burned_forest_image.putpixel((x, y), (0, 0, 0))
        forest_image.close()
        burned_forest_image.save(str(i + 1) + "_burned.png")
        print(i)



images_number, image_width, image_height, p0, pn = 10, 500, 500, 0.5, 0.9
create_forest_images(images_number, image_width, image_height, p0, pn)
burn_forest(images_number, 100)
