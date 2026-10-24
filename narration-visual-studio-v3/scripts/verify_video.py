#!/usr/bin/env python3
"""Validate the delivery encoding against a normalized V3 subtitle interval."""
import argparse
import json
import subprocess
from fractions import Fraction
from pathlib import Path


def verify(video, duration, fps=25):
    data=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)]))
    streams=data['streams']; videos=[s for s in streams if s['codec_type']=='video']
    errors=[]
    if len(videos)!=1: errors.append('Expected one video stream')
    else:
        stream=videos[0]
        if stream['codec_name']!='h264': errors.append('Expected H.264')
        if (stream['width'],stream['height'])!=(1920,1080): errors.append('Expected 1920x1080')
        if Fraction(stream['avg_frame_rate'])!=fps: errors.append('Unexpected frame rate')
        if abs(float(data['format']['duration'])-duration)>1/fps+1e-6: errors.append('Duration differs by more than one frame')
    if any(s['codec_type']=='audio' for s in streams): errors.append('Unexpected audio track')
    return {'ok':not errors,'errors':errors,'expected_duration':duration,'actual_duration':float(data['format']['duration']),'size':int(data['format']['size']),'video':videos[0] if videos else None,'audio_tracks':sum(s['codec_type']=='audio' for s in streams)}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('video',type=Path);p.add_argument('--input',required=True,type=Path);p.add_argument('--out',type=Path);a=p.parse_args()
    r=verify(a.video,json.loads(a.input.read_text())['duration']);s=json.dumps(r,ensure_ascii=False,indent=2)
    if a.out:a.out.write_text(s,encoding='utf-8')
    print(s);raise SystemExit(not r['ok'])
