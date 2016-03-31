#coding:utf-8

'''
    Title: TestComPersonProfileAnalysisLib.py
    Function:
        对 ComPersonProfileAnalysisLib.py 进行测试，对每个函数进行测试，注意，每个。
    Date: 2016.01.25

'''
from IMSLZY_Lib_ComPersonProfileAnalysis import *


def test_jieba_wordseg():
    test_str = u"兼任企业家协会"
    words_seq_cut = pseg.cut(test_str)
    words_seq = []
    for w in words_seq_cut:
        words_seq.append(w.word)
        print "w = ", w.word


def Test_Get_Seqs_and_Times():
    # Testing Check Orgname times.
    OrgNameList = [u"杜明迤：男，35岁，大学学历，政工师，"]
    for org_name in OrgNameList:
        print " Test content = ", org_name
        postag_words_seq, postag_pos_seq,TimeSeqStart,TimeSeqEnd = Get_Seqs_and_Times(org_name)
        print "Time Seqs"
        for time_start in TimeSeqStart:
            print "t start = ", time_start
        for time_end in TimeSeqEnd:
            print "t end = ", time_end
        print "Time expressions."
        for time_id in range(len(TimeSeqStart)):
            print "".join(postag_words_seq[TimeSeqStart[time_id]: TimeSeqEnd[time_id] + 1])

        postag_words_seq = [x for x in postag_words_seq]
        for post_word in postag_words_seq:
            print "post_word = ", post_word

        # 查看 Posttags
        CheckTimePos(postag_pos_seq)
        pass
    pass


def test_get_school_snippet():
    profile_basic_str = u"1970年西安交通大学电机系毕业,1974年至今在电气学院电器教研室任教,"
    profile_basic_str = u"并持有昆士兰科技大学会计学学士学位及香港理工大学企业金融学硕士学位"
    school_snippet_str = get_school_snippet(profile_basic_str)
    print "School snippet str = ", school_snippet_str


def Test_CheckTimePos():
    PosSeq = [u'm', u'm', u'm', u'm', u'p', u'm', u'm', u'm',
              u'm', u'x', u'n', u'n', u'n', u'x', u'm', u'm',
              u'm', u'm', u'd', u'n', u'n', u'n']
    content = u"杜明迤：男，35岁，大学学历，政工师，"
    content_words_seq, content_pos_seq = get_pseg_seq(content)

    CheckTimePos(content_pos_seq)
    pass


def Test_Check_GenderCall():
    gender_call_tip = u"先生"
    print Check_GenderCall(gender_call_tip)
    pass


def Test_Check_BirthInfo():
    # birth_age_str = u"1964年9月"
    birth_age_str = u"52岁"
    print Check_BirthInfo(birth_age_str)
    pass




def Test_PostPro_Position_Name():
    Position_name = u"历任店长"
    Position_name = u"副总裁职务"
    print PostPro_Position_Name(Position_name)
    pass


def Test_DetectTimeForWorkingSent():
    Org_name = u"医药导报副主任"
    print DetectTimeExpForOrgname(Org_name)
    pass


def Test_Check_BasicInfo():
    # basciInfoText = "高亦岑 高亦岑：中国国籍，无境外永久居留权，1972年4月生，安徽广播电视大学大专。"
    # basicInfoText = "沈善通，男，1964年10月9日出生，汉族，中国籍，无境外永久居留权2009年6月毕业于浙江省党校公共管理学专业，大专学历"
    basicInfoText = "陈烨平女士，1985年12月出生，中国国籍，无境外永久居留权，毕业于安徽黄山旅游学校旅游专业，专科学历"
    basicInfoText = u"公司|||李佳|||李佳，女，本科学历。江阴万事兴医疗器械股份有限公司董事。"
    basicInfoText = u"常州科威天使环保科技股份有限公司|||周革|||周革：男，1968年7月出生，美国国籍，无境外永久居留权，毕业于常州工学院，大专学历。"
    basicInfoText = u"潘忠武先生：中国国籍，现年53岁，本科学历，1966年参加工作，"

    Check_BasicInfo(basicInfoText)
    pass





def Test_Divide_TimeSeq_Working():
    """测试函数：测试根据时间表达进行句子划分的结果。"""
    # ProfileStr = u"陈信东 陈信东先生，副总经理，1968年9月出生，中国国籍，无境外永久居留权，大学本科学历。陈信东先生自1990年起进入川隆纺织有限公司工作，历任团委书记、车间主任、机动厂厂长、企划部长兼总经办主任、总经理助理；自1999年起加入福建昇兴，任执行董事助理兼总经办主任；自2003年3月至2004年9月就职于福建省中心检验所，任职认证咨询师、企业管理咨询师；自2004年10月再次加入本公司任职生产部负责人；自2012年12月起任本公司副总经理。"

    # ProfileStr = u"孟国强 孟国强：公司独立董事，男，出生于1953年，中国国籍，无永久境外居留权，研究生学历，1975年毕业于北京师范学院中文系，2002年于中央党校经济系研究生毕业。先后在中国企业管理协会秘书处、物资部政研司、国内贸易部市场司、政策法规司、国家国内贸易局行业司担任副处长、处长及副司长等职，曾任中国物流与采购联合会副秘书长，2008年至今任中国建筑材料流通协会会长。"
    # ProfileStr = u"赵志强先生，大专文化，MBA在读，注册税务师，曾任江阴市税务局滨江分局副局长，现任凯诺科技股份有限公司第二届董事会董事、副总经理兼董事会秘书。"
    # ProfileStr = u"周永平，现任江阴市协力毛纺织厂法人代表，凯诺科技股份有限公司第一届董事会董事"
    ProfileStr = u"哈尔滨誉衡药业股份有限公司|||刘月寅|||刘月寅：女，出生于1986年3月，硕士学历，中国国籍，无境外居留权。2010年6月至2013年8月，任职于北汽福田汽车股份有限公司，2013年9月加入公司，任证券事务助理。刘月寅女士具有深圳证券交易所颁发的《董事会秘书资格证书》，符合证券事务代表的任职资格；与本公司或其控股股东、实际控制人以及其他董事、监事、高级管理人员无任何关联关系，未直接或间接持有上市公司股份，未受过中国证监会及其他有关部门的处罚和证券交易所惩戒。同意聘任国磊峰先生、杨海峰先生担任公司副总经理，任期三年，至第三届董事会届满为止。"
    ProfileStr = u"李佳，女，本科学历。江阴万事兴医疗器械股份有限公司董事。"
    ProfileStr = u"湖北新洋丰肥业股份有限公司|||颜甫全|||2005-03-24连任。颜甫全，男，汉族，湖南娄底人，中共党员，大学文化程度，高级会计师。历任衡阳纺机厂财务科会计、总师办公室副主任、财务处处长、总会计师、厂长，中国纺织机械（集团）有限公司财务部部长，中国恒天集团公司副总会计师兼财务部部长，现任中国恒天集团公司总会计师，中国纺织机械（集团）有限公司总会计师，中国服装股份有限公司监事会主席。"
    ProfileStr = u"四川金路集团股份有限公司|||傅美巧|||2）傅美巧，女，新光建材城监事，1975年10月出生，中国国籍，无境外居留权。最近三年主要担任新光饰品财务总监、万厦房产及新光建材城监事。"
    ProfileStr = u"上海零动数码科技股份有限公司|||戴炜|||戴炜，男，中国国籍，无境外居留权，1978年1月出生，毕业于上海工程技术大学服装学院，本科学历。2001年至2003年任上海世纪出版集团《理财周刊》杂志社职员；2003年至2004年任日本《CHAI》杂志社职员；2004年1月8日至2009年9月9日创办上海敬一文化传播有限公司并担任公司执行董事兼总经理；2009年4月10日创办上海释尊广告有限公司并担任执行董事兼总经理；2014年3月19日起当选并担任上海零动数码科技股份有限公司董事，任期为三年。"
    ProfileStr = u"浙江康德药业集团股份有限公司|||章枕东|||营销总监：章枕东，男，中国国籍，无境外永久居留权。1972年12月出生，大专学历。1990年毕业于东北财经大学。1990年9月至1993年8月，任职于浙江省地质三大队；1993年9月至1997年12月，任浙江婴幼儿用品厂总经理；1998年1月至2011年12月，任海南亚洲制药集团销售经理；2012年1月至2012年2月，任海南亚洲制药集团销售经理；2012年3月至2013年2月，任浙江大航医疗科技有限公司销售副总经理；2013年3月至今，任公司营销总监。"

    Profile_Sentences_List = Divide_TimeSeq_Working(ProfileStr)
    print "Num of time seq sents ， = ", len(Profile_Sentences_List)
    if Show_Profile_Sents == 1:
        for sent in Profile_Sentences_List:
            if u"。" in sent:
                print "\t Full Stop Sent = ", sent
            else:
                print "\tProfile Sent = ", sent
    if Show_Profile_Str == 1:
        print "> ",ProfileStr
        pass
    pass


