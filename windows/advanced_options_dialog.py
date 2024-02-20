# coding: utf-8
def advanced_options(threads):
    print("unfinished, returns default values")
    
    quality = 22
    
    encoder_preset = "medium"
    if not threads < 6:
        encoder_threads = 4
    else:
        encoder_threads = 2
        
    audio_codec = "AAC"
    audio_bitrate = 128
    
    return quality, encoder_preset, encoder_threads, audio_codec, audio_bitrate