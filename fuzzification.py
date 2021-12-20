def line_spliter(line, dict_range):
    line = str(line).split("=")
    Term = line[0][:-2].split(" ")[1]
    line = line[1][1:-2].split(") (")
    try:
        start = tuple(map(float, line[0].replace(" ", "")[1:].split(",")))
        med = tuple(map(float, line[1].replace(" ", "").split(",")))
        end = tuple(map(float, line[2].replace(" ", "")[:-1].split(",")))
    except:
        if len(dict_range.keys()) == 0:
            # start = tuple(map(float, line[0].replace(" ", "")[1:].split(",")))
            med = tuple(map(float, line[0].replace(" ", "")[1:].split(",")))
            end = tuple(map(float, line[1].replace(" ", "")[:-1].split(",")))
        else:
            # start = tuple(map(float, line[0].replace(" ", "")[1:].split(",")))
            med = tuple(map(float, line[1].replace(" ", "")[:-1].split(",")))
            end = tuple(map(float, line[1].replace(" ", "")[:-1].split(",")))

    dict_range[Term] = [start, med, end]
    return Term, start, med, end


def read_fuzzy_map_data():
    data_file = open("controllers/complex.fcl", 'r')
    cp_range, cv_range, pa_range, pv_range, force_range = {}, {}, {}, {}, {}
    counter = 1
    for line in data_file.readlines():
        if (counter >= 16 and counter <= 25):
            line_spliter(line, pa_range)
        elif (counter >= 29 and counter <= 33):
            line_spliter(line, pv_range)
        elif (counter >= 37 and counter <= 41):
            line_spliter(line, cp_range)
        elif (counter >= 45 and counter <= 49):
            line_spliter(line, cv_range)
        elif (counter >= 53 and counter <= 57):
            line_spliter(line, force_range)
        counter += 1
    return cp_range, cv_range, pa_range, pv_range, force_range


def fuzzy_inference(ranges, world_num):
    if world_num < ranges[1][0]:
        # print "1"
        x1, x2, y1, y2 = ranges[0][0], ranges[1][0], ranges[0][1], ranges[1][1]
    else:
        # print "2"
        x1, x2, y1, y2 = ranges[2][0], ranges[1][0], ranges[2][1], ranges[1][1]
    # print x1, x2, y1, y2
    # print "fuzzzzy--------",(((y1 - y2 ) / (x1 - x2)) * (world_num - x1) )+ y1

    return (((y1 - y2 ) / (x1 - x2)) * (world_num - x1) )+ y1


def fuzzification_one(dict_range, world_num):
    # print "world_num",world_num
    fuzzy_dict = {}
    for key in dict(dict_range).keys():
        # print "----------------->>>>>>>>>",key
        if dict_range[key][0][0] > world_num or dict_range[key][2][0] < world_num:
            # print "->>>> NO   ",dict_range[key],dict_range[key][0][0]
            fuzzy_dict[key] = 0
        else:
            # print "->>>> YES   ",dict_range[key],dict_range[key][0][0]
            fuzzy_dict[key] = fuzzy_inference(dict_range[key], world_num)
    return fuzzy_dict


def fuzzification_all(cp_range, cv_range, pa_range, pv_range, world):
    fuzzy_cp = fuzzification_one(cp_range, world['cp'])
    fuzzy_cv = fuzzification_one(cv_range, world['cv'])
    fuzzy_pa = fuzzification_one(pa_range, world['pa'])
    fuzzy_pv = fuzzification_one(pv_range, world['pv'])

    return fuzzy_cp, fuzzy_cv, fuzzy_pa, fuzzy_pv
