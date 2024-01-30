import os
import platform
import curses
from curses import wrapper
import math
import numpy as np
import time
from datetime import datetime


# Utility functions
def clear_screen():
    os.system("cls") if platform.uname().system == "Windows" else os.system("clear")


def get_input_as_string(prompt) -> str:
    while True:
        data = input(prompt).strip()
        if not data:
            print("Cannot leave input blank, please try again!")
        else:
            return data


def get_input_as_int(prompt) -> int:
    while True:
        data = input(prompt).strip()
        try:
            return int(data)
        except ValueError:
            print("Invalid input, please try again!")


def get_input_as_float(prompt) -> float:
    while True:
        data = input(prompt).strip()
        try:
            return float(data)
        except ValueError:
            print("Invalid input, please try again!")


def get_input_as_float_floor(prompt) -> int:
    while True:
        data = input(prompt).strip()
        try:
            return int(math.floor(float(data) / 20.0 * 10.0))
        except ValueError:
            print("Invalid input, please try again!")


def output_padding(item) -> str:
    tab_width = 20
    return " " * (tab_width - len(str(item)))


def find_item_in_list(itemToFind, listToSearch, caseInsensitive) -> int:
    if caseInsensitive == 1:
        itemToFind = itemToFind.upper()
        for i in range(0, len(listToSearch)):
            if (
                listToSearch[i].get_name().upper() == itemToFind
                or listToSearch[i].get_id().upper() == itemToFind
            ):
                return i
    else:
        for i in range(0, len(listToSearch)):
            if (
                listToSearch[i].get_name() == itemToFind
                or listToSearch[i].get_id() == itemToFind
            ):
                return i
    return -1


def find_in_list(itemToFind, listToSearch) -> int:
    for i in range(0, len(listToSearch)):
        if itemToFind == listToSearch[i]:
            return i
    return -1


def get_input_as_date(prompt) -> datetime:
    while True:
        date_str = get_input_as_string(prompt)
        try:
            date = datetime.strptime(date_str, "%d-%m-%Y").date().strftime("%d-%m-%Y")
            return date
        except ValueError:
            print("Invalid date input. Please use the format DD-MM-YYYY and try again!")


def get_input_as_int_curses(window, prompt, silent, limit):
    if not silent:
        window.clear()
        window.addstr(prompt, curses.A_BOLD)
        window.refresh()
        
    num_str = ""
    while True:
        key = window.getch()  # Return the unicode, not the literal string representation of key
        if key >= ord("0") and key <= ord("9"):  # Ignore everything that not a number
            if len(num_str) >= limit:
                continue
            num_str += chr(key)
            window.addstr(chr(key), curses.A_BOLD)
        elif key == curses.KEY_BACKSPACE or key == 127:
            if len(num_str) > 0:
                num_str = num_str[:-1]
                window.addstr("\b \b")  # Delete the number replace by space then delete the space
        elif key in [10, "\n", "\r", curses.KEY_ENTER]:
            break
        window.refresh()

    return int(num_str) if num_str else 0


def choose_menu(choice):
    match str(choice):
        case "1":
            clear_screen()
            add_student(students, courses, marks)
        case "2":
            clear_screen()
            add_course(courses, marks)
        case "3":
            clear_screen()
            students.show_all_student()
            add_class_to_student(students, courses, marks)
        case "4":
            clear_screen()
            students.show_all_student()
            input("Press Enter to return.")
        case "5":
            clear_screen()
            print(f"Maximum number of courses: {courses.get_total()}\nCurrent number of courses: {courses.get_current()}\n")
            courses.show_courses()
            input("Press Enter to return.")
        case "6":
            clear_screen()
            show_all_student_course(students, courses)
            input("Press Enter to return.")
        case "7":
            clear_screen()
            courses.show_courses()
            add_mark_to_student(marks, courses)
        case "8":
            clear_screen()
            courses.show_courses()
            show_all_mark_course(marks, courses)
            input("Press Enter to return.")
        case "9":
            clear_screen()
            calculate_GPA(marks, students)
            input("Press Enter to return.")
        case "10":
            clear_screen()
            rank_GPA(marks, students)
            input("Press Enter to return.")
        case "11":
            clear_screen()
            exit()
        case "exit":
            clear_screen()
            exit()


def exit_curses(stdscr):
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()


