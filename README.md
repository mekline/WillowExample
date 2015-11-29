# WillowExample
Example code for a simple experiment using Willow/Python for online behavioral experiments

This is a simple video memory task for an online experiment using the excellent Willow Python package by Jaap Weel and Kevin McCabe. See http://econwillow.sourceforge.net/ for documentation and an absolutely fantastic tutorial - Willow itself has much more power than I'm using - such as the ability to have two participants interact with each other.

Willow allows for the display & modification of arbitrary html content; this code uses html5 video encoding with some fallback for browsers that use older html standards (like Internet Explorer.) Note that there are three versions of every video in this code, for different browsers. I make my videos in iMovie and export as *.mov files; there are plenty of free format converters online (I use Miro) to create the new versions- but always check your output files!

Probably there are more elegant video solutions, but Mechanical Turk feedback suggests that this code is working for at least 90% of users. The biggest problem is laggy videos that don't display to the end - as a sanity check I include a fixation cross at the end of all my test videos and ask subjects to report whether they saw it. 

The only other thing that I would mention about Willow is that I have found that scripts often run more smoothly from our Linux server than from local files on my PC - so if a movie isn't playing back or a picture isn't displaying, test it from your server before spending lots of time debugging locally.

This code was used for the studies reported in 

Kline, M., Muentener, P. & Schulz, L.E. (2013). Transitive and periphrastic sentences affect memory for simple causal scenes. Proceedings of the Thirty-Fifth Annual Conference of the Cognitive Science Society.

...but our results on replication did not confirm these findings. Please get in touch if you might be interested in using stimuli that appear in this example; some are mine and some are due to Paul Muentener & Laura Lakusta.)
