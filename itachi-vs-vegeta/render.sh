#!/bin/bash
# Assembles clips (timed to the voiceover), captions and audio into final.mp4
set -e
cut() { # clip target_duration out
  local f=$(python3 -c "print(max(1.0, $2/5.04))")
  ffmpeg -v error -y -i $1.mp4 -vf "setpts=$f*PTS,scale=w='trunc(1100*(1+0.10*t/$2)/2)*2':h=-2:eval=frame,crop=1080:1920,fps=30,format=yuv420p,trim=0:$2,setpts=PTS-STARTPTS" -an -c:v libx264 -preset fast -crf 18 seg_$1.mp4
}
cut c1 8.62; cut c2 3.43; cut c3 6.58; cut c4 4.55; cut c5 5.13; cut c6 6.62; cut c7 9.07
printf "file 'seg_%s.mp4'\n" c1 c2 c3 c4 c5 c6 c7 > list.txt
ffmpeg -v error -y -f concat -i list.txt -i vo.mp3 -vf "ass=captions.ass" -map 0:v -map 1:a -c:v libx264 -preset medium -crf 20 -c:a aac -b:a 192k -af apad -t 44 -movflags +faststart Itachi_vs_Vegeta.mp4
rm seg_*.mp4 list.txt
