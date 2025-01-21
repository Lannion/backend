DROP DATABASE IF EXISTS `enrollment_system`;
CREATE DATABASE IF NOT EXISTS `enrollment_system`;
USE `enrollment_system`;
CREATE TABLE IF NOT EXISTS `Address` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `street` varchar(55),
  `barangay` varchar(55),
  `city` varchar(55) NOT NULL,
  `province` varchar(55) NOT NULL
);

CREATE TABLE IF NOT EXISTS `Student` (
  `id` bigint PRIMARY KEY NOT NULL,
  `email` varchar(55) UNIQUE,
  `middle_name` varchar(55),
  `first_name` varchar(55) NOT NULL,
  `last_name` varchar(55) NOT NULL,
  `suffix` varchar(55),
  `address_id` int NOT NULL,
  `date_of_birth` date,
  `gender` ENUM ('MALE', 'FEMALE', 'PREFER_NOT_TO_SAY') NOT NULL DEFAULT 'PREFER_NOT_TO_SAY',
  `contact_number` varchar(55),
  `status` ENUM ('REGULAR', 'IRREGULAR', 'TRANSFEREE', 'RETURNEE', 'NEW_STUDENT') NOT NULL DEFAULT 'Regular',
  `section` int NOT NULL,
  `year_level` int NOT NULL,
  `academic_year` varchar(55),
  `category` ENUM ('OLD', 'NEW') NOT NULL DEFAULT 'Old',
  `program` ENUM ('NO_PROGRAM_YET', 'BSIT', 'BSCS')
);

CREATE TABLE IF NOT EXISTS `Schedule` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `course_id` int NOT NULL,
  `instructor_id` int NOT NULL,
  `from_time` time,
  `to_time` time,
  `year_level` int,
  `section` int,
  `category` ENUM ('LAB', 'LEC'),
  `day` ENUM ('MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY'),
  `room` varchar(55)
);

CREATE TABLE IF NOT EXISTS `Instructor` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `first_name` varchar(55) NOT NULL,
  `last_name` varchar(55) NOT NULL,
  `middle_name` varchar(55),
  `suffix` varchar(55),
  `email` varchar(55),
  `contact_number` varchar(55)
);

CREATE TABLE IF NOT EXISTS `Course` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `code` varchar(55) NOT NULL,
  `title` varchar(55) NOT NULL,
  `lab_units` int,
  `lec_units` int,
  `contact_hr_lab` int,
  `contact_hr_lec` int,
  `year_level` int NOT NULL,
  `semester` int NOT NULL,
  `program` ENUM ('NO_PROGRAM_YET', 'BSIT', 'BSCS')
);

CREATE TABLE IF NOT EXISTS `Pre_Requisite` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `pre_requisite` int NOT NULL,
  `course_id` int NOT NULL
);

CREATE TABLE IF NOT EXISTS `Enrollment` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `course_id` int NOT NULL,
  `student_id` bigint NOT NULL,
  `enrollment_date` timestamp NOT NULL,
  `status` ENUM ('ENROLLED', 'WAITLISTED') NOT NULL,
  `school_year` date NOT NULL
);

CREATE TABLE IF NOT EXISTS `Grade` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `student_id` bigint NOT NULL,
  `course_id` int NOT NULL,
  `grade` decimal(5,2) COMMENT '1.00 to 5.00 scale',
  `instructor_id` int NOT NULL,
  `remarks` ENUM ('PASSED', 'FAILED', 'INCOMPOLETE', 'UNCONDITIONAL_FAILURE', 'NOT_GRADED_YET') DEFAULT 'Not_Graded_Yet'
);

CREATE TABLE IF NOT EXISTS `Billing` (
  `id` int PRIMARY KEY NOT NULL,
  `type` varchar(55) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `category` ENUM ('LAB_FEES', 'OTHER_FEES', 'ASSESSMENT') NOT NULL,
  `student_id` bigint NOT NULL
);

CREATE UNIQUE INDEX `Schedule_index_0` ON `Schedule` (`course_id`, `category`, `day`, `from_time`, `to_time`);

CREATE UNIQUE INDEX `Course_index_1` ON `Course` (`code`, `program`);

CREATE UNIQUE INDEX `Enrollment_index_2` ON `Enrollment` (`course_id`, `student_id`);

CREATE UNIQUE INDEX `Grade_index_3` ON `Grade` (`student_id`, `course_id`);

ALTER TABLE `Student` ADD FOREIGN KEY (`address_id`) REFERENCES `Address` (`id`) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE `Schedule` ADD FOREIGN KEY (`course_id`) REFERENCES `Course` (`id`) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE `Schedule` ADD FOREIGN KEY (`instructor_id`) REFERENCES `Instructor` (`id`) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE `Pre_Requisite` ADD FOREIGN KEY (`pre_requisite`) REFERENCES `Course` (`id`) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE `Pre_Requisite` ADD FOREIGN KEY (`course_id`) REFERENCES `Course` (`id`) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE `Enrollment` ADD FOREIGN KEY (`course_id`) REFERENCES `Course` (`id`) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE `Enrollment` ADD FOREIGN KEY (`student_id`) REFERENCES `Student` (`id`) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE `Grade` ADD FOREIGN KEY (`student_id`) REFERENCES `Student` (`id`) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE `Grade` ADD FOREIGN KEY (`course_id`) REFERENCES `Course` (`id`) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE `Grade` ADD FOREIGN KEY (`instructor_id`) REFERENCES `Instructor` (`id`) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE `Billing` ADD FOREIGN KEY (`student_id`) REFERENCES `Student` (`id`) ON UPDATE CASCADE ON DELETE CASCADE;