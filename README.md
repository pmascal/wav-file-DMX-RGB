#### DMX generating RGB from frequencies<br />Peter Mascal

This code generates a spectrogram from a .wav file, and given any time t, RGB values as well as the overall level of brightness is returned based on the frequency at that moment (more specifically, the data for the frame that t is included in). These values are ranged a scale from 0 to 255. This was made to work with another member in my class, where a frame of DMX data (512 values) is passed to their code and converted to binary, then transferred to the hardware DMX group. Since DMX has 512 channels, it expects a frame to have 512 values, therefore every other channel (not housing brightness, red, green, or blue) is made to be 0.

This repository includes a .wav file of a gradually increasing frequency named `increasing.wav` that was used for testing purposes. This can be ran with my code to visualize how the RBG values are distributed using Matplotlib.

Check out the file `FunctionDescriptions.md` to see more detailed information about each function and how it works. 
