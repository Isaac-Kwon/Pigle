# CIMS-Pigle
Data Transfer with Google Drive REST-API, Sheet API // HIPEx Lab Atmosphere Monitoring

## Introduction
본 연구는 실험실 환경 (온도 및 습도) 의 실시간 조사와 웹페이지 업로드를 위해 진행되었다.


## 기본 필요사항
* 하드웨어
	* Raspberry Pi 3
	* DHT22 모듈
* 소프트웨어
	* WiringPi2
		* ``http://wiringpi.com/download-and-install/``
	* gspread
		* ``pip install gspread``
	* OAuth2
		* ``pip install --upgrade oauth2client``
	* screen
		* ``pip install screen``

		
## How to Use

### Install
````bash
$ git clone https://github.com/PNU-HIPEx/CIMS-Pigle.git
````

### Configure state

### Compile measuring code
````bash
$ cd CIMS-Pigle.git
  
$ gcc -o measuring measuring.c -l wiringpi
OR
$ sh compile.sh
````

### 