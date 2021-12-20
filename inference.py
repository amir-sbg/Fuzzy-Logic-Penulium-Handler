import re


# def result_maker(rule,)

def rule_handler(rule_str):
    conditions, result = rule_str.split("THEN")
    conditions, result = conditions[3:-1], result[result.find("IS") + 3:]
    return conditions, result


def read_fuzzy_rules_data():
    data_file = open("controllers/complex.fcl", 'r')
    counter = 1
    rules = []
    last = ""
    for line in data_file.readlines():
        if (counter >= 69 and counter <= 139):
            if "RULE" in line:
                rule_inLine = last.replace("\n", " ").replace("\t", " ").replace("    ", " ").replace("  ", " ")
                if len(rule_inLine) > 3:
                    conditions, result = rule_handler(rule_inLine[rule_inLine.find(":") + 2:rule_inLine.find(";")])
                    rules.append([conditions, result])
                last = line
            else:
                last += line

            # if "\n" != line:
            #  parts=line.split("AND")
            #  first_con= parts[0][parts[0].find("(")+1:parts[0].find(")")].split(" IS ")
            #  second_con= parts[1][parts[1].find("(")+1:parts[1].find(")")].split(" IS ")
            #  parts[1]=parts[1].split("THEN")[1]
            #  res_con= parts[1][1:parts[1].find(";")].split(" IS ")
            #  and_rules.append([first_con,second_con,res_con])

        counter += 1
    return rules


def rule_result(conditions, fuzzy_cp, fuzzy_cv, fuzzy_pa, fuzzy_pv):
    result = 0
    terms = []
    while "IS" in conditions:
        condition = conditions[conditions.find("(") + 1:conditions.find(")")]
        terms.append(condition)
        conditions = conditions.replace("(" + condition + ")", '')
    if len(terms) == 2:
        result = min(fuzzy_pa[terms[0].split(" ")[2]], fuzzy_pv[terms[1].split(" ")[2]])

    elif len(terms) == 3:
        a1t1 = fuzzy_pa[terms[0].split(" AND ")[0].split(" ")[2]]
        a1t2 = fuzzy_pv[terms[0].split(" AND ")[1].split(" ")[2]]
        a2t1 = fuzzy_pa[terms[1].split(" AND ")[0].split(" ")[2]]
        a2t2 = fuzzy_pv[terms[1].split(" AND ")[1].split(" ")[2]]
        a3t1 = fuzzy_pa[terms[2].split(" AND ")[0].split(" ")[2]]
        a3t2 = fuzzy_pv[terms[2].split(" AND ")[1].split(" ")[2]]
        result = max(min(a1t1, a1t2), min(a2t1, a2t2), min(a3t1, a3t2))

    return result

def result_of_rules(rules, fuzzy_cp, fuzzy_cv, fuzzy_pa, fuzzy_pv):
    results = []
    for rule in rules:
        results.append([rule[1], rule_result(rule[0], fuzzy_cp, fuzzy_cv, fuzzy_pa, fuzzy_pv)])
    return results

#
# for i in read_fuzzy_rules_data():
#     print i
