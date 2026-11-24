"""Copy the Blender stereo 360 renders into the VR app (JPEG) and write scenes/manifest.json.

Renders come from src/pvgen/landscape/blender_room.py (views pano_sit / pano_lie, job output/landscape/vr/render_job.json):
    output/landscape/vr/renders/<scene>_pano_<pose>_<L|R>.png   ->   vr_app/scenes/<scene>_<pose>_<L|R>.jpg

    python prepare_scenes.py            (run from patient_view/vr_app with the project venv)
"""
import json
import os

import cv2

HERE = os.path.dirname(os.path.abspath(__file__))
PV = os.path.dirname(HERE)
REN = os.path.join(PV, 'output', 'landscape', 'vr', 'renders')
OUT = os.path.join(HERE, 'scenes')
SCENES = [('original', 'Original room', 'Room'),
          ('B_golden_sunset', 'B · Golden sunset', 'B'),
          ('C_golden_cascade', 'C · Golden cascade', 'C'),
          ('D_poppies_alpenglow', 'D · Poppies, alpenglow', 'D'),
          ('E_valley_mist', 'E · Valley mist', 'E'),
          ('F_golden_sunstar', 'F · Sun star', 'F')]


def main():
    os.makedirs(OUT, exist_ok=True)
    man = {'poses': {'sit': 'Sitting up in bed', 'lie': 'Lying down (sleeping)'}, 'scenes': []}
    for sid, label, short in SCENES:
        poses = []
        for pose in ('sit', 'lie'):
            src = [os.path.join(REN, f'{sid}_pano_{pose}_{e}.png') for e in ('L', 'R')]
            if not all(os.path.exists(p) for p in src):
                continue
            for e, p in zip(('L', 'R'), src):
                dst = os.path.join(OUT, f'{sid}_{pose}_{e}.jpg')
                if not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(p):
                    cv2.imwrite(dst, cv2.imread(p), [cv2.IMWRITE_JPEG_QUALITY, 90])
            poses.append(pose)
        if poses:
            man['scenes'].append({'id': sid, 'label': label, 'short': short, 'poses': poses})
        print(f'{sid:22s} poses {poses}')
    json.dump(man, open(os.path.join(OUT, 'manifest.json'), 'w'), indent=1)
    print('manifest:', len(man['scenes']), 'scenes')


if __name__ == '__main__':
    main()
