#coding:utf-8
"""
#########################################
    Title:          IMSLZY_Lib_ComPersonProfileAnalysis.py
    Function:       库函数，对人物简历内容进行解析，从纯文本到Json数据结构。
    First Created:  2016.01.12
    Last Modified:  03.24
    Author:         yang.zhang(yang.zhang@imsl.org.cn)

#########################################
"""


import re
import jieba
import jieba.posseg as pseg
import sys
import copy
from IMSLZY_Vars_Lib_ComPersonProfileAnalysis import *

# File Coding.
# print "Old File Encoding = ",sys.getfilesystemencoding()
reload(sys)
sys.setdefaultencoding("utf-8")
# print "New File Encoding = ",sys.getfilesystemencoding()



PersonProfileFilename = "PersonProfileDataDir/PerProWithName_0128_3.txt"


Person_Profile_Data = copy.deepcopy(Person_Profile_Data_Init)   # 字典Dict类型数据，初始为空，后更新。


"""
Section: 函数结构：
        > 辅助函数
            >
            >
            >
        > 纯末尾函数，没有新的调用

        > 流程和操作函数
            >
            >
        > 核心函数
            >
"""


"""
Section: 辅助函数
    > 辅助函数
        >
"""
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

"""
Section 1:
    > 辅助函数：START.
        > get_pseg_seq(str_content)
        > change_2_unicode(Contents)
        > check_listitem_in_content(ListA, ContentB)
"""


def get_pseg_seq(str_content):
    """
    :param str_content: 待得到分词和POS的文本。
    :return: two list, list of words + list of POS.
    """
    str_content = change_2_unicode(str_content)
    content_words_seq = list()
    content_pos_seq = list()
    pseg_seq = pseg.cut(str_content)
    for w_id, w in enumerate(pseg_seq):
        content_words_seq.append(w.word)
        content_pos_seq.append(w.flag)
    return content_words_seq, content_pos_seq


# Unicode 格式转换，并进行空格去除
def change_2_unicode(contents):
    if type(contents) != unicode:
        contents = unicode(contents, "UTF-8")
        pass
    contents = re.sub("\s", "", contents)
    return contents
    pass


# Check if A list has element in Str B
def check_listitem_in_content(list_a, content_b):
    """
    :param list_a: 查找目标集合，遍历查找每一个。
    :param content_b: 查找范围，被查找区域。
    :return: 若ListA中某个元素存在于列表对象ContentB中，则返回存在的元素；若不存在，则返回false。
    """
    for item_a in list_a:
        if item_a in content_b:
            return item_a
            pass
        pass
    return False
    pass


# Regularization time expression(explict and  implicit) as sequences headings.
def regular_time_headings(time_seq_start, time_seq_end, words_seq):
    """
    :param time_seq_start:
    :param time_seq_end:
    :param words_seq:
    :return: new time_seq, start and end.
    合并显示/隐式时间表达，要求约束：1) end 与 下一个 start 之间<设定GAP; 2) 之间没有 句号等分隔符。
    """
    if len(time_seq_start) <= 1 or len(words_seq) <= 1:
        return time_seq_start, time_seq_end
    new_time_seq_start = [time_seq_start[0]]
    new_time_seq_end = []
    old_time_num = len(time_seq_start)
    time_index_id = 0
    while time_index_id <= (old_time_num-2):
        while(time_index_id <= old_time_num - 2 and time_seq_end[time_index_id] + TIME_GAP_LIMIT >= time_seq_start[time_index_id + 1] and u"。" not in words_seq[time_seq_end[time_index_id]: time_seq_start[time_index_id + 1]]):
            time_index_id += 1
        # end, need to stop;
        if time_index_id >= old_time_num - 1:
            break
        new_time_seq_end.append(time_seq_end[time_index_id])
        new_time_seq_start.append(time_seq_start[time_index_id + 1])
        time_index_id += 1
    # end.
    new_time_seq_end.append(time_seq_end[-1])
    return new_time_seq_start, new_time_seq_end


# 辅助函数，index all, 返回 位置 list.
def Added_Find_All(Contents, index_content):
    # Contents = change_2_unicode(Contents)
    index_content = change_2_unicode(index_content)
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


