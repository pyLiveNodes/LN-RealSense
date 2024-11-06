[![Format and Test](https://github.com/pyLiveNodes/LN-RealSense/actions/workflows/format_test.yml/badge.svg)](https://github.com/pyLiveNodes/LN-RealSense/actions/workflows/format_test.yml)
[![Publish](https://github.com/pyLiveNodes/LN-RealSense/actions/workflows/publish.yml/badge.svg)](https://github.com/pyLiveNodes/LN-RealSense/actions/workflows/publish.yml)

# Livenodes RealSense

Livenodes Package to interface the intel realsense cameras, namely the d435.

IMPORTANT: Requires installed librealsense and ffmpeg.

The package provides both interfaces for raw depth recording and colorized depth recording.
However, the focus lies on the latter one. The package roughly provides these nodes:
- RealSense input Node: connects to a realsense and forwards single images
- Out Node: takes an image stream and saves it to .avi either lossless or lossy compressed
- In Node: read .avi files and forward single images
- Playback Node: read .avi files and forward single images in the correct fps
- Draw Node: takes an image stream and draws them one after the other on a qt canvas

## Next Steps
- Consider implementing nodes such that they may receive and send batched images? 
    -> this might provide some performance gains, especially if added with specific video livenodes.bridges that utilize temporary compression over network
- Consider adding interfaces/converters to popular image/video processing libraries
- Consider adding interfaces/converters to ml applications


## Prerequisits: librealsense
Ubuntu:
- Install Intel RealSense SDK 2.0 (https://github.com/IntelRealSense/librealsense/releases/tag/v2.50.0)
    - Note: while there might be an issue with the amazon server, the installation might very well work.
- Alternatively: - https://github.com/IntelRealSense/librealsense/blob/master/doc/distribution_linux.md


RPI Ubuntu:
- https://github.com/IntelRealSense/librealsense/blob/master/doc/installation.md
- Possibly also: https://dev.intelrealsense.com/docs/open-source-ethernet-networking-for-intel-realsense-depth-cameras?_ga=2.231554143.1532698096.1674553494-26816367.1674553494#section-2-3-preparing-the-sd-card
- Alternativ: clone the rpi ubunto focal 20.04 realsense image (TODO yh: upload image somewhere and write short guide)