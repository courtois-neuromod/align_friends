# align_friends
Module to help align subtitles to audio using penn 2 forced aligner

**REQUIREMENTS** (see appendix for hints or more technical information)
try to do these in order  
- [ ] Download [Hidden Markov Model Toolkit (HTK)](https://htk.eng.cam.ac.uk/)
- [ ] conda install ffmpeg
- [ ] conda install swig
- [ ] pip install pocketsphinx
- [ ] pip install [Natural Language Toolkit (nltk)](https://pypi.org/project/nltk/)
- [ ] pip install [inflect](https://pypi.org/project/inflect/)
- [ ] pip install [unidecode](https://pypi.org/project/Unidecode/)

This was done on with
```sh
Distributor ID: Ubuntu
Description:    Ubuntu 18.04.2 LTS
Release:        18.04
Codename:       bionic
```

## how to use this?
**1.** Get the subtitles for an episode(s). I include examples from Season 2 in `subtitles\friends-season2\`. They should be in either following format extensions:  
  a)  **.srt** which is of the form
```
    1
    00:00:02,877 --> 00:00:04,294
    words words etc
    
    2
    00:00:04,407 --> 00:00:05,891
    words words etc
    words words etc
```    
   b)  **.sub** which is of the form  
```
    {1}{45}words words etc
    {48}{55}words words etc
```
   
**2.** Get the mp3/mkv/wav file for the episode(s). The Penn 2 Forced Aligner (p2fa) is expecting a certain input. Using 'ffmpeg' it is possible to convert the file:
  ``` python
import subprocess
import os
import sys

def convert_video_to_audio_ffmpeg(video_file, output_ext="wav"):
    """Converts video to audio directly using `ffmpeg` command
    with the help of subprocess module"""
    filename, ext = os.path.splitext(video_file)
    # 16 bit mono sampled 16000
    subprocess.call(["ffmpeg", "-y", "-i", video_file,"-acodec", "pcm_s16le", "-ac", "1", "-ar", "16000", f"{filename}.{output_ext}"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)

  ```  
  or using cmd line / terminal
  ```sh
  ffmpeg -i input.mp3 -acodec pcm_s16le -ac 1 -ar 16000 output.wav
  ```
    
**3.** Transform the subtitles into a json file that can be given to p2fa.  
  For ease of use:  
  ```sh
  python process_subtitles.py
  ```
  and all you have to modify is  
  a) choose the season `season = {x}` (assuming subtitles are stored in `subtitles/friends-season-{x}`)  
  b) run it twice for each episode for the first half ("a") and the second half ("b") `ending="a"`  
  c) add midpoint time / frame for each episode  `times = {1:"00:12:23", 2:"00:11:43", 3: 17068, 4: 16834}`  
    or  
    get the file in this format: **NOTE VERY IMPORTANT** if you have it as },\n] instead of }\n] at the end it will not work.
```json
    [
	  {
		  "speaker": "Narrator", 
		  "line": "What you guys don't understand is...  "
	  },
	  {
		  "speaker": "Narrator", 
		  "line": "...for us, kissing is as important as any part of it. "
	  }
  ]
```  
**4.** Now align the text to the audio! In my fork of p2fa-vislab `align.py` and `align_subtitles.py` are how to accomplish this feat.
```sh
cd p2fa-vislab  
python align.py {wav} {json} {outputfile}
```  
or 
```sh
cd p2fa-vislab  
python align_subtitles.py
```  
where  
 a) wav files were in `audios/s{s}/friends_s{s}e{stri}a.wav`  
 b) json files in `processed_subtitles/s{s}/s0{s}e{stri}a.json`  
 c) `aligned_output` folder exists
 
 ## Appendix
 Some Helpful Tips for Downloading HTK
 * When you **make** if you get the error `/usr/include/stdio.h:27:10: fatal error: bits/libc-header-start.h: No such file or directory #include <bits/libc-header-start.h>`  
  Do this: `sudo apt-get install gcc-multilib or sudo apt-get install g++-multilib` to install the missing 32 bit libraries per [this](https://stackoverflow.com/questions/54082459/fatal-error-bits-libc-header-start-h-no-such-file-or-directory-while-compili)  
* When you **make** if you get the error `"/usr/bin/ld: cannot find -lX11" error when installing htk`  
 Do this `sudo apt-get install libx11-dev`per [this](https://stackoverflow.com/questions/40451054/cant-install-htk-on-linux)  
* When you **make** if you get the error `"gnu/stubs-32.h: No such file or directory"`  
 Do one of these per [this](https://stackoverflow.com/questions/7412548/error-gnu-stubs-32-h-no-such-file-or-directory-while-compiling-nachos-source) (there is other systems in that answer)  
   * **UBUNTU** `sudo apt-get install libc6-dev-i386`
   * **CentOS 5.8** The package is `glibc-devel.i386`
   * **CentOS 6 /7** The package is `glibc-devel.i686`
   
 ## Why do we need those other python modules? 
 See my blog post [here](https://zacandcheese.github.io/research//personal/2022/03/10/pronounce.html)
