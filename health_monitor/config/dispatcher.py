"""All parameters associated with tests should go into the dispatcher dictionary.

dispatcher[test_name] = name of tests
dispatcher[test_name]['method'] = name of scoring test in scoring_logic.py
dispatcher[test_name]['model'] = name of model that test results are written to
dispatcher[test_name]['monitoring_url'] = url to get to test results
dispatcher[test_name]['params'] = test result values to be passed to calculate score using scoring_logic.py
dispatcher[test_name]['subscriber'] = list of subscribers which this test is revelant for
dispatcher[test_name]['time'] = name of the column that time is recorded (cannot be used in conjunction with start_time, end_time)
dispatcher[test_name]['start_time'] = name of the column that the start time is recorded (must be used with end_time)
dispatcher[test_name]['end_time'] = name of the column that the end time is recorded (must be used with start_time)

Example:
    dispatcher = {
        'heartbeat': {
            'method': 'health_score_heartbeat',
            'model': 'Heartbeat',
            'monitoring_url': 'heartbeat',
            'params': {
                'heartrate': 'heartrate',
                'arrhythmia': 'arrhythmia',
            },
            'subscriber': ['doctor', ],
            'time': 'time',
        },
        'sleep': {
            'method': 'health_score_sleep',
            'model': 'Sleep',
            'monitoring_url': 'sleep',
            'params': {
                'quality': 'quality',
            },
            'subscriber': ['doctor', ],
            'start_time': 'start_time',
            'end_time': 'end_time',
        }
    }
"""


