# video-inspector
Tool for comparison of different encodings and resolutions of a video.

## How to

### Prerequisites

1. Python 3
2. OpenCV for Python
    * `pip install opencv-python`
    * For more info check: https://pypi.org/project/opencv-python

### Run the tool

Run the tool from the command line specifying a project in JSON format. E.g.
```
python inspector.py -p my_project.json
```

It will load the videos specified in the project file. Then a Window will open up where you can navigate through the video. Some shortcuts (window has to be active):
* Press [A] or [D] key to switch between the different video files at the same frame.
* Press [W] or [S] key to zoom in/out of the frame.
* Press [E] key to go to the next frame.
* Press [Q] key to exit.

### Project file

*See `project.json` for a valid example file.*

A project file is a json file specifying:
* The starting frame number at which the tool will start. See `start`.
* The videos be inspected.
    * `path` file path to the videos.
    * `note` this text is shown in the inespector to identify the shown frame.
    * `offset` offset given in frames. Sometimes the videos are out of sync by 1 frame or so. Use this parameter to get them back in sync.

## TODO

* Cleaner text annotation
* Verify zoom procedure (interpolation method etc.)
* Switch between left and right eye image
