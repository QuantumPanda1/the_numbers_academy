-- File: test.sql
-- Drop existing tables if they exist
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS Homework_Submissions;
DROP TABLE IF EXISTS Homework;
DROP TABLE IF EXISTS Attendance;
DROP TABLE IF EXISTS Student_Courses;
DROP TABLE IF EXISTS Students;
DROP TABLE IF EXISTS Courses;
DROP TABLE IF EXISTS Teachers;

-- Create Teachers table
CREATE TABLE Teachers (
    teacher_id SERIAL PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Courses table
CREATE TABLE Courses (
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(20) NOT NULL CHECK (course_name IN ('Abacus', 'VedicMaths', 'RubiksCube')),
    level VARCHAR(20) NOT NULL,
    description TEXT,
    UNIQUE(course_name, level)
);

-- Create Students table
CREATE TABLE Students (
    student_id SERIAL PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    parent_name VARCHAR(100) NOT NULL,
    parent_occupation VARCHAR(100),
    address TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Student_Courses table
CREATE TABLE Student_Courses (
    enrollment_id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES Students(student_id),
    course_id INTEGER REFERENCES Courses(course_id),
    teacher_id INTEGER REFERENCES Teachers(teacher_id),
    enrollment_date DATE NOT NULL,
    current_level VARCHAR(20) NOT NULL
);

-- Create Attendance table
CREATE TABLE Attendance (
    attendance_id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES Students(student_id),
    course_id INTEGER REFERENCES Courses(course_id),
    date DATE NOT NULL,
    status VARCHAR(10) CHECK (status IN ('Present', 'Absent', 'Late'))
);

-- Create Homework table
CREATE TABLE Homework (
    homework_id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES Courses(course_id),
    teacher_id INTEGER REFERENCES Teachers(teacher_id),
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    due_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Homework_Submissions table
CREATE TABLE Homework_Submissions (
    submission_id SERIAL PRIMARY KEY,
    homework_id INTEGER REFERENCES Homework(homework_id),
    student_id INTEGER REFERENCES Students(student_id),
    submission_text TEXT,
    submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    grade VARCHAR(10),
    feedback TEXT
);

-- Insert test teachers (passwords are hashed version of 'password123')
INSERT INTO Teachers (email, full_name, password_hash) VALUES
('sarah.math@school.com', 'Sarah Johnson', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi'),
('mike.science@school.com', 'Michael Brown', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi'),
('emma.english@school.com', 'Emma Wilson', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi');

-- Insert course data
INSERT INTO Courses (course_name, level, description) VALUES
-- Abacus levels
('Abacus', 'Level 1', 'Introduction to Abacus'),
('Abacus', 'Level 2', 'Basic Addition and Subtraction'),
('Abacus', 'Level 3', 'Advanced Addition and Subtraction'),
('Abacus', 'Level 4', 'Basic Multiplication'),
('Abacus', 'Level 5', 'Advanced Multiplication'),
('Abacus', 'Level 6', 'Basic Division'),
('Abacus', 'Level 7', 'Advanced Division'),
('Abacus', 'Level 8', 'Combined Operations'),
('Abacus', 'Level 9', 'Speed Enhancement'),
('Abacus', 'Level 10', 'Mental Calculations'),
('Abacus', 'Level 11', 'Advanced Mental Calculations'),

-- Vedic Maths levels
('VedicMaths', 'Level 1', 'Basic Vedic Mathematics'),
('VedicMaths', 'Level 2', 'Intermediate Calculations'),
('VedicMaths', 'Level 3', 'Advanced Techniques'),
('VedicMaths', 'Level 4', 'Expert Level'),

-- Rubik's Cube levels
('RubiksCube', '3x3', 'Standard Cube Solving'),
('RubiksCube', '4x4', 'Advanced Cube Solving');