def get_dispatcher(original_dispatcher=False):
    dispatcher = {
        'bis_connection': {
            'method': 'health_score_bis_connection',
            'model': 'AcrServerStatus',
            'monitoring_url': 'bis_status',
            'params': {
                'bis_status_lv': 'bis_status_lv',
                'bis_status_sac': 'bis_status_sac',
                'bis_status_sc': 'bis_status_sc',
            },
            'subscriber': ['audio', ],
            'time': 'bis_status_time',
        },
        'bis_queue': {
            'method': 'health_score_bis_queue',
            'model': 'AcrServerStatus',
            'monitoring_url': 'bis_status',
            'params': {
                'submit_queue_lv': 'submit_queue_lv',
                'submit_queue_sac': 'submit_queue_sac',
                'submit_queue_sc': 'submit_queue_sc',
            },
            'subscriber': ['audio', ],
            'time': 'bis_status_time',
        },
        'datarate': {
            'method': 'health_score_datarate',
            'model': 'AcrChannelsStatus',
            'monitoring_url': 'datarate_and_volume',
            'params': {
                'datarate': 'datarate',
            },
            'subscriber': ['audio', ],
            'time': 'datarate_time',
        },
        'directv_match': {
            'method': 'health_score_directv_match',
            'model': 'DirectvFpMatch',
            'monitoring_url': 'directv_match',
            'params': {
                'match_status': 'match_status',
            },
            'subscriber': ['audio', ],
            'time': 'match_time',
        },
        'eam_api_match': {
            'description': 'TUI exists in EAM API',
            'method': 'health_score_eam_api_match',
            'model': 'EnswersEamApiValidation',
            'monitoring_url': 'eam_api_validation',
            'params': {
                'api_match': 'api_match',
                'ens_status': 'ens_status',
            },
            'subscriber': ['video', ],
            'time': 'time',
        },
        'eam_api_status': {
            'description': 'Running state in EAM API is as expected',
            'method': 'health_score_eam_api_status',
            'model': 'EnswersEamApiValidation',
            'monitoring_url': 'eam_api_validation',
            'params': {
                'ens_status': 'ens_status',
                'status': 'status',
                'use': 'use',
            },
            'subscriber': ['video', ],
            'time': 'time',
        },
        'ec_status_audio': {
            'description': 'Audio status in "service ec status" is as expected',
            'method': 'health_score_ec_status_audio',
            'model': 'EnswersChannelStatus',
            'monitoring_url': 'acr_video_channel_status',
            'params': {
                'audio': 'audio',
            },
            'subscriber': ['audio', 'video'],
            'time': 'status_time',
        },
        'ec_status_video': {
            'description': 'Video status in "service ec status" is as expected',
            'method': 'health_score_ec_status_video',
            'model': 'EnswersChannelStatus',
            'monitoring_url': 'acr_video_channel_status',
            'params': {
                'video': 'video',
            },
            'subscriber': ['video', ],
            'time': 'status_time',
        },
        'ec_status_network': {
            'description': 'Network status in "service ec status" is as expected',
            'method': 'health_score_ec_status_network',
            'model': 'EnswersChannelStatus',
            'monitoring_url': 'acr_video_channel_status',
            'params': {
                'network': 'network',
            },
            'subscriber': ['video', ],
            'time': 'status_time',
        },
        'ec_status_qsize': {
            'description': 'QSize status in "service ec status" is as expected',
            'method': 'health_score_ec_status_qsize',
            'model': 'EnswersChannelStatus',
            'monitoring_url': 'acr_video_channel_status',
            'params': {
                'qsize': 'qsize',
            },
            'subscriber': ['video', ],
            'time': 'status_time',
        },
        'ec_status_v_delay': {
            'description': 'V Delay status in "service ec status" is as expected',
            'method': 'health_score_ec_status_v_delay',
            'model': 'EnswersChannelStatus',
            'monitoring_url': 'acr_video_channel_status',
            'params': {
                'v_delay': 'v_delay',
            },
            'subscriber': ['video', ],
            'time': 'status_time',
        },
        'ec_status_v_fps': {
            'description': 'V FPS status in "service ec status" is as expected',
            'method': 'health_score_ec_status_v_fps',
            'model': 'EnswersChannelStatus',
            'monitoring_url': 'acr_video_channel_status',
            'params': {
                'v_fps': 'v_fps',
            },
            'subscriber': ['video', ],
            'time': 'status_time',
        },
        'epg_gap': {
            'method': 'health_score_epg_gap',
            'model': 'EpgGap',
            'monitoring_url': 'epg_gap',
            'params': {
                'gap_count': 'gap_count',
            },
            'subscriber': ['audio', ],
            'start_time': 'gap_start',
            'end_time': 'gap_end',
            'time': 'execution_time',
        },
        'epg_overlap': {
            'method': 'health_score_epg_overlap',
            'model': 'EpgOverlap',
            'monitoring_url': 'epg_overlap',
            'params': {
                'overlap_count': 'overlap_count',
            },
            'subscriber': ['audio', ],
            'start_time': 'overlap_start',
            'end_time': 'overlap_end',
            'time': 'execution_time',
        },
        'feature_proxy_delay': {
            'description': 'The delay in fingerprint timestamps received by feature proxy is acceptable.',
            'method': 'health_score_feature_proxy_delay',
            'model': 'FeatureProxyDelay',
            'monitoring_url': 'feature_proxy_delay',
            'params': {
                'delay': 'delay',
            },
            'subscriber': ['video', ],
            'time': 'time',
        },
        'fingerprint_rate': {
            'method': 'health_score_fingerprint_rate',
            'model': 'DatadumpFpStatus',
            'monitoring_url': 'fingerprint_rate',
            'params': {
                'sc_fingerprint_rate': 'sc_fingerprint_rate',
                'lv_fingerprint_rate': 'lv_fingerprint_rate',
                'sac_fingerprint_rate': 'sac_fingerprint_rate',
            },
            'subscriber': ['audio', ],
            'time': 'fp_status_time',
        },
        'harvest_fingerprint_rate': {
            'method': 'health_score_harvest_fingerprint_rate',
            'model': 'DatadumpFpStatus',
            'monitoring_url': 'fingerprint_rate',
            'params': {
                'harvest_fingerprint_rate': 'harvest_fingerprint_rate',
            },
            'subscriber': ['audio', ],
            'time': 'fp_status_time',
        },
        'hive_production_audio_match': {
            'method': 'health_score_hive_production_audio_match',
            'model': 'HiveProductionAudioMatch',
            'monitoring_url': 'hive_production_audio_match',
            'params': {
                'matches': 'matches',
            },
            'subscriber': ['audio', ],
            'time': 'time',
        },
        'mp3_match': {
            'method': 'health_score_mp3_match',
            'model': 'AcrMp3Match',
            'monitoring_url': 'mp3_monitoring',
            'params': {
                'match_status': 'match_status',
            },
            'subscriber': ['audio', ],
            'time': 'match_time',
        },
        'mp3_submit': {
            'method': 'health_score_mp3_submit',
            'model': 'AcrMp3Match',
            'monitoring_url': 'mp3_monitoring',
            'params': {
                'mp3_present': 'mp3_present',
            },
            'subscriber': ['audio', ],
            'time': 'match_time',
        },
        'stream_id_gracenote': {
            'description': 'Stream ID from channel list matches Samsung API',
            'method': 'health_score_stream_id_gracenote',
            'model': 'EncryptedStreamIdMatch',
            'monitoring_url': 'encrypted_stream_id_match',
            'params': {
                'gracenote_exist': 'gracenote_exist',
            },
            'subscriber': ['video', ],
            'time': 'time',
        },
        'stream_id_gracenote_kr': {
            'description': 'Stream ID from EAM API matches Samsung API',
            'method': 'health_score_stream_id_gracenote_kr',
            'model': 'EncryptedStreamIdMatch',
            'monitoring_url': 'encrypted_stream_id_match',
            'params': {
                'enswers_match': 'enswers_match',
            },
            'subscriber': ['video', ],
            'time': 'time',
        },
        'subscribed': {
            'method': 'health_score_subscribed',
            'model': 'ChannelSubscription',
            'monitoring_url': 'subscription',
            'params': {
                'live_tier': 'live_tier',
                'shift_tier': 'shift_tier',
                'tui': 'tui',
            },
            'subscriber': ['audio', ],
            'time': 'subscription_status_time',
        },
        'vm_cpu': {
            'description': 'VM CPU is acceptable',
            'method': 'health_score_vm_cpu',
            'model': 'EnswersVmStatus',
            'monitoring_url': 'vm_status',
            'params': {
                'cpu': 'cpu',
            },
            'subscriber': ['video', ],
            'time': 'time',
        },
        'vm_disk_free_percent': {
            'description': 'VM Disk Free is acceptable',
            'method': 'health_score_vm_disk_free_percent',
            'model': 'EnswersVmStatus',
            'monitoring_url': 'vm_status',
            'params': {
                'disk_free_percent': 'disk_free_percent',
            },
            'subscriber': ['video', ],
            'time': 'time',
        },
        'vm_ping': {
            'description': 'VM responds to ping',
            'method': 'health_score_vm_ping',
            'model': 'EnswersVmStatus',
            'monitoring_url': 'vm_status',
            'params': {
                'ping': 'ping',
            },
            'subscriber': ['video', ],
            'time': 'time',
        },
        'volume': {
            'method': 'health_score_volume',
            'model': 'AcrChannelsStatus',
            'monitoring_url': 'datarate_and_volume',
            'params': {
                'volume': 'volume',
            },
            'subscriber': ['audio', ],
            'time': 'volume_time',
            'uid': 'tui',
        },
    }

    return dispatcher
