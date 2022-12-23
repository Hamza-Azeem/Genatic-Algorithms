

var_list = []
fuzzy_list = {}
member_ships = {}
values = {}
out_member_ships = {}


def add_variables():
    print("Enter the variable’s name, type (IN/OUT) and range ([lower, upper]): (Press x to finish)")
    while (True):
        var = input()
        if (var == 'x' or var == 'X'):
            break
        var = var.split(" ")
        if (var[1] != "IN" and var[1] != "OUT"):
            print("Invalid variable type!")
            break
        var[2] = var[2][1:-1]
        try:
            var[3] = var[3][0:-1]
        except:
            print("You didn't enter the range with the right formate ([lower, upper])!")
            break
        try:
            var[2] = int(var[2])
            var[3] = int(var[3])
        except:
            print(
                "You either didn't enter the range with the right formate ([lower, upper]) or you didn't enter numbers!")
            break
        if (var[2] > var[3]):
            t = var[2]
            var[2] = var[3]
            var[3] = t
        var_list.append(var)


def check_var(var):
    for i in range(len(var_list)):
        if var == var_list[i][0]:
            return True
    else:
        return False


def fuzzy_sets():
    var_name = input("Enter the variable’s name: \n--------------------------\n")
    if not check_var(var_name):
        print("The variable name you entered doesn't exist!")
        return

    print("Enter the fuzzy set name, type (TRI/TRAP) and values: (Press x to finish)\n"
          "-----------------------------------------------------")
    fuzzy_set = []
    in_string = ""
    while in_string != "x":
        in_string = input()
        l = in_string.split()
        num = []
        flag = True
        for i in range(len(l)):
            if l[i] == "x":
                break
            if l[1] != "TRI" and l[1] != "TRAP":
                print("wrong type, please re enter the fuzzy set:")
                flag = False
                break

            if i > 1:
                l[i] = float(l[i])
                num.append(l[i])
        if l[0] != "x":
            if l[1] == "TRI":
                if len(num) != 3:
                    print("please re-enter this fuzzy set as count of number is incorrect")
                    continue
            if l[1] == "TRAP":
                if len(num) != 4:
                    print("please re-enter this fuzzy set as count of number is incorrect")
                    continue
        if flag:
            del l[2:]
            l.append(num)
            fuzzy_set.append(l)
    fuzzy_list[var_name] = fuzzy_set[:-1]


def inference_rules():
    count = 0
    print("Enter the rules in this format: (Press x to finish)\n"
          "IN_variable set operator IN_variable set => OUT_variable set\n"
          "------------------------------------------------------------")
    line = input()
    rule = []
    var1 = 0
    var2 = 3
    var3 = 6
    arrow = 5
    while line != "x":
        lines = line.split()
        # print(lines[var1],lines[var2],lines[var3])
        if not (check_var(lines[var1]) and check_var(lines[var2]) and check_var(lines[var3])):
            print("in correct variable names please re-enter the rule")
            line = input()
            continue
        del lines[arrow]
        rule.append(lines)
        count += 1
        line = input()
    return rule


def crisp_values():
    print("Enter the crisp values:")
    dict = {}
    ones_and_zeros_tri = {0: 0,
                          1: 1,
                          2: 0}
    ones_and_zeros_trap = {0: 0,
                           1: 1,
                           2: 1,
                           3: 0}

    for n in range(len(var_list)):
        if var_list[n][1] == 'IN':
            name = var_list[n][0]
            value = int(input(f"{name}: "))
            dict[name] = value
            for list in fuzzy_list[name]:
                val = dict[name]
                flag = False
                if list[1] == "TRI":
                    for k in range(len(list[2]) - 1):
                        if (val == list[2][k]) and (k == 0) and (
                                list[2][k] == list[2][k + 1]):
                            member_ships[list[0]] = 1
                            flag = True
                            break
                        elif val == list[2][k] and k == 1:
                            member_ships[list[0]] = 1
                            flag = True
                            break
                        elif val > list[2][k] and val < list[2][k + 1]:
                            m = (ones_and_zeros_tri[k + 1] - ones_and_zeros_tri[k]) / (
                                    list[2][k + 1] - list[2][k])
                            c = ones_and_zeros_tri[k] - (m * list[2][k])
                            member_ship = m * val + c
                            member_ships[list[0]] = member_ship
                            flag = True
                            break
                    if flag == False:
                        member_ships[list[0]] = 0
                else:
                    for k in range(len(list[2])):
                        if (val == list[2][k]) and ((k == 1) or (k == 2)):
                            member_ships[list[0]] = 1
                            flag = True
                            break
                        elif (val == list[2][k]) and (k == 3) and (list[2][k] == list[2][k - 1]):
                            member_ships[list[0]] = 1
                            flag = True
                            break
                        elif (k != 3) and (val > list[2][k]) and (val < list[2][k + 1]):
                            m = (ones_and_zeros_trap[k + 1] - ones_and_zeros_trap[k]) / (
                                    list[2][k + 1] - list[2][k])
                            c = ones_and_zeros_trap[k] - (m * list[2][k])
                            member_ship = m * val + c
                            member_ships[list[0]] = member_ship
                            flag = True
                            break
                    if flag == False:
                        member_ships[list[0]] = 0

