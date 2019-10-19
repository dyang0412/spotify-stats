### Production
Before this, you must have a github ssh key pair within your user account. It's found in  `~/.ssh/`.  
Run these commands to pull and restart the server with newest commits.  
First, `cd /home/dan/spotify-stats` in order to get to the right place.  
Then run the following:  

> git pull  
> sudo systemctl stop spotifystats  

Then wait for it to be done. If it hangs, press Ctrl+C and move to next step.  

> sudo systemctl start spotifystats

You can edit the gunicorn file at:  
> sudo nano /etc/systemd/system/spotifystats.service
