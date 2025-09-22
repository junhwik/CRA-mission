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


class AttendanceManager:
    def __init__(self):
        self.members_id = {}
        self.id_cnt = 0
        # dat[사용자ID][요일]
        self.attendance_cnt_by_wday = [[0] * 100 for _ in range(100)]
        self.attendance_points = [0] * 100
        self.grade = [0] * 100
        self.names = [''] * 100
        self.wednesday_attendance_cnts = [0] * 100
        self.weekend_attendance_cnts = [0] * 100

    def _regist_member(self, name):
        if name not in self.members_id:
            self.id_cnt += 1
            self.members_id[name] = self.id_cnt
            self.names[self.id_cnt] = name

    def _add_points(self, name, wday):
        id = self.members_id[name]

        point = self._get_point(wday)
        index = WDAY_IDX[wday]

        self.attendance_cnt_by_wday[id][index] += 1
        self.attendance_points[id] += point

        if wday in ["wednesday"]:
            self.wednesday_attendance_cnts[id] += 1

        if wday in ["saturday", "sunday"]:
            self.weekend_attendance_cnts[id] += 1

    def _get_point(self, wday) -> tuple[int, int]:
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
        for i in range(1, self.id_cnt + 1):
            if self.grade[i] in (GOLD_GRADE, SILVER_GRADE):
                continue
            if self.wednesday_attendance_cnts[i] != 0:
                continue
            if self.weekend_attendance_cnts[i] != 0:
                continue
            print(self.names[i])

    def _print_result(self):
        for i in range(1, self.id_cnt + 1):
            print(f"NAME : {self.names[i]}, POINT : {self.attendance_points[i]}, GRADE : ", end="")
            if self.grade[i] == GOLD_GRADE:
                print("GOLD")
            elif self.grade[i] == SILVER_GRADE:
                print("SILVER")
            else:
                print("NORMAL")
        print("\nRemoved player")
        print("==============")

    def _calculate_grade(self):
        for i in range(1, self.id_cnt + 1):
            special_attendance_cnt = sum([self.attendance_cnt_by_wday[i][WDAY_IDX[d]] for d in SPECIAL_WDAY])
            weekend_attendance_cnt = sum([self.attendance_cnt_by_wday[i][WDAY_IDX[d]] for d in WEEKEND_WDAY])
            if special_attendance_cnt >= SPECIAL_BONUS_THRESHOLD:
                self.attendance_points[i] += SPECIAL_BONUS_POINTS
            if weekend_attendance_cnt >= WEEKEND_BONUS_THRESHOLD:
                self.attendance_points[i] += WEEKEND_BONUS_POINTS

            if self.attendance_points[i] >= GOLD_GRADE_THRESHOLD:
                self.grade[i] = GOLD_GRADE
            elif self.attendance_points[i] >= SILVER_GRADE_THRESHOLD:
                self.grade[i] = SILVER_GRADE
            else:
                self.grade[i] = NORMAL_GRADE

    def analyze(self, attendance_list=None):

        if attendance_list is None:
            attendance_list = self._input_file()

        for line in attendance_list:
            parts = line.strip().split()
            if len(parts) != 2:
                continue
            name = parts[0]
            wday = parts[1]
            self._regist_member(name)
            self._add_points(name, wday)

        self._calculate_grade()
        self._print_result()
        self._print_low_attendance()


if __name__ == "__main__":
    attendance_manager = AttendanceManager()
    attendance_manager.analyze()
