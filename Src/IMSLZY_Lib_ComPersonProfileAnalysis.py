#coding:utf-8
'''
#########################################
#   Title:ZyTestPyReg.py
    Function:
        测试正则表达式，进行规则化人物信息提取。
    Date:2016.01.12
#########################################
'''
import re
import jieba
import jieba.posseg as pseg
import sys
import copy

# File Coding.
# print "Old File Encoding = ",sys.getfilesystemencoding()
reload(sys)
sys.setdefaultencoding("utf-8")
# print "New File Encoding = ",sys.getfilesystemencoding()

# PersonProfileFilename = "PersonProfileData.txt"
# PersonProfileFilename = "PersonProfileDataDir/PersonProfile_0121_DataClean.txt"

PersonProfileFilename = "PersonProfileDataDir/PerProWithName_0128_3.txt"
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
TIME_GAP_LIMIT = 6
# Set Org Ends Syns;
# “公司”分割；
OrgName_Ends_List = [u"分行", u"有限公司", u"公司", u"本公司", u"）", u")", u"厂", u"设备厂", u"总厂",  u"集团", u"会社", u"支行",
                     u"分行", u"银行", u"事务所", u"学会", u"委员会", u"委",
                     u"协会", u"大学", u"小学", u"司", u"局", u"某局", u"地矿局", u"有限", u"网易", u"网", u"在线", u"香港立法会", u"非线" , u"》", u">>", u"供销社", u"煤矿", u"研究所", u"中心"]    # 实例表明，此处公司简称的结束符也是有顺序的。

# 人工筛选公司名
Editable_Org_Names_List = [u"谷歌中国"]

OrgName_Ends_List = Editable_Org_Names_List + OrgName_Ends_List

Invalid_Org_Names_List = [u"参加", u"项目"]

Hidden_Time_Syn_List = [u"现任", u"曾", u"曾任", u"曾任职", u"历任", u"目前", u"先后", u"就任", u"兼任"]
Basic_info_Syn_List = [u"出生", u"岁", u"毕业", u"学历", u"国籍", u"汉族", u"攻读", u"硕士",u"大专", u"工商管理学士", u"就读", u"男", u"女"]


PreWorking_Org_Tips_List = [u"任职于", u"曾任职", u"任职於", u"工作于", u"供职于", u"入", u"创办", u"创建", u"就职于", u"创立"] # 提示下文，是纯粹的 机构名；
Org_Name_Start_Syn_List = [u"加入", u"进入", u"入", u"创办", u"创建", u"创立", u"任职", u"就职",
                           u"担任", u"出任", u"任", u"兼任",  u"任教于", u"于",u"在", u"系", u"是", u"为",
                           u"起任", u"创建", u"加盟", u"组建"] # 处理中文，尽可能都转成unicode，len是文字个数，那么，当中英文混合？ 提示下文，为[机构+职称];
 
Department_Name_List = [u"实验室", u"生产科", u"办公厅", u"秘书处", u"视讯部", u"大客户部", u"资产管理部", u"研究发展部", u"事业部",
                        u"供应部", u"行政部", u"运输部", u"财务处", u"技术部", u"市场部", u"质检部", u"标准化部",
                        u"研发部", u"财务部", u"财务科", u"销售经理", u"投融资", u"信息中心", u"董事",
                        u"监事会", u"董事会", u"分公司", u"博士生", u"党总支",
                        u"总经理", u"副总经理", u"总经理助理", u"发行人", u"监事会主席", u"人力资源",
                        u"机修车间", u"项目技术", u"副大队长"]  # 当 Org为此时，Org为空，Pos = Org + Pos;

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

Person_Profile_Data = copy.deepcopy(Person_Profile_Data_Init)   # 字典Dict类型数据，初始为空，后更新。


def TestDataTransUsingJson():
    # Test Load and dump data using json.
    global Person_Profile_Data
    print Person_Profile_Data
    return Person_Profile_Data
    pass


def DumpJsonData():
    """
        Function: 返回个人信息数据，为字典Dict类型。
        return: Person_Profile_Data, Dict 类型，包含更新后的个人信息结构化数据信息。
    """

    global Person_Profile_Data
    return Person_Profile_Data
    pass


def get_pseg_seq(str_content):
    """
    :param str_content:
    :return: two list, list of words + list of POS.
    """
    str_content = ChangeUnicode(str_content)
    content_words_seq = list()
    content_pos_seq = list()
    pseg_seq = pseg.cut(str_content)
    for w_id, w in enumerate(pseg_seq):
        content_words_seq.append(w.word)
        content_pos_seq.append(w.flag)
    return content_words_seq, content_pos_seq



def Check_GenderCall(gender_call_tip):
    # 统一性别称呼，先生变为男，女士变为女；
    if gender_call_tip == u"先生":
        return u"男"
    if gender_call_tip == u"女士":
        return u"女"
    return gender_call_tip


def Check_BirthInfo(birth_age_str):
    # 统一出生，将岁数统一为出生年
    if u"岁" in birth_age_str:
        birth_age_str_cutlist = pseg.cut(birth_age_str)
        for birth_age_item in birth_age_str_cutlist:
            if birth_age_item.flag == 'm':
                return ChangeUnicode(str(Cur_Year - int(birth_age_item.word))) + u"年"
    return birth_age_str
    pass


def PostCut_Symbol_function(now_index, next_index, postag_pos_seq):
    """
    :param now_index: 起始Post_words 索引位置；
    :param next_index: 下一个 时间表达索引位置；
    :param postag_pos_seq: 词序列；
    :return: 当前时间表达终点；

    Des:
        在当前时间表达开始索引之后，找到终结位置 = min(下一时间表达开始， 符号)
    """
    syn_end_index = now_index
    while syn_end_index < len(postag_pos_seq) and postag_pos_seq[syn_end_index] != 'x':
        syn_end_index += 1
    # return  min(next_index, syn_end_index)
    return  next_index


# 后修饰，保证时间表达式最后以符号结尾;
def PostCut_Symbol_function_Backup(end_index, postag_pos_seq):
    """函数：向前截断，找到最近的一个标点符号。
        Input: 我是中国人，你呢
        Output: 我是中国人
        """
    sym_end_index = end_index
    while postag_pos_seq[sym_end_index] != 'x' and sym_end_index >= 0:
        sym_end_index -= 1
        pass
    return sym_end_index
    pass



def LoadShowJsonData(Person_Profile_Data):
    # 测试单个人物信息数据结构，Dict类型，逐个输出显示。
    print "**********Show Dict&Json Data.**********"
    print "Basic Info"
    Basic_info_keynames = ["Name", "Birth", "Gender",
                           "Country", "Degree", "School"]

    for basic_info_key in Basic_info_keynames:
        print "\t", basic_info_key, Person_Profile_Data["Person_Basic_Info"][basic_info_key]
        pass
    print "Working Exp"
    if len(Person_Profile_Data["Person_CurWork_Info"]) > 1:
        for person_curwork_info in Person_Profile_Data["Person_CurWork_Info"]:
            if type(person_curwork_info) == dict:
                print "\t\t Org = ", person_curwork_info["Org"], " Job = ", person_curwork_info["Job"]
            elif type(person_curwork_info) == unicode:
                print "\t Time = ", person_curwork_info
            pass
    pass


def Check_IF_WorkingSent(WorkingSent):
    """函数：检测是否可能是描述工作的句子，条件宽松。"""
    Maybe_Working_WordsList = [u"现任", u"曾任", u"担任", u"任职", u"历任", u"兼任", u"任", u"兼", u"工作", u"经理", u"董事", u"监事", u"部长", u"委员", u"会长", u"秘书长", u"处长", u"工程师"]
    for maybe_working_word in Maybe_Working_WordsList:
        if maybe_working_word in WorkingSent:
            return True
            pass
        pass
    return False
    pass


