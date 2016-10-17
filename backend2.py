import subprocess
#from subprocess import PIPE, Popen
#p = Popen(["./upper"],shell=True, stdin=PIPE, stdout=PIPE, bufsize=80)
#for i in range(10): # repeat several times to show that it works
#    r = raw_input()
#    print p.communicate(r)[0]
    #r >>p.stdin, i # write input
    #p.stdin.flush() # not necessary in this case
    #print p.stdout.readline() # read output

#print p.communicate("n\n")[0]
#proc = subprocess.Popen(['upper'],shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,)

proc = subprocess.Popen(['/usr/local/MATLAB/R2014b/bin/matlab'],shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,)
for i in xrange(11):
    stdout_value = proc.stdout.readline()
    print stdout_value
print 'Matlab initialized\n'
proc.stdin.write('io_test\n');
print 'Ready to Go:\n'

def get_response(in_msg):
    r = in_msg
    def is_ascii(s):
        return all(ord(c) < 128 for c in s)
    if is_ascii(r):
        r = "'"+r+"'"
        proc.stdin.write(r+'\n')
        out_msg = proc.stdout.readline()
        out_msg = out_msg[2:].strip()
        print out_msg
        return out_msg
    else:
        return u'Sorry, can you speak English?'
