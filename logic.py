

def checkInputLogin(usern, passw):
    if usern == "" or passw == "":
        return False
    else:
        return True


def checkInputRegister(usern, passw, conpassw):
    if usern != "" and passw != "" and conpassw != "":
        return True
    else:
        return False


def checkInputAddStudent(fname, lname, student_id, course, section, course_code, time, day):
    if fname and lname and student_id and course and section and course_code and time and day != "":
        return True
    else:
        return False