# 检测表示时间的序列: Input: list of pos, Out:list of tuple(time start, time end)
def CheckTimePos(PosSeq):
    # print "Into Checking Time Pos."
    TimeSeqStart = []
    TimeSeqEnd = []
    InTimeFlag = False
    t_id_start = -1
    t_id_end = -1
    for pos_id, pos_tag in enumerate(PosSeq):
        # set start
        if (pos_id == 0 or PosSeq[pos_id - 1] != 'm') and pos_tag == 'm':
            TimeSeqStart.append(pos_id)
            pass
        # set end.
        if pos_tag == 'm' and ((pos_id == len(PosSeq) - 1) or (PosSeq[pos_id + 1] != 'm')):
            TimeSeqEnd.append(pos_id)
            pass
        pass
    # print "Time start seq = ", TimeSeqStart, "Time end seq = ", TimeSeqEnd
    # 时间模式处理：如果两个时间表达相距很近，则进行合并， 保持原来格式；
    if len(TimeSeqStart) != len(TimeSeqEnd):
        print "Wrong Time Seq ", " Time Start len = ", len(TimeSeqStart), " Time End len = ", len(TimeSeqEnd)
        pass
    TimeTupleList = [(TimeSeqStart[time_id], TimeSeqEnd[time_id])for time_id in range(len(TimeSeqStart))]
    TimeTupleList_New = []
    newtime_id = 0
    while newtime_id < len(TimeSeqStart):
        if newtime_id == len(TimeSeqStart) - 1:
            TimeTupleList_New.append((TimeSeqStart[newtime_id], TimeSeqEnd[newtime_id]))
            break
            pass
        if TimeSeqEnd[newtime_id] + TIME_GAP_LIMIT > TimeSeqStart[newtime_id+1]:  # 合并时间
            TimeTupleList_New.append((TimeSeqStart[newtime_id], TimeSeqEnd[newtime_id + 1]))
            newtime_id += 2
            pass
        else:
            TimeTupleList_New.append((TimeSeqStart[newtime_id], TimeSeqEnd[newtime_id]))
            newtime_id += 1
        pass

    # 合并，生成新的时间序列表达.
    if len(TimeSeqStart) > 0:
        #print "Time Seq Old, Start = ",TimeSeqStart," End = ",TimeSeqEnd
        TimeSeqStart = [time_tuple[0] for time_tuple in TimeTupleList_New]
        TimeSeqEnd = [time_tuple[1] for time_tuple in TimeTupleList_New]
        #print "Time Seq New, Start = ",TimeSeqStart," End = ",TimeSeqEnd
        pass
    # print "Into Checking Time Pos."
    # print "Leaving CheckTimePos, Time start seq = ", TimeSeqStart, "Time end seq = ", TimeSeqEnd
    return TimeSeqStart, TimeSeqEnd
    pass


# 字符截取函数：从 任/进入 等词语后进行截取;
def Syn_Cut_Func(Contents):
    if type(Contents) == unicode:
        Start_Syn_List = [u"进入", u"任", u"起任"]  #
        cut_down_syn = u"等"
        pass
    else:
        Start_Syn_List = ["进入", "任", "起任"]  #
        cut_down_syn = "等"

    # 处理中文，尽可能都转成unicode，len是文字个数，那么，当中英文混合？
    '''
    print "Into Contents = ", Contents
    for start_syn in Start_Syn_List:
        if start_syn in Contents:
            #print "Cut Before, Org_Name = ",Org_Name," Org_Name type = ",type(Org_Name)," start_syn type = ",type(orgname_start_syn)
            #print "Start Syn Index = ",Org_Name.index(orgname_start_syn)," len of syn = ",len(orgname_start_syn)," len of Org_Name = ",len(Org_Name)  # 不论中英文，统一unicode形式，不论是中文字还是英文字母，在len时都算作1.
            Contents = Contents[Contents.index(start_syn) + len(start_syn):]
            #print "Cut After, Org_Name = ",Org_Name
            pass
        pass
    '''
    # 出现"等"，则删除下文
    if cut_down_syn in Contents:
        Contents = Contents[:Contents.index(cut_down_syn)]
        pass
    # print "Leaving Contents = ", Contents
    return Contents
    pass


# 后处理机构名, PostProOrgName;
def PostPro_Org_Name(Org_Name):
    """

    :param Org_Name: 待后处理的机构名。
    :return:
    """
    global Cur_CompanyName
    # print "Into Postpro Org Name = ",Org_Name
    # 开始标记：从"进入"之后获取;
    Org_Name = ChangeUnicode(Org_Name)
    Org_Name_Words_Seq, Org_Name_Pos_Seq, Org_Name_Time_Start, Org_Name_Time_End =  Get_Seqs_and_Times(Org_Name)
    native_orgname_start_syn_list = Org_Name_Start_Syn_List + [u"就职", u"现在", u"参加", u"负责"]

    for orgname_start_syn in native_orgname_start_syn_list:
        if orgname_start_syn in Org_Name_Words_Seq:
            print "Into Postpro orgname, start_syn = ", orgname_start_syn, " orgname = ", Org_Name
            #print "Start Syn Index = ",Org_Name.index(orgname_start_syn)," len of syn = ",len(orgname_start_syn)," len of Org_Name = ",len(Org_Name)  # 不论中英文，统一unicode形式，不论是中文字还是英文字母，在len时都算作1.
            Org_Name = Org_Name[Org_Name.index(orgname_start_syn) + len(orgname_start_syn):]
            #print "Cut After, Org_Name = ",Org_Name
            break
            pass
        pass

    # 结束标记：公司。。。。。。
    # “公司”分割；
    for orgname_end in OrgName_Ends_List:
        if orgname_end in Org_Name:
            # print "Post org, orgname end = ", orgname_end
            CompanyIndex = Org_Name.index(orgname_end)
            Org_Name = Org_Name[:CompanyIndex + len(orgname_end)]
            break
            pass
        pass

    # 前向截取: 职位POS 里，"担任"和"任"之后的部分截取;
    org_start_syn_list = [u"担任", u"并任", u"历任", u"任", u"是", u"聘为"]
    Org_Name_WordsSeq = jieba.cut(Org_Name, cut_all = False) # 分词后的 任 分割；
    Org_Name_WordsSeq = [w for w in Org_Name_WordsSeq] #

    for org_start_syn in org_start_syn_list:
        if org_start_syn in Org_Name_WordsSeq:
            Org_Name = ChangeUnicode("".join(Org_Name_WordsSeq[ Org_Name_WordsSeq.index(org_start_syn)+1:])) # 当检测words_seq时，增加的只能是1个单位。
            break
            pass
        pass

    # 去除符号
    Org_Name = re.sub(u"。|\*|-|：|:|；|;|，|,", "", Org_Name)
    # 补充"任"无法分词的问题
    if Org_Name.startswith(u"任") or Org_Name.startswith(u"为"):
        Org_Name = Org_Name[1:]
        pass
    # 指代替换：例如结果是"公司，本公司，股份公司，有限公司"等，则相应替换为所在单位。
    # print "Now cur company = ", Org_Name
    corefer_orgname_list = [u"公司", u"本公司", u"有限公司", u"股份公司", u"本集团"]
    if(Org_Name in corefer_orgname_list) and len(Cur_CompanyName) >= 2:
        Org_Name = Cur_CompanyName


    return Org_Name
    pass


# Function: 任职职位的后处理;
# 要求：...等职务...，等职务之后的内容省略。
def PostPro_Position_Name(Position_Name):
    # 去除'的'等词；
    # print "Into PostPro of Position Name = ", Position_Name
    Position_Name = ChangeUnicode(Position_Name)
    Position_Name = re.sub(u"的|。|同时|期自|我们|；","",Position_Name)

    # 前向截取: 职位POS 里，"担任"和"任"之后的部分截取;
    pos_start_syn_list = [u"担任", u"并任", u"历任", u"任", u"是"]
    Position_Name_WordsSeq = jieba.cut(Position_Name, cut_all = False) # 分词后的 任 分割；
    Position_Name_WordsSeq = [w for w in Position_Name_WordsSeq] #

    for pos_start_syn in pos_start_syn_list:
        if pos_start_syn in Position_Name_WordsSeq:
            Position_Name = ChangeUnicode("".join(Position_Name_WordsSeq[ Position_Name_WordsSeq.index(pos_start_syn)+1:])) # 当检测words_seq时，增加的只能是1个单位。
            break
            pass
        pass
    # 后向截取：...等职务...之后的内容略去。 正则表达式是神器！！
    Position_Name = re.sub(u"(等职)+(.*)", "", Position_Name)
    Position_Name = re.sub(u"(职务)+(.*)", "", Position_Name) # 职务
    # 后处理最后符号
    if Position_Name.endswith(u"，") or Position_Name.endswith(u"；"):
        Position_Name = Position_Name[:-1]


    # Position_Name = Syn_Cut_Func(Position_Name)
    # print "Leaving PostPro of Position Name = ", Position_Name
    return Position_Name
    pass


