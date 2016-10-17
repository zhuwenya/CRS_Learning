import subprocess
proc = subprocess.Popen(['cat'],shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,)
proc.stdin.write('io_test\n');
out_msg = proc.stdout.readline()
print out_msg
