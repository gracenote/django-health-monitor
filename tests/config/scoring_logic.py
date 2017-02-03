# ADD DEFINITIONS FOR SCORING LOGIC HERE
def heart(heartrate, arrhythmia):
    heartrate = int(heartrate)
    arrhythmia = int(arrhythmia)

    if arrhythmia:
        return 3
    elif heartrate > 80:
        return 2
    else:
        return 1
