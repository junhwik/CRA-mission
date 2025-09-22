from abc import abstractmethod, ABC

from matplotlib.dates import WEEKDAYS

NORMAL_GRADE_THRESHOLD = 0
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
WEEKDAY_POINTS = 1
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

    def add_attendance_point(self, point):
        self.attendance_point += point

    def add_attendance_cnt(self, wday):
        if wday in SPECIAL_WDAY:
            self.special_attendance_cnt += 1
        if wday in WEEKEND_WDAY:
            self.weekend_attendance_cnt += 1

        self.attendance_cnt_by_wday[wday] += 1


class PointPolicy(ABC):
    @abstractmethod
    def get_point(self):
        ...


class SpecialPointPolicy(PointPolicy):
    def get_point(self):
        return SPECIAL_POINTS


class WeekendPointPolicy(PointPolicy):
    def get_point(self):
        return WEEKEND_POINTS


class WeekdayPointPolicy(PointPolicy):
    def get_point(self):
        return WEEKDAY_POINTS


class PointPolicyFactory:
    def get_policy(self, wday):
        if wday in SPECIAL_WDAY:
            point_policy = SpecialPointPolicy
        elif wday in WEEKEND_WDAY:
            point_policy = WeekendPointPolicy
        else:
            point_policy = WeekdayPointPolicy

        return point_policy()


class Grade(ABC):
    @abstractmethod
    def __init__(self):
        ...

    def get_threshold(self):
        return self.grade_threshold


class GoldGrade(Grade):
    def __init__(self):
        self.grade_idx = GOLD_GRADE
        self.grade_threshold = GOLD_GRADE_THRESHOLD


class SilverGrade(Grade):
    def __init__(self):
        self.grade_idx = SILVER_GRADE
        self.grade_threshold = SILVER_GRADE_THRESHOLD


class NormalGrade(Grade):
    def __init__(self):
        self.grade_idx = NORMAL_GRADE
        self.grade_threshold = NORMAL_GRADE_THRESHOLD


class GradeFactory:
    def __init__(self):
        self.grade_dict = {
            GOLD_GRADE: GoldGrade(),
            SILVER_GRADE: SilverGrade(),
            NORMAL_GRADE: NormalGrade(),
        }

    def get_grade(self, member: Member):
        point = member.attendance_point
        sorted_grade = sorted(self.grade_dict.items(), key=lambda x: -x[1].get_threshold())
        for grade in sorted_grade:
            if point >= grade[1].get_threshold():
                return grade[0]


class AttendanceManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance:
            return cls._instance
        cls._instance = super(AttendanceManager, cls).__new__(cls, *args, **kwargs)
        cls.club_members = {}
        cls.id_cnt = 0
        return cls._instance

    def __init__(self):
        if not self._instance:
            self.club_members = {}
            self.id_cnt = 0

    def clear(cls):
        cls._instance = None

    def _regist_member(self, name):
        if name not in self.club_members:
            self.id_cnt += 1
            self.club_members[name] = Member(self.id_cnt, name)

    def _add_points(self, name, wday):
        member = self.club_members.get(name, None)

        point_policy = PointPolicyFactory().get_policy(wday)
        point = point_policy.get_point()

        member.add_attendance_cnt(wday)
        member.add_attendance_point(point)

    def _input_file(self, list_file="attendance_weekday_500.txt"):
        try:
            with open(list_file, encoding='utf-8') as f:
                attendance_list = f.readlines()
        except FileNotFoundError:
            print("파일을 찾을 수 없습니다.")
            attendance_list = None
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
            member.grade = GradeFactory().get_grade(member)

    def _calculate_bonus(self):
        for _name, member in self.club_members.items():
            if member.special_attendance_cnt >= SPECIAL_BONUS_THRESHOLD:
                member.attendance_point += SPECIAL_BONUS_POINTS
            if member.weekend_attendance_cnt >= WEEKEND_BONUS_THRESHOLD:
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
