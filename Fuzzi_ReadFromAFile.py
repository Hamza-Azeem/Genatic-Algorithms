# Hamza Abd AlAzeem Mohamed         20198026
# Mohamed Ahmed Saleh               20198069
# Maryam Mohamad Mohamad Sobhi      20198082
# Dina Ashraf                       20198127
# Group (1), B3                     TA: Mohamed Atta

var_list = []
fuzzy_list = {}
member_ships = {}
values = {}
out_member_ships = {}
rule1 = []
temp_list_fuzz = []
output_file = open("output.txt", "w")
output_file.close()
output_file = open("output.txt", "a")
#
#
def add_variables(var):
    if (var == ['x'] or var == ['X']):
        return
    if (var[1] != "IN" and var[1] != "OUT"):
        output_file.write("Invalid variable type!\n")
        return
    var[2] = var[2][1:-1]
    try:
        var[3] = var[3][0:-1]
    except:
        output_file.write("You didn't enter the range with the right formate ([lower, upper])!\n")
        return
    try:
        var[2] = int(var[2])
        var[3] = int(var[3])
    except:
        output_file.write("You either didn't enter the range with the right formate ([lower, upper]) or you didn't enter numbers!\n")
        return
    if (var[2] > var[3]):
        t = var[2]
        var[2] = var[3]
        var[3] = t
    var_list.append(var)
#
#
def check_var(var):
    for i in range(len(var_list)):
        if var == var_list[i][0]:
            return True
    else:
        return False


def fuzzy_sets(var_name, in_string):
    if not check_var(var_name):
        output_file.write("The variable name you entered doesn't exist!\n")
        return

    fuzzy_set = []
    l = in_string
    num = []
    flag = True
    for i in range(len(l)):
        if l[i] == ["x"]:
            return
        if l[1] != "TRI" and l[1] != "TRAP":
            output_file.write("wrong type, please re enter the fuzzy set:\n")
            flag = False
            return

        if i > 1:
            l[i] = float(l[i])
            num.append(l[i])
    if l[0] != ["x"]:
        if l[1] == "TRI":
            if len(num) != 3:
                output_file.write("please re-enter this fuzzy set as count of number is incorrect\n")
                return
        if l[1] == "TRAP":
            if len(num) != 4:
                output_file.write("please re-enter this fuzzy set as count of number is incorrect\n")
                return

    return l


def inference_rules(line):
    var1 = 0
    var2 = 3
    var3 = 6
    arrow = 5
    lines = line
    if not (check_var(lines[var1]) and check_var(lines[var2]) and check_var(lines[var3])):
        output_file.write("in correct variable names please re-enter the rule\n")
        return
    del lines[arrow]
    rule1.append(lines)
    return rule1

def crisp_values(value):
    dict = {}
    ones_and_zeros_tri = {0: 0,
                          1: 1,
                          2: 0}
    ones_and_zeros_trap = {0: 0,
                           1: 1,
                           2: 1,
                           3: 0}
    v_counter = 0
    for n in range(len(var_list)):
        if var_list[n][1] == 'IN':
            name = var_list[n][0]
            output_file.write(f"Crisp value for {name}: \n")
            dict[name] = value[v_counter]
            v_counter+=1
            for list in fuzzy_list[name]:
                val = dict[name]
                flag = False
                if list[1] == "TRI":
                    for k in range(2):
                        if (val == list[2+k]) and (k == 0) and (
                                list[2+k] == list[2+k + 1]):
                            member_ships[list[0]] = 1
                            flag = True
                            break
                        elif val == list[2+k] and k == 1:
                            member_ships[list[0]] = 1
                            flag = True
                            break
                        elif val > list[2+k] and val < list[2+k + 1]:
                            m = (ones_and_zeros_tri[k + 1] - ones_and_zeros_tri[k]) / (
                                    list[2+k + 1] - list[2+k])
                            c = ones_and_zeros_tri[k] - (m * list[2+k])
                            member_ship = m * val + c
                            member_ships[list[0]] = member_ship
                            flag = True
                            break
                    if flag == False:
                        member_ships[list[0]] = 0
                else:
                    for k in range(4):
                        if (val == list[2+k]) and ((k == 1) or (k == 2)):
                            member_ships[list[0]] = 1
                            flag = True
                            break
                        elif (val == list[2+k]) and (k == 3) and (list[2+k] == list[2+k - 1]):
                            member_ships[list[0]] = 1
                            flag = True
                            break
                        elif (k != 3) and (val > list[2+k]) and (val < list[2+k + 1]):
                            m = (ones_and_zeros_trap[k + 1] - ones_and_zeros_trap[k]) / (
                                    list[2+k + 1] - list[2+k])
                            c = ones_and_zeros_trap[k] - (m * list[2+k])
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
                    for k in range(2):
                        if (val == list[2+k]) and (k == 0) and (
                                list[2+k] == list[2+k + 1]):
                            out_member_ships[list[0]] = 1
                            flag = True
                            break
                        elif val == list[2+k] and k == 1:
                            out_member_ships[list[0]] = 1
                            flag = True
                            break
                        elif val > list[2+k] and val < list[2+k + 1]:
                            m = (ones_and_zeros_tri[k + 1] - ones_and_zeros_tri[k]) / (
                                    list[2+k + 1] - list[2+k])
                            c = ones_and_zeros_tri[k] - (m * list[2+k])
                            member_ship = m * val + c
                            out_member_ships[list[0]] = member_ship
                            flag = True
                            break
                    if flag == False:
                        out_member_ships[list[0]] = 0
                else:
                    for k in range(4):
                        if (val == list[2+k]) and ((k == 1) or (k == 2)):
                            out_member_ships[list[0]] = 1
                            flag = True
                            break
                        elif (val == list[2+k]) and (k == 3) and (list[2+k] == list[2+k - 1]):
                            out_member_ships[list[0]] = 1
                            flag = True
                            break
                        elif (k != 3) and (val > list[2+k]) and (val < list[2+k + 1]):
                            m = (ones_and_zeros_trap[k + 1] - ones_and_zeros_trap[k]) / (
                                    list[2+k + 1] - list[2+k])
                            c = ones_and_zeros_trap[k] - (m * list[2+k])
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
    for i in range(len(rule1)):
        rule = rule1[i]
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

    for i in out:
        var = i[0]
        if i[1] == "TRI":
            centroids[var] = sum(i[2:]) / 3
        else:
            centroids[var] = sum(i[2:]) / 4
    keys = list(values.keys())
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
    output_file.write(f"The predicted {name} is {k} ({mean})\n")




