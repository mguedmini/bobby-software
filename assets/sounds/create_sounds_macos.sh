/bin/bash

say -v Markus "Hallo"'!' -o hallo.aiff
say -v Markus "Endlich alleine. Ich glaube, ich mache jetzt mal ein bisschen Yoga"'!' -o endlich_alleine.aiff
say -v Markus "Sitzhöhe erfasst" -o hoehe_erfasst.aiff
say -v Markus "Zu viel Gezappel. Sitz erstmal still"'!' -o gezappel.aiff
say -v Markus "Sei nicht dumm, sitz nicht krumm rum"'!' -o nicht_dumm_nicht_krumm.aiff
say -v Markus "Wir kalibrieren neu"'!'" Setz dich aufrecht hin"'!' -o kalibrieren.aiff

# brew install lame
lame -m m hallo.aiff hallo.mp3
lame -m m endlich_alleine.aiff endlich_alleine.mp3
lame -m m hoehe_erfasst.aiff hoehe_erfasst.mp3
lame -m m gezappel.aiff gezappel.mp3
lame -m m nicht_dumm_nicht_krumm.aiff nicht_dumm_nicht_krumm.mp3
lame -m m kalibrieren.aiff kalibrieren.mp3
