#coding:utf-8
from datetime import datetime

#价格用字典表示，每个点的价钱不同，时刻为K
weekdayprice={9:30,10:30,11:30,12:50,13:50,14:50,15:50,16:50,17:50,18:80,19:80,20:60,21:60}
weekendprice={9:40,10:40,11:40,12:50,13:50,14:50,15:50,16:50,17:50,18:60,19:60,20:60,21:60}

#场地的使用情况用字典表示，场地为K，预约情况用value二维矩阵表示
#如：{'A': [['2017-08-05', '09:00~11:00', 'U005', 1, 80], ['2017-08-05', '12:00~14:00', 'U001', 1, 100]], 'C': [], 'B': [], 'D': []}
site_list={}
site_list['A']=[]
site_list['B']=[]
site_list['C']=[]
site_list['D']=[]

#循环输入直至无输入结束
while 1:
    s1=raw_input()
    if s1!='':
        s=s1.split()

    #1/检查用户输入是否为有效字符串，有效返回True
        # 不是整点 + 时间超出 + CANCEL标志不是C字符 + 场地不在ABCD内
    	def check_valid(username,date,time,site,cancel='C'):
            if time[3] != '0' and time[4] != '0' and time[9] != '0' and time[10] != '0':
                return False
            if int(time[0:2]) >= int(time[6:8]) or int(time[6:8])>22 or int(time[0:2])<9:
                return False
            if cancel!='C':
                return False
            if site not in ['A','B','C','D']:
                return False
            return True

    #2/检查时间是否冲突：参数（字符串，场地字典），冲突返回True
        # （先确定场地，再确定场地的预约中的日期是否同一天，再确定时间是否有重叠）
        def time_conflict(s,sited):
            if sited.has_key(s[3]):
                for v in sited[s[3]]:
                    if v[3]==1:
                        if v[0]==s[1]:
                            if v[1][0:2]<=s[2][0:2]<v[1][6:8] or v[1][0:2]<s[2][6:8]<=v[1][6:8]:
                                return True
            return False

    #3/ 取消预约：参数（字符串，场地字典，周几），取消成功返回True，返回False说明订单不存在
        # （先限制仅在该场地的列表中的tag=1，即预约成功的订单中查找对比，对比成功后将tag=0，表示已失效订单，并计算违约金）
        def cancel_done(s,site_list,week):
            for l in site_list[site]:
                if l[3]==1:
                    if s[1]==l[0]:
                        if s[2] ==l[1]:
                            if s[0]==l[2]:
                                l[3]=0
                                if week <= 4:
                                    # 工作日交违约金50%，周末25%
                                    l[4] = l[4] / 2
                                else:
                                    l[4] = l[4] / 4
                                return True
            return False

    #4/ 计算价钱：参数（输入字符，周几），返回价格
        # 设置开始和结束时间a,b，将（a,b）对应的每小时价格累加
        def price(s,week):
            pri=0
            a = int(s[2][6:8])
            b = int(s[2][0:2])
            if week<=4:
                for k in range(b,a):
                    pri+=int(weekdayprice[k])
            else:
                for k in range(b,a):
                    pri+=int(weekendprice[k])
            return pri

    #5/ 收入汇总：计算与输出
        def list(l):
            total=0
            print '收入汇总'
            print '-------'
            for key in ['A','B','C','D']:
                print '场地：'+key
                if l[key]:
                    sl=sorted(l[key])
                    for v in sl:
                        sum=0
                        if int(v[3])==1:
                            print v[0]+' '+v[1]+' '+str(v[4])+'元'
                            sum+=v[4]
                        else:
                            print v[0]+' '+v[1]+' '+'违约金'+str(v[4])+'元'
                            sum += v[4]
                        total+=sum
                    print '小计：' + str(sum)+'\n'
                else:
                    print '小计：0元\n'
            print '-------'
            print '总计：'+str(total)

        # 1 四位长的输入作为预订处理:
    	if len(s)==4:
    	    username,date,time,site=s
            week = datetime.strptime(date, '%Y-%m-%d').weekday()
            # 1 / 检测输入的有效性
            if not check_valid(username,date,time,site):
                print 'Error:the booking is invalid'
            else:
                # 2 / 是否有时间冲突
                if time_conflict(s,site_list):
                    print 'Error:the booking is conflict with others'
                    continue
                else:
                    print 'Success: the booking is accepted!'
                    # 3 / 计算价格
                    pri=price(s,week)
                    # 4 /添加场地预约条目到场地列表
                    site_list[site].append([date,time,username,1,pri])
            print site_list

        # 2 五位长的输入作为取消订单处理:
        elif len(s)==5:
            username, date, time, site,cancel=s
            # 1 / 检测输入的有效性
            week = datetime.strptime(date, '%Y-%m-%d').weekday()
            if not check_valid(username,date,time,site,cancel):
                print 'Error:the cancel command is invalid'
            else:
                if site_list:
                    # 2 / 先查看清单里是否有该条目
                    if cancel_done(s,site_list,week):
                        print 'Success: the booking is cancelled!'
                    else:
                        print 'Error:the booking is not exist'
                else:
                    print 'Error:the booking is not exist'

        # 3 其他长度无效
        else:
            print 'Error:the form ofcommand is wrong'
    else:
        #停止输入后输出收入列表
        list(site_list)
    	break
