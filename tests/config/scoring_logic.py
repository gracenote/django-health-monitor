# ADD DEFINITIONS FOR SCORING LOGIC HERE
def health_score_bis_connection(bis_status_lv, bis_status_sac, bis_status_sc):
    bis_connected = []
    if bis_status_lv == 'OK':
        bis_connected.append(bis_status_lv)
    if bis_status_sac == 'OK':
        bis_connected.append(bis_status_sac)
    if bis_status_sc == 'OK':
        bis_connected.append(bis_status_sc)
    count = len(bis_connected)
    if count == 3:
        return 1
    elif count == 2:
        return 2
    elif count == 1:
        return 3
    elif count == 0:
        return 4
    else:
        return None


def health_score_bis_package_per_second(fp_package_lv, fp_package_sac, fp_package_sc):
    packages = []
    packages.append(float(fp_package_lv))
    packages.append(float(fp_package_sc))
    packages.append(float(fp_package_sac))
    packages.sort()
    lowest_value = packages[0]
    mid_value = packages[1]
    highest_value = packages[2]
    if highest_value < 2:
        return 4
    elif mid_value < 2:
        return 3
    elif lowest_value < 2:
        return 2
    elif 2 <= lowest_value:
        return 1
    else:
        return None


def health_score_bis_queue(submit_queue_lv, submit_queue_sac, submit_queue_sc):
    try:
        submit_queue_lv = int(submit_queue_lv)
    except Exception:
        submit_queue_lv = 0
    try:
        submit_queue_sac = int(submit_queue_sac)
    except Exception:
        submit_queue_sac = 0
    try:
        submit_queue_sc = int(submit_queue_sc)
    except Exception:
        submit_queue_sc = 0

    queues = []

    queues.append(submit_queue_lv)
    queues.append(submit_queue_sc)
    queues.append(submit_queue_sac)
    queues.sort()
    highest_value = queues[-1]
    if highest_value > 500:
        return 3
    elif 500 >= highest_value > 100:
        return 2
    elif 100 >= highest_value >= 0:
        return 1
    else:
        return None


def health_score_datarate(datarate):
    datarate = int(datarate)
    if datarate < 50:
        return 4
    elif 50 <= datarate < 80:
        return 3
    elif 80 <= datarate < 90:
        return 2
    elif 90 <= datarate:
        return 1
    else:
        return None


def health_score_directv_match(match_status):
    match_status = int(match_status)
    if not match_status:
        return 3
    else:
        return 1


def health_score_fingerprint_rate(sc_fingerprint_rate, lv_fingerprint_rate, sac_fingerprint_rate):
    def float_it(value):
        try:
            fval = float(value)
            return fval
        except Exception:
            return 0.0

    red_list = []

    fp_rates = []
    fp_rates.append(float_it(sc_fingerprint_rate))
    fp_rates.append(float_it(lv_fingerprint_rate))
    fp_rates.append(float_it(sac_fingerprint_rate))

    if not IS_DEV_FABRIC():
        for rate in fp_rates:
            if rate < 70:
                red_list.append(rate)
        bad_rate_count = len(red_list)
        if bad_rate_count == 3:
            return 4
        elif bad_rate_count == 2:
            return 3
        elif bad_rate_count == 1:
            return 2
        elif bad_rate_count == 0:
            return 1
        else:
            return None
    else:
        if lv_fingerprint_rate < 50:
            return 4
        elif 50 <= lv_fingerprint_rate < 70:
            return 3
        elif 70 <= lv_fingerprint_rate < 80:
            return 2
        elif 80 <= lv_fingerprint_rate:
            return 1
        else:
            return None


def health_score_harvest_fingerprint_rate(harvest_fingerprint_rate):
    def float_it(value):
        try:
            fval = float(value)
            return fval
        except Exception:
            return 0.0

    harvest_fingerprint_rate = float_it(harvest_fingerprint_rate)

    if harvest_fingerprint_rate < 70:
        return 2
    else:
        return 1


def health_score_hive_production_audio_match(matches):
    matches = int(matches)

    if matches <= 1:
        return 4
    else:
        return 1


def health_score_mp3_submit(mp3_present):
    mp3_present = int(mp3_present)
    if mp3_present == 0:
        return 2
    elif mp3_present == 1:
        return 1
    else:
        return None


# def health_score_subscribed(tui, live_tier, shift_tier):
#     tui = int(tui)
#     live_tier = int(live_tier)
#     shift_tier = int(shift_tier)
#     channel = Channel.objects.get(tui=tui)
#     # While the data source now uses 'yes'/'no', when it switches to booleans, update our healthy check.
#
#     def convert_yes_no(value):
#         if str(value).lower() == 'no':
#             return False
#         elif str(value).lower() == 'yes':
#             return True
#         else:
#             return value
#
#     # if not channel:
#     #     return None
#
#     live_tier = convert_yes_no(live_tier)
#     shift_tier = convert_yes_no(shift_tier)
#     if channel.subscribed_live == live_tier and channel.subscribed_shift == shift_tier:
#         return 1
#     elif channel.subscribed_live and not live_tier:  # Not subscribed to live!!
#         return 4
#     elif not channel.subscribed_shift and shift_tier:  # Over subscribed
#         return 2
#     else:
#         return 4


