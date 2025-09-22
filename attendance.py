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

        self.special_wday = ["wednesday"]
        self.weekend_wday = ["saturday", "sunday"]

    def _regist_member(self, name):
        if name not in self.members_id:
            self.id_cnt += 1
            self.members_id[name] = self.id_cnt
            self.names[self.id_cnt] = name

    def _add_points(self, name, wday):
        id = self.members_id[name]

        index, point = self._get_point(wday)

        self.attendance_cnt_by_wday[id][index] += 1
        self.attendance_points[id] += point

        if wday in ["wednesday"]:
            self.wednesday_attendance_cnts[id] += 1

        if wday in ["saturday", "sunday"]:
            self.weekend_attendance_cnts[id] += 1

    def _get_point(self, wday) -> tuple[int, int]:
        if wday == "monday":
            index = 0
            point = 1
        elif wday == "tuesday":
            index = 1
            point = 1
        elif wday == "wednesday":
            index = 2
            point = 3
        elif wday == "thursday":
            index = 3
            point = 1
        elif wday == "friday":
            index = 4
            point = 1
        elif wday == "saturday":
            index = 5
            point = 2
        elif wday == "sunday":
            index = 6
            point = 2
        return index, point

    def _input_file(self, list_file="attendance_weekday_500.txt"):
        try:
            with open(list_file, encoding='utf-8') as f:
                attendance_list = f.readlines()
        except FileNotFoundError:
            print("파일을 찾을 수 없습니다.")
        return attendance_list

    def _print_low_attendance(self):
        for i in range(1, self.id_cnt + 1):
            if self.grade[i] in (1, 2):
                continue
            if self.wednesday_attendance_cnts[i] != 0:
                continue
            if self.weekend_attendance_cnts[i] != 0:
                continue
            print(self.names[i])

    def _print_result(self):
        for i in range(1, self.id_cnt + 1):
            print(f"NAME : {self.names[i]}, POINT : {self.attendance_points[i]}, GRADE : ", end="")
            if self.grade[i] == 1:
                print("GOLD")
            elif self.grade[i] == 2:
                print("SILVER")
            else:
                print("NORMAL")
        print("\nRemoved player")
        print("==============")

    def _calculate_grade(self):
        for i in range(1, self.id_cnt + 1):
            if self.attendance_cnt_by_wday[i][2] > 9:
                self.attendance_points[i] += 10
            if self.attendance_cnt_by_wday[i][5] + self.attendance_cnt_by_wday[i][6] > 9:
                self.attendance_points[i] += 10

            if self.attendance_points[i] >= 50:
                self.grade[i] = 1
            elif self.attendance_points[i] >= 30:
                self.grade[i] = 2
            else:
                self.grade[i] = 0

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
