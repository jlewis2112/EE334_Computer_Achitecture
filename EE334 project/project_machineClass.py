key = {'0':"0000", '1':"0001", '2':"0010", '3':"0011", '4':"0100", '5':"0101", '6':"0110", '7':"0111", '8':"1000", '9':"1001", 'a':"1010", 'b':"1011", 'c':"1100", 'd':"1101", 'e':"1110", 'f':"1111"}
instructions = []


BTB = {} #{entre : [PC, Target, Prediction]}

#scan the instructions
def scan():
    item_list = open("Espresso_int.txt", "r+")
    count = 1
    line = item_list.readline()
    line2 = item_list.readline()
    while line2:
        instructions.append(line[0:-1])
        line = line2
        line2 = item_list.readline()
        count += 1

#convert str(hex) to int
def determine_int(a):
    result = 0
    c = 23
    d = 0
    try:
        b = key[a[0]] + key[a[1]] + key[a[2]] + key[a[3]] + key[a[4]] + key[a[5]]
    except:
        return 0
    while c >= 0:
        if b[c] == '1':
            result += (2**d)
        c -= 1
        d += 1
    return result

#determine entry value
def determine_entry(a):
    c = 9
    d = 0
    result = 0
    try:
        b = key[a[3]]+key[a[4]]+key[a[5]]
    except:
        print("error")
    while c >= 0:
        if b[c] == '1':
            result += (2**d)
        c -= 1
        d += 1
    return result

#determines if a pC is in the btb
def in_BTB(PC_current):
    for x in BTB.keys():
        if BTB[x][0] == PC_current:
            return True
    return False

#updates the state of a BTB entry
def state_update(pred, taken):
    result = pred
    if pred == "00":
        if taken == False:
            result = "01"
    elif pred == "01":
        if taken == True:
            result = "00"
        elif taken == False:
            result = "10"
    elif pred == "11":
        if taken == True:
            result = "10"
    elif pred == "10":
        if taken == True:
            result = "01"
        elif taken == False:
            result = "11"
    return result

#determines the prediction
def det_prediction(pred):
    if pred == "00" or pred == "01":
        return True
    return False



def main():
    x=0
    y=1
    Ic = 0
    Hit = 0
    Miss = 0
    Right = 0
    Wrong = 0
    B_Taken = 0
    Wrong_addr = 0
    Collision = 0
    scan()
    while y < len(instructions):
        if in_BTB(instructions[x]) == False:#PC not in btb
            if determine_int(instructions[x]) != (determine_int(instructions[y])-4):
                Miss += 1
                B_Taken += 1
                Entry = str(determine_entry(instructions[x]))
                if Entry in BTB.keys():
                    Collision += 1
                    new_pred = state_update(BTB[Entry][2], True)
                    BTB[Entry] = [instructions[x], instructions[y], new_pred]
                else:
                    BTB[Entry] = [instructions[x], instructions[y], "00"]
        elif in_BTB(instructions[x]) == True:#PC in btb
            Hit += 1
            Entry = str(determine_entry(instructions[x]))
            if det_prediction(BTB[Entry][2]) == True: #if prediction is taken
                if BTB[Entry][1] == instructions[y]:
                    Right += 1
                    B_Taken += 1
                    new_pred = state_update(BTB[Entry][2], True)
                    BTB[Entry] = [instructions[x], instructions[y], new_pred]
                else:
                    Wrong += 1#wrong target
                    if determine_int(instructions[x]) != (determine_int(instructions[y])-4):#is a branch taken
                        Wrong_addr += 1
                        B_Taken += 1
                        new_pred = state_update(BTB[Entry][2], True)
                        BTB[Entry] = [instructions[x], instructions[y], new_pred]
                    else:
                        new_pred = state_update(BTB[Entry][2], False)
                        BTB[Entry][2] = new_pred
            elif det_prediction(BTB[Entry][2]) == False:#if prediction is not taken
                if determine_int(instructions[x]) == (determine_int(instructions[y])-4):#is the branch taken
                    Right += 1
                    new_pred = state_update(BTB[Entry][2], False)
                    BTB[Entry][2] = new_pred
                else:
                    Wrong += 1
                    B_Taken += 1
                    new_pred = state_update(BTB[Entry][2], True)
                    BTB[Entry] = [instructions[x], instructions[y], new_pred]
        Ic += 1
        x += 1
        y = x + 1
    Ic += 1
    out = open("BTB.txt", "w")
    out.write("entry    PC   Target  Prediction\n")
    entry_sort = []
    for i in BTB.keys():
        entry_sort.append(int(i))
    for x in sorted(entry_sort):
        out.write(str(x) + "    " + BTB[str(x)][0] + "    " + BTB[str(x)][1] +"    " + BTB[str(x)][2] + "\n")
    print("instruction count = " + str(Ic))
    print("number of hits = " + str(Hit))
    print("number of misses= " + str(Miss))
    print("number of correct predictions= " + str(Right))
    print("number of wrong predictions= " + str(Wrong))
    print("number of taken branches= " + str(B_Taken))
    print("number of collisions= " + str(Collision))
    print("number of wrong address predictions= " + str(Wrong_addr))
    hit_rate = float(Hit)/(float(Hit) + float(Miss))
    print("hit rate = " + str(hit_rate))
    pred_acc = float(Right)/float(Hit)
    print("prediction accuracy = " + str(pred_acc))
    inc_add = float(Wrong_addr)/float(Wrong)
    print("incorrect address = " + str(inc_add))





main()