# 为单个 working sent 检测时间表达;
def DetectTimeForWorkingSent(Working_Sent):
    postag_words_seq, postag_pos_seq,TimeSeqStart,TimeSeqEnd = Get_Seqs_and_Times(Working_Sent)
    Working_time_Str = ""
    if len(TimeSeqStart) == 0:
        return ""
        pass
    Working_time_Str = "".join(postag_words_seq[TimeSeqStart[0]: TimeSeqEnd[0] + 1])
    return Working_time_Str
    pass


# Detect Time Expression and Cut them.d
def DetectTimeExpForOrgname(Org_Name):
    """

    :param Org_Name: 待显示的机构名
    :return: 删除时间表达的机构名.
    """
    print "Into detect time exp for orgname. = ", Org_Name
    global Cur_CompanyName
    postag_words_seq, postag_pos_seq,TimeSeqStart,TimeSeqEnd = Get_Seqs_and_Times(Org_Name)
    if len(TimeSeqStart) == 0:
        Org_Name = PostPro_Org_Name(Org_Name)
        print " org org name = ", Org_Name
        return Org_Name
        pass
    if len(TimeSeqStart) > 1:
        print "\t\tMore than One Time Expression."
        pass
    Working_time_Str = "".join(postag_words_seq[TimeSeqStart[0]: TimeSeqEnd[0] + 1])
    # print "Working time str = ",Working_time_Str

    '''
    for time_id in range(len(TimeSeqStart)):
        Working_time_Str = "".joint(postag_words_seq[TimeSeqStart[time_id]: TimeSeqEnd[time_id] + 1])
        pass
    '''
    Working_org_str = "".join(postag_words_seq[TimeSeqEnd[0] + 1:])

    Working_org_str = PostPro_Org_Name(Working_org_str)

    if len(Working_org_str) == 0:
        return ""
        pass
    if Need_WorkingTime == 1:
        Org_Name = Working_time_Str + " --- " + Working_org_str
        pass
    else:
        Org_Name = Working_org_str

    # Org_Name = re.sub("\s","",Org_Name)
    # 替换"公司"和"本公司"
    print "Now cur company = ", Org_Name
    if (Org_Name == u"本公司" or Org_Name == u"公司") and len(Cur_CompanyName) >= 2:
        Org_Name = Cur_CompanyName
        pass
    return Org_Name
    pass


# 辅助函数，index all, 返回 位置 list.
def Added_Find_All(Contents, index_content):
    # Contents = ChangeUnicode(Contents)
    index_content = ChangeUnicode(index_content)
    find_result_list = []
    left_index = 0
    while Contents.find(index_content) >= 0:
        now_index = Contents.find(index_content)
        find_result_list.append(now_index + left_index)
        left_index = now_index + len(index_content)
        Contents = Contents[left_index:]
    return find_result_list
    pass


def Added_List_Index_All(ListObj, ItemObj):
    return [i for i in range(len(ListObj)) if ListObj[i] == ItemObj]
    pass


def Test_Added_Find_All():
    Contents = "tabcxyzabcd"
    index_content = "abc"
    print "Find result list = ",Added_Find_All(Contents, index_content)
    pass


# Check Time.
def Get_Seqs_and_Times(OrgName):
    """函数：检测有效时间表达，非常有用。
    Output:
        <1>postag_words_seq,  分词序列，与下文的pos序列相同，可以公用索引；
        <2>postag_pos_seq, 词性标注序列，与上分词序列可以公用索引；
        <3>TimeSeqStart, 时间表达Start序列，其实在后，表示自身，并不表示下一位。
        <4>TimeSeqEnd  时间表达 End序列，其实在前，表示自身。
        """
    OrgName = ChangeUnicode(OrgName)
    # print "Into Detecting working times, Org Names = "
    line_postag_list = pseg.cut(OrgName)
    postag_words_seq = []
    postag_pos_seq = []
    for word_postag in line_postag_list:
        postag_words_seq.append(word_postag.word)
        postag_pos_seq.append(word_postag.flag)
        pass
    TimeSeqStart, TimeSeqEnd = CheckTimePos(postag_pos_seq)


    # 过滤掉以单位开头的内容;
    InValid_Time_Syn_List = [u"年", u"月", u"日", u"千", u"万", u"亿"]
    invalid_seq_id_list = []
    for time_id in range(len(TimeSeqStart)):
        for ivalid_time_syn in InValid_Time_Syn_List:
            #if postag_words_seq[TimeSeqStart[time_id]].startswith(ivalid_time_syn) or (TimeSeqStart[time_id] == TimeSeqEnd[time_id]):
            if postag_words_seq[TimeSeqStart[time_id]].startswith(ivalid_time_syn) or (len(postag_words_seq[TimeSeqStart[time_id]]) <= MIN_TIMEEXP_LEN):
                invalid_seq_id_list.append(time_id)
                break
                pass
            pass
        pass
    # print "In DetectingWorkingTime, Time start seq = ", TimeSeqStart, "Time end seq = ", TimeSeqEnd
    # print "Invalid seq list = ", invalid_seq_id_list
    TimeSeqStart = [TimeSeqStart[time_seq_id] for time_seq_id in range(len(TimeSeqStart)) if time_seq_id not in invalid_seq_id_list]
    TimeSeqEnd = [TimeSeqEnd[time_seq_id] for time_seq_id in range(len(TimeSeqEnd)) if time_seq_id not in invalid_seq_id_list]

    # 添加对"现任，曾任，至今"等隐藏时间词的支持;

    for hid_time_syn in Hidden_Time_Syn_List:
        if hid_time_syn in postag_words_seq:
            for find_id in Added_List_Index_All(postag_words_seq, hid_time_syn):
                TimeSeqStart.append(find_id)
                TimeSeqEnd.append(find_id)
                pass
            #TimeSeqStart.append(postag_words_seq.index(hid_time_syn))
            #TimeSeqEnd.append(postag_words_seq.index(hid_time_syn))
            pass
        pass
    # Sort time
    TimeSeqStart.sort()
    TimeSeqEnd.sort()

    # print "Into Detecting working times, Org Names = "
    return postag_words_seq, postag_pos_seq,TimeSeqStart,TimeSeqEnd
    pass




