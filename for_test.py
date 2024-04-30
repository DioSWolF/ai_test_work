import json


a = """{
"topic_id": 399,
"step_id": 6464,
"errors": [
"The wrong code prompts for input instead of directly reading integers.",
"The variable assignment is not following the correct order as specified in the task description.",
"The output format does not match the expected format."
],
"recommendations": [
"Read input directly without prompts using int(input()).",
"Ensure the correct order of variable assignment according to the task description.",
"Ensure the output format matches the expected format."
]},

{
"topic_id": 534,
"step_id": 10302,
"errors": [
"The wrong code uses a comma to separate variables in the print statement instead of concatenating them.",
"The correct code uses an f-string for formatting but the wrong code does not."
],
"recommendations": [
"Use proper string concatenation or formatting to print the equation in the correct format.",
"Consider using f-strings for cleaner and more readable code."
]},

{
"topic_id": 407,
"step_id": 6554,
"errors": [
"The wrong code does not convert input to integers, leading to incorrect comparison results.",
"The wrong code does not handle the case where Ann sleeps exactly A hours.",
"The output messages do not match the specified cases exactly."
],
"recommendations": [
"Convert input to integers using int() to ensure correct numerical comparison.",
"Consider adding a condition for when Ann sleeps exactly A hours.",
"Ensure the output messages exactly match the specified cases ("Deficiency," "Excess," "Normal")."
]},

{
"topic_id": 453,
"step_id": 6609,
"errors": [
"The wrong code does not correctly count the number of correct answers.",
"The wrong code does not implement the condition to stop counting after 3 incorrect answers.",
"The wrong code does not print the final score on a separate line."
],
"recommendations": [
"Ensure correct counting of correct answers and stopping after 3 incorrect answers.",
"Implement the condition to stop counting after 3 incorrect answers.",
"Print the final score on a separate line for clarity."
]},

{
"topic_id": 501,
"step_id": 6850,
"errors": [
"The wrong code directly prints the input string in uppercase without storing it in a variable.",
"The wrong code does not follow the correct output format."
],
"recommendations": [
"Store the input string in a variable before converting it to uppercase.",
"Ensure the output format matches the expected format."
]},

{
"topic_id": 1046,
"step_id": 6487,
"errors": [
"The wrong code uses a colon instead of a space in the output format.",
"The wrong code does not print the statistics in the correct format."
],
"recommendations": [
"Use a space instead of a colon to separate the word and its count in the output.",
"Ensure the statistics are printed in the correct format as specified."
]},

{
"topic_id": 534,
"step_id": 10301,
"errors": [
"The wrong code calls a function "greetings" that is not defined instead of "greeting".",
"The wrong code only calls the function once instead of twice as required."
],
"recommendations": [
"Ensure the correct function name "greeting" is called.",
"Call the function twice as specified in the task description."
]},

{
"topic_id": 440,
"step_id": 8213,
"errors": [
"The wrong code does not print the word exactly 2 times as required.",
"The wrong code does not use the correct multiplication to repeat the word."
],
"recommendations": [
"Use the correct multiplication operation to print the word exactly 2 times.",
"Ensure the word is repeated exactly 2 times without any separation."
]},

{
"topic_id": 404,
"step_id": 5918,
"errors": [
"The wrong code does not read the input numbers correctly using int(input).",
"The wrong code does not follow the correct order of variable assignment."
],
"recommendations": [
"Read input numbers directly as integers using int(input()).",
"Ensure the correct order of variable assignment according to the task description."
]},

{
"topic_id": 855,
"step_id": 8832,
"errors": [
"The wrong code checks if the first string is in the second string instead of the other way around.",
"The wrong code directly prints the result of the membership test without considering the correct order."
],
"recommendations": [
"Check if the second string is in the first string as required.",
"Ensure the membership test result is printed in the correct order."
]}"""
# a = a.replace("'", '"')
b = json.dumps(a)
b = json.loads(b)

# print(type(b))
with open("text.txt", "r") as file:
    json.load(file)
