
# Create Bash script
This is a "bonus" chapter.
We now want to write a bash script, which will execute our program for each of the 3 days in a row.

But first lets learn what a bash script is.

First of all you need to create a file, with the ending "sh" for example the file in "learn_area" with the name "test_bash.sh".
Inside this file you that just put in all linux commands. In the shell script you can also use variables. Here are the commands inside the file "test_bash.sh".

```bash
# this is a bash script.
ls
name=peter
echo "---------"
echo "his name is" $name 
```

Now run the bash file. Make sure you are in the shell and in the directory "learn_area". Then execute the following command:

```sh
bash test_bash.sh
```

As you can see, all the commands in the script where executed. First "ls" shows us all files. Then the name "peter" is stored in the variable "name". Then we have some "echo" which is like "print" in python.



### TASK 18 (CODING):
Now write your own bash script.
- write bash commands inside the file "bash_script.sh"
- The bash script should: create 3 variables with a value: name, age, job
- it should run our python program "run_with_parameters" with the 3 variables as an argument
- run the bash script.

### TASK 19 (PROJECT):
Now its time to add a bash script this to our project. Remember, we executed our program with 3 different days.
- write a bash script which executes our program for each of the 3 days.
- execute the bash script