# 输出机构+职位;
def Show_OrgName_Position_Name(Org_name, Position_name):
    global Person_Profile_Data
    # print "Into Show OrgName and Position_name ", Org_name," ", Position_name
    if type(Org_name) != list and type(Position_name) != list:
        Org_name = DetectTimeExpForOrgname(Org_name)
        Position_name = PostPro_Position_Name(Position_name)
        #print "After Show OrgName and Position_name ", Org_name," ", Position_name
       #print "len(Org_name)  and len(Position_name) = ", len(Org_name), len(Position_name)
        if (len(Org_name) >= 2 or len(Position_name) >= 2) and Org_name not in Invalid_Org_Names_List:
            # Check Org_name
            print "Here , org = ", Org_name, " pos = ", Position_name
            # 认为 Org 不能单独成立，需要与 Pos 合并的情形：例如 ...部，...中心结尾，并且长度小于 5
            if (Org_name in Department_Name_List or len(Org_name) <= 2) or ((Org_name.endswith(u"部") or Org_name.endswith(u"中心") or Org_name.endswith(u"处") or Org_name.endswith(u"科")) and len(Org_name) <= 5):
                Position_name = Org_name + Position_name
                Org_name = u""

            # 判断是否动词开头，如果是，则舍弃
            content_words_seq, content_pos_seq = get_pseg_seq(Org_name)
            if len(content_pos_seq) >= 1 and content_pos_seq[0] in No_OrgName_Start_Pos_List:
                return

            print ("\t\t\t- ***Org*** = %-20s, ***Pos*** = %-15s"%(Org_name, Position_name))
            # print "\t\t\t- ***Org*** = ",Org_name," ***Pos*** = ",Position_name
            working_infoitem = dict()



            working_infoitem["Org"], working_infoitem["Job"] = Org_name, Position_name
            Person_Profile_Data["Person_CurWork_Info"].append(working_infoitem)
            pass

        # Get_Seqs_and_Times(Org_name)
        return
        pass
    elif type(Org_name) != list and type(Position_name) == list:
        Org_name = DetectTimeExpForOrgname(Org_name)
        for position_name in Position_name:
            position_name = PostPro_Position_Name(position_name)
            # print "len(Org_name)  and len(Position_name) = ", len(Org_name), len(position_name)
            if (len(Org_name) > 2 or len(position_name) >= 2) and Org_name not in Invalid_Org_Names_List:
                print "Here , org = ", Org_name, " pos = ", position_name
                if Org_name in Department_Name_List or len(Org_name) <= 2:
                    position_name = Org_name + position_name
                    Org_name = u""

                # 判断是否动词开头，如果是，则舍弃
                content_words_seq, content_pos_seq = get_pseg_seq(Org_name)
                if len(content_pos_seq) >= 1 and (content_pos_seq[0] in No_OrgName_Start_Pos_List):
                    return

                print ("\t\t\t- ***Org*** = %-20s, ***Pos*** = %-15s"%(Org_name, position_name))
                # print "\t\t\t- ***Org*** = ",Org_name," ***Pos*** = ",position_name
                working_infoitem = dict()

                working_infoitem["Org"], working_infoitem["Job"] = Org_name, position_name
                Person_Profile_Data["Person_CurWork_Info"].append(working_infoitem)
                pass
            #Get_Seqs_and_Times(Org_name)
            pass
        return
    elif type(Org_name) == list and type(Position_name) != list:
        for org_name in Org_name:
            org_name = DetectTimeExpForOrgname(org_name)

            Position_name = PostPro_Position_Name(Position_name)
            # print "len(Org_name)  and len(Position_name) = ", len(org_name), len(Position_name)
            if (len(org_name) > 2 or len(Position_name) >= 2) and org_name not in Invalid_Org_Names_List:
                print "Here , org = ", org_name, " pos = ", Position_name
                if org_name in Department_Name_List or len(org_name) <= 2:
                    Position_name = org_name + Position_name
                    org_name = u""

                # 判断是否动词开头，如果是，则舍弃
                content_words_seq, content_pos_seq = get_pseg_seq(org_name)
                if len(content_pos_seq) >= 1 and content_pos_seq[0] in No_OrgName_Start_Pos_List:
                    return

                print ("\t\t\t- ***Org*** = %-20s, ***Pos*** = %-15s"%(org_name, Position_name))
                #print "\t\t\t- ***Org*** = ",org_name," ***Pos*** = ",Position_name
                working_infoitem = dict()

                working_infoitem["Org"], working_infoitem["Job"] = org_name, Position_name
                Person_Profile_Data["Person_CurWork_Info"].append(working_infoitem)
                pass

            #Get_Seqs_and_Times(org_name)
            pass
    else:
        print "None."
        return
    pass


# 处理单条任职经历，包括曾任和现任：Time, Org, Position;
def Check_WorkingSent(Cur_Working_Sent):
    """函数：接受按照时间序列划分的工作描述片段，做下一步处理。
    步骤：
        1) 显示包含的时间表述;
        2) 符号和关键字的划分，层次单元划分；
    """
    global Person_Profile_Data
    org_tip_list = [u"在", u"于", u"加入", u"就职于"]
    pos_tip_list = [u"担任", u"为", u"任", u"就职", u"任职", u"历任", u"工作"]
    Cur_Working_Sent = ChangeUnicode(Cur_Working_Sent)
    # print "Cur Working Sent = ", Cur_Working_Sent
    WorkingSent_Words_Seq, WorkingSent_Pos_Seq, WorkingSent_Time_Start, WorkingSent_Time_End =  Get_Seqs_and_Times(Cur_Working_Sent)
    # 检测是否为描述"工作任职经历"的句子。
    '''
    if Check_IF_WorkingSent(Cur_Working_Sent):
        print "Sent = ", Cur_Working_Sent, " Yes Working Sent."
        pass
    else:
        print "Sent = ", Cur_Working_Sent, " No Working Sent."
        return
    '''

    # 1) Show time.
    Time_Str = DetectTimeForWorkingSent(Cur_Working_Sent)
    if len(Time_Str) > 0 and Time_Str != u"担任":
        if If_MarkDown_Choice == 1:
            print "\t\t- Print Detect Time = ", Time_Str
            Person_Profile_Data["Person_CurWork_Info"].append(Time_Str)
        else:
            print "\t\t Print Detect Time = ", Time_Str
            Person_Profile_Data["Person_CurWork_Info"].append(Time_Str)
        pass

    # Seg Cur Working Items, divide into <org, position>
    org_tip_item = Check_ListItem_In_Content(org_tip_list, WorkingSent_Words_Seq)

    pos_tip_item = Check_ListItem_In_Content(pos_tip_list, WorkingSent_Words_Seq)

    print "org tip = ", org_tip_item, " pos tip = ", pos_tip_item

    if u"。" in Cur_Working_Sent[:-1] or u"；" in Cur_Working_Sent[:-1] or u";" in Cur_Working_Sent[:-1]:
        Cur_Working_Items_List = re.split(u"。|；|;|，|,",Cur_Working_Sent) # unicode，re.split也要添加.
        pass
    # 处理：[在，任职于]机构[担任，任]这种情况，提取机构名和职务名。
    elif org_tip_item and pos_tip_item and (WorkingSent_Words_Seq.index(org_tip_item) < WorkingSent_Words_Seq.index(pos_tip_item)): # 处理先后...、...、担任职务的状况;
        Org_Name = "".join(WorkingSent_Words_Seq[WorkingSent_Words_Seq.index(org_tip_item) + 1: WorkingSent_Words_Seq.index(pos_tip_item)])
        Position_Name = "".join(WorkingSent_Words_Seq[WorkingSent_Words_Seq.index(pos_tip_item) + 1:])
        if u"、" in Org_Name:
            Org_Name = re.split(u"、", Org_Name)
        elif u"、" in Position_Name:
            Position_Name = re.split(u"、", Position_Name)
        else:
            pass

        print "Cutting Tips,  Org_Name = ", Org_Name, " Pos_Name = ", Position_Name
        Show_OrgName_Position_Name(Org_Name, Position_Name)

        return
    elif u"，" in Cur_Working_Sent or u"," in Cur_Working_Sent:
        print "\tInto Working Sent: appear douhao"
        Cur_Working_Items_List = re.split(u"，|,",Cur_Working_Sent)

    elif u"、" in Cur_Working_Sent:
        # print "\tInto Working Sent: appear dunhao"
        if u"职于" in Cur_Working_Sent:
            Cur_Working_Items_List = re.split(u"、", Cur_Working_Sent)
            Org_name, Position_name = Check_Workig_Item(Cur_Working_Sent)
            Show_OrgName_Position_Name(Org_name, Position_name)
            return
            pass
        else:
            Cur_Working_Items_List = re.split(u"、",Cur_Working_Sent)
    elif u"和" in WorkingSent_Words_Seq or u"及" in WorkingSent_Words_Seq:
        Cur_Working_Items_List = re.split(u"和|及", Cur_Working_Sent)
    elif u"兼" in Cur_Working_Sent:
        Cur_Working_Items_List = re.split(u"兼", Cur_Working_Sent)
    else:
        Cur_Working_Items_List = [Cur_Working_Sent]
        pass
    # print "Cur_Working_Items_List = ", Cur_Working_Items_List

    for cur_id, cur_working_item  in enumerate(Cur_Working_Items_List):
        # print "Working_item_id = ", cur_id, " Working_item = ", cur_working_item
        # Check_Workig_Item(cur_working_item)
        Org_name, Position_name = Check_Workig_Item(cur_working_item)
        Show_OrgName_Position_Name(Org_name, Position_name)
        pass
    pass


