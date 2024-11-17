---
title: 자주 쓰는/쓰일 Kubernetes 명령어 모음
description: Kubernetes 및 Kind 클러스터 관리에 유용한 명령어 모음
date: 2024-09-17 21:49:00 +09:00
categories: [Tip, DevOps, Kubernetes]
pin: false
tags:
  [
    Kubernetes,
    K8S,
    Kind,
    Command
  ]
---

# 자주 쓰는 commands

## 클러스터 및 컨텍스트 관련

현재 컨텍스트 확인<br>
`$ kubectl config current-context`<br>

사용 가능한 컨텍스트 목록 확인<br>
`$ kubectl config get-contexts`<br>

컨텍스트 전환<br>
`$ kubectl config use-context {컨텍스트명}`<br>

| 옵션             | 설명                      |
|----------------|-------------------------|
| `--kubeconfig` | 사용할 kubeconfig 파일 경로 지정 |
| `--namespace`  | 기본 네임스페이스 설정            |

## 리소스 관련

모든 네임스페이스의 모든 리소스 조회<br>
`$ kubectl get all --all-namespaces`<br>

특정 네임스페이스의 모든 리소스 조회<br>
`$ kubectl get all -n {네임스페이스명}`<br>

파드 목록 조회<br>
`$ kubectl get pods`<br>

디플로이먼트 목록 조회<br>
`$ kubectl get deployments`<br>

| 옵션        | 설명                       |
|-----------|--------------------------|
| `-o wide` | 추가 정보 (IP, 노드 등)를 포함한 출력 |
| `--watch` | 실시간 업데이트 감시              |

리소스 상세 정보 확인<br>
`$ kubectl describe {리소스 종류} {리소스명}`<br>

리소스 삭제<br>
`$ kubectl delete {리소스 종류} {리소스명}`<br>

리소스 생성 (YAML 파일 기준)<br>
`$ kubectl apply -f {YAML 파일 경로}`<br>

## 로그 및 디버깅

파드 로그 출력<br>
`$ kubectl logs {파드명}`<br>

파드 실행 중 명령어 실행<br>
`$ kubectl exec -it {파드명} -- {명령어}`<br>

클러스터 상태 확인<br>
`$ kubectl cluster-info`<br>

## Kind 클러스터 관련

Kind 클러스터 생성<br>
`$ kind create cluster --name {클러스터명}`<br>

| 옵션         | 설명                       |
|------------|--------------------------|
| `--config` | 클러스터 생성에 사용할 설정 파일 경로 지정 |
| `--wait`   | 클러스터 생성 완료 대기 시간 설정      |

Kind 클러스터 삭제<br>
`$ kind delete cluster --name {클러스터명}`<br>

Kind 클러스터 목록 확인<br>
`$ kind get clusters`<br>

Kind 클러스터에 대한 kubeconfig 설정 확인<br>
`$ kind get kubeconfig --name {클러스터명}`<br>

### 추가적인 좋은 기능이 있다면 댓글 남겨주시면 감사하겠습니다 😀
