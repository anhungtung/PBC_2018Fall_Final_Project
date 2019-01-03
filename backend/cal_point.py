
def cal_point(data):
    myr = {'衛生':0,'住宅安寧':0,'交通安全':0,'住宅安全':0}
    for i in data:
        if "清" in i['派工項目']:
            myr['衛生'] += 1
        elif "噪音"in i["派工項目"]:
            myr['住宅安寧'] += 2   
        elif "路" in i['派工項目']:
            myr["交通安全"] += 1
        elif "海砂屋" in i['派工項目']:
            myr['住宅安全'] += 1    
        else:
            pass
    return myr