# 处理单挑任职职位 Position;
def Check_Working_Item_PositionName(PositionName):
    if type(PositionName) != unicode:
        PositionName = unicode(PositionName, "UTF-8")
        pass
    if u"、" in PositionName or u"兼" in PositionName:
        position_name_list = re.split(u"、|兼", PositionName)
        PositionName = position_name_list
        pass
    return PositionName
    pass


# Unicode 格式转换，并进行空格去除
def ChangeUnicode(Contents):
    if type(Contents) != unicode:
        Contents = unicode(Contents, "UTF-8")
        pass
    Contents = re.sub("\s","",Contents)
    return Contents
    pass


# 后处理单条<机构>名称;
def Check_Working_Item_OrgName(OrgName):
    OrgName = ChangeUnicode(OrgName)
    # print "Before checking working item orgname, orgname = ",OrgName
    working_tag_list = [u"历任",u"现任", u"曾任职", u"职于", u"职於", u"曾任"]
    # 截取;
    for working_tag in working_tag_list:
        if working_tag in OrgName:
            working_tag_index = OrgName.index(working_tag)
            OrgName = OrgName[working_tag_index+len(working_tag):]
            pass
        pass

    if u"、" in OrgName:
        OrgName = re.split(u"、", OrgName)
        pass
    # print "After checking working item orgname, orgname = ",OrgName
    return OrgName
    pass


# 判断是否可能含有 Org 机构名称;
def Check_IfContains_Org_Func(DesContent):
    Org_Symbol_List = ["大学", "学院", "公司", "研究所"]
    for org_symbol in Org_Symbol_List:
        if org_symbol in DesContent:
            return True
            pass
        pass
    return False
    pass


# 从顿号分割内容长度判断顿号模式：P1-{机构+职位、机构+职位};P2-{机构+职位、职位、职位、...、职位}; P3-{机构1、机构2、机构3担任；}
def Detect_MarkSplit_Mode(MarkListContent):
    mark_split_mode = 1
    # 模式3的检测：先后在 ...、...、担任...;

    # Check length, if smaller than 7chas, maybe P2;
    MarkItem_Length_List = [len(markitem) for markitem in re.split(u"、|兼", MarkListContent)]
    num_postionname = 0
    for markitem_len in MarkItem_Length_List:
        if markitem_len <= 6:
            num_postionname += 1
            pass
        pass
    # print "num_postionname = ", num_postionname
    if num_postionname >= max(2,(len(MarkItem_Length_List)/2 - 1)):  # 很有意思的设置.
        #print "Num Short Posname = ",num_postionname
        mark_split_mode = 2
        pass
    #print "mark_split_mode = ",mark_split_mode
    return mark_split_mode
    pass





# 处理单条任职经历：分解成 <Org, Position>, 注意，此时 working_item是unicode,后来str.
def Check_Workig_Item(working_item):
    """函数：对于单个条目Item，将其分割为 Org + Position。
        Steps-1: 去除末尾的“职务”和"等职"等字样；
        Steps-2: 解析词序列，词性标注序列，时间表达序列；
        Steps-3: 公司名先导语检查
            当出现"任职于，就职于，创办..."等词语时，认为这些是 公司名 Org_Names 的先导词，将后文当作 Org_names.
        Steps-4: "任"等词语截取；
        Steps-5: "公司"等后文截取，机构名截取；

    """
    working_item = ChangeUnicode(working_item)

    # print "Into Checking working item, working item = ", working_item
    orgname = ""
    working_item_position_name = ""

    # 停用词去除：等职，等职务，
    working_item = re.sub(u"(等职)+务*", "", working_item)
    print "After removing stopwords, Woking Item = ",working_item

    working_item_words_seq, working_item_pos_seq, TimeSeqStart, TimeSeqEnd = Get_Seqs_and_Times(working_item)

    # [公司+职称] 先导语
    for w in working_item_words_seq:
        print "w = ", w

    # 机构名，先导语检查，当出现时，整体当作公司名。
    for preworking_org_tip in PreWorking_Org_Tips_List:
        if preworking_org_tip in working_item:
            orgname = working_item
            orgname = Check_Working_Item_OrgName(orgname)
            print "In Checking working item, orgname = ",orgname," pos name = ",working_item_position_name
            return orgname, working_item_position_name

    # 特殊的"、"描述
    PartTime_Tag_List = [u"、", u"兼", u"和"]
    for parttime_tag in PartTime_Tag_List:
        if parttime_tag in working_item_words_seq and Detect_MarkSplit_Mode(working_item) == 2:
            # print "Mark dot, and part time appears"
            working_item_mark_list = re.split(parttime_tag, working_item)
            orgname, working_item_position_name = Check_Workig_Item(working_item_mark_list[0])
            working_item_mark_list = working_item_mark_list[1:]
            # print "Working mark list :"
            # print "Beginning Org = ",orgname," Pos name = ",working_item_position_name
            if type(working_item_position_name) == list:
                working_item_position_name.extend(working_item_position_name)
                pass
            if type(working_item_position_name) != list:
                working_item_mark_list.insert(0, working_item_position_name)
                pass
            # working_item_position_name = " ".join(working_item_mark_list)
            # print "\t\tMark::::: Org = ", orgname," Position = ",working_item_position_name
            working_item_position_name = working_item_mark_list[:]
            orgname = Check_Working_Item_OrgName(orgname)
            return orgname, working_item_position_name
            pass
        if parttime_tag in working_item_words_seq and Detect_MarkSplit_Mode(working_item) == 1:
            # print "Mode = 1, <org + position> partime_tag = ", parttime_tag
            Check_WorkingSent(working_item)
            # orgname = Check_Working_Item_OrgName(orgname)
            # working_item_position_name = Check_Working_Item_PositionName(working_item_position_name)
            return "",""
            pass
        pass
    print "Marking dot processing."


    for orgname_start_syn in Org_Name_Start_Syn_List:
        if orgname_start_syn in working_item_words_seq:
            print "org start syn = ", orgname_start_syn
            working_item = "".join(working_item_words_seq[working_item_words_seq.index(orgname_start_syn) + 1: ])
            print "[公司-职务]先导词, working item = ", working_item
            working_item_words_seq, working_item_pos_seq, TimeSeqStart, TimeSeqEnd = Get_Seqs_and_Times(working_item)
            break
            pass
        pass

    # “公司”分割；
    for orgname_end in OrgName_Ends_List:
        if orgname_end in working_item_words_seq:
            print "Working Item has orgname end = ", orgname_end
            CompanyIndex = working_item.index(orgname_end)
            orgname = working_item[:CompanyIndex + len(orgname_end)]
            working_item_position_name = working_item[CompanyIndex + len(orgname_end):]
            working_item_position_name = Check_Working_Item_PositionName(working_item_position_name)
            orgname = Check_Working_Item_OrgName(orgname)
            print u"\t\tAfter checking org ends, Org = ", orgname, " Position = ", working_item_position_name
            return orgname, working_item_position_name
            pass
        pass
    print u"\t\tAfter cutting orgnames end syn, working item ", working_item

    # 特殊情况：当过短 < 7个字时，直接当做 Pos
    print "Len of working item  = ", len(working_item)
    if len(working_item) <= 5:
        working_item_position_name = working_item
        working_item_position_name = Check_Working_Item_PositionName(working_item_position_name)
        print "Too short working item, as position name.", working_item_position_name
        return orgname, working_item_position_name
        pass

    # print "Org names processing."
    if u"、" in working_item:
        working_item_mark_list = re.split(u"、|兼", working_item)
        orgname, working_item_position_name = Check_Workig_Item(working_item_mark_list[0])
        working_item_mark_list = working_item_mark_list[1:]
        # print "Working mark list :"
        for working_mark in working_item_mark_list:
            print "\t\tworking maek = ",working_mark
            pass
        # print "Beginning Org = ",orgname," Pos name = ",working_item_position_name
        if type(working_item_position_name) == list:
            working_item_position_name.extend(working_item_position_name)
            pass
        if type(working_item_position_name) != list:
            working_item_mark_list.insert(0, working_item_position_name)
            pass
        # working_item_position_name = " ".join(working_item_mark_list)
        # print "\t\tMark::::: Org = ", orgname," Position = ",working_item_position_name
        working_item_position_name = working_item_mark_list[:]
        orgname = Check_Working_Item_OrgName(orgname)
        return orgname, working_item_position_name
        pass
    # End 后端截取，例如等职务,请删除
    # 特殊的兼任状况：
    if u"兼" in working_item_words_seq:
        PartTime_index = working_item_words_seq.index(u"兼")
        orgname = "".join(working_item_words_seq[:PartTime_index-1])
        working_item_position_name = working_item_words_seq[PartTime_index - 1] + " " + "".join(working_item_words_seq[PartTime_index + 1:])
        print "\t\t兼任::::: Org = ", orgname, " Position = ",working_item_position_name

    # End 截取

    # 通过词性分析：Position 应该是倒数第二个n之后，往后直到最后一个n;
    print "Into POS Seg <Org + Pos>"
    working_item_position_id_start = -1
    working_item_position_id_end = -1
    for working_item_word_id in range(len(working_item_words_seq) - 1, -1, -1):
        i = working_item_word_id
        item_pos = working_item_pos_seq[working_item_word_id]
        # print "i = ",working_item_word_id," word = ",working_item_words_seq[i]," pos = ",working_item_pos_seq[i]
        if working_item_position_id_start == -1 and item_pos.startswith('n'):
            # print "Yes n, start"
            working_item_position_id_start = working_item_word_id
            continue
            pass
        if working_item_position_id_start != -1 and (item_pos == 'x' or item_pos.startswith("n") or item_pos == "eng"):
            # print "Yes n, end"
            working_item_position_id_end = working_item_word_id + 1
            break
            pass
        pass
    if working_item_position_id_end == -1 and working_item_position_id_start >= 0:
        working_item_position_id_end = 0
        pass
    # print "Position End = ",working_item_position_id_end, " Start = ",working_item_position_id_start

    working_item_position_name = "".join(working_item_words_seq[working_item_position_id_end: working_item_position_id_start + 1])
    orgname = "".join(working_item_words_seq[:working_item_position_id_end])
    print "\t\tInto POS Org = ", orgname," Position = ",working_item_position_name
    # print "Working Item:::::: Type = ",type(orgname)," ",working_item_position_name
    orgname = Check_Working_Item_OrgName(orgname)
    return orgname, working_item_position_name
    pass


