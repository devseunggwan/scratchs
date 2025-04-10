export XAN_VERSION=0.48.0

wget https://github.com/medialab/xan/releases/download/$XAN_VERSION/xan_$XAN_VERSION\_x86_64-unknown-linux-musl.tar.gz
tar -xzf xan_$XAN_VERSION\_x86_64-unknown-linux-musl.tar.gz
rm xan_$XAN_VERSION\_x86_64-unknown-linux-musl.tar.gz
sudo mv xan /usr/local/bin
sudo chmod +x /usr/local/bin/xan