## Spectrogram
This function takes a file path and returns three items: a 
spectrogram as a 2-D array, a 1-D array containing frequencies,
and another 1-D array containing times.

The row indices of the spectrogram refer to the indices of the
frequency 1-D array, while the column indices refer to the indices
of the times 1-D array. The values of the spectrogram represent
the amplitudes of each frequency during that window.



## AverageValues
This function creates a list of average frequencies,
taking into account the amplitudes as weights.

A transpose of the spectrogram is made to loop through every
(original) column using the below method.

Next, Loop through each row, making 'amplitudes' a 1-D array 
of amplitudes that are present within that window of the spectrogram
with every loop.

Finally, calculate a weighted average of that window's frequency
by using the 'amplitudes' 1-D array values as weights, and add it
to the avg_vals list.

Note that if the sum of the amplitudes is 0 (no frequencies within 
that window), its average frequency is equaled to 0.



## FrameData:
This function takes the average frequency/amplitues from avg_vals/amp_vals, 
and creates a 2-D array of RGB/brightness values. The rows represent the frame.
The columns will represent the channels of the DMX. DMX is expecting 512 channels, so every channel that does not have values is 0, even though this code only generates values for the first 4, the rest must be made.
Channels 1,2,3,4 will represent brightness, red, green, and blue, respectively. Red minimum frequency, blue max.



## tcolor
This function takes time, assigns it to a window number,
and returns that window's frame data.

The time, t, is taken, and every element in the times array that is 
less than t is returned. Since it returns every
value less than t, only the last value in the array is used, ([-1]).
(e.g. if times collected were at [1,2,3], at t = 2.5 --> [1,2]
is returned, and the frame wanted is after 2 and before 3)
----> a = self.times[self.times <= t][-1]

"a" is a float value that defines the element that houses the given
time, and we use np.where to return the index of said element.
----> b = np.where(self.times == a)

The np.where function returns a numpy array with the first element
being a normal array that has the index of the light value that
we are looking for. Considering this, the returned value of
np.where needs to be modified to extract the single integer value.
-----> c = b[0][0]

This index value is then used to return the correct row in the frame
data 2-D array.
-----> self.frame_data(c)

If the given time does not fit into the times matrix, return 0.