def Test_Detect_MarkSplit_Mode():
    working_item = u"历任公司品质部主管、生产部经理助理、生产部经理、生产二部总监"
    Detect_MarkSplit_Mode(working_item)
    pass


def Test_Check_IF_WorkingSent():
    WorkingSent = u"1992年起，先后在美的集团、顺德指日工作。"
    if_workingsent = Check_IF_WorkingSent(WorkingSent)
    print "If workingsent = ", if_workingsent
    pass





def Test_Jieba():
    str_content = u"锺棋伟先生,工商管理学士,主席。一九七六年加入本集团并被委任为董事。於二零零零年被选为主席。於香港地产及建筑业务方面拥有超逾三十年之经验。锺仁伟先生及锺英伟先生之兄。"
    str_content = u"周永平，现任江阴市协力毛纺织厂法人代表，凯诺科技股份有限公司第一届董事会董事"
    str_content = u"1995年7月至1997年7月就职于东莞糖酒集团美佳连锁超市有限公司"
    str_content = u"常州科威天使环保科技股份有限公司|||周革|||周革：男，1968年7月出生，中国籍，无境外永久居留权，毕业于常州工学院，大专学历。"
    str_content = u"2011年1月起任公司董事长。"
    str_content = u"潘忠武先生：中国国籍，现年53岁，本科学历，1966年参加工作，"
    str_content = u"1995年7月至1997年7月就职于东莞糖酒集团美佳连锁超市有限公司"
    str_content = u"1993年8月，任职于浙江省地质三大队"
    str_content = u"2002年9月至今，创立深圳市华深科技有限公司，并任董事长、总经理"
    str_content = u"上海零动数码科技股份有限公司|||戴炜|||戴炜，男，中国国籍，无境外居留权，1978年1月出生，毕业于上海工程技术大学服装学院，本科学历。2001年至2003年任上海世纪出版集团《理财周刊》杂志社职员；2003年至2004年任日本《CHAI》杂志社职员；2004年1月8日至2009年9月9日创办上海敬一文化传播有限公司并担任公司执行董事兼总经理；2009年4月10日创办上海释尊广告有限公司并担任执行董事兼总经理；2014年3月19日起当选并担任上海零动数码科技股份有限公司董事，任期为三年。"
    str_content = u"2011年11月至今任本公司监事（职工代表监事）。"
    str_content = u"2005年4月至2008年3月就职于深圳赛银远古任项目经理"
    str_content = u"曾任职于上海市人民检察院政策研究室、上海市万国律师事务所、上海天和律师事务所。"

    postag_list = pseg.cut(str_content)
    for w_id, w in enumerate(postag_list):
        print "word id = ", w_id, " word = ", w.word, " flag = ", w.flag


def Test_PostPro_Org_Name():
    Org_Name = u"任山德晶琴乐器公司"
    Org_Name = PostPro_Org_Name(Org_Name)
    print "PostPro_Org_Name = ", Org_Name

    pass


def Test_Sents_Segmentation():
    ProfileStr_Contents = u"2005-03-24连任。颜甫全，男，汉族，湖南娄底人，中共党员，大学文化程度，高级会计师。历任衡阳纺机厂财务科会计、总师办公室副主任、财务处处长、总会计师、厂长，中国纺织机械（集团）有限公司财务部部长，中国恒天集团公司副总会计师兼财务部部长，现任中国恒天集团公司总会计师，中国纺织机械（集团）有限公司总会计师，中国服装股份有限公司监事会主席。"
    full_mark_spot_list = Sents_Segmentation(ProfileStr_Contents)
    for sent in full_mark_spot_list:
        print "Sent = ", sent


def Test_Show_OrgName_Position_Name():
    orgname = u"云南省开远市医药公司"
    posname = u"门市主任"
    orgname, posname = u"1982年任甘肃七七八厂", u"工程师"
    Show_OrgName_Position_Name(orgname, posname)
    pass



def Test_Check_Workig_Item():
    print "Into Test_Check_Workig_Item"
    # working_item = u"医药导报副主任编委"
    # working_item = u"张华农先生是中国化学与物理电源行业协会副理事长"
    # working_item = u"2003年|加入广东棕榈园林工程有限公司"
    # working_item = u"1998年7月至2000年1月就职于新疆乌鲁木齐市广货专卖店"
    # working_item = u"2005年4月-2008年5月任武汉政和实业有限公司弱电部经理"
    # working_item = "同时担任北京市高通律师事务所创始合伙人、主任、
    # 中国国际经济贸易仲裁委员会首席仲裁员、中华全国律师协会金融证券专业委员会委员、宣传联络委员会委员、欧美同学会留美分会理事、北京市朝阳区律师协会理事、金融证券业务研究会主任、首都经济贸易大学兼职教授、法学硕士导师"
    # working_item = u"一九七六年加入本集团并被委任为董事。"
    # working_item = u"任东阳新媒有限宣传部经理"
    # working_item = u"佛山泰银富时创业投资中心（有限合伙）执行合伙人"
    working_item = u"任职中文在线副总经理职务"
    working_item = u"2009年4月10日创办上海释尊广告有限公司并担任执行董事"
    working_item = u"1982年任甘肃七七八厂工程师"
    working_item = u"2012年5月至今任本公司总裁"
    working_item = u"2011年11月至今任本公司监事（职工代表监事）。"
    working_item = u"技术推广部副主任"
    working_item = u"技术科科长等职"
    working_item = u"2002年至2008年任浙江建达科技有限公司"
    working_item = u"2012年9月22日获委任为我们的独立非执行董事"
    working_item = u"彼获委任为香港立法会非官守议员"
    working_item = u"2008年5月至今担任厦门国贸独立董事"
    working_item = u"2005年4月至2008年3月就职于深圳赛银远古任项目经理"
    working_item = u"深圳市防静电行业协会会长"
    working_item = u"深圳红粹投资企业(有限合伙)执行事务合伙人"
    working_item = u"先后担任北京致一健康科技有限公司"
    working_item = u"大得控股董事。"
    working_item = u"浙江非线总经理"
    working_item = u"2010年11月就职公司"
    working_item = u"海澜集团有限公司董事长"
    working_item = u"2010年5月至2012年3月任网易副总裁、门户事业部总裁"
    working_item = u"2009年起任雏鹰农牧独立董事"
    working_item = u"深圳市发展和改革委投资处处长"
    working_item = u"1987年8月至1989年10月，龙游供销社工作"
    working_item = u"历任解放军总参谋部某局专业技术中尉"
    working_item = u"首席技术官。"
    working_item = u"１９９５年１２月至１９９８年４月任热电厂组干处处长。"
    working_item = u"2011年2月至2013年11月任掌讯集团有限公司副总裁"
    working_item = u"任上海乐通通信设备（集团）股份有限公司运营中心副总裁。"
    working_item = u"2013年至今供职于科润电力。"
    working_item = u"历任董事会秘书、副总经理"
    working_item = u"1991年10月在大庆石油学院工作"
    working_item = u"2012年11月至今任广东银商投资有限公司法定代表人"
    OrgName, PosName = Check_Workig_Item(working_item)
    print "After checking , orgname = ", OrgName, " PosName = ", PosName
    Show_OrgName_Position_Name(OrgName, PosName)
    pass