# 检查任职经历中是否分别包含显示 Pre 和 Cur 的指示词;
def Check_IfRefer_Pre_Cur(working_sent):
    pre_tip, cur_tip = -1, -1
    pre_tag_list = ["历任", "曾任"]
    cur_tag_list = ["现任", "至今"]
    for pre_tag in pre_tag_list:
        if pre_tag in working_sent:
            pre_tip = working_sent.index(pre_tag)
            pass
        pass
    for cur_tag in cur_tag_list:
        if cur_tag in working_sent:
            cur_tip = working_sent.index(cur_tag)
            pass
        pass
    return pre_tip, cur_tip
    pass


# 函数：针对简历文档，通过时间表达划分为句子条目，将"基本信息"一类合并为一条.
def Divide_TimeSeq_Working(ProfileStr):
    """

    :param ProfileStr: 简历内容
    :return: 按时间表达之后的分割，从时间表达开始。
    """
    # print "Into Divide Divide_TimeSeq_Working"
    postag_words_seq, postag_pos_seq, TimeSeqStart, TimeSeqEnd = Get_Seqs_and_Times(ProfileStr)

    len_time_sequences = len(TimeSeqStart)
    # print "Len of time seq = ", len_time_sequences
    time_seq_str_list = []
    # Show Time Sequens;
    for t_id in range(len_time_sequences):
        # print "start = ", TimeSeqStart[t_id], " end = ", TimeSeqEnd[t_id]
        pass
    # print "**********Show Time Sequens**********"
    if len_time_sequences == 0:
        seq_str_fullmark = ProfileStr.split(u"。")
        for seq_fullmark in seq_str_fullmark:
            if len(seq_fullmark) > 5:
                time_seq_str_list.append(seq_fullmark + u"。")
        return time_seq_str_list
        pass


    for time_id in range(len_time_sequences):
        time_seq_str = ""
        if time_id == 0:
            if len_time_sequences > 1:
                time_seq_str = "".join(postag_words_seq[TimeSeqStart[time_id]: PostCut_Symbol_function(TimeSeqStart[0], TimeSeqStart[1], postag_pos_seq)])
                pass
            else:
                time_seq_str = "".join(postag_words_seq)
            pass
        elif time_id < len_time_sequences - 1:
            seq_start_index = TimeSeqStart[time_id]
            seq_end_index = PostCut_Symbol_function(TimeSeqStart[time_id], TimeSeqStart[time_id+1], postag_pos_seq)
            # print "seq start id = ", seq_start_index, "word = ", postag_words_seq[seq_start_index],  "seq end id = ", seq_end_index, "word = ", postag_words_seq[seq_end_index]
            time_seq_str = "".join(postag_words_seq[TimeSeqStart[time_id]: PostCut_Symbol_function(TimeSeqStart[time_id], TimeSeqStart[time_id+1], postag_pos_seq)])
            pass
        else:
            time_seq_str = "".join(postag_words_seq[TimeSeqStart[time_id]: ])
        # print "\tTime Seq: = ", time_seq_str
        # 最后一个符号;


        # 当出现句号时，截取第一个句号之前内容。
        if u"。" in time_seq_str:
            time_seq_str = time_seq_str[:time_seq_str.index(u"。") + len(u"。")]

        # 当没有出现显式时间标记，并且没有隐式词语时，用句号分割。

        '''
        # 以句号 Full Mark为句子分隔符；
        if u"。" in time_seq_str:
            seq_str_fullmark = time_seq_str.split(u"。")
            for seq_fullmark in seq_str_fullmark:
                if len(seq_fullmark) > 5:
                    time_seq_str_list.append(seq_fullmark + u"。")
            #time_seq_str = time_seq_str[:time_seq_str.index(u"。") + len(u"。")]
            pass
        else:
            time_seq_str_list.append(time_seq_str)
        '''
        time_seq_str_list.append(time_seq_str)


        '''
        # 检测第一句时间表达是否为隐含表达，若是，则将首句单独设置为基本资料。
        hidden_time_item = Check_ListItem_In_Content(Hidden_Time_Syn_List, time_seq_str_list[0])
        if hidden_time_item:
            hidden_exp_list = re.split(hidden_time_item, time_seq_str_list[0])
            time_seq_str_list.insert(0, hidden_exp_list[0])
            time_seq_str_list[1] = hidden_time_item + hidden_exp_list[1]
        pass
        '''

    # 检测首部分是否应该加入第一句: 若第一句不是基本资料，则首部分独立；否则第一句加入首句。
    first_basic_info = "".join(postag_words_seq[: TimeSeqStart[0]])
    # print "First info = ", first_basic_info
    if Check_ListItem_In_Content(Basic_info_Syn_List, time_seq_str_list[0]):
        time_seq_str_list[0] = first_basic_info + time_seq_str_list[0]
    else:
        time_seq_str_list.insert(0, first_basic_info)
    # print "Into Divide Divide_TimeSeq_Working"
    return time_seq_str_list
    pass



# Check if A list has element in Str B
def Check_ListItem_In_Content(ListA, ContentB):
    """
    :param ListA: 查找目标集合，遍历查找每一个。
    :param ContentB: 查找范围，被查找区域。
    :return: 若ListA中某个元素存在于列表对象ContentB中，则返回存在的元素；若不存在，则返回false。
    """
    for item_a in ListA:
        if item_a in ContentB:
            return item_a
            pass
        pass
    return False
    pass


