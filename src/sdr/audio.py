import queue
import sys
import threading
from typing import Generator

import numpy as np
import sounddevice as sd


class Stream(threading.Thread):
    """
    Helper class for streaming audio in a separate thread.

    ```python
    audio_streamer = Stream(source, rate)
    audio_streamer.start()
    print("audio is playing")
    audio_streamer.stop()
    print("audio is stoped")
    ```
    """
    def __init__(
            self, 
            source:Generator[np.array, None, None],
            rate: int,
            blocksize:int=1024,
            buffersize:int=20,
            device: int | str | None = None,
            channels: int=1,
            dtype: str='int16'
        ):
        """
        Parameters
        ----------
        source: Generator[np.array] # generator which yields 1 block
        rate: int # Playback Speed samples / second
        blocksize: int=1024
        buffersize: int=20
        device: int | str | None = None
        channels: int=1,
        dtype: str='int16'
        """
        self.source = source
        self.rate = rate
        self.blocksize = blocksize
        self.buffersize = buffersize
        self.device = device
        self.channels = channels

        self.q = queue.Queue(maxsize=buffersize)
        threading.Thread.__init__(self)
        self.event = threading.Event()

        def callback(outdata, frames, time, status):
            assert frames == self.blocksize
            if status.output_underflow:
                print('Output underflow: increase blocksize?', file=sys.stderr)
                raise sd.CallbackAbort
            assert not status
            try:
                data = self.q.get_nowait()
            except queue.Empty as e:
                print('Buffer is empty: increase buffersize?', file=sys.stderr)
                raise sd.CallbackAbort from e
            assert len(data) == len(outdata), f"len(data) ({len(data)}) != len(outdata) ({len(outdata)})"
            outdata[:] = data
        self.stream = sd.OutputStream(
            samplerate=self.rate, blocksize=self.blocksize,
            device=self.device, channels=self.channels, dtype=dtype,
            callback=callback
        )

    def run(self):
        for _ in range(self.buffersize):
            self.q.put_nowait(next(self.source))
        self.stream.start()
        timeout = self.blocksize * self.buffersize / self.rate
        while not self.event.is_set():
            self.q.put(next(self.source), timeout=timeout)

    def stop(self):
        self.event.set()
        self.stream.stop()
