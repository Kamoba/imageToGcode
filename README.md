###########################################################################
#
# Hand writing to G-code
#
###########################################################################




REQUIREMENTS:
-------------
Python 3 <br>
opencv-python <br>
RasterCarve <br>
imutils <br>
numpy <br>
scipy <br>



Introduction:
-------------

This small tool allows you to convert an image into gcode.<br>
For an optimal conversion use a black writing on a sheet of paper, and the photo must have a good brightness and without borders. <br>




GETTING STARTED:
---------------
1. Go to the project folder and run the following command: <br>
   ``` pip3 install -r requirements.txt``` <br>	 <br>
2. Run: <br>
   ``` python imageToGcode.py test/very-bad-photo.jpg```


You can quickly visualize the gcode file thanks to free online services such as: <br>
For the stl: https://openjscad.org <br><br><br>



<article class="markdown-body entry-content container-lg" itemprop="text">
<pre><code>This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see &lt;http://www.gnu.org/licenses/&gt;.
</code></pre>
</article>