# Courses related class and functions
class Courses:
    def __init__(self):
        self.__courses = []  # List of course object
        self.__number_of_course = 0

    def get_total(self) -> int:
        return self.__number_of_course

    def get_current(self) -> int:
        return len(self.__courses)

    def set_number_of_course(self, numberOfCourse) -> int:
        if numberOfCourse > self.__number_of_course:
            self.__number_of_course = numberOfCourse
            return 0
        print("Invalid input, please try again!")
        return -1

    def add_course(self, newCourse):
        if find_item_in_list(newCourse.get_name(), self.__courses, 0) != -1:
            print("Duplicate course, please try again!")
        else:
            self.__courses.append(newCourse)

    def find_course(self, courseToFind) -> int:  # Course ID or name
        return find_item_in_list(courseToFind, self.__courses, 1)

    def get_course(self, coursePosition) -> object:
        return self.__courses[coursePosition]

    def is_full(self) -> bool:
        return len(self.__courses) >= self.__number_of_course

    def check_empty(self) -> bool:
        return len(self.__courses) == 0

    def show_courses(self):
        headers = ["Course name", "Course ID", "Number of student", "Current"]
        widths = [9, 11, 3, 0]
        for header, width in zip(headers, widths):
            print(f"{header}{' ' * width}", end="")
        print()

        for course in self.__courses:
            print(
                f"{course.get_name()}{output_padding(course.get_name())}"
                f"{course.get_id()}{output_padding(course.get_id())}"
                f"{course.get_total()}{output_padding(course.get_total())}"
                f"{course.get_current()}"
            )


class Course:
    def __init__(self, name, id, total):
        self.__name = name
        self.__id = id
        self.__total = total
        self.__current = 0
        self.__studentsID = []  # Student ID only, not object

    def __str__(self) -> str:
        return f"Course name {self.__name}\nCourse Id: {self.__id}\nTotal student: {self.__total}\nCurrent number of student: {self.__current}"

    def get_name(self) -> str:
        return self.__name

    def get_id(self) -> str:
        return self.__id

    def get_total(self) -> int:
        return self.__total

    def set_total(self, newTotal):
        if newTotal > self.__total:
            self.__total = newTotal
        else:
            print(
                "Invalid input, please enter a number greater than the current total."
            )

    def get_current(self) -> int:
        return self.__current

    def is_full(self) -> bool:
        return self.__current >= self.__total

    def add_student(self, newStudentID) -> int:
        if self.is_full():
            if (
                get_input_as_string(
                    "The course is full. Do you want to add more student? (Y/N) "
                ).upper()
                == "Y"
            ):
                self.set_total(
                    get_input_as_int(
                        f"Current maximum: {self.get_total()}. Enter the new value: "
                    )
                )
            else:
                input("Failed to add student to course, please try again!")
                return -1

        if find_in_list(newStudentID, self.__studentsID) == -1:
            self.__current += 1
            self.__studentsID.append(newStudentID)
            return 0
        else:
            print("Duplicate student.")
            return -1

    def check_duplicate_student(self, newStudentID):
        return find_in_list(newStudentID, self.__studentsID) != -1

    def show_all_student(self, studentList):
        headers = ["Student name", "Student ID", "Date of birth"]
        widths = [8, 10, 7]
        for header, width in zip(headers, widths):
            print(f"{header}{' ' * width}", end="")
        print()

        for student_id in self.__studentsID:
            student_position = studentList.find_student(student_id)
            student = studentList.get_student(student_position)
            print(
                f"{student.get_name()}{output_padding(student.get_name())}"
                f"{student.get_id()}{output_padding(student.get_id())}"
                f"{student.get_dob()}"
            )


class Students:
    def __init__(self):
        self.__students = []  # List of object student

    def add_student(self, newStudent):  # Object newStudent
        self.__students.append(newStudent)

    def check_duplicate(self, newStudent):
        return find_item_in_list(newStudent.get_id(), self.__students, 0) != -1

    def find_student(self, student) -> int:
        return find_item_in_list(student, self.__students, 1)

    def get_student(self, studentPosition) -> object:
        return self.__students[studentPosition]

    def get_student_list(self) -> list:
        return self.__students

    def check_empty(self) -> bool:
        return len(self.__students) == 0

    def show_all_student(self):
        print(f"Total number of student: {len(self.__students)}")
        headers = ["Student name", "Student ID", "Date of birth"]
        widths = [8, 10, 7]
        for header, width in zip(headers, widths):
            print(f"{header}{' ' * width}", end="")
        print()

        for student in self.__students:
            print(
                f"{student.get_name()}{output_padding(student.get_name())}"
                f"{student.get_id()}{output_padding(student.get_id())}"
                f"{student.get_dob()}"
            )


