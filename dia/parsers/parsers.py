from scipy.signal import find_peaks


def filestr_to_list(filestr):
    result = filestr[:-1].split(',')
    return result


def parse_lines(filename):
    line_list = []
    a = 0
    with open(filename, 'r') as file:
        line = 0
        for i in file:
            if "#EOF" in i:
                break
            if line >= 75:
                res_lst = filestr_to_list(i)
                if not a:
                    a = int(res_lst[0])
                line_list.append(float(res_lst[1]))
            else:
                line += 1
    a = 0
    zero_lst = [0 for i in range(a)]

    return zero_lst + line_list


def __get_str_dot(lst, x):
    result = f'[{x};{int(lst[x])}]'
    result += ' ' * (14-(len(result)))
    return result


def print_all_dots(lst_peaks, lst, label="No label"):
    print(label + '-'*(42 - len(label)), end=':')
    for i in lst_peaks:
        if i > 300:
            break
        print(__get_str_dot(lst, i), end=' ')
    print()


def parse_peaks(lst):
    peaks, _ = find_peaks(lst)
    return peaks
