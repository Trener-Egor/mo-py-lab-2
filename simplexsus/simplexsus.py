"""
Программа реализует симплекс-метод для решения задач линейного программирования.
Содержит функции для проверки входных данных, создания симплекс-таблицы,
поиска разрешающего элемента, выполнения итераций симплекс-метода и вывода
результатов на экран.

Функции:
- check_simplex_table: Проверяет корректность входных данных для симплекс-метода.
- check_simplex_response: Проверяет возможность существования решения и наличие отрицательных значений.
- create_simplex_table: Создает симплекс-таблицу из заданных коэффициентов, ограничений и правых частей.
- print_simplex_table: Выводит симплекс-таблицу в консоль в форматированном виде.
- find_simplex_resolve: Находит разрешающий элемент в симплекс-методе.
- find_min_ratio: Находит минимальное отношение для заданного столбца.
- simplex_table_iteration: Выполняет одну итерацию симплекс-метода, обновляя коэффициенты и ограничения.
- simplexsus: Основная функция симплекс-метода, выполняет проверку данных и находит оптимальное решение.

Для использования достаточно задать коэффициенты целевой функции, ограничения и правые части.
Результатом будет оптимальное значение целевой функции и соответствующие решения переменных.
"""


def check_simplex_table(c, A, b):
    """
    Проверка корректности входных данных для симплекс-метода.
    """
    len_A = len(A[0])  # Количество переменных

    # Проверяет, что все строки матрицы A имеют одинаковую длину
    # и содержат допустимые значения
    for row in A:
        if len(row) != len_A:
            return False  # Длина строки не соответствует ожидаемой

        # for num in row:
        #     if num < 0:
        #         return False    # Неподходящее значение

    # Проверяем, что длины векторов c и b соответствуют количеству строк в A
    if (len(c) != len_A) or (len(b) != len(A)):
        return False

    # Проверка пройдена успешно
    return True


def check_simplex_response(c, A, b):
    """
    Проверяет, существует ли решение симплекс-метода
    """
    if c.count(0) == len(c):
        return False  # Все коэффициенты равны нулю

    for row in range(len(b)):
        if b[row] < 0:  # Если есть отрицательный элемент в b
            for col in range(len(A[0])):  # Ошибка в исходном коде: A должен быть матрицей
                if A[row][col] < 0:
                    return True  # Существуют отрицательные коэффициенты
            return False  # Нет подходящих коэффициентов

    return True


def create_simplex_table(c, A, b, f):
    """
    Создает симплекс-таблицу из коэффициентов c, матрицы A и вектора b и f.
    """
    table = []

    # Формируем таблицу, добавляя строки с b и A
    for i in range(len(A)):
        table.append([b[i]] + A[i])

    # Добавляем строку с коэффициентами c
    table.append([f] + c)

    return table


def print_simplex_table(simplex_table):
    """
    Выводит симплекс-таблицу в терминал с заголовками.
    """
    # Определяем максимальную ширину для форматирования
    max_width = max(len(str(float(j))) for row in simplex_table for j in row) + 2

    # Выводим заголовки
    headers = ["b"] + [f"x{i+1}" for i in range(len(simplex_table[0]) - 1)]
    print(" | ".join(f"{header:>{max_width}}" for header in headers))
    print("-" * (max_width * len(headers) + 3 * (len(headers) - 1)))

    for i in range(len(simplex_table)):
        for j in simplex_table[i]:
            # Выравнивание по правому краю, 2 знака после запятой
            print(f"{float(j):>{max_width}.2f}", end=" | ")
        print()


def find_simplex_resolve(c, A, b):
    """
    Находит разрешающий элемент в симплекс-методе.
    Возвращает информацию о минимальном отношении или специальные строки.
    """

    if check_simplex_response(c, A, b):
        # Проверяем, корректна ли симплекс-таблица

        for row in range(len(b)):
            if b[row] < 0:
                for col in range(len(A[0])):
                    if A[row][col] < 0:
                        # Возвращаем минимальное отношение для данного столбца
                        try:
                            return find_min_ratio(A, b, col)
                        except:
                            return ["inf"]

        c_max_value = max(c)
        if c_max_value < 0:
            # Если максимальное значение меньше нуля
            return ["not"]

        c_max_index = c.index(c_max_value)
        try:
            return find_min_ratio(A, b, c_max_index)
        except:
            return ["inf"]

    else:
        return ["not"]


def find_min_ratio(A, b, min_ratio_col):
    """
    Находит минимальное отношение для заданного столбца в симплекс-таблице.
    """
    min_ratio = float("inf")
    min_ratio_row = -1

    for row in range(len(A)):
        if A[row][min_ratio_col] == 0:
            continue

        ratio = b[row] / A[row][min_ratio_col]

        # Обновляем минимальное отношение, если нашли новое
        if (ratio > 0) and (ratio < min_ratio):
            min_ratio = ratio
            min_ratio_row = row

    # Если не найден подходящий индекс, выбрасываем ошибку
    if min_ratio_row == -1:
        raise ValueError("[ ! ] Нет допустимого разрешающего элемента.")

    return [A[min_ratio_row][min_ratio_col], min_ratio_row, min_ratio_col]


