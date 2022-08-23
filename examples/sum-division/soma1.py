print("Digite números inteiros, cada um seguido de Enter, ou ˆD para finalizar o programa.")

total = 0
count = 0

while True:
    try:
        line = input()
        if line:
            number = int(line)
            total += number
            count += 1
    except ValueError as err:
        print(err)
        continue
    except EOFError:
        break

    if count:
        print("count =", count, "total =", total, "mean =", total / count)