def final_check_org_pos(org_name, pos_name):
    """
        :param org_name: 最后判断 org_name 是否合法
        :param pos_name:
        :return boolean
        Rules:
            1> if rules, return right;
                - contains org/company ends;
                - ratio of pos 'n' higher than 1/2;
            2> if rules, return wrong;
                - ratio of pos
            3> if org is null,
                - if ratio of pos 'n' of pos_name > 1/2
    """
    if len(org_name) < 2 and len(pos_name) < 2:
        return False
    words_seq_org, postag_seq_org = get_pseg_seq(org_name)
    words_seq_pos, postag_seq_pos = get_pseg_seq(pos_name)
    if len(org_name) < 2:
        p_pos_n = 0
        for pos_ in postag_seq_pos:
            if 'n' in pos_:
                p_pos_n += 1
        ratio_p_pos_n = float(p_pos_n)/len(postag_seq_pos)
        print "Position, num of n = ", p_pos_n, " total = ", len(postag_seq_pos)
        if ratio_p_pos_n >= 0.5:
            return True

    elif 2 < len(org_name) < 8:
        if check_listitem_in_content(OrgName_Ends_List, org_name):
            return True
    else:
        p_org_n = 0
        for pos_ in postag_seq_org:
            if 'n' in pos_:
                p_org_n += 1
        ratio_p_org_n = float(p_org_n)/len(postag_seq_org)
        print "Org, num of n = ", p_org_n, " total = ", len(postag_seq_org)
        if ratio_p_org_n >= 0.5:
            return True

    return False






"""
Section:
    > 辅助函数：END.
"""

"""
Section:
    > 纯End函数(没有新的调用) START.
        > PostCut_Symbol_function(now_index, next_index, postag_pos_seq)
        > PostPro_Org_Name(Org_Name)
        > PostPro_Position_Name(Position_Name)
        > Check_Working_Item_PositionName(PositionName)
        > Check_Working_Item_OrgName(OrgName)
        > Detect_MarkSplit_Mode(MarkListContent)
        > Check_GenderCall(gender_call_tip)
        > Check_BirthInfo(birth_age_str)
        > get_school_snippet(profile_basic_str)
        > CheckTimePos(PosSeq)

"""


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
    return next_index


# 后处理机构名, PostProOrgName;
def PostPro_Org_Name(Org_Name):
    """

    :param Org_Name: 待后处理的机构名。
    :return:
    """
    global Cur_CompanyName
    # print "Into Postpro Org Name = ",Org_Name
    # 开始标记：从"进入"之后获取;
    Org_Name = change_2_unicode(Org_Name)
    Org_Name_Words_Seq, Org_Name_Pos_Seq, Org_Name_Time_Start, Org_Name_Time_End =  Get_Seqs_and_Times(Org_Name)
    native_orgname_start_syn_list = Org_Name_Start_Syn_List + [u"就职", u"现在", u"参加"]

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
            Org_Name = change_2_unicode("".join(Org_Name_WordsSeq[ Org_Name_WordsSeq.index(org_start_syn)+1:])) # 当检测words_seq时，增加的只能是1个单位。
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
    Position_Name = change_2_unicode(Position_Name)
    Position_Name = re.sub(u"的|。|同时|期自|我们|；","",Position_Name)

    # 前向截取: 职位POS 里，"担任"和"任"之后的部分截取;
    pos_start_syn_list = [u"担任", u"并任", u"历任", u"任", u"是"]
    Position_Name_WordsSeq = jieba.cut(Position_Name, cut_all=False)  # 分词后的 任 分割；
    Position_Name_WordsSeq = [w for w in Position_Name_WordsSeq]

    for pos_start_syn in pos_start_syn_list:
        if pos_start_syn in Position_Name_WordsSeq:
            Position_Name = change_2_unicode("".join(Position_Name_WordsSeq[ Position_Name_WordsSeq.index(pos_start_syn)+1:])) # 当检测words_seq时，增加的只能是1个单位。
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

# 后处理单条<机构>名称;
def Check_Working_Item_OrgName(OrgName):
    OrgName = change_2_unicode(OrgName)
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
                return change_2_unicode(str(Cur_Year - int(birth_age_item.word))) + u"年"
    return birth_age_str
    pass

