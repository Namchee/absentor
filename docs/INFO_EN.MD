# Discord Student Attendance Bot

## Context

Building a Discord Bot for student attendance in a Discord server and save attendance history for the students in a particular server in a Google sheet.

## Background

Because of a recent global event, an increasing amount of schools and universities are moving online to do their activities. One of the software that’s popularly used for this task is Discord. Discord is a software that specializes in text, image, video, and audio communication.

Since attendance is a crucial part of school / classroom activities, attendance system became important for both teachers and students alike. Unfortunately, it is very hard to determine whether someone in a discord server is using a real account, because as if for now there are only few ways a teacher could confirm the identity of aperson in a discord server. First by face cam, but that would need for everyone to have a camera and if they all do it would be very tedious for a teacher to do and also time consuming, especially in a classroom where there are plenty of students. Second is by voice, this one the teacher has to know every single voice of his/her student, it would be hard to do unless the teacher have a very good hearing.

Because of the previously mentioned problems and the lack of service provided for recording student attendance in a Discord server is why this project is initiated.

## Expected Outcome

A working Discord Bot that will help with reducing the possibility of a fake attendance done by a student and help the teachers to record student attendance for his/her students automatically.

## Expected Features

1. A member in a Discord server with a specific Role initiated a command to tell the bot to start recording student attendance in a period of time.
2. During this time, students can type a command that will tell the bot that the respective student are here in this server at that moment.
3. The bot will see your name and student unique id and record your name into a Google Sheet. if a student doesn’t do the command during this period of time the bot will assume that you are not attending the class and the correspondng student will be marked as absent.

## Limitations

1. Student must set their Discord name in a specific format, namely `<name> - <npm>`. Example: `Cristopher - 2017730017` is a valid format while `Fariz` is not a valid format and will be ignored by the bot

## Tech Stack

1. Python
2. Discord API