def Test_Check_WorkingSent():
    # Cur_Working_Sent = u"先后在中国企业管理协会秘书处、物资部政研司、国内贸易部市场司、政策法规司、国家国内贸易局行业司担任副处长、处长及副司长等职，"
    # Cur_Working_Sent = u"2010年7月至今在深捷科技任技术部经理"
    # Cur_Working_Sent = u"2006年至2007年就职于珠海市华逸格广告有限责任公司，任财务经理；"
    # Cur_Working_Sent = u"曾任戴维有限总工程师办公室主任、标准化部主任"
    # Cur_Working_Sent = u"就职于上海市人民检察院政策研究室、上海市万国律师事务所、上海天和律师事务所"
    Cur_Working_Sent = u"2007年6月至2012年11月担任爆米花网副总裁职务"
    Cur_Working_Sent = u"历任三五四三工厂计划员、调度员、统计员、副处长、处长、经销公司总经理、厂长助理、副厂长"
    Cur_Working_Sent = u"1988年--1997年在湖南省进出口总公司就职"
    Cur_Working_Sent = u"1995年7月至1997年7月就职于东莞糖酒集团美佳连锁超市有限公司"
    Cur_Working_Sent = u"1993年8月，任职于浙江省地质三大队"
    Cur_Working_Sent = u"2003年10月至今，参与创建广州巴菲特投资咨询有限公司，担任总经理"
    Cur_Working_Sent = u"2002年9月至今，创立深圳市华深科技有限公司，并任董事长、总经理"
    Cur_Working_Sent = u"2009年3月至今，就职上海锦湖日丽塑料有限公司，任项目经理"
    Cur_Working_Sent = u"历任广东温氏食品集团有限公司办公室主任、副总经理、董事、副总裁、执行董事"
    Cur_Working_Sent = u"2009年4月10日创办上海释尊广告有限公司并担任执行董事"
    Cur_Working_Sent = u"1996年5月至1998年12月，任实达集团广东海达信息设备有限公司税务经理"
    Cur_Working_Sent = u"2005年4月至2008年3月就职于深圳赛银远古任项目经理"
    Cur_Working_Sent = u"先后在电子工业部、信息产业部综合规划司担任处长、副司长、信息产业部计算机信息系统集成资质办公室主任等职务,主持或参加过多个国家电子工业及电子信息产业五年规划和专项规划的编制,参与多个国家重大电子工程建设"
    Cur_Working_Sent = u"历任上海复旦大学管理学院副教授;中国南山开发(集团)股份有限公司研究发展部总经理;招商局集团有限公司业务发展部副总经理等职"
    Cur_Working_Sent = u"1987年8月至1989年10月，龙游供销社工作"
    Cur_Working_Sent = u"1991年10月在大庆石油学院工作"
    Cur_Working_Sent = u"2012年11月至今任广东银商投资有限公司法定代表人"
    Cur_Working_Sent = u"2004年4月至2015年5月，负责北京金诺佳音文化传播有限公司全面经营管理工作"
    Cur_Working_Sent = u"1982年至1984年任上海财经大学会计系讲师"
    Cur_Working_Sent = u"2008年4月至2010年6月任谷歌中国信用分析师"
    Cur_Working_Sent = u"2012年11月担任爆米花网副总裁职务；"

    # 分词结果
    postag_list = pseg.cut(Cur_Working_Sent)
    for w in postag_list:
        print "word = ", w.word, " flag = ", w.flag
    Check_WorkingSent(Cur_Working_Sent)
    pass

