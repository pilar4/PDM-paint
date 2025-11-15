from src import window
# import keyboard  # optional if using keyboard library

def main():
    window.draw()
    e_points = window.euler_points()
    pdm_points = window.pdm_points()
    print("Euler Points:")
    print()
    print()
    print(e_points)
    print("PDM Points:")
    print()
    print()
    print(pdm_points)



if __name__ == '__main__':
    main()
