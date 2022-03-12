import cv2
import numpy as np
import moviepy.editor as mp


def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def rgb_to_hex(red, green, blue):
    return '%02x%02x%02x' % (red, green, blue)


# width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

mapAddLog = []
VIDEO_FPS = 30 
FRAME_SPLIT = 14 # ex)(30 / 14) frame/s, must be even
FOLDER_LINK = 'C:\\Users\\Mitama\\Desktop\\'

vidCap = cv2.VideoCapture(FOLDER_LINK + 'video.mp4')

print(int(vidCap.get(cv2.CAP_PROP_FRAME_HEIGHT)), '*', int(vidCap.get(cv2.CAP_PROP_FRAME_WIDTH)), 'video file')

HEIGHT = 150 #int(input("Enter the video height value: "))
WIDTH = 200 #int(input("Enter the video width value: "))

#clip = mp.VideoFileClip(FOLDER_LINK + "Video.mp4")
#clip.audio.write_audiofile(FOLDER_LINK + "Audio.mp3")

mapFileLog = '''{
	"pathData": "PATH_DATA", 
	"settings":
	{
		"version": 1, 
		"artist": "", 
		"specialArtistType": "None", 
		"artistPermission": "", 
		"song": "", 
		"author": "Mitama's ADOFAI Video Printer", 
		"separateCountdownTime": "Enabled", 
		"previewImage": "", 
		"previewIcon": "", 
		"previewIconColor": "003f52", 
		"previewSongStart": 0, 
		"previewSongDuration": 10, 
		"seizureWarning": "Disabled", 
		"levelDesc": "", 
		"levelTags": "", 
		"artistLinks": "", 
		"difficulty": 1, ,
		"songFilename": "SONG_LINK", 
		"bpm": MAP_BPM, 
		"volume": 100, 
		"offset": 0, 
		"pitch": 100, 
		"hitsound": "Kick", 
		"hitsoundVolume": 0, 
		"countdownTicks": 0,
		"trackColorType": "Single", 
		"trackColor": "debb7b", 
		"secondaryTrackColor": "ffffff", 
		"trackColorAnimDuration": 2, 
		"trackColorPulse": "None", 
		"trackPulseLength": 10, 
		"trackStyle": "Standard", 
		"trackAnimation": "None", 
		"beatsAhead": 3, 
		"trackDisappearAnimation": "None", 
		"beatsBehind": 4,
		"backgroundColor": "000000", 
		"bgImage": "", 
		"bgImageColor": "ffffff", 
		"parallax": [100, 100], 
		"bgDisplayMode": "FitToScreen", 
		"lockRot": "Disabled", 
		"loopBG": "Disabled", 
		"unscaledSize": 100,
		"relativeTo": "Tile", 
		"position": [0, CMR_Y], 
		"rotation": 0, 
		"zoom": CMR_ZOOM,
		"bgVideo": "", 
		"loopVideo": "Disabled", 
		"vidOffset": 0, 
		"floorIconOutlines": "Disabled", 
		"stickToFloors": "Disabled", 
		"planetEase": "Linear", 
		"showDefaultBGIfNoImage": "Disabled",
		"planetEaseParts": 1
	},
	"actions":
	[        
'''

txtAddSheet = '''{ "floor": 1, "eventType": "AddText", "decText": "TXT", "font": "Default", "position": [0, 0], "relativeTo": "Tile", "pivotOffset": [0, POS_Y], "rotation": 0, "scale": [100, 100], "color": "ffffff", "opacity": 100, "depth": -1, "parallax": [100, 100], "tag": "TAG" },
'''
txtChangeSheet = '''{ "floor": 1, "eventType": "SetText", "decText": "TXT", "tag": "TAG", "angleOffset": TILE_ANGLE, "eventTag": "" }
'''

mapFileLog = mapFileLog.replace("PATH_DATA", 'R' * 10).replace('CMR_Y', str(10000)).replace('MAP_BPM', '0.01').replace('SONG_LINK', 'Audio.mp3').replace('CMR_ZOOM', str(HEIGHT * 8))

frameNum = int(vidCap.get(cv2.CAP_PROP_FRAME_COUNT)) / FRAME_SPLIT

mapFile = open(FOLDER_LINK + 'Map1.adofai', 'w', encoding='utf-8')
mapFile.write(mapFileLog)

beforeLineList = []
for i in range(HEIGHT):
    beforeLineList.append('')
    mapFile.write(txtAddSheet.replace('TXT', '□' * WIDTH).replace('POS_Y', str((HEIGHT / 4 - (i / 2)) * 1.05 - 0.25)).replace('TAG', str(i)))

angle = 0
frameCount = 0
LineTXT = ''

while vidCap.isOpened() and vidCap.grab():

    ret, image = vidCap.read()

    if int(vidCap.get(1)) % FRAME_SPLIT == 0 and image is not None:
        image = cv2.resize(image, (WIDTH, HEIGHT))
        pixel = np.array(image)
        for i in range(HEIGHT):

            for j in range(WIDTH):

                if (pixel[i][j][2] + pixel[i][j][1] + pixel[i][j][0]) / 3 >= 50:
                    LineTXT += '■'
                else:
                    LineTXT += '□'

            if not beforeLineList[i] == LineTXT:
                mapFile.write(txtChangeSheet.replace('TILE_ANGLE', str(angle)).replace('TAG', str(i)).replace('TXT', LineTXT))
            beforeLineList[i] = LineTXT
            LineTXT = ''

        print(str(frameCount) + 'th frame done')
        angle += ((1 / (VIDEO_FPS / FRAME_SPLIT)) / 100) * 3

        frameCount += 1
        tileNum = 2


vidCap.release()

mapFile.write(''']
}''')
mapFile.close()

print("Map.adofai file has been created.")

