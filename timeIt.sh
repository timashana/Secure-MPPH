# From https://stackoverflow.com/questions/556405/what-do-real-user-and-sys-mean-in-the-output-of-time1

# Real refers to actual elapsed time; User and Sys refer to CPU time used only by the process.

#     Real is wall clock time - time from start to finish of the call. This is all elapsed time including time slices used by other processes and time the process spends blocked (for example if it is waiting for I/O to complete).

#     User is the amount of CPU time spent in user-mode code (outside the kernel) within the process. This is only actual CPU time used in executing the process. Other processes and time the process spends blocked do not count towards this figure.

#     Sys is the amount of CPU time spent in the kernel within the process. This means executing CPU time spent in system calls within the kernel, as opposed to library code, which is still running in user-space. Like 'user', this is only CPU time used by the process. See below for a brief description of kernel mode (also known as 'supervisor' mode) and the system call mechanism.

# User+Sys will tell you how much actual CPU time your process used. 


#replace sleep 2 with your application of choice
(time sleep 2) |& cut -f2 | cut -d"m" -f2 | head -n3 | tail -n2 | cut -d"s" -f1 | tr "\n" "\t" | cut -f1,2 | tr "\t" "+" | bc