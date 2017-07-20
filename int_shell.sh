while true
do
sudo ./measuring

sudo python upload_google.py
rm -f tempD.csv

sleep 60
done
