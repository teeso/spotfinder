apt-get update
apt-get install -y build-essential
apt-get install -y curl
apt-get install -y git
# --- MongoDB ---
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
echo "deb http://repo.mongodb.org/apt/ubuntu precise/mongodb-org/3.2 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-3.2.list
apt-get update
apt-get install -y mongodb-org

# --- Python
apt-get install -y python-dev
apt-get install -y python-pip
pip install git+https://github.com/mit-nlp/MITIE.git
if [ ! -d /opt/MITIE-models ]; then
	curl -sL https://github.com/mit-nlp/MITIE/releases/download/v0.4/MITIE-models-v0.2.tar.bz2 | tar jxv -C /opt/
fi

wget -P analysis/nlu/data/ https://s3-eu-west-1.amazonaws.com/mitie/total_word_feature_extractor.dat \