# 提取毕业院校：1) 找到"毕业"字样; 2) 找到"毕业"所在的单个句子，前后标点算进去；
def get_school_snippet(profile_basic_str):
    """
    :param profile_basic_str: 包含基本信息的信息片段；
    :return: 推测出的院校；
    Steps:
        1) 找到标记词"毕业"及位置；
        2) 找到所在的短句片段，前后都是标点；Snippet.
        3) 找到学校的开头和结尾;
    """
    school_tip_word_list = [u"毕业", u"就读", u"攻读", u"学位", u"学士学位", u"硕士学位", u"博士学位", u"学习"]
    school_tip_word_index = 0
    school_start_words_index = 0
    school_end_words_index = 0
    basic_str_words_seq, basic_str_pos_seq = get_pseg_seq(profile_basic_str)
    for school_tip_word in school_tip_word_list:
        if school_tip_word in basic_str_words_seq:
            school_tip_word_index = basic_str_words_seq.index(school_tip_word)
            school_start_words_index = school_tip_word_index
            school_end_words_index = school_tip_word_index
            break
    if school_tip_word_index == 0:
        return u""
    print "school_tip_word_index = ", school_tip_word_index
    """
    for w in basic_str_words_seq:
        print "w = ", w
    for p in basic_str_pos_seq:
        print "p = ", p

    print "school_start_words_index = ", school_start_words_index, basic_str_pos_seq[school_start_words_index]
    print "school_end_words_index = ", school_end_words_index, basic_str_pos_seq[school_end_words_index]
    """

    while (school_start_words_index >= 0 and basic_str_pos_seq[school_start_words_index] != u'x'):
        school_start_words_index -= 1
    while (school_end_words_index <= len(basic_str_words_seq) - 1 and basic_str_pos_seq[school_end_words_index] != u'x'):
        school_end_words_index += 1
    print "school start index = ", school_start_words_index, " school end index = ", school_end_words_index
    school_snippet_str = "".join(basic_str_words_seq[school_start_words_index+1: school_end_words_index])
    print "school sinppet str = ", school_snippet_str
    school_snippet_str = change_2_unicode(school_snippet_str)

    # Get start and end index of school names.
    school_start_str_index = 0
    school_end_str_index = 0
    Edu_Sch_Syn_List = [u"分校", u"学院", u"大学", u"党校", u"学校", u"中学"]
    for edu_sch_syn in Edu_Sch_Syn_List:
        if edu_sch_syn in school_snippet_str: # 大学只能用 String.
            school_end_str_index = school_snippet_str.find(edu_sch_syn) + len(edu_sch_syn) # 从后往前找.
            if school_end_str_index <= (len(school_snippet_str) - 1) and school_snippet_str[school_end_str_index] == u"）":
                school_end_str_index += 1
                pass
            print "edu_sch_syn = ", edu_sch_syn
            break
            pass
        pass

    school_start_tip_words_list = [u"取得", u"获得", u"毕业于", u"于", u"毕业於", u"於", u"就读", u"在", u"月", u"年", u"持有", u"和"]
    for school_start_tip_word in school_start_tip_words_list:
        if school_start_tip_word in school_snippet_str:
            school_start_str_index = school_snippet_str.index(school_start_tip_word) + len(school_start_tip_word)
            print "school start tip word = ", school_start_tip_word
            break
    print "school start str index = ", school_start_str_index, " end str index = ", school_end_str_index
    print "Start str = ", school_snippet_str[school_start_str_index], " End str = ", school_snippet_str[school_end_str_index - 1]
    school_name = u""
    school_name = u"".join(school_snippet_str[school_start_str_index : school_end_str_index])

    print "School name = ", school_name

    return school_name



# 检测表示时间的序列: Input: list of pos, Out:list of tuple(time start, time end)
def CheckTimePos(PosSeq):
    # print "Into Checking Time Pos."
    TimeSeqStart = []
    TimeSeqEnd = []
    InTimeFlag = False
    t_id_start = -1
    t_id_end = -1
    # print "Posseq = ", PosSeq
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
        if (TimeSeqEnd[newtime_id] + TIME_GAP_LIMIT > TimeSeqStart[newtime_id+1]) and u'x' not in PosSeq[TimeSeqEnd[newtime_id]: TimeSeqStart[newtime_id + 1]]:  # 当间隔过小，并且中间没有符号时，前后合并。
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


