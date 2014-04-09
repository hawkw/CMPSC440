# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from timeit import timeit
import numpy as np
import re
from subprocess import call, check_output

# <codecell>

ms = lambda seconds: seconds*1000

def count_files(result):
    lines = result.split('\n')
    files = 1
    last_line = ""
    
    for line in lines:
        if line.split(':')[0] == last_line:
            files += 1
        last_line = line.split(':')[0]
        
    return files

def profile(command, query, name):
    """Runs a command 30 times to profile it, returning a list of runs"""
    times = []
    instances = []
    files = []
    for i in range(30):
        times.append(ms(timeit('subprocess.call({c})'.format(c=command.split(' ')), 
                                setup="import subprocess", 
                                number=1
                                )))
        output = check_output(command, shell=True)
        instances.append(
                        len(re.findall(
                                        query, 
                                        str(output)
                                        )
                            )
                        )
        files.append(count_files(str(output)))
            
    return (times, instances, files, name)

def stats(values):
    return {
            'std': np.std(values),
            'mean': np.mean(values),
            'min': np.amin(values),
            'max': np.amax(values)
            }

results = {}

def build_result (times, instances, files, name):
    """Takes the result tuple from a profile() command and adds it to the results dict"""
    results[name] = {
            'times' : stats(times),
            'instances' : stats(instances),
            'files' : stats(files)
            }

# <codecell>

#-- DO TEST ONE: ---------------------------------#
#-- search ~/Documents for Java source code files
#-- which contain the word "Twitter"
build_result(*profile('ag --java twitter ~/Documents', 'twitter', 'ag_1'))
build_result(*profile('ack --java twitter ~/Documents', 'twitter', 'ack_1'))
build_result(*profile('grep -r -i --include \*.java twitter ~/Documents', 'twitter', 'grep_1'))

# <codecell>

#-- DO TEST TWO: ---------------------------------#
#-- search ~/Documents for Python source code files containing classes
build_result(*profile('ag --python class ~/Documents', 'class', 'ag_2'))
build_result(*profile('ack --python class ~/Documents', 'class'), 'ack_2')
build_result(*profile('grep -r -i --include \*.py class ~/Documents', 'class', 'grep_2'))

# <codecell>

#-- DO TEST THREE: ---------------------------------#
#-- search ~/Documents/DOCUMENTS/Projects/Knightingale for
# Java projects containing the word "knightingale"
build_result(*profile('ag  --java knightingale ~/Documents/DOCUMENTS/Projects/Knightingale',
                        'knightingale', 'ag_3'))
build_result(*profile('ack  --java knightingale ~/Documents/DOCUMENTS/Projects/Knightingale',
                        'knightingale', 'ack_3'))
build_result(*profile('grep -r -i --include \*.java knightingale ~/Documents/DOCUMENTS/Projects/Knightingale', 
                       'knightingale', 'grep_3'))

# <codecell>

#-- DO TEST FOUR: ---------------------------------#
#-- search ~/Documents/DOCUMENTS/Projects for a 
# source code files containing strings matching a
# regular expression which matches a website url.
build_result(*profile(R"ag 'https?:\/\/[^ \"\(\)\<\>]*[.][^ \"\(\)\<\>]*[.](com|net|org|edu|gov)' ~/Documents/DOCUMENTS/Projects/",
                        R'https?:\/\/[^ \"\(\)\<\>]*[.][^ \"\(\)\<\>]*[.](com|net|org|edu|gov)', 'ag_4'))
build_result(*profile(R'ack  "https?:\/\/[^ \"\(\)\<\>]*[.][^ \"\(\)\<\>]*[.](com|net|org|edu|gov)" ~/Documents/DOCUMENTS/Projects/',
                       R'https?:\/\/[^ \"\(\)\<\>]*[.][^ \"\(\)\<\>]*[.](com|net|org|edu|gov)', 'ack_4'))
build_result(*profile(R"grep -E 'https?:\/\/[^ \"\(\)\<\>]*[.][^ \"\(\)\<\>]*[.](com|net|org|edu|gov)' -r ~/Documents/DOCUMENTS/Projects", 
                       R'https?:\/\/[^ \"\(\)\<\>]*[.][^ \"\(\)\<\>]*[.](com|net|org|edu|gov)', 'grep_4'))

# <codecell>

#-- DO TEST FIVE: ---------------------------------#
#-- search /usr/share/dict/words for words 
# containing the  pattern 'ing'
build_result(*profile('ag ing /usr/share/dict/words', 'ing', 'ag_5'))
#build_result(*profile('ack ing /usr/share/dict/words', 'ing', 'ack_5'))
build_result(*profile('grep ing /usr/share/dict/words', 'ing', 'grep_5'))

# <codecell>

results

# <codecell>

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# <codecell>

sns.set_context("notebook")
sns.set_style("ticks")
palette = sns.color_palette('hls',3)
N = 5

# <codecell>

