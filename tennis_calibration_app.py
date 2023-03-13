import glob
from venv import create
import cv2
import numpy as np
from module import utils
import argparse
import json

class TennisCalibrationApp:
    def __init__(self,dir_path, output_cali_param_path):
        self.dir_path = dir_path
        self.output_cali_param_path = output_cali_param_path
        self.calibration_parameter_info = {'dir_path':dir_path}

        # mouse control 
        self.mouse_xy = None
        self.clicked = False

        self.court_2d, self.court_pts = self.create_reference_court_2d()
        self.excute()
        
        
    def create_reference_court_2d(self):
        court_2d_path = 'assert/2d_tennis_court.png'
        self.calibration_parameter_info['court_2d_path'] = court_2d_path

        court_2d = cv2.imread(court_2d_path)
        p0 = [419,385]
        p1 = [419,338]
        p2 = [419,192]
        p3 = [419,47]
        p4 = [419,2]
        p5 = [645,338]
        p6 = [645,192]
        p7 = [645,47]
        p8 = [835,385]
        p9 = [835,338]
        p10 = [835,192]
        p11 = [835,47]
        p12 = [835,2]

        court_pts = [p0,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12]
        for pt_idx,pt in enumerate(court_pts):
            diff_x,diff_y = 0,0
            if pt_idx in [0,1,2,3,4,5,6,7]:
                diff_x = 10
            
            if pt_idx in [8,9]:
                diff_x = -55
            
            if pt_idx in [10,11,12]:
                diff_x = -70

            if pt_idx in [2,6,10]:
                diff_y = 6
            
            if pt_idx in [1,5,9]:
                diff_y = -5
            
            if pt_idx in [3,7,11]:
                diff_y = 17

            if pt_idx in [0,8]:
                diff_y = -8

            if pt_idx in [4,12]:
                diff_y = 20

            cv2.circle(court_2d,tuple(pt),10,(0,100,255),-1)
            cv2.putText(court_2d,'pt'+str(pt_idx),(pt[0]+diff_x,pt[1]+diff_y),cv2.FONT_HERSHEY_SIMPLEX, 0.8, (10, 10, 10), 2, cv2.LINE_AA)
        
        return court_2d,court_pts

    def _draw_circle(self,event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.mouse_xy = (x,y)
            self.clicked = True

    def excute(self):
        image_path = sorted(glob.glob(self.dir_path+'/*'))[0]
        _, img = utils.convert_to_imgArray(image_path)

        matched_coords = [None]*13
        current_img = img.copy()
        is_good_to_saved_param = False

        count = 0
        while True:
            if count == len(self.court_pts):
                is_good_to_saved_param = True
                break
            
            show_img = current_img.copy()
            
            if self.clicked:
                cv2.circle(show_img,self.mouse_xy,3,(0,164,255),-1)

            cv2.putText(show_img,'Is p{} matched to {}? [Y/n]'.format(count,str(self.mouse_xy)),(10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 2, cv2.LINE_AA)
            cv2.namedWindow('demo')
            cv2.setMouseCallback('demo',self._draw_circle)
            cv2.imshow('demo',show_img)

            cv2.namedWindow('2d_court',cv2.WINDOW_NORMAL)
            cv2.imshow('2d_court',self.court_2d)


            k = cv2.waitKey(20) & 0xFF
            if k == 27:
                break
        
            
            if k == ord('y'):
                matched_coords[count] = self.mouse_xy
                count+=1
                self.mouse_xy = None
                self.clicked = False

                for ii,v in enumerate(matched_coords):
                    if v is not None:
                        current_img = cv2.circle(img,v,3,(255,0,0),-1)
                        cv2.putText(current_img,str(ii),v, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 2, cv2.LINE_AA)
            
            if self.clicked and k == ord('n'):
                self.mouse_xy = None
                self.clicked = False

        if is_good_to_saved_param:
            dst = []
            src = []
            for i,pt in enumerate(self.court_pts):
                print ('p{} -> {}'.format(i,str(matched_coords[i])))
                if matched_coords[i] is not None:
                    dst.append(pt)
                    src.append(matched_coords[i])
            print ('\n')
                    
            self.calibration_parameter_info['dst'] = dst
            self.calibration_parameter_info['src'] = src

            # save calibration parameter
            json_obj = json.dumps(self.calibration_parameter_info, indent=4)
            with open(self.output_cali_param_path,'w') as outfile:
                outfile.write(json_obj)

            print ('Tennis court parameters is saved to:',self.output_cali_param_path)
        else:
            print ('Faild to create the calibration parameter file.')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--image_dir', help='input image path', type=str, default='dataset/cam_1_20220920_153428')
    parser.add_argument('-o', '--output_path', help='output court parameter path', type=str, default='court_parameters.json')
    args = parser.parse_args()

    print ('Loading frame_dir:',args.image_dir)
    app = TennisCalibrationApp(args.image_dir,args.output_path)