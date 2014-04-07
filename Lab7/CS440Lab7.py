
# coding: utf-8

# In[58]:

from timeit import timeit
import numpy as np
import re
from subprocess import call, check_output


# In[89]:

def count_files(result):
    lines = result.split('\n')
    files = 1
    last_line = ""
    
    for line in lines:
        if line.split(':')[0] == last_line:
            files += 1
        last_line = line.split(':')[0]
        
    return files

def profile(command, query):
    """Runs a command 30 times to profile it, returning a list of runs"""
    times = []
    instances = []
    files = []
    if command[:3] == 'ack':
        for i in range(30):
            times.append(timeit('subprocess.call(\"{c}\")'.format(c=command), 
                                setup="import subprocess", 
                                number=1
                                )
                         )
            output = check_output(command)
            instances.append(
                            len(re.findall(query, output))
                            )
            files.append(count_files(output))
    else:
        for i in range(30):
            times.append(timeit("subprocess.call(\"{c}\", shell=True)".format(c=command), 
                                setup="import subprocess", 
                                number=1
                                )
                         )
            output = check_output(command, shell=True)
            instances.append(
                            len(re.findall(query, output))
                            )
            files.append(count_files(output))
            
    return (command, times, instances, files)

def stats(values):
    return {
            'std': np.std(values),
            'mean': np.mean(values),
            'min': np.amin(values),
            'max': np.amax(values)
            }

results = {}

def build_result (command, times, instances, files):
    """Takes the result tuple from a profile() command and adds it to the results dict"""
    results[command] = {
            'times' : stats(times),
            'instances' : stats(instances),
            'files' : stats(files)
            }


# In[98]:

#-- DO TEST ONE: ---------------------------------#
#-- search ~/Documents for Java source code files
#-- which contain the word "Twitter"
#build_result(*profile('ag --java twitter ~/Documents', 'twitter'))
build_result(*profile('grep -r -i --include \*.java twitter ~/Documents', 'twitter'))


# In[93]:

#-- DO TEST TWO: ---------------------------------#
#-- search ~/Documents for Python source code files containing classes
build_result(*profile('ag --python class ~/Documents', 'class'))
build_result(*profile('grep -r -i --include \*.py class ~/Documents', 'class'))


# In[94]:

#-- DO TEST THREE: ---------------------------------#
#-- search ~/Documents/DOCUMENTS/Projects/Knightingale for
# Java projects containing the word "knightingale"
build_result(*profile('ag  --java knightingale ~/Documents/DOCUMENTS/Projects/Knightingale',
                        'knightingale'))
build_result(*profile('grep -r -i --include \*.java knightingale ~/Documents/DOCUMENTS/Projects/Knightingale', 
                       'knightingale'))


# In[96]:

#-- DO TEST FOUR: ---------------------------------#
#-- search ~/Documents/DOCUMENTS/Projects for a 
# source code files containing strings matching a
# regular expression which matches a url ending in .com:
# /(\S+\.com(\/\S+)?)/
build_result(*profile('ag  \"(\\S+\\.(com|net|org|edu|gov)(\\\/\\S+)?)\" ~/Documents/DOCUMENTS/Projects/',
                        R'(\S+\.(com|net|org|edu|gov)(\/\S+)?)'))
build_result(*profile('grep -r -e \"(\\S+\\.(com|net|org|edu|gov)(\\\/\\S+)?)\"~/Documents/DOCUMENTS/Projects/', 
                       R'(\S+\.(com|net|org|edu|gov)(\/\S+)?)'))


# In[97]:

results


# In[ ]:



