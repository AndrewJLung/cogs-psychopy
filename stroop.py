import time
import sys
import os
import random
from psychopy import visual,event,core,gui
from generate_trials import generate_trials

# I want to preface this submission by saying I followed the tutorial on the website very closely
# There may be something wrong with the code that I can't find even though most of the code is directly from the site
# When I run the code on my environment, the program stalls and cannot exit after implementing PT2

stimuli = ['red', 'orange', 'yellow', 'green', 'blue']
valid_response_keys = ['r', 'o', 'y', 'g', 'b']
trial_types = ['congruent','incongruent']

def get_runtime_vars(vars_to_get,order,exp_version="Stroop"):
    infoDlg = gui.DlgFromDict(dictionary=vars_to_get, title=exp_version, order=order)
    if infoDlg.OK:
        return vars_to_get
    else: 
        print('User Cancelled')

def import_trials(trial_filename, col_names=None, separator=','):
    trial_file = open(trial_filename, 'r')
    if col_names is None:
        col_names = trial_file.readline().rstrip().split(separator)
    trials_list = []
    for cur_trial in trial_file:
        cur_trial = cur_trial.rstrip().split(separator)
        assert len(cur_trial) == len(col_names)
        trial_dict = dict(zip(col_names, cur_trial))
        trials_list.append(trial_dict)
    return trials_list

# init constant vars
win = visual.Window([800,600],color="gray", units='pix',checkTiming=False)
placeholder = visual.Rect(win,width=180,height=80, fillColor="lightgray",lineColor="black", lineWidth=6,pos=[0,0])
word_stim = visual.TextStim(win,text="", height=40, color="black",pos=[0,0])
instruction = visual.TextStim(win,text="Press the first letter of the ink color", height=20, color="black",pos=[0,-200],autoDraw=True)
fixation = visual.TextStim(win,height=40,color="black",text="+")
feedback_incorrect = visual.TextStim(win,text="INCORRECT", height=40, color="black",pos=[0,0])
feedback_too_slow = visual.TextStim(win,text="TOO SLOW", height=40, color="black",pos=[0,0])

# init run-time vars
order =  ['subj_code','seed','num_reps']
runtime_vars = get_runtime_vars({'subj_code':'stroop_101','seed': 101, 'num_reps': 25}, order)

# gen trials
generate_trials(runtime_vars['subj_code'],runtime_vars['seed'],runtime_vars['num_reps'])
trial_path = os.path.join(os.getcwd(),'trials',runtime_vars['subj_code']+'_trials.csv')
trial_list = import_trials(trial_path)
print(trial_list)

try:
    os.mkdir('data')
    print('Data directory did not exist. Created data/')
except FileExistsError:
    pass 
separator=","
data_file = open(os.path.join(os.getcwd(),'data',runtime_vars['subj_code']+'_data.csv'),'w')
header = separator.join(['subj_code','seed', 'word','color','trial_type','orientation','trial_num','response','is_correct','rt'])
data_file.write(header+'\n')

response_timer = core.Clock() # set response timer clock
# trial loop
# add a trial number
trial_num = 1

for cur_trial in trial_list:

    cur_word = cur_trial['word']
    cur_color = cur_trial['color']
    trial_type = cur_trial['trial_type']
    cur_ori = cur_trial['orientation']

    word_stim.setText(cur_word) #set text
    word_stim.setColor(cur_color) #set color

    if cur_ori=='upside_down':
        word_stim.setOri(180)
    else:
        word_stim.setOri(0)
    
    placeholder.draw()
    fixation.draw()
    win.flip()
    core.wait(0.5)
    placeholder.draw()
    win.flip()
    core.wait(0.5)
    placeholder.draw()
    word_stim.draw()
    win.flip()
    core.wait(1.0)
    placeholder.draw() 
    win.flip()

    response_timer.reset()
    key_pressed = event.waitKeys(keyList=valid_response_keys,maxWait=2)
    rt = round(response_timer.getTime()*1000,0)

    if not key_pressed:
        is_correct = 0
        response = "NA"
        feedback_too_slow.draw()
        win.flip()
        core.wait(1.0)
    elif key_pressed[0] == 'q':
        break
    elif key_pressed[0] == cur_color[0]:
        is_correct = 1
        response = key_pressed[0]
        pass
    else:
        is_correct = 0
        response = key_pressed[0]
        feedback_incorrect.draw()
        win.flip()
        core.wait(1)

    #writing a response
    response_list=[cur_trial[_] for _ in cur_trial]
    print(response_list)
	#write dependent variables
    response_list.extend([trial_num,response,is_correct,rt])
    responses = map(str,response_list)
    print(response_list)
    line = separator.join([str(i) for i in response_list])
    data_file.write(line+'\n')

    # increment trial number
    trial_num += 1

data_file.close()