from module import utils
from module.tennis_tracking_side import TennisTrackingSide

import glob
import os
import time
import argparse

class TennisTrackerApp:
    def __init__(self,cali_param,frame_dir=None,showInfo=False,saveVideo=False):
        self.cfg = utils.read_json(cali_param)
        if frame_dir is not None:
            self.cfg['dir_path'] = frame_dir
        
        print ('- Calibration parameters info:')
        for c_info,c_value in self.cfg.items():
            print ('    [{}]: {}'.format(c_info,c_value))

        output_path = False
        if saveVideo is not False:
            if self.cfg['dir_path'][-1] == '/':
                output_path = os.path.basename(self.cfg['dir_path'][:-1])+'.avi'
            else:
                output_path = os.path.basename(self.cfg['dir_path'])+'.avi'
            print ('- Demo video is saved to:', output_path, '\n')

        self.tts = TennisTrackingSide(self.cfg,isShowInfo=showInfo,saveVideo=output_path)
        self.excute()

    def excute(self): 
        files_path = os.path.join(self.cfg['dir_path'],'*')
        files = sorted(glob.glob(files_path))
        st = time.time()

        for f_idx,f in enumerate(files):
            utils.loading_bar(f,f_idx,len(files))
            self.tts.recvive(f)

        print ('\n-Total cost time:',round(time.time()-st,2),'(sec)')
        bounced_info = self.tts.bounced_balls_2d
        print ('\n-Find {} bounced balls'.format(len(bounced_info)))
        if len(bounced_info) > 0:
            print ('    idx | (bounced_2d_court_xy), (bounced_xy), file_time_name')
            for i in range(len(bounced_info)):
                print ('    {} | {}'.format(i,bounced_info[i]))
            


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--cali_param', help='input court calibration parameter path.', type=str, default='./assert/court_left_parameters.json')
    parser.add_argument('-d', '--dir_frame', help='input frame dir path.', type=str, default=None)
    parser.add_argument('-s', '--show', help='set to show demo info', action='store_true')
    parser.add_argument('-sv','--save_video', help='save demo video to ./tennis_detect.result.avi ', action='store_true')

    args = parser.parse_args()

    TennisTrackerApp(args.cali_param, frame_dir=args.dir_frame, showInfo=args.show, saveVideo=args.save_video)
