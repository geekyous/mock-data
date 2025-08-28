import random
import uuid
from datetime import datetime

from faker import Faker
from pydantic import BaseModel

import sm2
import sql


class ThreeKind(BaseModel):
    userId: str


class Mock:
    def __init__(self):
        self.conn = sql.create_connection()
        self.cursor = self.conn.cursor()
        self.fake = Faker()
        self.random = random
        self.datetime = datetime
        self.SINGLE_PROJECT_CODE_LIST = ()
        self.WEEK_PLANS_RISK_PRECAUTION = {}
        self.WEEK_PLANS_TEAM = {}
        self.TEAM_ID_LIST = []
        self.result = {}

    def generate_data(self, plan_start_time, plan_end_time):

        # 1. 查询工程
        self.list_single_project_code()
        # 2. 生成周计划
        self.generate_jj_weeks_plan(plan_start_time, plan_end_time)
        # 3. 生成班组
        self.generate_jj_team()
        # 4. 生成班组人员
        self.generate_jj_team_people()
        # 5. 生成风险底数一本账
        self.generate_risk_precaution()

        self.conn.cursor().close()
        self.conn.close()
        self.result['generated_at'] = datetime.now().isoformat()

        return self.result

    def list_single_project_code(self):
        single_project_select_query = "SELECT  DISTINCT single_project_code FROM jj_single_info"
        self.cursor.execute(single_project_select_query)
        fetched_data = self.cursor.fetchall()
        self.SINGLE_PROJECT_CODE_LIST = [row[0] for row in fetched_data]
        print(f"查询到 {len(self.SINGLE_PROJECT_CODE_LIST)} 单项工程")
        self.result["single_project_num"] = len(self.SINGLE_PROJECT_CODE_LIST)

    def generate_jj_weeks_plan(self, plan_start_time, plan_end_time):
        """生成周计划"""
        insert_query = """
                       INSERT INTO jj_weeks_plan (id,
                                                  risk_precaution_id,
                                                  huv_flag,
                                                  team_id,
                                                  planned_start_date,
                                                  planned_end_date,
                                                  single_project_code,
                                                  create_time,
                                                  creater_id,
                                                  delete_flag)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) \
                       """
        data_to_insert = []
        current_time = datetime.now()
        risk_precaution_total = []
        for single_project_code in self.SINGLE_PROJECT_CODE_LIST:
            size = random.randint(1, 5)
            risk_precaution_ids = []
            team_ids = []
            for i in range(size):
                record_id = str(uuid.uuid4().hex)[:32]
                risk_precaution_id = str(uuid.uuid4().hex)[:32]
                # 周计划与风险一本账关联
                risk_precaution_ids.append(
                    {"risk_precaution_id": risk_precaution_id, "single_project_code": single_project_code})
                risk_precaution_total.append(risk_precaution_id)
                team_id = str(uuid.uuid4().hex)[:32]
                team_ids.append({"team_id": team_id, "single_project_code": single_project_code})
                # 周计划与班组关联
                planned_start_date = plan_start_time
                planned_end_date = plan_end_time
                single_project_code = single_project_code
                record = (record_id, risk_precaution_id, 0, team_id, planned_start_date, planned_end_date,
                          single_project_code, current_time, 'mock', 0)
                data_to_insert.append(record)
            self.WEEK_PLANS_RISK_PRECAUTION[single_project_code] = risk_precaution_ids
            self.WEEK_PLANS_TEAM[single_project_code] = team_ids

        cursor = self.conn.cursor()
        cursor.executemany(insert_query, data_to_insert)
        print(f"周计划：成功插入 {cursor.rowcount} 条班周计划数据！")
        self.result["weeks_plan_num"] = cursor.rowcount

    def generate_jj_team(self):
        """生成班组"""
        insert_query = """
                       INSERT INTO jj_team (id,
                                            huv_flag,
                                            working_team_name,
                                            single_project_code,
                                            team_status,
                                            create_time,
                                            creater_id,
                                            delete_flag)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s) \
                       """
        data_to_insert = []
        current_time = datetime.now()
        for team_item in self.WEEK_PLANS_TEAM.values():
            for item in team_item:
                team_id = item['team_id']
                working_team_name = self.fake.name()
                single_project_code = item['single_project_code']
                record = (team_id, '0', working_team_name, single_project_code, '01', current_time, 'mock', 0)
                data_to_insert.append(record)

        cursor = self.conn.cursor()
        cursor.executemany(insert_query, data_to_insert)
        print(f"班组：成功插入 {cursor.rowcount} 条班组数据！")
        self.result["team_num"] = cursor.rowcount

    def generate_jj_team_people(self):
        """生成班组人员"""
        POSITION_CODE_LIST = ['0900101', '0900102', '0900103']
        insert_query = """
                       INSERT INTO jj_team_people (id,
                                                   team_id,
                                                   position_code,
                                                   real_name,
                                                   id_card,
                                                   create_time,
                                                   creater_id,
                                                   delete_flag)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s) \
                       """
        data_to_insert = []
        current_time = datetime.now()

        for team_item in self.WEEK_PLANS_TEAM.values():
            for item in team_item:
                team_id = item['team_id']
                for position_code in POSITION_CODE_LIST:
                    record_id = str(uuid.uuid4().hex)[:32]
                    realname = self.fake.name()
                    id_card = self.fake.ssn()
                    record = (record_id, team_id, position_code, realname, id_card, current_time, 'mock', 0)
                    data_to_insert.append(record)

        cursor = self.conn.cursor()
        cursor.executemany(insert_query, data_to_insert)
        print(f"班组人员：成功插入 {cursor.rowcount} 条班组人员数据！")
        self.result["team_people_num"] = cursor.rowcount

    def generate_risk_precaution(self):
        """生成风险底数一本账"""
        work_procedure_list = [
            '流动式起重机立塔（塔高 60米以上）',
            '人力、车辆或畜力运输（含栈桥搭设、拆除施工）',
            '开掘敷设和焊接回填',
            '流动式起重机立塔（塔高 60米以上）',
            '人力、车辆或畜力运输（含栈桥搭设、拆除施工）',
            '杆塔螺栓复紧与消缺',
            '混凝土浇筑作业',
            '一般跨越架搭设和拆除（全高18m以下）',
            '一般土石方及掏挖基础机械开挖',
            '开掘敷设和焊接回填'
        ]

        working_content_list = [
            '工序：人力、车辆或畜力运输（含栈桥搭设、拆除施工）作业部位：#72、#68',
            '工序：开掘敷设和焊接回填作业部位：G70',
            '工序：流动式起重机立塔（塔高 60米以上）作业部位：G31、G20'
            '工序：人力、车辆或畜力运输（含栈桥搭设、拆除施工）作业部位：#72、#68',
            '工序：杆塔螺栓复紧与消缺作业部位：G5、G3、G11、G12、G21、G27、G33、G31、G35、G38、G39、G13、G24、G26、G10',
            '工序：混凝土浇筑作业作业部位：G68、G67、G64、G53、G54、G65、G66、G69',
            '工序：一般跨越架搭设和拆除（全高18m以下）作业部位：G48~G49~G50~G51~G52~G53~G54~G55~G56~G57~G58~G59~G60~G61~G62~G63~G64~G65~G66~G67~G68~G69~G70~G71~G72~G73~G74~G75~G76~G77~G78~G79~G80~G81~G82~G83~G84~G85~G86~G87~G88~G89~G90',
            '工序：一般土石方及掏挖基础机械开挖作业部位：A1-13、A2-13、A1-17、A2-17',
            '工序：开掘敷设和焊接回填作业部位：A2-17、A2-13、A2-15、A1-15'
        ]
        risk_level_list = [1, 2, 3, 4]

        insert_query = """
                       INSERT INTO jj_risk_precaution (id, \
                                                       work_procedure, \
                                                       assessment_risk_level, \
                                                       re_assessment_risk_level, \
                                                       work_content, \
                                                       single_project_code, \
                                                       create_time, \
                                                       creater_id, \
                                                       delete_flag) \
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) \
                       """
        data_to_insert = []
        current_time = datetime.now()
        for precaution_item in self.WEEK_PLANS_RISK_PRECAUTION.values():
            for item in precaution_item:
                work_procedure = random.choice(work_procedure_list)
                work_content = random.choice(working_content_list)
                risk_level = random.choice(risk_level_list)
                precaution_id = item['risk_precaution_id']
                single_project_code = item['single_project_code']
                record = (precaution_id, work_procedure, risk_level, risk_level, work_content, single_project_code,
                          current_time, 'mock', 0)
                data_to_insert.append(record)
        cursor = self.conn.cursor()
        cursor.executemany(insert_query, data_to_insert)
        print(f"风险一本账：成功插入 {cursor.rowcount} 条风险一本账数据！")
        print(f"风险一本账：成功插入 {cursor.rowcount} 条风险一本账数据！")
        self.result["risk_precaution_num"] = cursor.rowcount

    def three_kind(self, param: ThreeKind):
        """班组人员评分"""
        user_id = param.userId
        user_id_text = sm2.decrypt_from_java(user_id)
        user_id_list = user_id_text.split(',')
        data = []
        for user_id in user_id_list:
            info = {'score': random.randint(1, 50), 'isNew': random.choice([1, 0]),
                    'idCard': sm2.encrypt_for_java(user_id),
                    'evaluate': random.choice(['A', 'B', 'C'])}
            data.append(info)
        return data
