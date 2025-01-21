# Wag muna gamitin hindi pa tapos
DELIMITER $$

-- Trigger for `user` table
CREATE TRIGGER trg_user_insert BEFORE INSERT ON `user`
FOR EACH ROW
BEGIN
    IF NEW.username NOT REGEXP '^(([A-Za-z][A-Za-z0-9@._-]{7,})|(((18|19|20)\d{2})(10|11)\d{3}))$' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid username format.';
    END IF;
    IF NEW.password NOT REGEXP '^[\x21-\x7E]{8,}$' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid password format.';
    END IF;
    IF NEW.contact_number NOT REGEXP '^(\+63|0)(2\d{8}|9\d{9})$' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid password format.';
    END IF;
    IF NEW.email NOT REGEXP '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid username format.';
    END IF;
END$$

-- Trigger for `program` table
CREATE TRIGGER trg_program_insert BEFORE INSERT ON `program`
FOR EACH ROW
BEGIN
    SET NEW.username = UPPER(NEW.username);
END$$

-- Trigger for `student` table
CREATE TRIGGER trg_student_insert BEFORE INSERT ON `student`
FOR EACH ROW
BEGIN
    IF NEW.id NOT REGEXP '^((19|20)\d{2})(10|11)\d{3}$' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid _id format for student.';
    END IF;
     IF NEW.contact_number NOT REGEXP '^(\+63|0)(2\d{8}|9\d{9})$' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid password format.';
    END IF;
    IF NEW.email NOT REGEXP '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid username format.';
    END IF;
END$$

-- Trigger for `instructor` table
CREATE TRIGGER trg_instructor_insert BEFORE INSERT ON `instrutor`
FOR EACH ROW
BEGIN
     IF NEW.contact_number NOT REGEXP '^(\+63|0)(2\d{8}|9\d{9})$' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid password format.';
    END IF;
    IF NEW.email NOT REGEXP '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid username format.';
    END IF;
END$$

-- Trigger for `course` table
CREATE TRIGGER trg_course_insert BEFORE INSERT ON `course`
FOR EACH ROW
BEGIN
    IF NEW.school_year NOT REGEXP '^(19|20)\d{2}-(19|20)\d{2}$' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid _id format for course.';
    END IF;
    IF NEW.code NOT REGEXP '^[A-Z]{4}\d{1,3}[A-Z]?$' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid code format.';
    END IF;
END$$

-- Trigger for `enrollment` table
CREATE TRIGGER trg_enrollment_insert BEFORE INSERT ON `enrollment`
FOR EACH ROW
BEGIN
    IF NEW.course_id NOT REGEXP '^[A-Z]{4}\d{1,3}[A-Z]?$' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid course_id format.';
    END IF;
END$$

-- Trigger for `grade` table
CREATE TRIGGER trg_grade_insert BEFORE INSERT ON `grade`
FOR EACH ROW
BEGIN
    IF NEW.student_id NOT REGEXP '^((18|19|20)\d{2})(10|11)\d{3}$' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid student_id format.';
    END IF;
END$$

DELIMITER ;