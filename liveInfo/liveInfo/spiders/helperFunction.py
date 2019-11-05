import re

def trimString(lineUp):
    result = []
    checkSymbol = re.compile('[_!#$%^*<>?/\|}{~:]')
    for line in lineUp:
        line = line.strip()
        if "■" in line:
            line = line.replace("■", "")
            result.append(line)
        else:
            result.append(line)
        # if(checkSymbol.search(line) == None):
        #     print("good", line)
        # else:
        #     print("bad", line)
    return result
    # for item in list:
    #     if(item.find("/")):
    #         item = item.split("/")
    #     if(item.find("■")):
    #         item = item.replace("■", "")
    #     item = item.strip()
    #     result.append(item)
    # print(result)
    return result