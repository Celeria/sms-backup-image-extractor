# sms-backup-image-extractor
A popular app called SMS Backup and Restore, generates .xml backups of all your texts, including images.
I am not affliated with this developer, but the app can be found here:

https://play.google.com/store/apps/details?id=com.riteshsahu.SMSBackupRestore

This Python script neatly extracts all images from the .xml backup file output by SMS Backup and Restore.

Run it from the same directory your .xml file is in, and replace the name in the script with your filename.

I wrote it in an evening using help from Gemini AI, because I was curious if it could be done, and I wasn't familiar with the format.

It does work, in a reasonable amount of time. My 3.5 GB backup file with thousands of images is processed in 360 seconds on a modern laptop. I attempted to get multi-threading working, but it corrupts the images sometimes, and I didn't feel like spending additional time on this since it was meant as a curiosity. If it seems messy its because I bodged it together with a robot, and simply tested if it worked, which it does.