ag_time_means = (
                results['ag_1']['times']['mean'],
                results['ag_2']['times']['mean'],
                results['ag_3']['times']['mean'],
                results['ag_4']['times']['mean'],
                results['ag_5']['times']['mean']
                )
ag_time_stds = (
                results['ag_1']['times']['std'],
                results['ag_2']['times']['std'],
                results['ag_3']['times']['std'],
                results['ag_4']['times']['std'],
                results['ag_5']['times']['std']
                )

grep_time_means = (
                results['grep_1']['times']['mean'],
                results['grep_2']['times']['mean'],
                results['grep_3']['times']['mean'],
                results['grep_4']['times']['mean'],
                results['grep_5']['times']['mean']
                 )
grep_time_stds = (
                results['grep_1']['times']['std'],
                results['grep_2']['times']['std'],
                results['grep_3']['times']['std'],
                results['grep_4']['times']['std'],
                results['grep_5']['times']['std']
                )

ind = np.arange(N)  # the x locations for the groups
width = 0.35       # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind, ag_time_means, width, color=palette[0], yerr=ag_time_stds)
rects2 = ax.bar(ind+width, grep_time_means, width, color=palette[1], yerr=grep_time_stds)

# add some
ax.set_ylabel('Execution time')
ax.set_title('Execution time by query and search tool')
ax.set_xticks(ind+width)
ax.set_xticklabels( ('Query I', 'Query II', 'Query III', 'Query IV', 'Query V') )

ax.legend( (rects1[0], rects2[0]), ('ag', 'grep') )

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%.0f ms'% height,
                ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)
sns.despine()

plt.show()

# <codecell>

sns.set_context("notebook")
sns.set_style("ticks")

N = 5
ag_time_means = (
                results['ag_1']['instances']['mean'],
                results['ag_2']['instances']['mean'],
                results['ag_3']['instances']['mean'],
                results['ag_4']['instances']['mean'],
                results['ag_5']['instances']['mean']
                )
ag_time_stds = (
                results['ag_1']['instances']['std'],
                results['ag_2']['instances']['std'],
                results['ag_3']['instances']['std'],
                results['ag_4']['instances']['std'],
                results['ag_5']['instances']['std']
                )

grep_time_means = (
                results['grep_1']['instances']['mean'],
                results['grep_2']['instances']['mean'],
                results['grep_3']['instances']['mean'],
                results['grep_4']['instances']['mean'],
                results['grep_5']['instances']['mean']
                 )
grep_time_stds = (
                results['grep_1']['instances']['std'],
                results['grep_2']['instances']['std'],
                results['grep_3']['instances']['std'],
                results['grep_4']['instances']['std'],
                results['grep_5']['instances']['std']
                )

ind = np.arange(N)  # the x locations for the groups
width = 0.35       # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind, ag_time_means, width, color='r', yerr=ag_time_stds)
rects2 = ax.bar(ind+width, grep_time_means, width, color='y', yerr=grep_time_stds)

# add some
ax.set_ylabel('Instances of query')
ax.set_title('Instances of query by query and search tool')
ax.set_xticks(ind+width)
ax.set_xticklabels( ('Query I', 'Query II', 'Query III', 'Query IV', 'Query V') )

ax.legend( (rects1[0], rects2[0]), ('ag', 'grep') )

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%.0f'% height,
                ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)
sns.despine()

plt.show()

# <codecell>

sns.set_context("notebook")
sns.set_style("ticks")

N = 5
ag_time_means = (
                results['ag_1']['files']['mean'],
                results['ag_2']['files']['mean'],
                results['ag_3']['files']['mean'],
                results['ag_4']['files']['mean'],
                results['ag_5']['files']['mean']
                )
ag_time_stds = (
                results['ag_1']['files']['std'],
                results['ag_2']['files']['std'],
                results['ag_3']['files']['std'],
                results['ag_4']['files']['std'],
                results['ag_5']['files']['std']
                )

grep_time_means = (
                results['grep_1']['files']['mean'],
                results['grep_2']['files']['mean'],
                results['grep_3']['files']['mean'],
                results['grep_4']['files']['mean'],
                results['grep_5']['files']['mean']
                 )
grep_time_stds = (
                results['grep_1']['files']['std'],
                results['grep_2']['files']['std'],
                results['grep_3']['files']['std'],
                results['grep_4']['files']['std'],
                results['grep_5']['files']['std']
                )

ind = np.arange(N)  # the x locations for the groups
width = 0.35       # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind, ag_time_means, width, color='r', yerr=ag_time_stds)
rects2 = ax.bar(ind+width, grep_time_means, width, color='y', yerr=grep_time_stds)

# add some
ax.set_ylabel('Unique files')
ax.set_title('Unique files found by query and search tool')
ax.set_xticks(ind+width)
ax.set_xticklabels( ('Query I', 'Query II', 'Query III', 'Query IV', 'Query V') )

ax.legend( (rects1[0], rects2[0]), ('ag', 'grep') )

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%.0f'% height,
                ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)
sns.despine()

plt.show()

# <codecell>