"""
Section: 纯End函数。 End.
"""


"""
Section:
    > 核心函数
        > Get_Seqs_and_Times(OrgName)
        > Divide_TimeSeq_Working(ProfileStr)
        > DetectTimeForWorkingSent(Working_Sent)
        > DetectTimeExpForOrgname(Org_Name)
        > Show_OrgName_Position_Name(Org_name, Position_name)
        > Check_BasicInfo(ProfileStr)
        > Check_Workig_Item(working_item)
        > Check_WorkingSent(Cur_Working_Sent)
        > Divide_Pre_Cur_Working(ProfileStr)
        > Load_Get_Person_Profile(PersonProfileFilename, TEST_PERSON_NUM)
"""
# 提取基本信息函数：Check_BasicInfo
# 函数：针对简历文档，通过时间表达划分为句子条目，将"基本信息"一类合并为一条.

# Check Time.
def Get_Seqs_and_Times(OrgName):
    """函数：检测有效时间表达，非常有用。
    Output:
        <1>postag_words_seq,  分词序列，与下文的pos序列相同，可以公用索引；
        <2>postag_pos_seq, 词性标注序列，与上分词序列可以公用索引；
        <3>TimeSeqStart, 时间表达Start序列，其实在后，表示自身，并不表示下一位。
        <4>TimeSeqEnd  时间表达 End序列，其实在前，表示自身。
        """
    OrgName = change_2_unicode(OrgName)
    # print "Into Detecting working times, Org Names = "
    line_postag_list = pseg.cut(OrgName)
    postag_words_seq = []
    postag_pos_seq = []
    for word_postag in line_postag_list:
        postag_words_seq.append(word_postag.word)
        postag_pos_seq.append(word_postag.flag)
        pass
    TimeSeqStart, TimeSeqEnd = CheckTimePos(postag_pos_seq)
    # print "After Check Time Pos , time seq start = ", TimeSeqStart, " time seq end = ", TimeSeqEnd


    # 过滤掉以单位开头的内容;
    InValid_Time_Syn_List = [u"年", u"月", u"日", u"千", u"万", u"亿"]
    invalid_seq_id_list = []
    for time_id in range(len(TimeSeqStart)):
        time_str = u"".join(postag_words_seq[TimeSeqStart[time_id]: TimeSeqEnd[time_id] + 1])
        for ivalid_time_syn in InValid_Time_Syn_List:
            #if postag_words_seq[TimeSeqStart[time_id]].startswith(ivalid_time_syn) or (TimeSeqStart[time_id] == TimeSeqEnd[time_id]):


            if time_str.startswith(ivalid_time_syn) or (u"年" not in time_str and u"岁" not in time_str):
                invalid_seq_id_list.append(time_id)
                break
            """
            if postag_words_seq[TimeSeqStart[time_id]].startswith(ivalid_time_syn) or (u"年" not in postag_words_seq[TimeSeqStart[time_id]] and u"岁" not in  )):
                invalid_seq_id_list.append(time_id)
                break
                pass
            """
            pass
        pass
    # print  "In DetectingWorkingTime, Time start seq = ", TimeSeqStart, "Time end seq = ", TimeSeqEnd
    # print "Invalid seq list = ", invalid_seq_id_list
    TimeSeqStart = [TimeSeqStart[time_seq_id] for time_seq_id in range(len(TimeSeqStart)) if time_seq_id not in invalid_seq_id_list]
    TimeSeqEnd = [TimeSeqEnd[time_seq_id] for time_seq_id in range(len(TimeSeqEnd)) if time_seq_id not in invalid_seq_id_list]
    # print "Valid? DetectingWorkingTime, Time start seq = ", TimeSeqStart, "Time end seq = ", TimeSeqEnd

    # 添加对"现任，曾任，至今"等隐藏时间词的支持;

    for hid_time_syn in Hidden_Time_Syn_List:
        if hid_time_syn in postag_words_seq:
            print "hid_time_syn = ", hid_time_syn
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

    # Regularization
    TimeSeqStart, TimeSeqEnd = regular_time_headings(TimeSeqStart, TimeSeqEnd, postag_words_seq)

    # print "Into Detecting working times, Org Names = "
    return postag_words_seq, postag_pos_seq, TimeSeqStart, TimeSeqEnd
    pass


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
        hidden_time_item = check_listitem_in_content(Hidden_Time_Syn_List, time_seq_str_list[0])
        if hidden_time_item:
            hidden_exp_list = re.split(hidden_time_item, time_seq_str_list[0])
            time_seq_str_list.insert(0, hidden_exp_list[0])
            time_seq_str_list[1] = hidden_time_item + hidden_exp_list[1]
        pass
        '''

    # 检测首部分是否应该加入第一句: 若第一句不是基本资料，则首部分独立；否则第一句加入首句。
    first_basic_info = "".join(postag_words_seq[: TimeSeqStart[0]])
    # print "First info = ", first_basic_info
    if check_listitem_in_content(Basic_info_Syn_List, time_seq_str_list[0]):
        time_seq_str_list[0] = first_basic_info + time_seq_str_list[0]
    else:
        time_seq_str_list.insert(0, first_basic_info)
    # print "Into Divide Divide_TimeSeq_Working"
    return time_seq_str_list
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
            """
            # 判断是否动词开头，如果是，则舍弃
            content_words_seq, content_pos_seq = get_pseg_seq(Org_name)
            if len(content_pos_seq) >= 1 and content_pos_seq[0] in No_OrgName_Start_Pos_List:
                return
            """
            # Final check org and pos names.
            if not final_check_org_pos(Org_name, Position_name):
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
                """
                content_words_seq, content_pos_seq = get_pseg_seq(Org_name)
                if len(content_pos_seq) >= 1 and (content_pos_seq[0] in No_OrgName_Start_Pos_List):
                    return
                """
                if not final_check_org_pos(Org_name, position_name):
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
                """
                content_words_seq, content_pos_seq = get_pseg_seq(org_name)
                if len(content_pos_seq) >= 1 and content_pos_seq[0] in No_OrgName_Start_Pos_List:
                    return
                """
                if not final_check_org_pos(org_name, Position_name):
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
    for w_id in range(len(postag_words_seq)):
        print "w = ", postag_words_seq[w_id], " pos = ", postag_pos_seq[w_id]
    print len(TimeSeqStart)
    for t_id in range(len(TimeSeqEnd)):
        print ' start  = ', TimeSeqStart[t_id], " end = ", TimeSeqEnd[t_id]

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
        for time_i in range(len(TimeSeqEnd)):
            time_str = u"".join(postag_words_seq[TimeSeqStart[time_i]: TimeSeqEnd[time_i] + 1])
            if u"年" in time_str or u"岁" in time_str:
                time_index_end, time_index_start = TimeSeqEnd[time_i], TimeSeqStart[time_i]
                break

        # time_index_end, time_index_start = TimeSeqEnd[0], TimeSeqStart[0] # 第一个时间表达，默认为年龄或者出生时间
        birth_age_str = "".join(postag_words_seq[time_index_start:time_index_end + 1])
        print "birth age str = ", birth_age_str
        birth_age_str = Check_BirthInfo(birth_age_str)
        print u"\t*出生/年龄* = ", birth_age_str
        Person_Profile_Data["Person_Basic_Info"]["Birth"] = birth_age_str
        pass

    # 国籍: 如果是中国，不显示；如果不是，写出;
    country_syn_list = [u"国籍", u"中国籍"]
    country_syn = check_listitem_in_content(country_syn_list, postag_words_seq)
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
    Education_syn_List = [u"研究生", u"博士",u"硕士",u"硕士学位", u"本科",u"学士", u"工商管理学士", u"学士学位", u"大学专科", u"专科",u"大专", u"中专", u"高中", u"职高", u"初中", u"EMBA", u"MBA", u"学历"]
    degree_list = [u"博士", u"硕士", u"大学", u"本科", u"专科", u"大学专科", u"中学"]
    edu_syn_index = 0
    edu_syn_content = ""
    for edu_syn in Education_syn_List:
        if edu_syn in postag_words_seq:
            edu_syn_index = postag_words_seq.index(edu_syn)
            #if postag_words_seq[edu_syn_index - 1] == "博士" or postag_words_seq[edu_syn_index - 1] == "硕士" or postag_words_seq[edu_syn_index - 1] == "大学":
            if postag_words_seq[edu_syn_index - 1] in degree_list:
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
    school_name = get_school_snippet(ProfileStr)
    if len(school_name) > 2:
        print u"\t*学校* = ", school_name
        Person_Profile_Data["Person_Basic_Info"]["School"] = school_name


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
    working_item = change_2_unicode(working_item)

    # print "Into Checking working item, working item = ", working_item
    orgname = ""
    working_item_position_name = ""

    # 停用词去除：等职，等职务，
    working_item = re.sub(u"(等职)+务*", "", working_item)
    print "After removing stopwords, Woking Item = ", working_item

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


# 处理单条任职经历，包括曾任和现任：Time, Org, Position;
def Check_WorkingSent(Cur_Working_Sent):
    """函数：接受按照时间序列划分的工作描述片段，做下一步处理。
    步骤：
        1) 显示包含的时间表述;
        2) 符号和关键字的划分，层次单元划分；
    """
    global Person_Profile_Data
    org_tip_list = [u"在", u"于", u"於", u"加入", u"就职于"]
    pos_tip_list = [u"担任", u"为", u"任", u"就职", u"任职", u"历任", u"工作"]
    Cur_Working_Sent = change_2_unicode(Cur_Working_Sent)
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
    org_tip_item = check_listitem_in_content(org_tip_list, WorkingSent_Words_Seq)

    pos_tip_item = check_listitem_in_content(pos_tip_list, WorkingSent_Words_Seq)

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
    ProfileStr = change_2_unicode(ProfileStr)
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

    pre_tag_list = [u"历任", u"曾任", u"任职", u"任", u"工作", u"先后", u"就任", u"就职于", u"就职", u"创办", u"创立", u"创建", u"擢升"]
    cur_tag_list = [u"现任", u"至今", u"目前", u"兼任", u"起任", u"起", u"兼职情况："]
    pre_sents_list = []
    cur_sents_list = []
    info_sents_list = []
    # Step-2: Sentences Classification: 句子分类，分现任/曾任方法2: 如果出现现任，至今等的，为Cur; 否则为曾经;

    for working_sent in Profile_Sentences_List:
        if check_listitem_in_content(Basic_info_Syn_List, working_sent):
            info_sents_list.append(working_sent)
            print "info sent = ",working_sent
        elif(check_listitem_in_content(cur_tag_list, working_sent)):
            print "cur sent = ",working_sent
            cur_sents_list.append(working_sent)
        elif(check_listitem_in_content(pre_tag_list, working_sent)):
            print "pre sent = ",working_sent
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
        basic_info_sent = change_2_unicode("".join(info_sents_list))
        print "\t\tBasic sent ", basic_info_sent
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
            print "\t\tBasic sent.", basic_info_sent
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
            # print "\n\n#### Person Id = ", person_id, "Name = ", unicode(person_profile.split()[0], "utf-8"),"\n"
            print "\n\n#### Person Id = ", person_id, "Name = ", unicode(person_profile_head[1], "utf-8"),"\n"

            pass
        else:
            print "\n\n********************\nPerson Id = ", person_id, "\n********************"
        Divide_Pre_Cur_Working(person_profile)
        pass
    PersonProfileFile.close()
    pass



def main():
    ProfileStr = "刘宏女士，女，53岁，1962年生，1962年5月出生，中国国籍，无境外永久居留权，毕业于湖南生物与机电工程职业技术学院，博士研究生学历。曾任中国纺织大学团委副书记；上海纺织品进出口公司开发部经理助理、党办宣传员；上海市华达进出口公司董事兼副总经理；上海市对外经济贸易委员会办公室秘书，借调上海市政府、上海市人大工作（历任上海市对外经济贸易委员会副处级调研员、正处级调研员）；联合发展党委委员、副总经理，党委副书记、副总经理（主持工作）；上海外高桥（集团）有限公司党委委员、副总经理。现任本公司副董事长，上海外高桥集团股份有限公司党委书记、董事兼副总经理，上海外高桥西北保税物流有限公司董事长，联合发展党委书记、董事、总经理，上海市外高桥保税区三联发展有限公司执行董事、法定代表人。"
    Load_Get_Person_Profile(PersonProfileFilename, TEST_PERSON_NUM)
    pass

if __name__ == '__main__':
    main()
