echo "[Installing pip3]=========================================================================="
sudo apt --yes install python3-pip
echo "[Installing python requirements]==========================================================="
pip3 install -r /vagrant/requirements.txt
echo "[Installing solver Coin-OR]================================================================"
apt --yes install coinor-cbc
echo "[PROCESS COMPLETE]"

