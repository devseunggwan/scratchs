## 개요

* Rochy-Linux 내에 폐쇠망 환경에 Python 환경을 배포하기 위한 과정을 설명합니다.
* Python 가상 환경 및 Dependency 관리는 UV로 진행합니다.
* Rochy-Linux 8.10, Python 3.12.8, UV 0.5.18 기준으로 작성하였습니다.

## 1. Python 설치

### 1-1. 파일 다운로드

* dnf를 사용하여 Python 및 Dependency를 다운로드 받습니다.

``` sh

dnf install --downloaddir {download-path} --downloadonly python3.12 python3.12-pip python3.12-devel  -y

```

### 1-2. Python 설치

* 다운로드 받은 파일은 rpm 형태로 구성되어 있고, download-path에 들어가서 설치 진행합니다.

``` sh

rpm -ivh *.rpm

```


### 1-3. Python 설치 확인

* 설치가 되었다면 정상적으로 설치되었는 지 확인합니다.

``` sh
python3 -V # OK
python3.12 -V # OK
python # ERROR
```


## 2. UV 설치 

### 2-1. 파일 다운로드

* Github Repo에 들어가서 UV Release를 확인하고, OS Version에 맞는 설치 파일을 다운로드 받습니다.

``` sh

wget https://github.com/astral-sh/uv/releases/download/0.5.18/uv-x86_64-unknown-linux-gnu.tar.gz

```

### 2-2. UV 설치

* 다운로드 받은 UV 파일을 압축 해제하고 해제한 파일들은 shell에서 사용할 수 있도록 조치해야 합니다.
* 해제 후 크게 보안 이슈가 없다면 `/usr/bin` 에 파일들을 욺겨서 사용할 수 있도록 합니다.

> UV 스크립트로 설치하면 `$HOME/.local/bin/env`에 설치된 파일들이 추가되고 shell에 등록해야 합니다.

``` sh

tar -xvf uv-x86_64-unknown-linux-gnu.tar.gz

```

### 2-3. UV 설치 확인

* 설치가 완료되었는 지 확인합니다.

``` sh
uv
```
