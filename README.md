# Diversity Challenge

*A python code written to run Diversity Challenge quiz events for the Raspberry Pi and associated hardware.* :+1:

This code can be adapted for other quiz like ideas.

## Getting Started

These instructions will enable you to run the software, how to add questions, and some hints on how you can edit the code for your quiz idea.

### What you need

```
1. A Raspberry Pi 3 Model B+ (what it was originally used on)
2. Raspbian installed
3. Pygame and its dependencies
(see https://www.pygame.org/wiki/GettingStarted)
4. Diversity Challenge buzzer setup
```

### Installing the code

Open the terminal on your Raspberry Pi (RPi) and type `ls`. It should say

> /home/pi

. Next run this command in the terminal

```
git clone https://github.com/patherlkd/Diversity-Challenge.git
```
, if you get any error messages please see this guide: https://help.github.com/en/articles/cloning-a-repository. To check the code works change to the Diversity-Challenge directory `cd Diversity-Challenge` and run `python3.6 DC_main.py`, the start screen should appear.

### Adding questions

The Diversity Challenge code requires a database of questions. This database is located at
> DC_QUESTIONS/questions/questions.csv
which is structured as follows
> N/A, author, contact, category, question, answer
. The structure is due to the initial construction of the Diversity Challenge database, you can, of course, change this structure in the 
