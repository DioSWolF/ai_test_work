After testing several prompt and code designs, I chose this option because:

1.It is universal 
2.It provides answers that can be further processed and checked
3.It is more suitable for future development, where tasks will be automatically generated
4.Can be used as a test and quality check option for automatically generated prompt for each task

There was an option to write a prompt for each task, but it is worse in terms of development, since you will have to generate a prompt for each task manually.

Neural networks get over-trained and after some time prompts need to be changed. Using a prompt for each task leads to a lot of editing and changes to prompts when over-training the LLM agent and this is more difficult to check and monitor.

The prompt is divided into 2 main parts, there is a “code review” and a “friendly reply format” prompt. 

“Code review” prompt analyses student’s code, compares it to the correct answer, depending on the error found it gives recommendation and additional tips. 

“Friendly reply format” prompt creates the student-friendly format of the answer. 