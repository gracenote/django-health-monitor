"""All parameters associated with tests should go into the dispatcher dictionary.

dispatcher[test_name] = name of tests
dispatcher[test_name]['scoring_logic'] = name of scoring test in scoring_logic.py
dispatcher[test_name]['params'] = test result values to be passed to calculate score using scoring_logic.py
dispatcher[test_name]['group'] = list of groups which this test is revelant for

Example:
    dispatcher = {
        'heartbeat': {
            'scoring_logic': 'health_score_heartbeat',
            'params': {
                'heartrate': 'heartrate',
                'arrhythmia': 'arrhythmia',
            },
            'group': ['doctor', ],
        },
        'sleep': {
            'scoring_logic': 'health_score_sleep',
            'params': {
                'quality': 'quality',
            },
            'group': ['doctor', ],
            'start_time': 'start_time',
            'end_time': 'end_time',
        }
    }
"""


def get_dispatcher(original_dispatcher=False):
    dispatcher = {
        'bis_connection': {
            'scoring_logic': 'health_score_bis_connection',
            'params': {
                'bis_status_lv': 'bis_status_lv',
                'bis_status_sac': 'bis_status_sac',
                'bis_status_sc': 'bis_status_sc',
            },
            'group': ['audio', ],
        },
        'bis_queue': {
            'scoring_logic': 'health_score_bis_queue',
            'params': {
                'submit_queue_lv': 'submit_queue_lv',
                'submit_queue_sac': 'submit_queue_sac',
                'submit_queue_sc': 'submit_queue_sc',
            },
            'group': ['audio', ],
        },
        'datarate': {
            'scoring_logic': 'health_score_datarate',
            'params': {
                'datarate': 'datarate',
            },
            'group': ['audio', ],
        },
        'directv_match': {
            'scoring_logic': 'health_score_directv_match',
            'params': {
                'match_status': 'match_status',
            },
            'group': ['audio', ],
        },
        'eam_api_match': {
            'description': 'TUI exists in EAM API',
            'scoring_logic': 'health_score_eam_api_match',
            'params': {
                'api_match': 'api_match',
                'ens_status': 'ens_status',
            },
            'group': ['video', ],
        },
        'eam_api_status': {
            'description': 'Running state in EAM API is as expected',
            'scoring_logic': 'health_score_eam_api_status',
            'params': {
                'ens_status': 'ens_status',
                'status': 'status',
                'use': 'use',
            },
            'group': ['video', ],
        },
        'ec_status_audio': {
            'description': 'Audio status in "service ec status" is as expected',
            'scoring_logic': 'health_score_ec_status_audio',
            'params': {
                'audio': 'audio',
            },
            'group': ['audio', 'video'],
        },
        'ec_status_video': {
            'description': 'Video status in "service ec status" is as expected',
            'scoring_logic': 'health_score_ec_status_video',
            'params': {
                'video': 'video',
            },
            'group': ['video', ],
        },
        'ec_status_network': {
            'description': 'Network status in "service ec status" is as expected',
            'scoring_logic': 'health_score_ec_status_network',
            'params': {
                'network': 'network',
            },
            'group': ['video', ],
        },
        'ec_status_qsize': {
            'description': 'QSize status in "service ec status" is as expected',
            'scoring_logic': 'health_score_ec_status_qsize',
            'params': {
                'qsize': 'qsize',
            },
            'group': ['video', ],
        },
        'ec_status_v_delay': {
            'description': 'V Delay status in "service ec status" is as expected',
            'scoring_logic': 'health_score_ec_status_v_delay',
            'params': {
                'v_delay': 'v_delay',
            },
            'group': ['video', ],
        },
        'ec_status_v_fps': {
            'description': 'V FPS status in "service ec status" is as expected',
            'scoring_logic': 'health_score_ec_status_v_fps',
            'params': {
                'v_fps': 'v_fps',
            },
            'group': ['video', ],
        },
        'epg_gap': {
            'scoring_logic': 'health_score_epg_gap',
            'params': {
                'gap_count': 'gap_count',
            },
            'group': ['audio', ],
            'start_time': 'gap_start',
            'end_time': 'gap_end',
        },
        'epg_overlap': {
            'scoring_logic': 'health_score_epg_overlap',
            'params': {
                'overlap_count': 'overlap_count',
            },
            'group': ['audio', ],
            'start_time': 'overlap_start',
            'end_time': 'overlap_end',
        },
        'feature_proxy_delay': {
            'description': 'The delay in fingerprint timestamps received by feature proxy is acceptable.',
            'scoring_logic': 'health_score_feature_proxy_delay',
            'params': {
                'delay': 'delay',
            },
            'group': ['video', ],
        },
        'fingerprint_rate': {
            'scoring_logic': 'health_score_fingerprint_rate',
            'params': {
                'sc_fingerprint_rate': 'sc_fingerprint_rate',
                'lv_fingerprint_rate': 'lv_fingerprint_rate',
                'sac_fingerprint_rate': 'sac_fingerprint_rate',
            },
            'group': ['audio', ],
        },
        'harvest_fingerprint_rate': {
            'scoring_logic': 'health_score_harvest_fingerprint_rate',
            'params': {
                'harvest_fingerprint_rate': 'harvest_fingerprint_rate',
            },
            'group': ['audio', ],
        },
        'hive_production_audio_match': {
            'scoring_logic': 'health_score_hive_production_audio_match',
            'params': {
                'matches': 'matches',
            },
            'group': ['audio', ],
        },
        'mp3_match': {
            'scoring_logic': 'health_score_mp3_match',
            'params': {
                'match_status': 'match_status',
            },
            'group': ['audio', ],
        },
        'mp3_submit': {
            'scoring_logic': 'health_score_mp3_submit',
            'params': {
                'mp3_present': 'mp3_present',
            },
            'group': ['audio', ],
        },
        'stream_id_gracenote': {
            'description': 'Stream ID from channel list matches Samsung API',
            'scoring_logic': 'health_score_stream_id_gracenote',
            'params': {
                'gracenote_exist': 'gracenote_exist',
            },
            'group': ['video', ],
        },
        'stream_id_gracenote_kr': {
            'description': 'Stream ID from EAM API matches Samsung API',
            'scoring_logic': 'health_score_stream_id_gracenote_kr',
            'params': {
                'enswers_match': 'enswers_match',
            },
            'group': ['video', ],
        },
        'subscribed': {
            'scoring_logic': 'health_score_subscribed',
            'params': {
                'live_tier': 'live_tier',
                'shift_tier': 'shift_tier',
                'tui': 'tui',
            },
            'group': ['audio', ],
        },
        'vm_cpu': {
            'description': 'VM CPU is acceptable',
            'scoring_logic': 'health_score_vm_cpu',
            'params': {
                'cpu': 'cpu',
            },
            'group': ['video', ],
        },
        'vm_disk_free_percent': {
            'description': 'VM Disk Free is acceptable',
            'scoring_logic': 'health_score_vm_disk_free_percent',
            'params': {
                'disk_free_percent': 'disk_free_percent',
            },
            'group': ['video', ],
        },
        'vm_ping': {
            'description': 'VM responds to ping',
            'scoring_logic': 'health_score_vm_ping',
            'params': {
                'ping': 'ping',
            },
            'group': ['video', ],
        },
        'volume': {
            'scoring_logic': 'health_score_volume',
            'params': {
                'volume': 'volume',
            },
            'group': ['audio', ],
            'uid': 'tui',
        },
    }

    return dispatcher