# MAIN:

f = open("input.txt")
file_input = ""
for line in f:
    file_input+=line
file_input = file_input.split("\n")
test = []
for ele in file_input:
    test.append(ele.split(" "))
line_counter = 0
temp_par1 = []

while(line_counter < len(test)):
    if test[line_counter] == ['1']:
        output_file.write("Enter the variable’s name, type (IN/OUT) and range ([lower, upper]): (Press x to finish)\n")
        line_counter+=1
        while(test[line_counter] != ['2'] and test[line_counter] != ['3'] and test[line_counter] != ['4'] and test[line_counter]!=['x']):
            add_variables(test[line_counter])
            line_counter+=1
    elif test[line_counter] == ['2']:
        output_file.write("Enter the variable’s name: \n--------------------------\n")
        output_file.write("Enter the fuzzy set name, type (TRI/TRAP) and values: (Press x to finish)\n"
              "-----------------------------------------------------\n")
        temp_list_fuzz = []
        line_counter+=1
        v = "".join(test[line_counter])
        #output_file.write(test[line_counter])
        t = fuzzy_sets(v, test[line_counter + 1])
        temp_list_fuzz.append(t)
        #output_file.write(test[line_counter+1])
        line_counter+=2

        while(test[line_counter] != ['1'] and test[line_counter] != ['3'] and test[line_counter] != ['4'] and test[line_counter]!=['2'] and test[line_counter] != ['x']):
            t = fuzzy_sets(v, test[line_counter])
            temp_list_fuzz.append(t)
            line_counter+=1
        fuzzy_list[v] = temp_list_fuzz
    elif(test[line_counter]== ['3']):
        output_file.write("Enter the rules in this format: (Press x to finish)\n"
              "IN_variable set operator IN_variable set => OUT_variable set\n"
              "------------------------------------------------------------\n")
        line_counter += 1
        while (test[line_counter] != ['2'] and test[line_counter] != ['3'] and test[line_counter] != ['4'] and test[line_counter] != ['x']):
            inference_rules(test[line_counter])
            line_counter += 1
    elif(test[line_counter]==['4']):
        if fuzzy_list == {} or var_list == []:
            output_file.write("CAN’T START THE SIMULATION! Please add the fuzzy sets and rules first.\n")
            continue
        output_file.write("Enter Crisp values: \n")
        line_counter+=1
        crisp_list = []
        while (test[line_counter] != ['2'] and test[line_counter] != ['3'] and test[line_counter] != ['4'] and test[line_counter] != ['x']):
            x = ''.join(test[line_counter])
            x = int(x)
            crisp_list.append(x)
            line_counter+=1
        crisp_values(crisp_list)
        inference()
        weighted_average()

    line_counter+=1

f.close()
output_file.close()