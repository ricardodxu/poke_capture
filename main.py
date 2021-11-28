'''
a simple program calculate capture rate for Pokemon in 4th the generation
formula from: https://wiki.52poke.com/zh-hans/%E6%8D%95%E8%8E%B7%E7%8E%87
'''
import requests

def calc_B_weight(ball_weight, status_weight, health_weight, poke_weight):
    B_weight = 1.0 * health_weight * ball_weight *\
               status_weight * poke_weight
    return B_weight

def calc_G_weight(B_weight):
    G_weight = 1048560.0/((16711680/B_weight) ** 0.25)
    return G_weight

def calc_rate_(B_weight):
    if B_weight >= 255:
        return 1.0
    G_weight = calc_G_weight(B_weight)
    cap_rate = (G_weight/65535) ** 4
    return min(1, cap_rate)

def calc_rate(ball_weight, status_weight, health_weight,\
              poke_weight):
    B_weight = calc_B_weight(ball_weight, status_weight,\
              health_weight, poke_weight)
    cap_rate = calc_rate_(B_weight)
    return cap_rate



if __name__ == "__main__":
    # pre load balls data 
    balls = {
             1: ["精灵球", 1, 1, "精灵球"],
             2: ["超级球", 1.5, 1.5, "超级球"],
             3: ["高级球", 2, 2, "高级球"],
             4: ["大师球", 255, 255, "大师球"],
             5: ["狩猎球", 1.5, 1.5, "只在狩猎地带使用"],
             6: ["捕网球", 1, 3, "3: 水/虫 1: 其他"],
             7: ["计时球", 1, 4, "最大4(30回合) 最小1"],
             7: ["黑暗球", 1, 3.5, "3: 洞窟/黑夜 1: 其他"],
             8: ["先机球", 1, 4, "4: 第一回合 1: 其他"],
            }

    # pre load status data
    status = {
             0: ["无", 1],
             1: ["冰冻", 2],
             2: ["睡眠", 2],
             3: ["中毒", 1.5],
             4: ["灼伤", 1.5],
             5: ["麻痹", 1.5],
            }

    # use the middle value of 帝牙卢卡 at lv 50
    # assume curr hp == 1
    health = 183.5
    # health_weight = 1
    health_weight = (3 * health - 2 * 1)/(3 * health)
    
    
    
    print("请输入宝可梦图鉴编号：")
    poke_id = input()
    r = requests.get("https://pokeapi.co/api/v2/pokemon-species/"+poke_id+"/")
    poke_data = r.json()
    


    print("请确认精灵球类型：")
    for key, value in balls.items():
        print("\t{}:{}\t\t描述: {}".format(key, value[0], value[3]))
    ball_id = int(input())
    ball_data = balls[ball_id]
    print("\t{} \t\t最小值: {}\t\t最大值: {}\t\t".format(\
         ball_data[0], ball_data[1], ball_data[2]))
    

    print("请确认宝可梦状)态类型：")
    for key, value in status.items():
        print("\t{}:{} {}".format(key, value[0], value[1]))
    status_id = int(input())
    status_data = status[status_id]


    upper_bound = calc_rate(ball_data[1], status_data[1],\
                            health_weight, float(poke_data["capture_rate"]))
    lower_bound = calc_rate(ball_data[2], status_data[1],\
                            health_weight, float(poke_data["capture_rate"]))


    # print(poke_data["names"][10]["name"])
    # print(poke_data["capture_rate"])
    print("图鉴id:\t{}\n名称:\t{}\n精灵球:\t{}\n状态:\t{}\n最小成功率:\t{}\n最大成功率:\t{}".\
            format(poke_id, \
                   poke_data["names"][10]["name"],\
                   ball_data[0],\
                   status_data[0],
                   lower_bound, upper_bound))
    print("备注: " + ball_data[3])