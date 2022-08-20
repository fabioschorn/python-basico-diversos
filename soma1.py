print("Digite números inteiros, cada um seguido de enter, ou apenas Enter para finalizar o programa.")

total = 0
count = 0

while True:
    line = input("integer: ")
    if line:
        try:
            number = int(line)
        except ValueError as err:
            print(err)
            continue
        total += number
        count += 1
    else:
        break

    if count:
        print("count =", count, "total =", total, "mean =", total / count)