class Student:
    def __init__(self, name, id, dob):
        self.__name = name
        self.__id = id
        self.__dob = dob
        self.__GPA = 0

    def __str__(self) -> str:
        return (
            f"Student name: {self.__name}\nStudent ID: {self.__id}\nDOB: {self.__dob}"
        )

    def __eq__(self, otherStudent) -> bool:
        if not isinstance(otherStudent, Student):
            return NotImplemented
        else:
            return self.__GPA == otherStudent.get_GPA()

    def __lt__(self, otherStudent) -> bool:
        if not isinstance(otherStudent, Student):
            return NotImplemented
        else:
            return self.__GPA < otherStudent.get_GPA()

    def get_name(self) -> str:
        return self.__name

    def get_id(self) -> str:
        return self.__id

    def get_dob(self) -> str:
        return self.__dob

    def set_GPA(self, GPA):
        self.__GPA = GPA

    def get_GPA(self) -> str:
        return self.__GPA


class Marks(Courses):
    def __init__(self):
        super().__init__()

    def add_course(self, newCourse):
        self._Courses__courses.append(newCourse)

    def get_total(self):
        pass

    def get_current(self):
        pass

    def set_number_of_course(self, numberOfCourse):
        pass

    def is_full(self):
        pass

    def check_empty(self):
        pass

    def show_courses(self):
        pass

    def calculate_GPA(self, student, omitOutput) -> int:
        listMarks, totalECTs = [], 0

        if not omitOutput:
            headers = ["Course name", "Course ID", "ECTs", "Mark"]
            widths = [9, 11, 16, 0]
            for header, width in zip(headers, widths):
                print(f"{header}{' ' * width}", end="")
            print()

        for mark in self._Courses__courses:
            studentPosition = mark.find_student(student)
            if studentPosition != -1:
                studentData = mark.get_student(studentPosition)
                studentMark = studentData.get_mark()
                listMarks.append(studentMark * mark.get_ECTs())
                totalECTs += mark.get_ECTs()

            if not omitOutput:
                print(
                    f"{mark.get_name()}{output_padding(mark.get_name())}"
                    f"{mark.get_id()}{output_padding(mark.get_id())}"
                    f"{mark.get_ECTs()}{output_padding(mark.get_ECTs())}"
                    f"{studentMark if studentPosition != -1 else 'No info'}"
                )

        gpaArray = np.array(listMarks, dtype=int)
        return gpaArray.sum() / totalECTs


class Mark(Course):
    def __init__(self, name, id, ECTs):
        super().__init__(name, id, 0)
        self.__ECTs = ECTs
        self.__students = []  # Student mark object

    def __str__(self) -> str:
        return f"Course name: {self._Course__name}\nCourse ID: {self._Course__id}"

    def get_total(self):
        pass

    def set_total(self):
        pass

    def get_current(self):
        pass

    def get_ECTs(self) -> int:
        return self.__ECTs

    def is_full(self):
        pass

    def add_student(self, newStudent):
        self.__students.append(newStudent)

    def find_student(self, student) -> int:
        if len(self.__students) == 0:
            return -1
        position = find_item_in_list(student, self.__students, 1)
        position = (
            position
            if position != -1
            else find_item_in_list(student, self.__students, 1)
        )
        return position

    def get_student(self, studentPosition) -> object:
        return self.__students[studentPosition]

    def show_all_student(self):
        headers = ["Student name", "Student ID", "Mark"]
        widths = [8, 10, 16]
        for header, width in zip(headers, widths):
            print(f"{header}{' ' * width}", end="")
        print()

        for student in self.__students:
            print(
                f"{student.get_name()}{output_padding(student.get_name())}"
                f"{student.get_id()}{output_padding(student.get_id())}"
                f"{student.get_mark()}{output_padding(student.get_mark())}"
            )


