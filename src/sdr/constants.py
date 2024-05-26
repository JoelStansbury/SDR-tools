class AudioStreamer:
    BLOCKSIZE=1024
    """Number of frames to send to audio device at a time."""
    BUFFERSIZE=20
    """Number of blocks to store in memory (for handoff to audio device)"""