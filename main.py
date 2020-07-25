from controller import Controller
import sys
import os


if __name__ == "__main__":
    controller = None
    try:
        if len(sys.argv) >= 3:
            controller = Controller(int(sys.argv[1]), int(sys.argv[2]))
        else:
            controller = Controller(path_to_file=sys.argv[1])
    except IndexError:
        print("\nUsage:")
        print("\tpython3 main.py PATH_TO_FILE\n\n")
        print("\tpython3 main.py WIDTH HEIGHT\n")
        exit(1)
    except FileNotFoundError as e:
        print("No such file or directory: {}".format(e.filename))
        exit(1)
    os.system("clear")
    controller.start()