class StudentMark(Student):
    def __init__(self, name, id, dob):
        super().__init__(name, id, dob)
        self.__mark = 0

    def get_mark(self) -> int:
        return self.__mark

    def set_mark(self, mark) -> int:
        if mark < 0:
            print("Invalid input, please try again!")
            return -1
        else:
            self.__mark = mark
            return 0


def add_course(courseList, markList):
    if courseList.is_full():
        increase_courses = get_input_as_string("Course list is full, do you want to increase the number of courses? (Y/N) ").upper()
        if increase_courses == "N":
            return
        print(f"Current number of courses: {courseList.get_current()}")
        while True:
            if (courseList.set_number_of_course(get_input_as_int("Enter new number of courses: "))== -1):
                continue
            break
    name, id, total = "", "", 0
    name = get_input_as_string("Enter the Course name: ").title()
    id = get_input_as_string("Enter the Course ID: ").upper()
    total = get_input_as_int("Enter the number of student in the course: ")
    ECTs = get_input_as_int("Enter ECTs: ")
    newCourse = Course(name, id, total)
    newMark = Mark(name, id, ECTs)
    courseList.add_course(newCourse)
    markList.add_course(newMark)


def show_all_student_course(studentList, courseList):
    courseInput = get_input_as_string("Enter Course name or ID: ")
    coursePosition = courseList.find_course(courseInput)
    if coursePosition == -1:
        input("Course not found, press Enter to continue.")
        return
    course = courseList.get_course(coursePosition)
    print(course)
    course.show_all_student(studentList)


def add_student(studentList, courseList, markList):
    if courseList.check_empty():
        input("Course list empty, please add a Course. Press Enter to try again!")
        return
    newStudent, name, id, dob = "", "", "", ""
    while True:
        name = get_input_as_string("Enter student name: ").title()
        id = get_input_as_string("Enter student ID: ").upper()
        dob = get_input_as_date(f'Enter "{name}" date of birth (DD-MM-YYYY): ')
        newStudent = Student(name, id, dob)
        newMark = StudentMark(name, id, dob)
        if studentList.check_duplicate(newStudent):
            print("Duplicate student, please try again!")
            continue
        break
    studentList.add_student(newStudent)

    courseList.show_courses()
    while True:
        courseChoice = get_input_as_string(
            'Enter the Course ID to add student or "empty" to skip: '
        ).upper()
        if courseChoice == "EMPTY":
            break
        coursePosition = courseList.find_course(courseChoice)
        if coursePosition == -1:
            input("Course not found, press Enter to try again!")
            continue
        course = courseList.get_course(coursePosition)
        mark = markList.get_course(coursePosition)

        if course.add_student(newStudent.get_id()) == -1:
            continue

        markChoice = get_input_as_string(
            "Do you want to add mark to student? (Y/N): "
        ).upper()
        if markChoice == "Y":
            while True:
                # if newMark.set_mark(get_input_as_float("Enter mark: ")) != -1:
                if newMark.set_mark(get_input_as_float_floor("Enter mark: ")) != -1:
                    break
        mark.add_student(newMark)
        break


def add_class_to_student(studentList, courseList, markList):
    if studentList.check_empty():
        input(
            "No student found in the system, please add one!\nPress Enter to continue."
        )
        return
    student, mark = "", ""
    while True:
        studentInput = get_input_as_string("Enter student name or id: ").upper()
        studentPosition = studentList.find_student(studentInput)
        if studentPosition == -1:
            print("Student not found, please try again!")
            continue
        clear_screen()
        student = studentList.get_student(studentPosition)
        print(student)
        break
    print()
    courseList.show_courses()

    while True:
        courseInput = get_input_as_string("Enter course name or ID to add student: ")
        coursePosition = courseList.find_course(courseInput)
        if coursePosition == -1:
            choice = get_input_as_string(
                "Course not found, do you want to try again? (Y/N) "
            ).upper()
            if choice == "N":
                return
        mark = markList.get_course(coursePosition)
        course = courseList.get_course(coursePosition)
        if course.check_duplicate_student(student.get_id()):
            print("Duplicate student, please try again!")
            continue
        course.add_student(student.get_id())
        break

    newMark = StudentMark(student.get_name(), student.get_id(), student.get_dob())
    while True:
        # if newMark.set_mark(get_input_as_float("Enter mark: ")) != -1:
        if newMark.set_mark(get_input_as_float_floor("Enter mark: ")) != -1:
            break
    mark.add_student(newMark)