def simplex_table_iteration(c, A, b, f, simplex_resolve):
    """
    Функция для выполнения одной итерации симплекс-метода.

    Параметры:
    c : list
        Коэффициенты целевой функции.
    A : list of lists
        Матрица ограничений системы.
    b : list
        Вектор правых частей ограничений (свободные коэффициенты).
    f : float
        Текущее значение целевой функции.
    simplex_resolve : tuple
        Кортеж, содержащий информацию о разрешающем элементе:
        (значение разрешающего элемента, строка, столбец).

    Возврат:
    new_c : list
        Обновленные коэффициенты целевой функции.
    new_A : list of lists
        Обновленная матрица ограничений.
    new_b : list
        Обновленный вектор правых частей (свободные коэффициенты).
    new_f : float
        Обновленное значение целевой функции.
    """

    # Получаем значение разрешающего элемента
    new_simplex_resolve = 1 / simplex_resolve[0]

    new_c = [0] * len(c)  # Инициализируем новый вектор коэффициентов целевой функции
    new_b = [0] * len(b)  # Инициализируем новый вектор правых частей
    new_A = [[0 for _ in range(len(A[0]))] for _ in range(len(A))]  # Инициализируем новую матрицу ограничений

    # Заполняем колонну A
    for i in range(len(A)):
        if i == simplex_resolve[1]:  # Текущая строка разрешающего элемента
            new_A[i][simplex_resolve[2]] = new_simplex_resolve
        else:  # Остальные строки
            new_A[i][simplex_resolve[2]] = A[i][simplex_resolve[2]] / simplex_resolve[0] * -1

    # Обновляем коэффициенты целевой функции для разрешающего столбца
    new_c[simplex_resolve[2]] = c[simplex_resolve[2]] / simplex_resolve[0] * -1

    # Заполняем строку A для разрешающего элемента
    for i in range(len(A[0])):
        if i == simplex_resolve[2]:
            continue
        new_A[simplex_resolve[1]][i] = A[simplex_resolve[1]][i] / simplex_resolve[0]

    # Обновляем вектор правых частей для разрешающего элемента
    new_b[simplex_resolve[1]] = b[simplex_resolve[1]] / simplex_resolve[0]

    # Обновляем остальные коэффициенты целевой функции
    for i in range(len(c)):
        if i == simplex_resolve[2]:
            continue
        new_c[i] = c[i] - (A[simplex_resolve[1]][i] * c[simplex_resolve[2]]) / (simplex_resolve[0])

    # Обновляем вектор правых частей для остальных строк
    for i in range(len(b)):
        if i == simplex_resolve[1]:
            continue
        new_b[i] = b[i] - ((A[i][simplex_resolve[2]] * b[simplex_resolve[1]]) / simplex_resolve[0])

    # Обновляем матрицу ограничений
    for i in range(len(A)):
        for j in range(len(A[0])):
            if (i == simplex_resolve[1]) or (j == simplex_resolve[2]):
                continue
            new_A[i][j] = A[i][j] - ((A[i][simplex_resolve[2]] * A[simplex_resolve[1]][j]) / simplex_resolve[0])

    # Обновляем значение целевой функции
    new_f = f - ((c[simplex_resolve[2]] * b[simplex_resolve[1]]) / simplex_resolve[0])

    #####################################################################
    # if new_f <= f:                                                    #
    #     return new_c, new_A, new_b, new_f                             #
    # raise ValueError("[ ! ] Не получается улучшить симплекс-таблицу") #
    #####################################################################
    return new_c, new_A, new_b, new_f


def to_dual_task(c, A, b, minimize):
    """
    Преобразует заданные параметры для двойственной задачи линейного программирования.
    """
    new_c = b.copy()
    new_b = [-x for x in c]

    # Создаем новую матрицу A для двойственной задачи
    # Размерность new_A: количество столбцов A x количество строк A
    new_A = [[0 for _ in range(len(A))] for _ in range(len(A[0]))]

    # Заполняем новую матрицу A, транспонируя оригинальную матрицу A
    for row in range(len(A)):
        for col in range(len(A[0])):
            new_A[col][row] = A[row][col] * -1

    return new_c, new_A, new_b, not minimize


def simplexsus(minimize, c, A, b, f):
    """
    Основная функция симплекс-метода. Выполняет проверку входных данных
    и находит решение.
    """
    # Проверка условий
    if check_simplex_table(c, A, b):
        print("[ + ] Check: OK")

        # Инвертируем c, если ищем минимум
        if minimize:
            for i in range(len(c)):
                c[i] *= -1

        while (max(c) > 0) or (min(b) < 0):
            ######################
            # i = 0              #
            # while i < 4:       #
            ######################
            simplex_table = create_simplex_table(c, A, b, f)  # Создание симплекс-таблицы
            print_simplex_table(simplex_table)  # Вывод симплекс-таблицы

            simplex_resolve = find_simplex_resolve(c, A, b)  # Поиск и выбор разрешающего элемента

            # Обработка результатов нахождения разрешающего элемента
            if simplex_resolve == ["not"]:
                print("[ - ] There's no answer")
                return 1
            if simplex_resolve == ["inf"]:
                print("[ - ] Infinite number of solutions")
                return 1

            print("[ * ] The resolving element is found:", simplex_resolve)

            c, A, b, f = simplex_table_iteration(c, A, b, f, simplex_resolve)

            ##########
            # i +=1  #
            ##########

        # Найдено оптимальное решение
        print("\n[ + ] OPTI ANS")
        simplex_table = create_simplex_table(c, A, b, f)  # Создание симплекс-таблицы
        print_simplex_table(simplex_table)  # Вывод симплекс-таблицы

    else:
        print("[ - ] Check: BAD")
        return 1

    if minimize:
        print("[ * ] The function goes to the minimum")
        return f

    print("[ * ] The function goes to the maximum")
    return f * -1
