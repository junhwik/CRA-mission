members_id = {}
id_cnt = 0

# dat[사용자ID][요일]
attendance_cnt_by_wday = [[0] * 100 for _ in range(100)]
attendance_points = [0] * 100
grade = [0] * 100
names = [''] * 100
wednesday_attendance_cnts = [0] * 100
weekend_attendance_cnts = [0] * 100


def input2(name, wday):
    global id_cnt

    if name not in members_id:
        id_cnt += 1
        members_id[name] = id_cnt
        names[id_cnt] = name

    add_points(name, wday)


def add_points(name, wday):
    id2 = members_id[name]

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

    attendance_cnt_by_wday[id2][index] += 1
    attendance_points[id2] += point

    if wday in ["wednesday"]:
        wednesday_attendance_cnts[id2] += 1

    if wday in ["saturday", "sunday"]:
        weekend_attendance_cnts[id2] += 1


def input_file(list_file="attendance_weekday_500.txt"):
    try:
        with open(list_file, encoding='utf-8') as f:
            attendance_list = f.readlines()
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")
    return attendance_list


def analyze_attendance(attendance_list: list[str]):
    for line in attendance_list:
        parts = line.strip().split()
        if len(parts) == 2:
            input2(parts[0], parts[1])

    for i in range(1, id_cnt + 1):
        if attendance_cnt_by_wday[i][2] > 9:
            attendance_points[i] += 10
        if attendance_cnt_by_wday[i][5] + attendance_cnt_by_wday[i][6] > 9:
            attendance_points[i] += 10

        if attendance_points[i] >= 50:
            grade[i] = 1
        elif attendance_points[i] >= 30:
            grade[i] = 2
        else:
            grade[i] = 0

        print(f"NAME : {names[i]}, POINT : {attendance_points[i]}, GRADE : ", end="")
        if grade[i] == 1:
            print("GOLD")
        elif grade[i] == 2:
            print("SILVER")
        else:
            print("NORMAL")

    print("\nRemoved player")
    print("==============")
    for i in range(1, id_cnt + 1):
        if grade[i] not in (1, 2) and wednesday_attendance_cnts[i] == 0 and weekend_attendance_cnts[i] == 0:
            print(names[i])


if __name__ == "__main__":
    attendance_list = input_file()
    analyze_attendance(attendance_list)
