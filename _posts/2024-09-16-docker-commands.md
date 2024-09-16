---
title: 자주 쓰는/쓰일 Docker 명령어 모음
description: Docker 및 Dockerfile 명령어를 효과적으로 활용하기 위한 모음
date: 2024-09-16 00:21:45 +09:00
categories: [DevOps, docker]
pin : true
tags:
  [
    Docker,
    Container,
    Command,
    Dockerfile,
    Tip
  ]
---

# 자주 쓰는 commands

## Docker 컨테이너 관리

이미지 목록 조회<br>
`$ docker images`<br>

컨테이너 목록 조회<br>
`$ docker ps`<br>

중지된 컨테이너 목록 포함 조회<br>
`$ docker ps -a`<br>

컨테이너 실행<br>
`$ docker run -d --name {컨테이너명} {이미지명}`<br>


| 옵션          | 설명                 |
|-------------|--------------------|
| `-d`        | 백그라운드에서 실행         |
| `-p`        | 호스트와 컨테이너 간 포트 포워딩 |
| `--name`    | 컨테이너에 이름 부여        |
| `--network` | 네트워크 설정            |

컨테이너 중지<br>
`$ docker stop {컨테이너명}`<br>

컨테이너 재시작<br>
`$ docker restart {컨테이너명}`<br>

컨테이너 삭제<br>
`$ docker rm {컨테이너명}`<br>

이미지 삭제<br>
`$ docker rmi {이미지명}`<br>

## Docker 이미지 관리

이미지 빌드<br>
`$ docker build -t {이미지명}:{태그} .`<br>

| 옵션           | 설명                 |
|--------------|--------------------|
| `-t`         | 빌드된 이미지에 이름과 태그 부여 |
| `--no-cache` | 캐시를 사용하지 않고 새로 빌드  |

이미지 푸시<br>
`$ docker push {이미지명}:{태그}`<br>

이미지 다운로드<br>
`$ docker pull {이미지명}:{태그}`<br>

## Docker 네트워크 및 볼륨

Docker 네트워크 목록 조회<br>
`$ docker network ls`<br>

Docker 네트워크 생성<br>
`$ docker network create {네트워크명}`<br>

Docker 볼륨 목록 조회<br>
`$ docker volume ls`<br>

Docker 볼륨 생성<br>
`$ docker volume create {볼륨명}`<br>

## Dockerfile 관련 명령어

기본 이미지 지정<br>
`FROM {기본 이미지}`<br>

환경 변수 설정<br>
`ENV {변수명}={값}`<br>

작업 디렉토리 설정<br>
`WORKDIR /{디렉토리명}`<br>

파일 복사<br>
`COPY {호스트 파일 경로} {컨테이너 경로}`<br>

명령어 실행<br>
`RUN {명령어}`<br>

컨테이너 시작 시 실행할 명령어 지정<br>
`CMD ["{실행 파일}", "{인자1}", "{인자2}"]`<br>

포트 노출<br>
`EXPOSE {포트 번호}`<br>

## 유용한 Docker 명령어

모든 컨테이너 중지<br>
`$ docker stop $(docker ps -q)`<br>

모든 중지된 컨테이너 삭제<br>
`$ docker rm $(docker ps -a -q)`<br>

모든 사용되지 않는 이미지, 네트워크, 볼륨 삭제<br>
`$ docker system prune`<br>

### 추가적인 좋은 기능이 있다면 댓글 남겨주시면 감사하겠습니다 😀
