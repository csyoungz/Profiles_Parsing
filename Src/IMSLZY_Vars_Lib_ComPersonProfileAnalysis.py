#coding:utf-8

"""
    Title: IMSLZY_Vars_Lib_CompersonProfileAnalysis.py
    Des:
        存放使用到的全局变量，只读，不修改。
    Date: 2016.03.24
    
"""

TEST_PERSON_NUM = 500

# To Text or Markdown.
If_MarkDown_Choice = 1
Need_WorkingTime = 0
Show_Profile_Sents = 1
Show_Profile_Str = 0
Cur_Year = 2015
Cur_CompanyName = u""
Cur_PersonName = u""
MIN_TIMEEXP_LEN = 3 # 判断数量词是否为有效的时间表达，设置的最小长度，即"第一届"被视为非时间表达。
TIME_GAP_LIMIT = 4
# Set Org Ends Syns;
# “公司”分割；
OrgName_Ends_List = [u"分行", u"有限公司", u"公司", u"本公司", u"）", u")", u"厂", u"设备厂", u"总厂",  u"集团", u"会社", u"支行",
                     u"分行", u"银行", u"事务所", u"学会", u"委员会", u"委",
                     u"协会", u"大学", u"小学", u"司", u"局", u"某局", u"地矿局", u"有限", u"网易", u"网", u"在线", u"香港立法会", u"非线" , u"》", u">>", u"供销社", u"煤矿", u"研究所", u"中心"]    # 实例表明，此处公司简称的结束符也是有顺序的。

# 人工筛选公司名
Editable_Org_Names_List = [u"谷歌中国"]

OrgName_Ends_List = Editable_Org_Names_List + OrgName_Ends_List

Invalid_Org_Names_List = [u"参加", u"项目"]

Hidden_Time_Syn_List = [u"现任", u"曾", u"曾任", u"曾任职", u"历任", u"目前", u"先后", u"就任", u"兼任", u"就职于", u"兼职情况"]
Basic_info_Syn_List = [u"出生", u"岁", u"毕业", u"学历", u"国籍", u"汉族", u"攻读", u"硕士",u"大专", u"工商管理学士", u"就读", u"男", u"女"]


PreWorking_Org_Tips_List = [u"任职于", u"曾任职", u"任职於", u"工作于", u"供职于", u"入", u"创办", u"创建", u"就职于", u"创立"] # 提示下文，是纯粹的 机构名；
Org_Name_Start_Syn_List = [u"加入", u"进入", u"入", u"创办", u"创建", u"创立", u"任职", u"就职",
                           u"担任", u"出任", u"任", u"兼任",  u"任教于", u"于",u"在", u"系", u"是", u"为",
                           u"起任", u"创建", u"加盟", u"组建"] # 处理中文，尽可能都转成unicode，len是文字个数，那么，当中英文混合？ 提示下文，为[机构+职称];

Department_Name_List = [u"实验室", u"设计室", u"生产科", u"办公厅", u"秘书处", u"视讯部", u"大客户部", u"资产管理部", u"研究发展部", u"事业部",
                        u"供应部", u"行政部", u"运输部", u"财务处", u"技术部", u"市场部", u"质检部", u"标准化部",
                        u"研发部", u"财务部", u"财务科", u"销售经理", u"投融资", u"信息中心", u"董事",
                        u"监事会", u"董事会", u"分公司", u"博士生", u"党总支",
                        u"总经理", u"副总经理", u"总经理助理", u"发行人", u"监事会主席", u"人力资源",
                        u"机修车间", u"项目技术", u"副大队长", u"教授级", u"副主任"]  # 当 Org为此时，Org为空，Pos = Org + Pos;

# 当Org首字开头词性在其中，则否定。
No_OrgName_Start_Pos_List = [u"v", u"c", u"p"]

Person_Profile_Data_Init = {
    "Person_Basic_Info":
        {
            "Name": "Yang Zhang",
            "Birth": "",
            "Gender": "",
            "Country": "",
            "Nationality": "",
            "Degree": "",
            "School": ""
        },
    "Person_CurWork_Info":
    #  str: time_str, dict: org + job
        []
    }
