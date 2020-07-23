from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
import random


def main():
    rectangles = []
    for _ in range(5):
        x = random.uniform(0.0, 10.0)
        y = random.uniform(0.0, 10.0)

        w = 3
        h = 3
        rectangles.append([(x,y), (x+w,y), (x,y+h), (x+w,y+h)])

    color = [c/256 for c in (136, 150, 142)]  # rgb values between 0 and 1
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set(xlim=(0, 10), ylim=(0, 10))
    ax.axis('off')

    for rectangle in rectangles:
        xy = rectangle[0]
        width = rectangle[3][0] - rectangle[0][0]
        height = rectangle[3][1] - rectangle[0][1]
        rect = Rectangle(xy, width, height, linewidth=1, edgecolor='none', facecolor=color, alpha=0.3)
        ax.add_patch(rect)

    plt.savefig("test.png", bbox_inches='tight', dpi=300)
    plt.show()


if __name__ == "__main__":
    main()