def crisp_values2(msquare):
    dict = {}
    ones_and_zeros_tri = {0: 0,
                          1: 1,
                          2: 0}
    ones_and_zeros_trap = {0: 0,
                           1: 1,
                           2: 1,
                           3: 0}

    for n in range(len(var_list)):
        if var_list[n][1] == 'OUT':
            name = var_list[n][0]
            dict[name] = msquare
            for list in fuzzy_list[name]:
                val = dict[name]
                flag = False
                if list[1] == "TRI":
                    for k in range(len(list[2]) - 1):
                        if (val == list[2][k]) and (k == 0) and (
                                list[2][k] == list[2][k + 1]):
                            out_member_ships[list[0]] = 1
                            flag = True
                            break
                        elif val == list[2][k] and k == 1:
                            out_member_ships[list[0]] = 1
                            flag = True
                            break
                        elif val > list[2][k] and val < list[2][k + 1]:
                            m = (ones_and_zeros_tri[k + 1] - ones_and_zeros_tri[k]) / (
                                    list[2][k + 1] - list[2][k])
                            c = ones_and_zeros_tri[k] - (m * list[2][k])
                            member_ship = m * val + c
                            out_member_ships[list[0]] = member_ship
                            flag = True
                            break
                    if flag == False:
                        out_member_ships[list[0]] = 0
                else:
                    for k in range(len(list[2])):
                        if (val == list[2][k]) and ((k == 1) or (k == 2)):
                            out_member_ships[list[0]] = 1
                            flag = True
                            break
                        elif (val == list[2][k]) and (k == 3) and (list[2][k] == list[2][k - 1]):
                            out_member_ships[list[0]] = 1
                            flag = True
                            break
                        elif (k != 3) and (val > list[2][k]) and (val < list[2][k + 1]):
                            m = (ones_and_zeros_trap[k + 1] - ones_and_zeros_trap[k]) / (
                                    list[2][k + 1] - list[2][k])
                            c = ones_and_zeros_trap[k] - (m * list[2][k])
                            member_ship = m * val + c
                            out_member_ships[list[0]] = member_ship
                            flag = True
                            break
                    if flag == False:
                        out_member_ships[list[0]] = 0


def inference():
    operator = 2
    var1 = 1
    var2 = 4
    for i in range(len(rules)):
        rule = rules[i]
        out_set = rule[6]
        degree1 = member_ships[rule[var1]]
        degree2 = member_ships[rule[var2]]
        if rule[operator] == "and":
            value = min(degree1, degree2)
            if(out_set in values.keys()):
                values[out_set] = max(values[out_set], value)
            else:
                values[out_set] = value
        if rule[operator] == "or":
            value = max(degree1, degree2)
            if (out_set in values.keys()):
                values[out_set] = max(values[out_set], value)
            else:
                values[out_set] = value

        if rule[operator] == "or_not":
            value = max(degree1, 1 - degree2)
            if (out_set in values.keys()):
                values[out_set] = max(values[out_set], value)
            else:
                values[out_set] = value
        if rule[operator] == "and_not":
            value = min(degree1, 1 - degree2)
            if (out_set in values.keys()):
                values[out_set] = max(values[out_set], value)
            else:
                values[out_set] = value

def weighted_average():
    name = ""
    for i in var_list:
        for j in range(len(i)):
            if i[j] == "OUT":
                name = i[0]
    out = fuzzy_list[name]
    # sets = len(fuzzy_list)
    # out = fuzzy_list[sets-1]
    centroids = {}
    var = ""
    num = 2
    summ = 0
    mean = 0
    for i in range(len(out)):
        var = out[i][0]
        centroids[var] = sum(out[i][num]) / len(out[i][num])
    keys = list(values.keys())
    print(f"centroids {centroids}")
    for i in keys:
        summ += values[i] * centroids[i]
    vals = list(values.values())
    mean = summ / sum(vals)
    crisp_values2(mean)
    max = -1
    k = ''
    for i in out_member_ships.keys():
        if out_member_ships[i] > max:
            max = out_member_ships[i]
            k = i
    print(f"The predicted {name} is {k} ({mean})")




# MAIN:

while (True):
    print("Fuzzy Logic Toolbox")
    print("===================")
    print("1- Create a new fuzzy system")
    print("2- Quit")
    ans = int(input())
    if (ans == 2):
        break
    elif (ans != 1):
        print("Invalid input, The tool is going to shutdown")
        break
    print("Enter the system’s name and a brief description:")
    print("------------------------------------------------")
    proj_name = input()
    descrip = input()
    while (True):
        print("Main Menu:")
        print("==========")
        print("1- Add variables.")
        print("2- Add fuzzy sets to an existing variable.")
        print("3- Add rules.")
        print("4- Run the simulation on crisp values.")
        main_ans = input()
        if (main_ans == "1"):
            add_variables()
        elif (main_ans == "2"):
            fuzzy_sets()
        elif (main_ans == "3"):
            rules = inference_rules()
        elif (main_ans == "4"):
            member_ships = {}
            values = {}
            if fuzzy_list == {} or var_list == []:
                print("CAN’T START THE SIMULATION! Please add the fuzzy sets and rules first.")
                continue
            crisp_values()
            print("Running the simulation…")
            print("Fuzzification => done")
            print("Inference => done")
            print("Defuzzification => done")
            inference()
            weighted_average()
        elif(main_ans == "Close"):
            break
        else:
            print("Invalid input, The system is going to shutdown")
            break
    var_list = []
    fuzzy_list = {}
    member_ships = {}
    values = {}
    rules = []