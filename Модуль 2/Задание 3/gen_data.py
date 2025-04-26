from random import randrange, choice


with open('Задание 3/create_and_fill.sql', 'w') as file:
    file.write(
        'CREATE TABLE Product (maker VARCHAR(50), model INTEGER, type VARCHAR(7));\n'
    )
    file.write(
        'CREATE TABLE PC (code INTEGER, model INTEGER, speed INTEGER, ram INTEGER, '
        'hdd NUMERIC(10,1), cd VARCHAR(25), price NUMERIC(10,2));\n'
    )
    file.write(
        'CREATE TABLE Laptop (code INTEGER, model INTEGER, speed INTEGER, ram INTEGER, '
        'hdd NUMERIC(10,1), screen NUMERIC(3,2), price NUMERIC(10,2));\n'
    )
    file.write(
        'CREATE TABLE Printer (code INTEGER, model INTEGER, color CHAR(1), type VARCHAR(6), price NUMERIC(10,2));\n'
    )

    file.write('\nINSERT INTO Product\n')
    file.write('VALUES\n')

    values = []
    for model in range(1042, 1857):
        values.append(
            f"(\'{choice(list('ABCDEFGLMOS'))}\', {model}, \'{'Laptop' if model < 1442 else 'PC' if model < 1663 else 'Printer'}\')"
        )

    file.write(',\n'.join(values) + ';\n')


    file.write('\nINSERT INTO Laptop\n')
    file.write('VALUES\n')

    values = []
    for i, model in enumerate(range(1042, 1442), start=1):
        values.append(
            f'({i}, {model}, {randrange(500, 901, 100)},'
            f' {randrange(32, 129, 32)}, {randrange(5, 21, 5)},'
            f' {randrange(133, 180) / 10}, {randrange(200, 851, 50)})'
        )

    file.write(',\n'.join(values) + ';\n')


    file.write('\nINSERT INTO PC\n')
    file.write('VALUES\n')

    values = []
    for i, model in enumerate(range(1442, 1663), start=1):
        values.append(
            f'({i}, {model}, {randrange(500, 901, 100)},'
            f' {randrange(32, 129, 32)}, {randrange(5, 21, 5)},'
            f' \'{randrange(12, 53, 4)}x\', {randrange(350, 1001, 50)})'
        )

    file.write(',\n'.join(values) + ';\n')


    file.write('\nINSERT INTO Printer\n')
    file.write('VALUES\n')

    values = []
    for i, model in enumerate(range(1663, 1857), start=1):
        values.append(
            f"({i}, {model}, \'{choice(['n', 'y'])}\', \'{choice(['Laser', 'Jet', 'Matrix'])}\', {randrange(300, 1201, 100)})"
        )

    file.write(',\n'.join(values) + ';\n')
