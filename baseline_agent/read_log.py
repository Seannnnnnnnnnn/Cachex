with open("../game.log") as f:
    i = 0
    for row in f:
        color = "r" if i % 2 == 0 else "b"
        print(f"state.update('{color}', ('Place', {row[-6:-2]}))")
        print("print(state)")
        i += 1

