SILVER_GRADE_THRESHOLD = 30
GOLD_GRADE_THRESHOLD = 50
NORMAL_GRADE = 0
SILVER_GRADE = 2
GOLD_GRADE = 1
WEEKEND_BONUS_POINTS = 10
SPECIAL_BONUS_POINTS = 10
WEEKEND_BONUS_THRESHOLD = 10
SPECIAL_BONUS_THRESHOLD = 10
WEEKEND_POINTS = 2
SPECIAL_POINTS = 3
NORMAL_POINTS = 1
SPECIAL_WDAY = ["wednesday"]
WEEKEND_WDAY = ["saturday", "sunday"]
WDAY_IDX = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
}


class Member:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.attendance_cnt_by_wday = {
            "monday": 0,
            "tuesday": 0,
            "wednesday": 0,
            "thursday": 0,
            "friday": 0,
            "saturday": 0,
            "sunday": 0,
        }
        self.attendance_point = 0
        self.special_attendance_cnt = 0
        self.weekend_attendance_cnt = 0
        self.grade = 0


class AttendanceManager:
    def __init__(self):
        self.club_members = {}
        self.id_cnt = 0

    def _regist_member(self, name):
        if name not in self.club_members:
            self.id_cnt += 1
            self.club_members[name] = Member(self.id_cnt, name)

    def _add_points(self, name, wday):
        member = self.club_members.get(name, None)
        if not member:
            return

        point = self._get_point(wday)

        member.attendance_cnt_by_wday[wday] += 1
        member.attendance_point += point

        if wday in ["wednesday"]:
            member.special_attendance_cnt += 1

        if wday in ["saturday", "sunday"]:
            member.weekend_attendance_cnt += 1

    def _get_point(self, wday):
        if wday in SPECIAL_WDAY:
            point = SPECIAL_POINTS
        elif wday in WEEKEND_WDAY:
            point = WEEKEND_POINTS
        else:
            point = NORMAL_POINTS
        return point

    def _input_file(self, list_file="attendance_weekday_500.txt"):
        try:
            with open(list_file, encoding='utf-8') as f:
                attendance_list = f.readlines()
        except FileNotFoundError:
            print("파일을 찾을 수 없습니다.")
        return attendance_list

    def _print_low_attendance(self):
        print("\nRemoved player")
        print("==============")
        for _name, member in self.club_members.items():
            if member.grade in (GOLD_GRADE, SILVER_GRADE):
                continue
            if member.special_attendance_cnt != 0:
                continue
            if member.weekend_attendance_cnt != 0:
                continue
            print(member.name)

    def _print_result(self):
        for _name, member in self.club_members.items():
            print(f"NAME : {member.name}, POINT : {member.attendance_point}, GRADE : ", end="")
            if member.grade == GOLD_GRADE:
                print("GOLD")
            elif member.grade == SILVER_GRADE:
                print("SILVER")
            else:
                print("NORMAL")

    def _calculate_grade(self):
        for _name, member in self.club_members.items():
            if member.attendance_point >= GOLD_GRADE_THRESHOLD:
                member.grade = GOLD_GRADE
            elif member.attendance_point >= SILVER_GRADE_THRESHOLD:
                member.grade = SILVER_GRADE
            else:
                member.grade = NORMAL_GRADE

    def _calculate_bonus(self):
        for _name, member in self.club_members.items():
            special_attendance_cnt = sum([member.attendance_cnt_by_wday[d] for d in SPECIAL_WDAY])
            weekend_attendance_cnt = sum([member.attendance_cnt_by_wday[d] for d in WEEKEND_WDAY])
            if special_attendance_cnt >= SPECIAL_BONUS_THRESHOLD:
                member.attendance_point += SPECIAL_BONUS_POINTS
            if weekend_attendance_cnt >= WEEKEND_BONUS_THRESHOLD:
                member.attendance_point += WEEKEND_BONUS_POINTS

    def _is_valid(self, parts):
        if len(parts) != 2:
            return False
        if parts[1].lower() not in WDAY_IDX:
            return False

        return True

    def analyze(self, attendance_list=None):

        if attendance_list is None:
            attendance_list = self._input_file()

        for line in attendance_list:
            parts = line.strip().split()
            if not self._is_valid(parts):
                continue
            name = parts[0].capitalize()
            wday = parts[1].lower()
            self._regist_member(name)
            self._add_points(name, wday)

        self._calculate_bonus()
        self._calculate_grade()
        self._print_result()
        self._print_low_attendance()


if __name__ == "__main__":
    attendance_manager = AttendanceManager()
    attendance_manager.analyze()