def add_mark_to_student(markList, courseList):
    if courseList.check_empty():
        input("No course found, press Enter to continue!")
        return
    while True:
        mark = show_all_mark_course(markList, courseList)
        if mark:
            break
    print()
    studentInput = get_input_as_string("Enter student name or ID: ")

    studentPosition = mark.find_student(studentInput)
    if studentPosition == -1:
        input("Student not found, please try again!")
        return
    studentMark = mark.get_student(studentPosition)
    while True:
        # if studentMark.set_mark(get_input_as_float("Enter mark: ")) != -1:
        if studentMark.set_mark(get_input_as_float_floor("Enter mark: ")) != -1:
            break


def show_all_mark_course(markList, courseList) -> object:
    courseInput = get_input_as_string("Enter Course name or ID: ")
    coursePosition = courseList.find_course(courseInput)
    if coursePosition == -1:
        input("Course not found, press Enter to continue.")
        return None
    mark = markList.get_course(coursePosition)
    clear_screen()
    print(mark)
    print()
    mark.show_all_student()
    return mark


def calculate_GPA(markList, studentList):
    studentInput = get_input_as_string("Enter student name or ID: ")
    if studentList.find_student(studentInput) == -1:
        print("Student not found, please try again!")
        return
    GPA = markList.calculate_GPA(studentInput, False)
    print("GPA: " + str(GPA))


def rank_GPA(markList, studentList):
    students = studentList.get_student_list()
    totalStudents = len(students)

    for student in students:
        student.set_GPA(markList.calculate_GPA(student.get_name(), True))

    # Bubble sort, horrible complexity but just for the sake of implement sorting
    for i in range(0, totalStudents):
        for j in range(0, totalStudents - i - 1):
            if students[j].__eq__(students[j + 1]):
                continue
            if students[j].__lt__(students[j + 1]):
                temp = students[j]
                students[j] = students[j + 1]
                students[j + 1] = temp

    headers = ["Student name", "Student ID", "GPA"]
    widths = [8, 10, 13]
    for header, width in zip(headers, widths):
        print(f"{header}{' ' * width}", end="")
    print()

    for student in students:
        print(
            f"{student.get_name()}{output_padding(student.get_name())}"
            f"{student.get_id()}{output_padding(student.get_id())}"
            f"{student.get_GPA()}"
        )


students = Students()
courses = Courses()
marks = Marks()


def old_UI():
    clear_screen()
    courses.set_number_of_course(get_input_as_int("Enter number of courses: "))
    while True:
        clear_screen()
        startup_display = (
            "1. Enter student's information.\n"
            + "2. Enter course's information\n"
            + "3. Add course to existing student\n"
            + "4. Show all students data\n"
            + "5. Show all Courses\n"
            + "6. Show all student from a Course\n"
            + "7. Add marks for a student in a given course.\n"
            + "8. Display marks for a given course\n"
            + "9. Show student GPA\n"
            + "10. Rank student's GPA\n"
            + '"exit" to quit the program.\n'
        )
        choice = input(startup_display)
        choose_menu(choice)


