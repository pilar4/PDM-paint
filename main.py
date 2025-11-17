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

    e_points_click = window.euler_click_points()
    pdm_points_click = window.pdm_click_points()
    print("Euler Click Points:")
    print(e_points_click)
    print("PDM Click Points:")
    print(pdm_points_click)


if __name__ == '__main__':
    main()