def Sents_Segmentation(ProfileStr_Contents):
    """
    :param ProfileStr_Contents: 简历中|||分割的第三部分。
    :return: List of sents, basic info, or start with time expressions.
    Steps:
        1) 完全句号分割，避免只取首局为Basic_info句；
        2) 判断是否basic语句，加入其中;
        3) 识别时间表达，进入其中；
    """

    full_mark_spot = u"。"
    full_mark_sents_list = [sent + full_mark_spot for sent in  ProfileStr_Contents.split(full_mark_spot) if len(sent) > 3]
    seg_sents = []
    for full_mark_sent in full_mark_sents_list:
        pass

    return full_mark_sents_list


# 得到指示 曾任信息 和 现任信息两部分：
def Divide_Pre_Cur_Working(ProfileStr):
    """
    :param ProfileStr: "公司|||姓名|||简历"
    :return:
    """
    """
        Step:    1) Sents Segmentation, 时间序列分句;
                 2) Sents Categrization, 通过时间指示词，划分句子所属三类别；
                 3) Sents Analysis 分步骤解析三类别句子;
    """
    global Person_Profile_Data, Cur_CompanyName, Cur_PersonName
    Person_Profile_Data = copy.deepcopy(Person_Profile_Data_Init)
    ProfileStr = ChangeUnicode(ProfileStr)
    print "Original Person Profile Contents = ", ProfileStr
    Cur_CompanyName, Cur_PersonName, ProfileStr = ProfileStr.split('|||')

    # Step: 1) 用时间序列分割;
    Profile_Sentences_List = Divide_TimeSeq_Working(ProfileStr)
    if Show_Profile_Sents == 1:
        for sent in Profile_Sentences_List:
            if len(sent) > 2:
                if u"。" in sent:
                    print "\t Full Stop Sent = ", sent
                else:
                    print "\tProfile Sent = ", sent
                pass

    if Show_Profile_Str == 1:
        print "> ", ProfileStr
        pass


    # Step: 2) Detect Cur and Pre Working Exps;
    Maybe_Working_WordsList = [u"现任", u"曾任", u"担任", u"任职", u"历任", u"兼任", u"任", u"兼", u"经理", u"董事", u"监事", u"部长", u"委员", u"会长", u"秘书长", u"处长", u"工程师"]

    pre_tag_list = [u"历任", u"曾任", u"任职", u"任", u"工作", u"先后", u"就任", u"就职于", u"就职", u"创办", u"创立", u"创建"]
    cur_tag_list = [u"现任", u"至今", u"目前", u"兼任", u"起任", u"起"]
    pre_sents_list = []
    cur_sents_list = []
    info_sents_list = []
    # Step-2: Sentences Classification: 句子分类，分现任/曾任方法2: 如果出现现任，至今等的，为Cur; 否则为曾经;

    for working_sent in Profile_Sentences_List:
        if Check_ListItem_In_Content(Basic_info_Syn_List, working_sent):
            info_sents_list.append(working_sent)
            # print "info sent = ",working_sent
        elif(Check_ListItem_In_Content(cur_tag_list, working_sent)):
            # print "cur sent = ",working_sent
            cur_sents_list.append(working_sent)
        elif(Check_ListItem_In_Content(pre_tag_list, working_sent)):
            # print "pre sent = ",working_sent
            pre_sents_list.append(working_sent)
        else:
            pass
        pass
    # Step 3: Analysis Basic infomation
    if If_MarkDown_Choice == 1:
        print u"\n- **Section-2:人物基本资料**\n"
    else:
        print u"\n**********Section-2:人物基本资料**********:"

    if If_MarkDown_Choice == 1:
        basic_info_sent = ChangeUnicode("".join(info_sents_list))
        #print "\t\t", basic_info_sent
        Check_BasicInfo(basic_info_sent)
        '''
        for basic_info_sent in info_sents_list:
            print "\t\t",basic_info_sent
            Check_BasicInfo(basic_info_sent)
        '''
        print u"\n- **Section-3:工作经历**"
        print u"\n\t- **Section-3-1:现任工作**"
        for cur_sent in cur_sents_list:
            print "\t", cur_sent
            Check_WorkingSent(cur_sent)
        print u"\n\t- **Section-3-2:曾任工作**"
        for pre_sent in pre_sents_list:
            print "\t", pre_sent
            Check_WorkingSent(pre_sent)
            pass
        pass

    else:
        for basic_info_sent in info_sents_list:
            # print "\t\t",basic_info_sent
            Check_BasicInfo(basic_info_sent)
        print u"\n**********Section-3:工作经历.**********"
        print u"\t**********Section-3-1:现任工作**********"
        for cur_sent in cur_sents_list:
            # print "\t", cur_sent
            Check_WorkingSent(cur_sent)
        print u"\t**********Section-3-2:曾任工作**********"
        for pre_sent in pre_sents_list:
            #print "\t",pre_sent
            Check_WorkingSent(pre_sent)
            pass


# 提取基本信息函数：Check_BasicInfo
def Check_BasicInfo(ProfileStr):
    global Person_Profile_Data, Cur_PersonName

    #print "Type of basic info = ", type(ProfileStr)
    if type(ProfileStr) != unicode:
        ProfileStr = unicode(ProfileStr, "UTF-8")
        pass
    if len(ProfileStr) <= 5:
        return
        pass
    print "Basic info sent = ", ProfileStr
    person_profile_head = ProfileStr.split()[0].split('|||')
    Cur_CompanyName = person_profile_head[0]
    postag_words_seq, postag_pos_seq, TimeSeqStart, TimeSeqEnd = Get_Seqs_and_Times(ProfileStr)
    if len(TimeSeqStart) > 1:
        # print "More than 1 time in basic info."
        pass
    # Name: Detect Name, 1)before 先生or 女士; 2) 第一个符号前
    Gender_call_list = [u"先生", u"女士", u"男", u"女"]
    gender_call_index = 0
    for gender_call_tip in Gender_call_list:
        if gender_call_tip in postag_words_seq:
            # print "Gender call"
            '''
            gender_call_index = postag_words_seq.index(gender_call_tip)
            print u"\t*性别/称呼* = ", postag_words_seq[gender_call_index]
            '''
            gender_call_tip = Check_GenderCall(gender_call_tip)
            print u"\t*性别/称呼* = ", gender_call_tip
            Person_Profile_Data["Person_Basic_Info"]["Gender"] = gender_call_tip
            break
            pass
        pass

    print u"\t*姓名* = ", Cur_PersonName
    Person_Profile_Data["Person_Basic_Info"]["Name"] = Cur_PersonName


    # Age or Birth: 用时间数量词, 注意，end,start，包含首位;
    print "TimeSeqStart = ", TimeSeqStart
    if len(TimeSeqStart) > 0:
        time_index_end, time_index_start = TimeSeqEnd[0], TimeSeqStart[0] # 第一个时间表达，默认为年龄或者出生时间
        birth_age_str = "".join(postag_words_seq[time_index_start:time_index_end + 1])
        birth_age_str = Check_BirthInfo(birth_age_str)
        print u"\t*出生/年龄* = ", birth_age_str
        Person_Profile_Data["Person_Basic_Info"]["Birth"] = birth_age_str
        pass

    # 国籍: 如果是中国，不显示；如果不是，写出;
    country_syn_list = [u"国籍", u"中国籍"]
    country_syn = Check_ListItem_In_Content(country_syn_list, postag_words_seq)
    if country_syn:
        country_syn_index = postag_words_seq.index(country_syn)
        if country_syn == u"国籍":
            country_name = postag_words_seq[country_syn_index - 1]
        else:
            country_name = u"中国"
        # print u"\t*国籍* = ", postag_words_seq[country_syn_index - 1]
        # Person_Profile_Data["Person_Basic_Info"]["Country"] = postag_words_seq[country_syn_index - 1]
        print u"\t*国籍* = ", country_name
        Person_Profile_Data["Person_Basic_Info"]["Country"] = country_name
        '''
        if postag_words_seq[country_syn_index - 1] != "国":
            print u"\t*国籍* = ", postag_words_seq[country_syn_index - 1]
            Person_Profile_Data["Person_Basic_Info"]["Country"] = postag_words_seq[country_syn_index - 1]
            pass
        '''
        pass

    # 学历：
    Education_syn_List = [u"研究生", u"博士",u"硕士",u"硕士学位", u"本科",u"学士", u"工商管理学士", u"学士学位",u"专科",u"大专", u"中专", u"高中", u"职高", u"初中", u"EMBA", u"MBA", u"学历"]

    edu_syn_index = 0
    edu_syn_content = ""
    for edu_syn in Education_syn_List:
        if edu_syn in postag_words_seq:
            edu_syn_index = postag_words_seq.index(edu_syn)
            if postag_words_seq[edu_syn_index - 1] == "博士" or postag_words_seq[edu_syn_index - 1] == "硕士" or postag_words_seq[edu_syn_index - 1] == "大学":
                edu_syn_content = "".join(postag_words_seq[edu_syn_index - 1: edu_syn_index + 1])
                pass
            else:
                edu_syn_content = "".join(postag_words_seq[edu_syn_index])
            print u"\t*学历* = ", edu_syn_content
            Person_Profile_Data["Person_Basic_Info"]["Degree"] = edu_syn_content
            break
            pass
        pass

    # 毕业院校: (毕业于|符号)开始，大学，学院，结尾;
    Edu_School = ""
    gra_sch_str = "毕业"
    school_start_index = 0
    school_end_str_index = 0
    Edu_Sch_Syn_List = [u"分校", u"大学", u"学院", u"党校", u"学校"]
    for edu_sch_syn in Edu_Sch_Syn_List:
        if edu_sch_syn in ProfileStr: # 大学只能用 String.
            school_end_str_index = ProfileStr.rfind(edu_sch_syn) + len(edu_sch_syn) # 从后往前找.
            if school_end_str_index <= (len(ProfileStr) - 1) and ProfileStr[school_end_str_index] == u"）":
                school_end_str_index += 1
                pass
            break
            pass
        pass
    if school_end_str_index != 0:
        rough_School = ProfileStr[:school_end_str_index]
        #print "Rough School = ",rough_School
        school_name = (re.split(u"于|，|。|；|,", rough_School))[-1] # 确定教育场所开头，毕业于字样或者往前第一个标点符号。
        if len(school_name) > 2:
            print u"\t*学校* = ", school_name
            Person_Profile_Data["Person_Basic_Info"]["School"] = school_name
            pass
        pass
    pass