# Just an interface to replace the old UI, everything else stay the same
def welcome_screen(stdscr):
    curses.curs_set(False)  # Hide the cursor

    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
    BLUE_AND_BLACK = curses.color_pair(1)
    WHITE_AND_RED = curses.color_pair(2)
    CYAN_AND_BLACK = curses.color_pair(3)

    stdscr.clear()
    stdscr.refresh()

    max_y, max_x = stdscr.getmaxyx()

    if max_x < 120 or max_y < 33:
        stdscr.addstr(f"Current size: {max_x} x {max_y}. Please use a terminal bigger than 120x32.",
            curses.A_BOLD,)
        stdscr.refresh()
        stdscr.nodelay(True)
        warningWindow = curses.newwin(max_y, max_x, 1, 0)
        for i in range(0, 4):
            warningWindow.addstr(
                0, 0, "Terminal too small! Using compact UI...", WHITE_AND_RED | curses.A_BLINK
            )
            warningWindow.refresh()
            time.sleep(1)
        exit_curses(stdscr)
        old_UI()
        clear_screen()
        exit()
    else:
        headerWindow = curses.newwin(6, 115, 2, (max_x - 114) // 2)
        header = """███╗   ███╗ █████╗ ██████╗ ██╗  ██╗██╗███╗   ██╗ ██████╗     ███████╗██╗   ██╗███████╗████████╗███████╗███╗   ███╗
████╗ ████║██╔══██╗██╔══██╗██║ ██╔╝██║████╗  ██║██╔════╝     ██╔════╝╚██╗ ██╔╝██╔════╝╚══██╔══╝██╔════╝████╗ ████║
██╔████╔██║███████║██████╔╝█████╔╝ ██║██╔██╗ ██║██║  ███╗    ███████╗ ╚████╔╝ ███████╗   ██║   █████╗  ██╔████╔██║
██║╚██╔╝██║██╔══██║██╔══██╗██╔═██╗ ██║██║╚██╗██║██║   ██║    ╚════██║  ╚██╔╝  ╚════██║   ██║   ██╔══╝  ██║╚██╔╝██║
██║ ╚═╝ ██║██║  ██║██║  ██║██║  ██╗██║██║ ╚████║╚██████╔╝    ███████║   ██║   ███████║   ██║   ███████╗██║ ╚═╝ ██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝     ╚══════╝   ╚═╝   ╚══════╝   ╚═╝   ╚══════╝╚═╝     ╚═╝"""

    header = [char for char in header]
    for i in range(0, len(header)):
        headerWindow.addstr(header[i], BLUE_AND_BLACK)
        headerWindow.refresh()
        time.sleep(0.001)

    boxWindow = curses.newwin(9, 120, 10, (max_x - 120) // 2)
    boxWindow.attron(CYAN_AND_BLACK)
    boxWindow.box()
    boxWindow.refresh()

    messageWindow = curses.newwin(7, 118, 11, (max_x - 118) // 2)
    message1 = "Welcome to the Student Marks Management System, an interactive and user-friendly application designed to streamline   the process of managing and tracking student performance across various courses. This system is an ideal tool for     educational institutions, teachers, and administrative staff who seek an efficient way to handle academic records."
    message2 = "\n\nUpon launching the Student Marks Management System, you will be greeted with a main menu offering various options,    such as adding or viewing student information, managing courses, and recording marks. Navigate through these options  using the keyboard, and follow the on-screen prompts to input or retrieve data."
    messageWindow.addstr(message1)
    messageWindow.addstr(message2)
    messageWindow.refresh()

    menuWindow = curses.newwin(15, 45, 21, (max_x - 34) // 2)
    choiceWindow = curses.newwin(2, 11, 21, (max_x - 58) // 2)

    curses.curs_set(True)
    courses.set_number_of_course(get_input_as_int_curses(menuWindow, "Enter number of courses: ", False, 19))
    curses.curs_set(False)
    startup_display = [
        "1. Enter student's information.",
        "2. Enter course's information.",
        "3. Add course to existing student.",
        "4. Show all students data.",
        "5. Show all Courses.",
        "6. Show all student from a Course.",
        "7. Add marks for a student in a given course.",
        "8. Display marks for a given course.",
        "9. Show student GPA.",
        "10. Rank student's GPA.",
        '"exit" to quit the program.',
    ]

    option = 1
    while True:
        menuWindow.clear()
        for i in range(0, len(startup_display)):
            if i == option - 1:
                display = "=>" + startup_display[i]
                menuWindow.addstr(i, 0, display, curses.A_BLINK | BLUE_AND_BLACK)
            else:
                menuWindow.addstr(i, 0, startup_display[i])
        menuWindow.refresh()

        key = stdscr.getkey()
        if key == "KEY_UP":
            option -= 1 if option >= 0 else 0
            if option == 0: option = 11
        elif key == "KEY_DOWN":
            option += 1 if option < 12 else 0
            if option == 12: option = 0
        elif key in [10, "\n", "\r", curses.KEY_ENTER]:
            if option == 11: exit(1)
            elif option in range(1, 11):
                curses.endwin()
                choose_menu(option)
            # Return the terminal back to curses
            stdscr = curses.initscr()
            curses.cbreak()
            stdscr.keypad(True)
        elif key in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
            choiceWindow.addstr("Choice: ")
            choice = get_input_as_int_curses(choiceWindow, "", True, 2)
            choiceWindow.clear()
            choiceWindow.refresh()
            curses.endwin()
            choose_menu(choice)
            curses.cbreak()
            stdscr.keypad(True)

wrapper(welcome_screen)