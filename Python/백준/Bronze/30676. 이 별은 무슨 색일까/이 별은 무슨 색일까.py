def spectrum(nm):
    color = None

    if 620 <= nm <= 780:
        color = "Red"
    if 590 <= nm < 620:
        color = "Orange"
    if 570 <= nm < 590:
        color = "Yellow"
    if 495 <= nm < 570:
        color = "Green"
    if 450 <= nm < 495:
        color = "Blue"
    if 425 <= nm < 450:
        color = "Indigo"
    if 380 <= nm < 425:
        color = "Violet"

    return color


if __name__ == "__main__":
    nm = int(input())

    print(spectrum(nm))
