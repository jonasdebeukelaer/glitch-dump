from internal import tools


def mixup(img):
    weight = 0.4
    cutoff = 100
    y_max = img.shape[0]
    x_max = img.shape[1]
    new_img = img
    for y in range(0, y_max):
        tools.display_percentage("running mixup... ", y, y_max)
        for x in range(0, x_max):
            if img[y, x, 2] < cutoff and img[y, x, 1] < cutoff:
                new_x = int(((x + img[y, x, 2]) * 2) % x_max)

                new_img[y, new_x][:] = ((1.0 - weight) * img[y, x][:] + weight * img[y, new_x][:])
                new_img[y, x][:] = (weight * img[y, x][:] + (1.0 - weight) * img[y, new_x][:])

    return new_img
