# Solar ESS EMS Docker 배포 가이드

## 1. 배포 설명

Linux 서버에는 Node.js와 Python을 별도로 설치하지 않는다. Docker Engine과 Docker Compose plugin만 설치한다.

---

## 2. 배포 파일 생성

### 2.1 사전 준비

Docker 엔진 확인:

```powershell
docker version
docker compose version
```

Docker 설치 되여 있지 않았으면 Docker 설치 해주세요.

### 2.2 Linux amd64 배포 패키지 생성

Docker 엔진 확인 후 프로젝트 루트에서 실행한다.

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\package-docker-linux.ps1
```

일반적인 Intel 또는 AMD 기반 Linux 서버는 `amd64` 패키지를 사용한다.

생성 파일:

```text
release/solar-ems-linux-amd64-deploy.zip
```

ZIP 내부 구성:

```text
solar-ems-images-linux-amd64.tar
compose.deploy.yaml
README.md
```

### 2.3 ARM64 Linux 서버용 패키지 생성

ARM 기반 서버를 사용할 때만 실행한다.

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\package-docker-linux.ps1 -Architecture arm64
```

생성 파일:

```text
release/solar-ems-linux-arm64-deploy.zip
```

---

## 3. Linux 서버 준비

### 3.1 Docker 설치 확인

```bash
docker version
docker compose version
```

Docker 서비스가 중지되어 있으면 시작한다.
Docker 설치 되어 있지않으면 설치 후 진행하세요.
Linux 내부에 Docker 설치하려면 [Linux 내부 Docker 설치 방법](#12-linux-내부-docker-설치-방법)을 참조하세요.


```bash
sudo service docker start
```

권한 설정 안하면 모든 Docker 명령 앞에 `sudo`를 붙인다.

---

## 4. Linux 서버 배포

### 4.1 배포 파일 업로드

`solar-ems-linux-amd64-deploy.zip` 파일을 Linux 서버에 복사한다.

예시:

```bash
mkdir -p ~/solar-ems-deploy
cd ~/solar-ems-deploy
```

WSL에서 Windows 프로젝트 파일을 직접 복사하는 경우:

```bash
cp /mnt/c/Users/sangy/Desktop/project/solar-ems/release/solar-ems-linux-amd64-deploy.zip .
```

### 4.2 압축 해제

```bash
sudo apt update
sudo apt install -y unzip

unzip solar-ems-linux-amd64-deploy.zip -d solar-ems
cd solar-ems
```

### 4.3 Docker 이미지 로드

```bash
sudo docker load -i solar-ems-images-linux-amd64.tar
sudo docker images | grep solar-ems
```

확인 대상:

```text
solar-ems-frontend
solar-ems-backend
```

### 4.4 컨테이너 실행

```bash
mkdir -p data
sudo docker compose -f compose.deploy.yaml up -d
sudo docker compose -f compose.deploy.yaml ps
```

---

## 5. 접속 확인

### 5.1 Linux 서버 내부 확인

```bash
curl http://localhost
```

### 5.2 브라우저 확인

동일 PC에서 실행한 경우:

```text
http://localhost
```

별도 Linux 서버에 배포한 경우:

```text
http://리눅스서버IP
```

기본 로그인 계정:

```text
ID: admin
Password: 1111
```

---

## 6. 외부 PC 접속

같은 공유기 또는 사내 네트워크의 다른 PC에서는 배포 서버 IP로 접속한다.

```text
http://192.168.x.x
```

접속되지 않으면 서버 방화벽 또는 클라우드 보안 그룹에서 TCP `80` 포트를 허용한다.

Ubuntu UFW 예시:

```bash
sudo ufw allow 80/tcp
sudo ufw status
```

WSL에서 테스트할 때는 Windows 방화벽 설정도 필요할 수 있다.

---

## 7. SQLite 데이터 관리

SQLite 데이터는 컨테이너 내부가 아니라 Linux 호스트 디스크에 저장한다.

```text
solar-ems/data/solar_ems.db
```

컨테이너를 제거하거나 재배포해도 `data` 디렉터리는 유지된다.

백업:

```bash
cp -a data "data-backup-$(date +%Y%m%d-%H%M%S)"
```

복구:

```bash
docker compose -f compose.deploy.yaml down
cp data-backup-YYYYMMDD-HHMMSS/solar_ems.db data/solar_ems.db
docker compose -f compose.deploy.yaml up -d
```

---

## 8. 재배포

개발 PC에서 새 패키지를 생성하고 Linux 서버에 업로드한 뒤 실행한다.

```bash
unzip -o solar-ems-linux-amd64-deploy.zip -d solar-ems
cd solar-ems

docker load -i solar-ems-images-linux-amd64.tar
docker compose -f compose.deploy.yaml up -d
```

SQLite 데이터는 `data` 디렉터리에 유지된다.

---

## 9. 로그 및 상태 확인

컨테이너 상태:

```bash
docker compose -f compose.deploy.yaml ps
```

전체 로그:

```bash
docker compose -f compose.deploy.yaml logs --tail=100
```

백엔드 로그:

```bash
docker compose -f compose.deploy.yaml logs --tail=100 backend
```

프론트엔드 Nginx 로그:

```bash
docker compose -f compose.deploy.yaml logs --tail=100 frontend
```

---

## 10. 중지 및 제거

중지:

```bash
docker compose -f compose.deploy.yaml stop
```

컨테이너 제거:

```bash
docker compose -f compose.deploy.yaml down
```

`down`을 실행해도 `data/solar_ems.db`는 삭제되지 않는다.

---

## 11. Linux 내부 Docker 설치 방법

```bash
sudo apt update
sudo apt install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings

sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  -o /etc/apt/keyrings/docker.asc

sudo chmod a+r /etc/apt/keyrings/docker.asc

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
  https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo ${UBUNTU_CODENAME:-$VERSION_CODENAME}) stable" \
  | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io \
  docker-buildx-plugin docker-compose-plugin

sudo service docker start
sudo docker version

```


# MobaXterm를 사용한 배포 

1. MobaXterm 실행 
1. cd /opt/www/ems   배포할 경로
1. ls   파일 목록 확인

1. docker images  이미지 확인 
1. docker ps -a  도커 상태 확인

1. docker-compose down 프로젝트 down
1. docker rmi 87528cd94feb 46f37d81ca6f  프로젝트 이미지 삭제 

1. 배포할 프로젝트 이미지를 배포경로에 복사 

1. docker load -i solar-ems-images-linux-amd64.tar  로드 이미지 
1. docker images  이미지 확인 

1. docker-compose up -d 프로젝트 실행 