# 辅助函数，re.split，检测re.split的有效结果;
def AddFunc_ValidReSplit(sp_item, sp_whole):
    sp_init = re.split(sp_item, sp_whole)
    sp_result = [sp_i for sp_i in sp_init if len(sp_i) > 1]
    return sp_result
    pass


# 载入公司高管个人信息文件;
def Load_Get_Person_Profile(PersonProfileFilename, TEST_PERSON_NUM):
    """

    :param PersonProfileFilename: 公司高管列表文件名，很多人。
    :param TEST_PERSON_NUM: 选取显示的人数量。
    :return:
    """
    print "Into Loading"
    PersonProfileFile = open(PersonProfileFilename)
    for person_id, person_profile in enumerate(PersonProfileFile.readlines()[:TEST_PERSON_NUM]):
        if len(person_profile) < 2:
            continue
            pass
        person_profile_head = person_profile.split()[0].split('|||')
        if If_MarkDown_Choice == 1:
            #print "\n\n#### Person Id = ", person_id, "Name = ", unicode(person_profile.split()[0], "utf-8"),"\n"
            print "\n\n#### Person Id = ", person_id, "Name = ", unicode(person_profile_head[1], "utf-8"),"\n"

            pass
        else:
            print "\n\n********************\nPerson Id = ", person_id, "\n********************"
        Divide_Pre_Cur_Working(person_profile)
        pass
    PersonProfileFile.close()
    pass


def Find_Person_Attributes_RegExp(ProfileStr):
    # 1) Name
    '''
    name_end_index = re.search("，",ProfileStr).start()
    print "姓名EndIndex = ",name_end_index
    print "Name = ",ProfileStr[:name_end_index]
    '''
    # 2) Gender + Birth + Degree
    print "\n\n\nSection-1: 人物基本信息(姓名，性别，出生，教育程度......)\n"
    Person_BasicInfo_Keys = ["Name", "Gender", "Birth"]
    Basic_info_ReExp_ch = "(?P<Name>.{6,50})，(?P<Gender>男|女).*，(?P<Birth>(?P<Birth_Year>\d+)年(?P<Birth_Day>\d+)月)出生.*，(?P<Degree>(.{6,15})(学位|学历))" # (?P<key>pattern) 为分组命名
    basic_info_search_result = re.search(Basic_info_ReExp_ch, ProfileStr)
    print "Group Name = ",basic_info_search_result.group("Name")
    print "Group Gender = ",basic_info_search_result.group("Gender")
    print "Group Birth = ",basic_info_search_result.group("Birth")
    print "Group Birth Year = ",basic_info_search_result.group("Birth_Year")
    print "Group Degree = ",basic_info_search_result.group("Degree")






    # 3.1) 现任职务: 现任now_job_1，...,。
    print "\n\n\nSection-2:人物职业经历(现任，曾任)\n"
    job_now_tag_ch = "现任(.*)。"
    job_now_search_result = re.search(job_now_tag_ch, ProfileStr)
    job_now_search_span = job_now_search_result.span()
    job_now_group_text = job_now_search_result.group(1)
    print "job_now_group_text = ",job_now_group_text
    job_now_split_list = job_now_group_text.split("，")
    print "Job Now List leng = ",len(job_now_split_list)
    for job_now in job_now_split_list:
        print "Job Now = ", job_now
        pass

    # 3.2) 曾经职务：曾任pre_job_1，...，。
    job_pre_tag_ch = "曾任(.*)。"
    job_pre_search_result = re.search(job_pre_tag_ch, ProfileStr)
    job_pre_search_span = job_pre_search_result.span()
    job_pre_group_text = job_pre_search_result.group(1)
    # re.split(syn1|syn2, str)
    job_pre_split_list = re.split("；|，", job_pre_group_text)
    print "job_pre_group_text = ", job_pre_group_text
    for job_pre in job_pre_split_list:
        print "Job_pre = ",job_pre
        pass
    print "Len of 张杨",len("张杨")
    pass


def main():
    ProfileStr = "刘宏女士，女，53岁，1962年生，1962年5月出生，中国国籍，无境外永久居留权，毕业于湖南生物与机电工程职业技术学院，博士研究生学历。曾任中国纺织大学团委副书记；上海纺织品进出口公司开发部经理助理、党办宣传员；上海市华达进出口公司董事兼副总经理；上海市对外经济贸易委员会办公室秘书，借调上海市政府、上海市人大工作（历任上海市对外经济贸易委员会副处级调研员、正处级调研员）；联合发展党委委员、副总经理，党委副书记、副总经理（主持工作）；上海外高桥（集团）有限公司党委委员、副总经理。现任本公司副董事长，上海外高桥集团股份有限公司党委书记、董事兼副总经理，上海外高桥西北保税物流有限公司董事长，联合发展党委书记、董事、总经理，上海市外高桥保税区三联发展有限公司执行董事、法定代表人。"
    # Find_Person_Attributes(ProfileStr)
    # Find_Person_Attributes_RegExp(ProfileStr)
    # Find_Person_Attributes_RegExp_Demo(ProfileStr)

    Load_Get_Person_Profile(PersonProfileFilename, TEST_PERSON_NUM)

    # OrgName, WorkingPositionName = Check_Workig_Item("历任财务部会计")
    # Show_OrgName_Position_Name(OrgName, WorkingPositionName)
    #Test_Check_Workig_Item()

    # Test_CheckTimePos()
    # TestGet_Seqs_and_Times()
    # Test_Divide_TimeSeq_Working()
    # Test_Check_BasicInfo()
    # Test_Added_Find_All()
    pass

if __name__ == '__main__':
    main()
