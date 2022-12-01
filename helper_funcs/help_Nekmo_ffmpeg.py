#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# the logging things
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
import time
import os
import asyncio
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def place_water_mark(input_file, output_file, water_mark_file):
    watermarked_file = output_file + ".watermark.png"
    metadata = extractMetadata(createParser(input_file))
    width = metadata.get("width")
    # https://stackoverflow.com/a/34547184/4723940
    shrink_watermark_file_genertor_command = [
        "ffmpeg",
        "-i", water_mark_file,
        "-y -v quiet",
        "-vf",
        "scale={}*0.5:-1".format(width),
        watermarked_file
    ]
    # print(shrink_watermark_file_genertor_command)
    process = await asyncio.create_subprocess_exec(
        *shrink_watermark_file_genertor_command,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    commands_to_execute = [
        "ffmpeg",
        "-i", input_file,
        "-i", watermarked_file,
        "-filter_complex",
        # https://stackoverflow.com/a/16235519
        # "\"[0:0] scale=400:225 [wm]; [wm][1:0] overlay=305:0 [out]\"",
        # "-map \"[out]\" -b:v 896k -r 20 -an ",
        "\"overlay=(main_w-overlay_w):(main_h-overlay_h)\"",
        # "-vf \"drawtext=text='@FFMovingPictureExpertGroupBOT':x=W-(W/2):y=H-(H/2):fontfile=" + Config.FONT_FILE + ":fontsize=12:fontcolor=white:shadowcolor=black:shadowx=5:shadowy=5\"",
        output_file
    ]
    # print(commands_to_execute)
    process = await asyncio.create_subprocess_exec(
        *commands_to_execute,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    return output_file