def Test_Divide_Pre_Cur_Working():
    ProfileStr = u"苏州金枪新材料股份有限公司|||俞雪华|||俞雪华：男，1963年出生，中国国籍，无永久境外居留权，硕士，会计学副教授，1984年7月～1985年7月，南京农业大学团委干事；1985年7月～1993年7月，南京农业大学经贸学院讲师；1993年7月～1999年5月，苏州大学商学院讲师；1999年5月至今，苏州大学商学院副教授；2008年9月至今，苏州大学商学院院长助理，MBA中心主任。2014年10月至今任股份公司独立董事。"
    ProfileStr = u"深圳市赛为智能股份有限公司|||陈中云|||陈中云：男，1962年出生，中国国籍，无境外永久居留权，硕士研究生学历，中共党员，注册自动化系统工程师。1988年--1997年在湖南省进出口总公司就职；1998年--至今任职公司，现任公司董事。兼任广东赛翼智能科技有限公司董事、深圳前海赛为智慧城市科技有限公司董事。"
    ProfileStr = u"江苏省交通规划设计院股份有限公司|||明图章|||明图章,男,1963年生,中国国籍,无永久境外居留权,教授级高级工程师,江苏省有突出贡献中青年专家,交通部“新世纪十百千人才工程”第一层次人选。江苏省优秀工程勘察设计师。1983年7月东南大学道路工程专业本科毕业,1989年5月东南大学道路工程专业硕士研究生毕业。1992年12月到交通院工作,历任道路设计室副主任、主任、副总工程师、副院长、院长等职务。2005年8月起任交通院有限董事长、总经理。2008年8月起任交通院有限董事长。2011年1月起任公司董事长。"
    ProfileStr = u"新疆天富能源股份有限公司|||潘忠武|||潘忠武先生：中国国籍，现年53岁，本科学历，1966年参加工作，1973年至1980年任华北石油运输指挥部主任，其间兼任华北石油技术学校筹备处主任，1980年至1984年任首汽国宾车队负责人，1984年至1995年任新疆人民政府驻京办事处处长和基建办公室主任，1995年至1996年任国务院发展研究中心服务局经济合作部副部长，1996年至1998年兼任国发兴业投资公司内部董事，1996年至今任中国社会经济决策咨询中心秘书长。"
    ProfileStr = u"无锡先导自动化设备股份有限公司|||缪丰|||缪丰:男,中国国籍,无境外永久居留权,1979年8月出生,本科学历,江南大学机电一体化专业毕业。2002年7月至2002年11月,任高新张铜股份有限公司设备科技术员;2002年12月至2005年2月,任无锡新区华光自动化系统有限公司技术支持及售后服务专员;2005年3月至2008年3月,任先导有限电气研发部负责人,2008年3月至2011年11月任电气研发部经理,2011年12月20日起,任本公司副总经理,负责公司的电气研发工作。"
    ProfileStr = u"西安达刚路面机械股份有限公司|||李太杰|||李太杰先生：中国国籍，汉族，1935年出生，中共党员，本科学历。东北工学院筑路机械专业毕业，副教授。1993年起享受国务院―政府特殊津贴‖，1955年8月至2007年11月，历任辽宁省交通厅公路局机械处技术员，西安公路学院筑机系主任，西安达刚路面车辆有限公司执行董事、经理，西安达刚公路沥青设备有限公司董事长，西安达刚公路机电科技有限公司总工程师等职；2007年12月至2010年12月任西安达刚路面机械股份有限公司副董事长；2010年12月至2013年11月任西安达刚路面机械股份有限公司副董事长，2013年11月起退休。4、其他持股在10%以上的法人股东无。"
    ProfileStr = u"深圳市昌红科技股份有限公司|||赵阿荣|||赵阿荣先生:中国国籍,无永久境外居留权,1961年出生,高中学历。曾担任浙江省上虞市驿亭塑胶厂车间组长、浙江省上虞市中利镇油漆公司仓管组长,现担任公司职工代表监事、仓库组长"
    ProfileStr = u"四川金路集团股份有限公司|||傅美巧|||2）傅美巧，女，新光建材城监事，1975年10月出生，中国国籍，无境外居留权。最近三年主要担任新光饰品财务总监、万厦房产及新光建材城监事。"
    ProfileStr = u"中国再生能源投资有限公司|||阮立基|||阮立基先生,捷腾电子(深圳)有限公司董事兼董事总经理。於一九八六年加入JIC集团前,彼於一九八四年至一九八六年期间於SlexsWatchCo.,Ltd.担任生产经理。於一九九四年,彼获JIC集团保送往日本学习液晶注入技术。其後,彼成功在捷腾电子(深圳)有限公司设立LCD前工序、中工序及後工序生产线。阮先生於二零零零年获擢升为捷腾电子(深圳)有限公司副董事总经理,於二零零五年成为董事总经理。彼於LCD制造行业拥有约二十年经验。"
    ProfileStr = u"深圳市浩丰科技股份有限公司|||朱亿廖|||朱亿廖，男，1984年出生，中国国籍，无境外永久居留权，专科学历。2007年2月至2010年5月在深圳市龙岗区光台电子厂肖后任职项目工程会、生产技术主管，2010年7月至2012年6月在深圳市东明胜五金制品有限公司任职产品工程会，2013年1月至2014年7月任公司工程会，2014年8月任研发部经理。"
    ProfileStr = u"广州集泰化工股份有限公司|||李军|||5、李军先生，中国国籍，出生于1974年11月，研究生学历。1993年9月至1995年7月就读于河南省周口师范高等专科学校（现周口师范学院）数学系；1995年7月至1997年7月就职于东莞糖酒集团美佳连锁超市有限公司，历任班长、店长；1997年8月至1998年6月就职于屈臣氏集团（深圳）食品饮料有限公司，担任销售主任；1998年7月至2000年1月就职于新疆乌鲁木齐市广货专卖店，担任店长；2000年2月至2001年4月就职于深圳东鼎数字电器有限公司，担任大区经理；2001年5月至2003年2月就职于深圳市万佳百货股份有限公司，历任主管、部门副经理；2003年3月至2003年10月就职于广东本草药业连锁有限公司，担任购销部经理；2003年10月至今，参与创建广州巴菲特投资咨询有限公司，担任总经理。现任广东泰银投资有限公司总经理，广东嘉信瑞成创业投资中心（有限合伙）执行合伙人，佛山泰银富时创业投资中心（有限合伙）执行合伙人。现任公司董事。"
    ProfileStr = u"苏州金枪新材料股份有限公司|||俞雪华|||俞雪华：男，1963年出生，中国国籍，无永久境外居留权，硕士，会计学副教授，1984年7月～1985年7月，南京农业大学团委干事；1985年7月～1993年7月，南京农业大学经贸学院讲师；1993年7月～1999年5月，苏州大学商学院讲师；1999年5月至今，苏州大学商学院副教授；2008年9月至今，苏州大学商学院院长助理，MBA中心主任。2014年10月至今任股份公司独立董事。"
    ProfileStr = u"北京聚智未来科技股份有限公司|||张强|||张强，男，1971年出生，中国籍，无境外永久居留权，研究生学历。1994年6月至2002年6月任中国农牧渔业国际合作公司项目经理，2002年7月至2009年10月任中国住房投资建设公司经理，2009年11月至今任北京必胜房地产开发公司副总经理，北京金佰瑞产业投资有限公司副总经理。2015年6月起任股份公司董事。"
    ProfileStr = u"上海零动数码科技股份有限公司|||戴炜|||戴炜，男，中国国籍，无境外居留权，1978年1月出生，毕业于上海工程技术大学服装学院，本科学历。2001年至2003年任上海世纪出版集团《理财周刊》杂志社职员；2003年至2004年任日本《CHAI》杂志社职员；2004年1月8日至2009年9月9日创办上海敬一文化传播有限公司并担任公司执行董事兼总经理；2009年4月10日创办上海释尊广告有限公司并担任执行董事兼总经理；2014年3月19日起当选并担任上海零动数码科技股份有限公司董事，任期为三年。"
    ProfileStr = u"北京金诺佳音国际文化传媒股份公司|||黎灶喜|||黎灶喜，男，1982年9月出生，中国国籍，无永久境外居留权，2002年6月毕业于广州交通运输中等职业学校，中专学历。2002年8月至2008年7月任跨时代手机店经理职务；2008年8月至2012年10月任广州市中营房地产办理有限公司销售经理职务；2012年11月至今任广东银商投资有限公司法定代表人、执行董事职务，2015年6月至今，担任北京金诺佳音国际文化传媒股份公司董事。"
    ProfileStr = u"北京网动网络科技股份有限公司|||陈云志|||陈云志，技术部经理，男，1979年出生，中国国籍，无境外永久居留权。1998年毕业于黄冈机电工程学校计算机应用专业；1998年至2000年在北京蓝色快车服务中心担任技术工程师；2000年至2001年北京深蓝世纪计算机有限责任公司担任技术工程师；2002年至2012年6月在北京网动科技有限公司担任技术部经理、资深技术支持；2012年6月至今在北京网动网络科技股份有限公司担任技术部经理。"
    ProfileStr = u"浙江康德药业集团股份有限公司|||章枕东|||营销总监：章枕东，男，中国国籍，无境外永久居留权。1972年12月出生，大专学历。1990年毕业于东北财经大学。1990年9月至1993年8月，任职于浙江省地质三大队；1993年9月至1997年12月，任浙江婴幼儿用品厂总经理；1998年1月至2011年12月，任海南亚洲制药集团销售经理；2012年1月至2012年2月，任海南亚洲制药集团销售经理；2012年3月至2013年2月，任浙江大航医疗科技有限公司销售副总经理；2013年3月至今，任公司营销总监。"
    ProfileStr = u"广州栋方生物科技股份有限公司|||崔婷|||崔婷，女，1981年3月出生，中国国籍，无境外永久居留权，毕业于青岛大学，本科学历。2002年5月至2004年3月任青岛金王财务中心管理会计；2004年3月至2009年3月任青岛金王财务中心税收主管；2009年3月至2013年12月任青岛金王财务中心副经理；2013年12月至今担任青岛金王财务中心副总经理兼财务管理部经理。2015年7月至今担任公司监事。"
    ProfileStr = u"深圳市浩丰科技股份有限公司|||朱亿廖|||朱亿廖，男，1984年出生，中国国籍，无境外永久居留权，专科学历。2007年2月至2010年5月在深圳市龙岗区光台电子厂肖后任职项目工程会、生产技术主管，2010年7月至2012年6月在深圳市东明胜五金制品有限公司任职产品工程会，2013年1月至2014年7月任公司工程会，2014年8月任研发部经理。"
    ProfileStr = u"浙江田歌实业股份有限公司|||刘竹青|||刘竹青女士，1989年出生，中国籍，无境外永久居留权。毕业于浙江大学，硕士学历，食品安全师（中级）职称。2013年加入田歌股份，现任技术部经理兼监事。监事任期自2015年8月至2018年8月。"
    ProfileStr = u"航天长征化学工程股份有限公司|||唐国宏|||唐国宏先生,1961年3月出生,中国国籍,博士,中共党员,研究员,无境外居留权。历任北京航空航天大学讲师、教授,中国航天工业供销公司副总经理,中国运载火箭技术研究院经营投资部部长、院长助理,航天煤化工董事长。现任中国运载火箭技术研究院副院长,航天投资控股有限公司监事,长征火箭工业有限公司董事长,中国卫星通信集团有限公司董事,深圳航天科技创新研究院理事,新加坡APMT公司董事,中国四维测绘技术有限公司董事,本公司董事长。"
    ProfileStr = u"济南同智创新能源科技股份有限公司|||王季伟|||王季伟先生，男，监事会主席，1987年6月出生，中国国籍，无境外永久居留权，本科学历。2010年-2011年在青岛锦绣前程节能玻璃科技有限公司担任工艺工程师；2011年3月-2014年8月在同智有限担任机械工程师；2014年9月至今担任同智科技监事，任期3年。"
    ProfileStr = u"广州杰赛科技股份有限公司|||刘汝林|||刘汝林:男,1945年3月出生,汉族,中共党员,研究员级高级工程师、教授,现任中国电子学会副理事长。1963年9月至1968年12月在清华大学工程力学数学系计算数学专业学习。1968年12月至1981年6月在北京广播器材厂任技术员、工程师。参加多项军事电子装备及国防重点工程开发研制,其中两项成果获国家科技大会成果奖。1981年6月至1993年9月任中国计算机技术服务公司(后为中软总公司)工程师、高级工程师,从事计算机软件及应用系统开发,开发成果获多项国家部委奖励。1993年9月至2005年6月先后在电子工业部、信息产业部综合规划司担任处长、副司长、信息产业部计算机信息系统集成资质办公室主任等职务,主持或参加过多个国家电子工业及电子信息产业五年规划和专项规划的编制,参与多个国家重大电子工程建设。2004年11月至2012年4月任中国电子学会秘书长,副理事长兼秘书长。2012年4月至今任中国电子学会副理事长。现任太极计算机、杰赛科技、新北洋股份、久其软件独立董事,并任中国科协全国委员会委员、工信部电子科技委委员,中国云计算技术与产业联盟副理事长等职务。"
    ProfileStr = u"东方财富信息股份有限公司|||沈国权|||沈国权，男，1965年3月生，中国国籍，无永久境外居留权，硕士研究生。曾任职于上海市人民检察院政策研究室、上海市万国律师事务所、上海天和律师事务所。现任上海市锦天城律师事务所高级合伙人，上海新华传媒股份公司独立董事、浙江水晶光电科技股份公司独立董事，报告期内任本公司独立董事，任期为2011年01月至2014年01月。"
    ProfileStr = u"天津市环宇橡塑股份有限公司|||宗浩|||宗浩，女，出生于1973年2月，中国国籍，无境外居留权。天津市第一轻工业学校，化工机械专业，中专学历。1995年12月至今历任天津市环宇橡塑股份有限公司操作工、内勤、商务部部长助理、商务部副部、物流部部长、采购部部长；2015年6月担任公司监事。"
    ProfileStr = u"视觉(中国)文化发展股份有限公司|||蒋顺生|||2004-6-3：任副总裁，蒋顺生，58岁，大专学历，助理经济师。历任常州服装二厂副厂长、常州市服装六厂厂长、莱索托豪华纺织有限公司总经理、远东实业股份有限公司股票办主任、总经理助理、党总支副书记、副总裁、董事会秘书等职。现任公司第四届董事会秘书。"
    ProfileStr = u"东风汽车集团股份有限公司|||范仲|||范仲,本公司董事。范先生为研究员级高级工程师,於一九八二年毕业於渖阳机电学院机械制造工艺及设备专业,获工学学士学位。彼加入东风汽车公司之前,曾任辽宁省北票市副市长。彼於一九九三年加入东风汽车公司出任朝阳柴油机副总经理。一九九九年至二零零一年,范先生曾任朝阳柴油机总经理,自二零零一年起担任该公司董事长。范先生在东风朝阳柴油机有限责任公司并无担任任何行政职位。自二零零一年起,范先生出任东风汽车公司党委副书记,并将於本公司上市後留任此职位。范先生在中国汽车工业拥有20多年从业和管理经验。"
    ProfileStr = u"江苏金瀚科技股份有限公司|||宗玉杰|||宗玉杰，女，1980年5月出生，中国国籍，无境外永久居住权，身份证号码：37292519800501****；住所：山东省青岛市李沧区金岭路10号；最近五年主要工作经历：2010年9月至2011年2月，担任北京众博恒信科技有限公司副总经理；2011年3月至2015年8月担任北京国石天玺投资有限公司副总经理；2015年8月至今主要担任北京国石天安投资有限公司、北京国石天辰拍卖有限公司、北京融信征信有限公司执行董事、总经理。"
    ProfileStr = u"中国创新支付集团有限公司|||黄荣智|||黄荣智先生,为SYSCAN,Inc.的副总裁,负责系统产品工程,尤其是软件开发、销售及制造支援,并负责现有产品的改良工作。<br><br>彼於系统工程(尤以软件开发而言)积逾20年经验。黄先生於一九九九年七月加入本集团之前,曾在ACCMicroelectronicsCorporation、ArtisCorp(Microtek图像艺术业务部)及02Micro,Inc.担任多个高级职位。彼持有美国加州西北理工大学机电工程学士学位。"
    ProfileStr = u"北京盖特佳信息科技股份有限公司|||叶长晖|||叶长晖，男，1976年9月出生，东华大学计算机系本科毕业，2006年进入盖特佳公司工作，现任北京盖特佳信息科技股份有限公司技术总监，主持公司多项信息技术产品的研发，拥有丰富的产品开发经验。于2015年3月20日公司职工代表大会当选为公司职工监事。"
    ProfileStr = u"中国东方航空股份有限公司|||邵瑞庆|||邵瑞庆先生,男,1957年9月出生,汉族,浙江湖州人,博士研究生学历,现任上海立信会计学院教授、博士生导师,兼任中国交通会计学会副会长、中国会计学会常务理事、中国审计学会理事、上海市会计学会副会长兼学术委员会主任、上海市审计学会常务理事等,被交通运输部聘为软科学决策咨询专家与财会专家咨询委员会委员,被教育部聘为会计学专业教学指导委员会委员。上海市第十三届人大代表。"
    ProfileStr = u"新疆九圣禾种业股份有限公司|||王大和|||王大和先生：公司董事，中国国籍，无境外居留权，1951年11月出生，硕士研究生学历，上海交大EMBA，高级农业经济师。1976年8月至1985年3月任酒泉地区行署办公室、秘书处干部；1985年4月至1988年8月历任酒泉地委经济部副科长、科长；1988年9月至1994年3月任酒泉地委研究室副主任；1994年4月至1997年6月任中共酒泉地委副秘书长；1997年7月至2000年8月任甘肃省酒泉地区农业委员会主任兼酒泉地区农业建设指挥部指挥；2000年9月至2004年2月任酒泉地区现代农业（控股集团）有限责任公司党委书记、董事长兼总经理；2000年8月至2014年6月任甘肃省敦煌种业股份有限公司董事长；2014年10月至今任九圣禾种业董事。"
    ProfileStr = u"保定天威保变电气股份有限公司|||徐国祥|||徐国祥先生:中国国籍,无境外永久居留权,1960年3月出生,研究生学历,获经济学博士学位,国家二级教授,博士生导师。历任上海海运学院管理系讲师;上海财经大学统计学系讲师、副教授、教授、系主任、会计与财务研究院教授等。现任上海财经大学讲习教授、应用统计研究中心主任、统计与管理学院教授;兼任教育部高等学校统计学类专业教学指导委员会副主任委员、国家社科基金学科规划评审组专家、中国统计学会常务理事、中国统计教育学会常务理事、上海统计学会副会长、上海证券交易所指数专家委员会委员、中证指数有限公司专家委员会委员、上海社会调查研究中心上海财经大学分中心主任、上海市统计高级职称评审委员会副主任委员等职务。2011年9月至2011年10月任公司独立董事,2011年11月至今任公司监事会主席。2012年10月至今任中华企业股份有限公司独立董事。"
    ProfileStr = u"新疆天富能源股份有限公司|||吴革|||吴革先生，法学硕士，律师。曾任河南省息县司法局律师，河南省第三律师事务所律师，河南省先河律师事务所主任，北京市观韬律师事务所律师，现任北京市中闻律师事务所主任，新疆天富热电股份有限公司独立董事，安徽山鹰纸业股份有限公司独立董事。"
    ProfileStr = u"北京大津硅藻新材料股份有限公司|||郑建军|||郑建军先生，出生于1983年8月，中国籍，本科学历，无境外永久居留权。2006年进入公司，历任公司车间主任。副厂长兼实验室主任。现任公司生产部经理兼实验室主任。"
    ProfileStr = u"洁华控股股份有限公司|||夏国平|||夏国平：男，中国国籍，无境外永久居留权，1965年11月出生，大专学历，工程师。1984年8月到1997年8月历任海宁县除尘设备厂、海宁市除尘设备厂、海宁市除尘设备总厂、海宁市除尘设备实业总公司技术设计组组长、电研室主任、技术科科长等职；1997年8月到2004年12月，历任公司技术科科长、营销部副部长、营销部部长、副总工程师、董事；2004年12月到2008年2月历任公司董事、海宁洁华总工程师、海宁洁华副总经理。2008年2月至今任公司董事、副总工程师。"
    ProfileStr = u"粤丰环保电力有限公司|||谢宇斌|||谢宇斌先生,於二零零五年四月加入本集团。彼现任科伟及科维常务副总经理,负责该等公司的日常管理。谢先生於一九九九年十一月获得中华人民共和国人事部(现称中华人民共和国人力资源和社会保障部)认可的金融经济专业初级资格。谢先生於一九九三年三月至二零零五年四月任职於中国工商银行股份有限公司东莞分行。谢先生於二零零三年七月毕业於广东工业大学,取得会计专业大专学历。彼透过函授於二零零九年一月毕业於中央广播电视大学(现称国家开放大学),获得行政管理专业学士毕业证书。"
    ProfileStr = u"北京建设数字科技股份有限公司|||朱磊|||朱磊先生，中国国籍，毕业于武汉大学，本科学历，工程师。曾任职广西测绘局，自2006年起在北京建设数字科技股份有限公司任职，现担任遥感事业部经理，北京建设数字科技股份有限公司监事长。"
    ProfileStr = u"长春经开(集团)股份有限公司|||陈平|||陈平，男，汉族，中共党员，大学学历，高级经济师，曾任长春经济技术开发区热力有限责任公司总经理、长春经济技术开发区城乡党委书记、社会事业发展局局长、长春市供热发展有限公司总经理、长春经济技术开发区管理委员会招商引资办公室主任(兼商务局局长、经济合作局局长)。2002年4月—2004年2月曾任本公司第四届董事会董事，现任本公司董事长、党委书记。"
    ProfileStr = u"湖北优尼科光电技术股份有限公司|||龙文|||龙文，男，生于1972年，中国籍，无境外永久居留权，毕业于杭州电子科技大学电子工程专业，本科学历。1994年9月至1996年7月任职电子工业部南京第55研究所工程师；1996年8月至2004年9月历任香港精电国际有限公司深圳分公司工程主管，高级工程师，副经理；2004年9月至2006年10月，历任清华大学深圳迪斯泰电子有限公司高级经理、生产制造总监，ISO9000（2000版）管理者代表；2006年10月至2010年12月任职深圳市卓尔视光电技术有限公司总经理；2010年12月至2012年4月任职湖北优尼科光电技术有限公司总经理；2012年6月至今就职于东莞市元虹光电科技有限公司执行（常务）董事、总经理。现任湖北优尼科光电技术股份有限公司董事。"

    ProfileStr = u"华扬联众数字技术股份有限公司|||包锦堂|||包锦堂，中国国籍，无境外永久居留权，1937年9月出生，身份证号：31010419370927****；1999年2月退休，持有公司0.47%的股权。包锦堂目前主要从事股权投资，除公司外，还投资了北京光线传媒股份有限公司、上海华石投资有限公司、海南华兴基石创业投资中心（有限合伙）等企业。"
    ProfileStr = u"新疆宝地矿业股份有限公司|||彭方洪|||彭方洪，男，1966年生，现任本公司董事，中国国籍，无境外永久居留权，成都地质学院矿产资源评价专业大专学历。彭方洪先生于1983年6月至2012年2月历任新疆地矿局第六地质大队地质员、组长、副分队长兼技术负责、分队长兼技术负责、经营开发部（科）主任、副总工程师、总支书记、副总经理、董事长、副处级调研员、党委委员、副大队长等职务，于2012年3月至2014年5月任新疆地矿局第一地质大队党委委员、副大队长职务，于2014年6月至今任新疆地矿局第七地质大队大队长、党委副书记。"
    ProfileStr = u"烟台龙源电力技术股份有限公司|||张宝全|||张宝全先生，1960年出生，中国国籍，硕士研究生学历，教授级高级工程师。历任电力科学研究院高压研究所工程师，中国电力企业联合会科技工作部工程师，中能电力科技开发公司工程项目部副经理，中能电力技术贸易公司经理、总经理，中能电力电气公司总经理，中能电力科技开发公司总经理助理、总经理，中能电力科技开发有限公司总经理、党委书记，龙源电力集团公司总经理助理，中共龙源电力集团公司在京直属委员会委员，北京中能联创风电技术有限公司总经理，龙源电力集团公司总经济师，龙源电力集团股份有限公司总经济师，龙源电力集团股份有限公司可再生能源研究发展中心常务副主任、主任。现任龙源电力集团股份有限公司党组成员、副总经理，中共龙源电力集团股份有限公司在京直属委员会委员，本公司董事。"
    ProfileStr = u"粤丰环保电力有限公司|||袁国桢|||袁国桢先生,於二零一四年九月二十四日获委任为执行董事。袁先生为本集团的行政总裁。彼负责执行本集团的整体策略及管理本集团的日常营运。袁先生自二零零三年六月起任科伟的董事,并自二零一一年十月起任科维的董事兼总经理。彼亦於湛江粤丰及粤丰谘询各自成立以来担任其法定代表人兼董事。彼於一九九五年九月至二零零四年七月任东莞市三阳实业发展有限公司(前称东莞市三阳实业发展公司)执行副总经理,主要负责协助总经理营运及管理公司。袁先生於二零零四年七月至二零零八年九月任东莞东城东兴热电有限公司(现称东莞中电新能源热电有限公司)的总经理。彼於二零零七年十一月至二零零八年十二月担任云南双星绿色能源有限公司(现称昆明中电环保电力有限公司)的总经理。东莞中电新能源热电有限公司(中国电力新能源的附属公司)的主要业务包括天然气发电。云南双星绿色能源有限公司亦为中国电力新能源的附属公司,其主要业务包括发电及售电。袁先生於二零零九年六月取得华南理工大学高级管理人员工商管理硕士学位。"
    ProfileStr = u"汉唐国际控股有限公司|||陈旭明|||陈旭明毕业於中国统计干部学院。彼於一九八四年加入广州轮胎厂,并分配至人事部,致力於建立科学人力资源分配及薪金发放系统。彼自一九九八年以来担任人事部主管一职,最近於二零零四年晋升为副总经理,负责采购与物流部及人事部。彼於一九九四年加入合资企业。"
    ProfileStr = u"中国华融资产管理股份有限公司|||王克悦|||王克悦先生,2009年3月起担任本公司副总裁,2012年9月27日起担任本公司执行董事、副总裁,1994年12月获中国工商银行评为高级经济师。王先生於1994年12月毕业於中央党校函授学院经济专业本科,1997年6月於首都经济贸易大学经济法专业修完研究生课程,1999年2月於西南财经大学金融学专业修完研究生课程。"
    ProfileStr = u"南戈壁资源有限公司|||付凯|||付凯先生,注册税务师、会计师,毕业於湖北大学经济学院会计系。付先生现时为本公司总会计师,主要负责本公司会计核算与财务管理。彼亦为本公司全资附属公司同方照明产业集团有限公司总会计师兼财务中心总经理。自二零零四年至今,历任同方吉兆科技有限公司财务部成本经理、财务经理;同方股份数字电视产业本部财务部财务经理;同方股份财务部总经理助理、副总经理。"

    ProfileStr = u"北京鼎汉技术股份有限公司|||曹五顺|||曹五顺,男,1946年10月出生,中国国籍,无永久境外居留权。1970年西安交通大学电机系毕业,1974年至今在电气学院电器教研室任教,历任电器实验室主任,院党委副书记、书记。兼任陕西省电工技术学会理事、副秘书长,陕西省建筑电气学术委员会委员。现任公司第三届董事会独立董事。"


    ProfileStr = u"五矿发展股份有限公司|||刘青春|||刘青春先生,1966年12月出生,管理学博士,国际商务师。毕业于上海对外贸易学院国际经济法专业,1999年7月、2005年7月获得加拿大圣玛丽大学工商管理专业研究生学历、工商管理硕士学位和北京理工大学研究生学历、管理学博士学位。历任本公司监事、五矿贸易有限责任公司副总经理,五矿总公司焦炭部总经理,五矿总公司原材料板块副总经理,香港企荣贸易有限公司董事、总经理,中国五矿香港控股有限公司董事、副总经理兼香港企荣贸易有限公司董事、总经理等职务。"
    ProfileStr = u"同佳国际健康产业集团有限公司|||郑孝仁|||郑孝仁先生,一九八三年於上海交通大学取得工商管理硕士学位,具银行业务之经验。郑先生於一九八四年十月至一九八六年三月期间出任云南地质矿业局计划财务处之副处长,於一九八六年四月至一九八八年四月期间出任昆明市经济委员会副主任,并於一九八八年五月至一九九六年期间出任交通银行昆明分行行长。"
    ProfileStr = u"深圳市凯莱特科技股份有限公司|||刘剑|||刘剑，男，1977年12月出生，中国国籍，无境外永久居留权，硕士学历。1995年9月至1999年7月就读于湖南大学机电工程专业；1999年7月至2002年9月就职于中国航空工业供销江西分公司，担任硬件工程师；2002年9月至2004年12月就读湖南大学机电工程专业；2005年1月至2011年9月就职于深圳华强三洋技术设计有限公司，担任项目经理；2011年9月至今就职于公司，担任开发部经理；现任公司监事会主席，任期三年。"
    ProfileStr = u"民众金服控股有限公司|||卢更新|||卢先生,持有美利坚合众国(「美国」)印第安纳大学工商管理硕士学位及美国伊利诺大学机电工程学士学位。於香港及加拿大的金融、投资及银行业拥有超过28年经验。卢先生一间香港上市公司威利国际控股有限公司之执行董事,直至2008年4月彼请辞为止。除此以外,卢先生於过往三年并无出任任何其他上市公司董事之职位。"
    ProfileStr = u"江苏省交通规划设计院股份有限公司|||明图章|||明图章,男,1963年生,中国国籍,无永久境外居留权,教授级高级工程师,江苏省有突出贡献中青年专家,交通部“新世纪十百千人才工程”第一层次人选。江苏省优秀工程勘察设计师。1983年7月东南大学道路工程专业本科毕业,1989年5月东南大学道路工程专业硕士研究生毕业。1992年12月到交通院工作,历任道路设计室副主任、主任、副总工程师、副院长、院长等职务。2005年8月起任交通院有限董事长、总经理。2008年8月起任交通院有限董事长。2011年1月起任公司董事长。"
    ProfileStr = u"宏峰太平洋集团有限公司|||李小虎|||李小虎,本公司总裁助理、生产部总经理兼渭南分公司总经理。李先生於一九八七年毕业於陕西机械学院,主修工业电气自动化。李先生於二零零零年三月加入本公司。此前,李先生於一九八一年十月至二零零零年二月期间曾担任西安液压件厂液压阀分厂厂长、生产科副科长、总调度、经营部副经理及厂办主任。"
    ProfileStr = u"宝峰时尚国际控股有限公司|||梁子冲|||梁子冲先生,分别於一九九一年及一九九六年取得香港理工大学商业研究文学士学位及新南威尔斯大学工商管理硕士学位。彼为合资格认许市务师,於工商管理及市场营销拥有逾二十年丰富经验。自二零一一年十一月起,梁先生为北儒精密股份有限公司之法定代表,该公司之股份於中华民国证券柜台买卖中心买卖。"
    ProfileStr = u"民众金服控股有限公司|||陈汉云|||陈汉云先生,为本公司财务总监兼公司秘书,於二零一四年四月加入本集团。陈先生於一九八六年毕业於澳洲麦格理大学,获得经济学学士学位,并於二零零五年毕业於香港理工大学,获得会计学硕士学位。陈先生现为香港会计师公会及澳洲特许会计师公会资深会员。陈先生於会计及金融领域拥有逾27年丰富经验,曾於一家国际会计师事务所及多家上市公司任职。一九九五年至一九九八年,彼担任联交所主板上市公司大快活集团有限公司(股份代号:00052)财务总监。二零零零年至二零零五年,彼担任德士活有限公司企业财务主管。二零零六年至二零零八年,彼担任德士活集团的业务主管。二零零八年九月至二零零九年四月,陈先生担任联交所主板上市公司民丰控股有限公司(股份代号:00279,现称为民丰企业控股有限公司)公司秘书、合资格会计师兼授权代表。"
    ProfileStr = u"江苏雅百特科技股份有限公司|||伍小杰|||伍小杰，男，1966年生，中国国籍，无境外永久居留权。先后获得中国矿业大学工业自动化专业学士学位、电力电子与电力传动专业硕士学位和博士学位，长期从事电机控制与保护、电力电子与电力传动等方面的研究开发和教学工作。现任中国矿业大学教授，博士生导师；中国矿业大学信息与电气工程学院副院长。2013年5月参加了深交所组织的独立董事资格培训并取得结业证书。与公司控股股东及其他关联方无任何关联，未受到过证监会和深交所的任何处罚。。"
    ProfileStr = u"苏州安洁科技股份有限公司|||李国昊|||李国昊先生:男,1975年出生,中国国籍,无境外永久居留权,博士学历。2006年4月起历任江苏大学工商管理学院工商管理系副主任、副教授、硕士生导师、江苏大学管理学院副院长,现任苏州安洁科技股份有限公司独立董事。"
    ProfileStr = u"深圳市家鸿口腔医疗股份有限公司|||王志新|||王志新：男，1965年12月出生，毕业于苏州大学，硕士学历，会计专业。1991年9月至1995年7月，历任苏州大学会计学讲师、硕士生导师；1995年10月至2001年5月，历任苏州新加坡工业园财税局处长；2001年6月至2005年7月，历任东瑞制药（控股）有限公司CFO；2005年9月至2008年11月，历任艾格服饰有限公司CFO；2008年11月至2014年3月，历任朗力福集团控股有限公司CFO；2008年11月至今，任职德摩资本有限公司，现任董事总经理、合伙人；2014年5月至今，任职安信德摩牙科基金管理有限公司，现任总经理；现任公司董事。"
    ProfileStr = u"民众金服控股有限公司|||孙益麟|||孙益麟先生，于二零一一年四月加入本集团。彼亦获委任为马斯葛集团之公司秘书。彼为香港会计师公会资深会员及澳洲会计师公会会员，并持有昆士兰科技大学会计学学士学位及香港理工大学企业金融学硕士学位。孙先生于财务及会计方面拥有逾15年经验。于加入马斯葛集团前，彼曾任职于数间香港上市公司，负责会计及财务工作。于二零一零年九月二日至二零一一年三月十四日期间，彼为民丰企业控股有限公司（前称「民丰控股有限公司」）执行董事，该公司为一间于香港联合交易所有限公司主板上市之公司。"
    ProfileStr = u"成都博世德能源科技股份有限公司|||韩燕|||韩燕，女，1979年10月出生，中国国籍，无境外永久居留权，研究生学历。1999年9月至2003年7月在石家庄铁道大学学习，会计学专业；2004年9月至2007年9月在西南大学攻读研究生，教育管理学专业。2003年8月至2008年4月就职于成都工业学院，任外事秘书；2008年5月至2009年2月就职于宏华集团，任财务中心主管；2009年2月至今就职于四川沃力商贸有限公司，任经理。"
    ProfileStr = u"天津斯巴克瑞汽车电子股份有限公司|||王淑华|||王淑华女士，1962年出生，中国籍，无境外永久居留权，本科学历。1982年7月至1985年9月任实验工厂（光电通信公司前身）宣传部干事。1985年10月至1988年9月在大连大学会计专业学习，获大专学历。1988年10月至1994年3月任天津光电通信公司财务部科员。1994年4月至1998年4月任天津光电通信公司财务科(九分厂）主管会计。1998年5月至2005年3月任天津光电通信技术有限公司主管会计。2005年3月至2007年11月任斯巴克瑞汽车电子有限公司财务部部长。2007年11月至2012年6月任天津光电集团有限公司财务部副部长。2011年3月至今任天津光电集团有限公司财务部党支部书记。2012年7月至今任天津光电集团有限公⑷财务部部长。2015年5月28日被公司股东大会选举为监事会成员，任期三年。"
    ProfileStr = u"山东豪迈机械科技股份有限公司|||冯立强|||冯立强先生:大学专科学历,曾获高密市经贸委、财政局、机械工业局、团市委的“先进工作者”、“先进个人”、“青年岗位能手”称号。2001年加入本公司,曾任公司财务科长,现任公司融资主管。"
    ProfileStr = u"广州集泰化工股份有限公司|||李军|||5、李军先生，中国国籍，出生于1974年11月，研究生学历。1993年9月至1995年7月就读于河南省周口师范高等专科学校（现周口师范学院）数学系；1995年7月至1997年7月就职于东莞糖酒集团美佳连锁超市有限公司，历任班长、店长；1997年8月至1998年6月就职于屈臣氏集团（深圳）食品饮料有限公司，担任销售主任；1998年7月至2000年1月就职于新疆乌鲁木齐市广货专卖店，担任店长；2000年2月至2001年4月就职于深圳东鼎数字电器有限公司，担任大区经理；2001年5月至2003年2月就职于深圳市万佳百货股份有限公司，历任主管、部门副经理；2003年3月至2003年10月就职于广东本草药业连锁有限公司，担任购销部经理；2003年10月至今，参与创建广州巴菲特投资咨询有限公司，担任总经理。现任广东泰银投资有限公司总经理，广东嘉信瑞成创业投资中心（有限合伙）执行合伙人，佛山泰银富时创业投资中心（有限合伙）执行合伙人。现任公司董事。"
    ProfileStr = u"恒生电子股份有限公司|||黄辰立|||黄辰立,男,中国国籍,无境外永久居留权,1980年6月出生。2002年7月毕业于上海交通大学;2002年7月至2006年6月任中国国际金融有限公司员工;2006年6月至2007年7月就读于英士国际商学院MBA专业;2007年7月至2008年2月就职于巴克莱亚洲有限公司;2008年2月至2010年3月就职于J.PMorgan;2010年3月至2013年5月就职于中国国际金融有限公司;2013年5月至今就职于浙江蚂蚁小微金融服务集团。2014年4月至2015年8月作为云鑫投资代表担任云觅有限监事,2015年8月至今作为云鑫投资代表担任虎嗅科技监事。"
    ProfileStr = u"浙江钱江摩托技术开发有限公司|||周西平|||周西平：男，1965年2月24日出生，本科学历，籍贯温岭。1984年12月至1991年11月在温岭机床厂工作；1991年12月随温岭机床厂并入浙江摩托车厂；1995年3月至1996年9月任浙江钱江摩托集团有限公司齿轮分厂副厂长；1996年10月至2001年12月任浙江益鹏发动机配件有限公司总装厂厂长；2002年1月至2005年10月任浙江益鹏发动机配件有限公司副总经理；2005年4月至2005年10月兼任本公司热处理分公司及有色金属铸造分公司负责人；2005年9月至2005年10月兼任本公司齿轮分公司负责人；2005年10月至今任本公司董事常务副总经理。兼职情况：浙江益中摩托车电器有限公司董事长、浙江钱江摩托进出口有限公司董事长，浙江美可达摩托车有限公司董事、浙江益荣汽油机零部件有限公司董事、浙江益鹏发动机配件有限公司董事、浙江瓯联创业投资有限公司董事、浙江钱江摩托技术开发有限公司董事。  "
    ProfileStr = u"四川天邑康和通信股份有限公司|||王国伟|||王国伟，中国国籍，身份证号码：510129196309******，无境外永久居留权，男，1963年9月出生，大专学历、高级会计师。2001年至2003年8月，任天邑信科财务负责人；2003年8月至2011年，任天邑信科财务负责人、副总经理；2012年至今，任天邑有限及公司财务负责人、副总经理。2012年6月至今，任公司董事。"
    ProfileStr = u"四川天邑康和通信股份有限公司|||李俊画|||李俊画，中国国籍，身份证号码：510129197207******，无境外永久居留权，女，1972年7月出生，本科、工程师。2000年11月至2012年10月任天邑集团董事长、法定代表人；2012年10月至今任天邑集团董事；2001年6月至今，任天邑信科董事；2012年6月至今，任公司董事、总经理，同时兼任天邑房地产监事等职务。"
    ProfileStr = u"上海国际港务(集团)股份有限公司|||杨智勇|||杨智勇,男,1972年10月出生,汉族,1994年8月参加工作,1998年4月加入中国共产党,大学学历,硕士学位,高级工程师,一级项目经理。历任上海港务工程公司经理助理兼生产科科长;上海港务工程公司经理助理兼洋山深水港区一期工程项目经理总部常务副总经理;上海港务工程公司党委委员、副经理;上海港务工程公司党委委员、副经理(主持工作);上海港务工程公司党委委员、经理;上海港务工程公司党委委员、经理兼上港集团宝山地块开发项目筹备组组长;上海港务工程公司党委委员、总经理兼上港集团瑞泰发展有限责任公司党支部书记、总经理;中建港务建设有限公司党委委员、总经理兼上港集团瑞泰发展有限责任公司党支部书记、总经理等职。"
    ProfileStr = u"上海国际港务(集团)股份有限公司|||范洁人|||范洁人，男，1957年10月出生，汉族，1978年5月参加工作，1986年6月加入中国共产党，研究生学历，高级政工师，历任上海港张华浜港务公司党委委员、工会主席；上港集团张华浜分公司党委委员、工会主席；上港集团张华浜分公司纪委书记、工会主席；上海冠东国际集装箱码头有限公司党委副书记、纪委书记、工会主席。现任上海国际港务（集团）股份有限公司监事、纪委副书记、监察室主任。"
    ProfileStr = u"中国石化齐鲁股份有限公司|||杜明迤|||杜明迤：男，35岁，大学学历，政工师，1999年8月起任塑料厂工会主席，2000年10月30日当选本公司职工监事。"
    ProfileStr = u"盈方微电子股份有限公司|||付德银|||2004-6-21：第六届连任，付德银男，38岁，党员，硕士研究生，高级经济师。曾任中国建设银行荆州市分行信贷管理科副科长、沙市支行、北湖支行副行长，现任天发石油股份有限公司财务总监。"
    ProfileStr = u"广州启光智造技术服务股份有限公司|||陈志坚|||陈志坚，董事，1965年6月出生，中国国籍，无境外永久居留权，无外国护照，毕业于番禺南村中学，中学学历。1983年至2010年11月，就职于广东省广州番禺电缆厂有限公司，历任生产工、车间主管等职务；2010年11月就职公司，现为公司生产部部长。"
    ProfileStr = u"中国再生能源投资有限公司|||阮立基|||阮立基先生,捷腾电子(深圳)有限公司董事兼董事总经理。於一九八六年加入JIC集团前,彼於一九八四年至一九八六年期间於SlexsWatchCo.,Ltd.担任生产经理。於一九九四年,彼获JIC集团保送往日本学习液晶注入技术。其後,彼成功在捷腾电子(深圳)有限公司设立LCD前工序、中工序及後工序生产线。阮先生於二零零零年获擢升为捷腾电子(深圳)有限公司副董事总经理,於二零零五年成为董事总经理。彼於LCD制造行业拥有约二十年经验。"
    ProfileStr = u"浙江钱江摩托技术开发有限公司|||周西平|||周西平：男，1965年2月24日出生，本科学历，籍贯温岭。1984年12月至1991年11月在温岭机床厂工作；1991年12月随温岭机床厂并入浙江摩托车厂；1995年3月至1996年9月任浙江钱江摩托集团有限公司齿轮分厂副厂长；1996年10月至2001年12月任浙江益鹏发动机配件有限公司总装厂厂长；2002年1月至2005年10月任浙江益鹏发动机配件有限公司副总经理；2005年4月至2005年10月兼任本公司热处理分公司及有色金属铸造分公司负责人；2005年9月至2005年10月兼任本公司齿轮分公司负责人；2005年10月至今任本公司董事常务副总经理。兼职情况：浙江益中摩托车电器有限公司董事长、浙江钱江摩托进出口有限公司董事长，浙江美可达摩托车有限公司董事、浙江益荣汽油机零部件有限公司董事、浙江益鹏发动机配件有限公司董事、浙江瓯联创业投资有限公司董事、浙江钱江摩托技术开发有限公司董事。  "



    Divide_Pre_Cur_Working(ProfileStr)


def main():
    #Test_Check_GenderCall()
    #Test_Check_BirthInfo()
    # Test_PostPro_Position_Name()
    # Test_Check_Workig_Item()
    #Test_Show_OrgName_Position_Name()
    # Test_PostPro_Position_Name()
    # Test_Check_BasicInfo()
    #

    # Test_DetectTimeForWorkingSent()
    # Test_Detect_MarkSplit_Mode()
    # Test_Check_IF_WorkingSent()
    # Test_Check_WorkingSent()
    # Test_PostPro_Org_Name()
    #
    # Test_CheckTimePos()
    # test_jieba_wordseg()
    # Test_Sents_Segmentation()

    # test_get_school_snippet()
    # Test_Jieba()
    Test_Get_Seqs_and_Times()
    #Test_Divide_TimeSeq_Working()

    #Test_Show_OrgName_Position_Name()
    #Test_Check_Workig_Item()
    # Test_Check_WorkingSent()
    Test_Divide_Pre_Cur_Working()
    pass


if __name__ == '__main__':
    main()
