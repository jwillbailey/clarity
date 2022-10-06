!#/bin/bash

TRAIN=/shared/spandh_bessemer/Shared/data/clarity/clarity_CEC2_data_zt/clarity_CEC2_data/clarity_data/train/reset_hr_files

DEV=/shared/spandh_bessemer/Shared/data/clarity/clarity_CEC2_data_zt/clarity_CEC2_data/clarity_data/dev/reset_hr_files

EVAL=/shared/spandh_bessemer/Shared/data/clarity/clarity_CEC2_data_zt/clarity_CEC2_data/clarity_data/eval/reset_hr_files

scp ac1wb@bessemer.sheffield.ac.uk:$TRAIN/S05946_hr.wav ./files/
scp ac1wb@bessemer.sheffield.ac.uk:$TRAIN/S05924_hr.wav ./files/
scp ac1wb@bessemer.sheffield.ac.uk:$TRAIN/S00849_hr.wav ./files/


scp ac1wb@bessemer.sheffield.ac.uk:$DEV/S06470_hr.wav ./files/
scp ac1wb@bessemer.sheffield.ac.uk:$DEV/S06206_hr.wav ./files/
scp ac1wb@bessemer.sheffield.ac.uk:$DEV/S06476_hr.wav ./files/
scp ac1wb@bessemer.sheffield.ac.uk:$DEV/S07264_hr.wav ./files/
scp ac1wb@bessemer.sheffield.ac.uk:$DEV/S07237_hr.wav ./files/
scp ac1wb@bessemer.sheffield.ac.uk:$DEV/S06464_hr.wav ./files/
scp ac1wb@bessemer.sheffield.ac.uk:$DEV/S06209_hr.wav ./files/

scp ac1wb@bessemer.sheffield.ac.uk:$EVAL/S08618_hr.wav ./files/
scp ac1wb@bessemer.sheffield.ac.uk:$EVAL/S09635_hr.wav ./files/
scp ac1wb@bessemer.sheffield.ac.uk:$EVAL/S08539_hr.wav  ./files/