def health_score_volume(volume):
    volume = int(volume)
    if volume == 0:
        return 4
    elif volume < -70:
        return 3
    elif -70 <= volume < -50:
        return 2
    elif -50 <= volume <= -1:
        return 1
    else:
        return None


def health_score_mp3_match(match_status):
    match_status = int(match_status)
    if match_status:
        return 1
    elif not match_status:
        return 3
    else:
        return None


def health_score_for_mp3_matches(list_of_matches):
    # Expects the list to be ordered oldest->newest
    fail_count = []
    for match in list_of_matches:
        if match == 3:
            fail_count.append(match)
    if len(fail_count) == len(list_of_matches):
        # All matches were failures
        return 3
    elif list_of_matches[-1] == 3:
        # Latest failed but not every one was a failures
        return 2
    else:
        return 1


def health_score_epg_gap(gap_count):
    gap_count = int(gap_count)
    if gap_count > 0:
        return 2
    elif gap_count == 0:
        return None
    else:
        return None


def health_score_epg_overlap(overlap_count):
    overlap_count = int(overlap_count)
    if overlap_count > 0:
        return 2
    elif overlap_count == 0:
        return None
    else:
        return None


def health_score_eam_api_match(api_match, ens_status):
    api_match = int(api_match)
    ens_status = str(ens_status)

    if ens_status == 'inactive' or api_match:
        return 1
    else:
        return 4


def health_score_eam_api_status(ens_status, status, use):
    use = int(use)

    if ens_status.lower() == 'active':
        if use:
            if status == 'ON':
                return 1
            else:
                return 3
        else:
            return 4
    elif ens_status.lower() == 'inactive':
        if use:
            if status == 'ON':
                return 3
            elif status == 'UNKNOWN':
                return 2
            else:
                return 1
        else:
            if status == 'ON':
                return 3
            else:
                return 1
    else:
        return 1


def health_score_vm_ping(ping):
    ping = int(ping)
    if ping:
        return 1
    else:
        return 4


def health_score_vm_cpu(cpu):
    if not cpu or str(cpu) == 'None':
        return None

    cpu = float(cpu)

    if cpu >= 0.70:
        return 4
    elif cpu >= 0.65:
        return 3
    else:
        return 1


def health_score_ec_status_audio(audio):
    audio = str(audio)

    if 'NOT READY YET' == audio or 'NO PROCESS' == audio or 'DECODING_FAILED' == audio:
        return 4
    elif 'STOPPED' == audio:
        return 3
    elif 'NOT UPDATED' == audio or 'NOT_UPDATED' == audio or 'SKIPPING' == audio:
        return 2
    elif 'DECODING' == audio:
        return 1
    else:
        return 0


def health_score_ec_status_video(video):
    video = str(video)

    if 'NOT READY YET' == video or 'NO PROCESS' == video or 'DECODING_FAILED' == video:
        return 4
    elif 'STOPPED' == video:
        return 3
    elif 'NOT UPDATED' == video or 'NOT_UPDATED' == video or 'SKIPPING' == video:
        return 2
    elif 'DECODING' == video:
        return 1
    else:
        return 0


def health_score_ec_status_network(network):
    network = str(network)

    if network == 'BAD' or network == 'NOT READY YET':
        return 4
    elif network == 'GOOD':
        return 1
    else:
        return 0


def health_score_ec_status_qsize(qsize):
    qsize = int(qsize)

    if qsize > 15000:
        return 4
    elif qsize > 7000 and qsize <= 15000:
        return 3
    else:
        return 1


def health_score_ec_status_v_delay(v_delay):
    v_delay = float(v_delay)

    if v_delay >= 9999:
        return 3
    else:
        return 1


def health_score_ec_status_v_fps(v_fps):
    v_fps = float(v_fps)

    if v_fps < 5 or v_fps >= 9999:
        return 4
    elif v_fps >= 5 and v_fps < 7:
        return 3
    elif v_fps >= 7 and v_fps < 8:
        return 2
    elif v_fps >= 8:
        return 1
    else:
        return 0


def health_score_stream_id_gracenote(gracenote_exist):
    gracenote_exist = int(gracenote_exist)

    if gracenote_exist:
        return 1
    else:
        return 4


def health_score_stream_id_gracenote_kr(enswers_match):
    enswers_match = int(enswers_match)

    if enswers_match:
        return 1
    else:
        return 4


def health_score_stream_id_samsung(samsung_exist):
    samsung_exist = int(samsung_exist)

    if samsung_exist:
        return 1
    else:
        return 4


def health_score_vm_disk_free_percent(disk_free_percent):
    disk_free_percent = float(disk_free_percent)
    if disk_free_percent < 5:
        return 4
    elif disk_free_percent < 10:
        return 3
    elif 10 <= disk_free_percent <= 100:
        return 1
    else:
        return None


def health_score_feature_proxy_delay(delay):
    try:
        if delay == 'None' or delay is None:
            return 4
    except Exception:
        pass

    delay = int(delay)
    if delay > 600:
        return 4
    elif delay > 2:
        return 3
    else:
        return 1
