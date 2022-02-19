#TG:ChauhanMahesh/DroneBots
#Github.com/vasusen-code

import asyncio
import time
import subprocess
import re
import os
from datetime import datetime as dt
from .. import Drone, BOT_UN, LOG_CHANNEL
from telethon import events
from ethon.telefunc import fast_download, fast_upload
from ethon.pyfunc import video_metadata
from LOCAL.localisation import SUPPORT_LINK, JPG, JPG2, JPG3
from LOCAL.utils import ffmpeg_progress
from telethon.errors.rpcerrorlist import MessageNotModifiedError
from telethon.tl.types import DocumentAttributeVideo
from main.plugins.actions import LOG_START, LOG_END

async def compress(event, msg):
    Drone = event.client
    edit = await Drone.send_message(event.chat_id, "Process boshlandi", reply_to=msg.id)
    new_name = "out_" + dt.now().isoformat("_", "seconds")
    if hasattr(msg.media, "document"):
        file = msg.media.document
    else:
        file = msg.media
    mime = msg.file.mime_type
    if 'mp4' in mime:
        n = "media_" + dt.now().isoformat("_", "seconds") + ".mp4"
        out = new_name + ".mp4"
    elif msg.video:
        n = "media_" + dt.now().isoformat("_", "seconds") + ".mp4"
        out = new_name + ".mp4"
    elif 'x-matroska' in mime:
        n = "media_" + dt.now().isoformat("_", "seconds") + ".mkv" 
        out = new_name + ".mp4"            
    elif 'webm' in mime:
        n = "media_" + dt.now().isoformat("_", "seconds") + ".webm" 
        out = new_name + ".mp4"
    else:
        n = msg.file.name
        ext = (n.split("."))[1]
        out = new_name + ext
    DT = time.time()
    log = await LOG_START(event, f'**Siqish boshlandi**\n\nBot navbat bilan ishlaydi')
    log_end_text = f'**Siqish yakunlandi**\n\nBot hozirda tekin'
    try:
        await fast_download(n, file, Drone, edit, DT, "**Yuklanmoqda:**")
    except Exception as e:
        os.rmdir("compressmedia")
        await log.delete()
        await LOG_END(event, log_end_text)
        print(e)
        return await edit.edit(f"Yuklashda xatolik!\n\nMurojat: [ADMIN]({SUPPORT_LINK})", link_preview=False) 
    name = '__' + dt.now().isoformat("_", "seconds") + ".mp4"
    os.rename(n, name)
    FT = time.time()
    progress = f"progress-{FT}.txt"
    cmd = f'ffmpeg -hide_banner -loglevel quiet -progress {progress} -i """{name}""" -preset ultrafast -vcodec libx265 -crf 28 -acodec copy """{out}""" -y'
    try:
        await ffmpeg_progress(cmd, name, progress, FT, edit, '**Siqilmoqda:**')
    except Exception as e:
        await log.delete()
        await LOG_END(event, log_end_text)
        os.rmdir("compressmedia")
        print(e)
        return await edit.edit(f"Qandaydir xatolik!\n\nMurojat: [ADMIN]({SUPPORT_LINK})", link_preview=False)  
    out2 = dt.now().isoformat("_", "seconds") + ".mp4" 
    if msg.file.name:
        out2 = msg.file.name
    else:
        out2 = dt.now().isoformat("_", "seconds") + ".mp4" 
    os.rename(out, out2)
    i_size = os.path.getsize(name)
    f_size = os.path.getsize(out2)     
    text = f'**Siqildi**: @{BOT_UN} da\n\nSiqishdan oldin: `{i_size/1000000}` mb\nSiqishdan keyin: `{f_size/1000000}` mb'
    UT = time.time()
    if 'x-matroska' in mime:
        try:
            uploader = await fast_upload(f'{out2}', f'{out2}', UT, Drone, edit, '**Yuborilmoqda:**')
            await Drone.send_file(event.chat_id, uploader, caption=text, thumb=JPG, force_document=True)
        except Exception as e:
            await log.delete()
            await LOG_END(event, log_end_text)
            os.rmdir("compressmedia")
            print(e)
            return await edit.edit(f"Yuborishda xatolik!\n\nMurojat: [ADMIN]({SUPPORT_LINK})", link_preview=False)
    elif 'webm' in mime:
        try:
            uploader = await fast_upload(f'{out2}', f'{out2}', UT, Drone, edit, '**Yuborilmoqda:**')
            await Drone.send_file(event.chat_id, uploader, caption=text, thumb=JPG, force_document=True)
        except Exception as e:
            await log.delete()
            await LOG_END(event, log_end_text)
            os.rmdir("compressmedia")
            print(e)
            return await edit.edit(f"Yuborishda xatolik!\n\nMurojat: [ADMIN]({SUPPORT_LINK})", link_preview=False)
    else:
        metadata = video_metadata(out2)
        width = metadata["width"]
        height = metadata["height"]
        duration = metadata["duration"]
        attributes = [DocumentAttributeVideo(duration=duration, w=width, h=height, supports_streaming=True)]
        try:
            uploader = await fast_upload(f'{out2}', f'{out2}', UT, Drone, edit, '**Yuborilmoqda:**')
            await Drone.send_file(event.chat_id, uploader, caption=text, thumb=JPG3, attributes=attributes, force_document=False)
        except Exception:
            try:
                uploader = await fast_upload(f'{out2}', f'{out2}', UT, Drone, edit, '**Yuborilmoqda:**')
                await Drone.send_file(event.chat_id, uploader, caption=text, thumb=JPG, force_document=True)
            except Exception as e:
                await log.delete()
                await LOG_END(event, log_end_text)
                os.rmdir("compressmedia")
                print(e)
                return await edit.edit(f"Yuborishda xatolik!\n\nMurojat: [ADMIN]({SUPPORT_LINK})", link_preview=False)
    await edit.delete()
    os.remove(name)
    os.remove(out2)
    await log.delete()
    log_end_text2 = f'**Process yakunlandi**\n\nKetgan vaqt: {round((time.time()-DT)/60)} minut\nOldingi hajm: {i_size/1000000}mb.\nKeyingi hajm: {f_size/1000000}mb.\n\nBot hozircha tekin'
    await LOG_END(event, log_end_text2)
    


