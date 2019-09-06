# Index

이 프로젝트를 진행하며 내가 사용해본것들이다.
좀 더 자세한 튜토리얼은 추후 작성할 예정이다.

1. ECS + Docker Compose

2. Buddy CI

3. AWS KMS

4. Django Form

## 1. ECS + Docker Compose

원래는 ECS + Docker 조합을 사용하고 있었는데, 이번에 새 프로젝트를 시작하면서 새 기술들을 좀 써보자 마음먹고 사용해봤다.
별 다른 이유는 없고, 그냥 사용한다길래 사용해봤다..

그래도 왜 쓰는지 정도는 알아야하니.

### Docker Compose.. 왜 쓸까?

내가 아는바로는 Docker Compose 는 여러 도커 애플리케이션을 정의하고 실행할 수 있게 도와주는 도구이다.

작은 프로젝트에는 유용하지 않을 것 같고, 규모, 복잡도 있는 환경에서 마이크로 서비스 아키텍처를 구현할 때 좋은것 같다.

#### 마이크로 서비스 아키텍처?

서비스 하나를 한꺼번에 만드는게 아닌, 서비스 내부의 기능을 분해해 하나하나 기능을 만들고 따로따로 서비스하는것을 의미한다.
 
서비스가 작고, 독립적이되어서 좋은게 뭐가있을까?

- 독립적인건 변경이 일어나도 다른 서비스에 영향을 거의 미치지 않는다. 또한 기능별로 배포하여 빠르고 많이 배포할 수 있는 장점을 가진다.
- 만약 사용자가 많다면 서비스 전체를 스케일 업하는게 아니라 특정 기능만 스케일 업 할 수 있어 효율적인 자원 사용이 가능하게 한다.

단점은?

- 서비스가 독립적으로 존재하기때문에 서로 통신할 수 있는 추가 처리가 필요하다.
- 많은 서비스들의 개별 배포 관리가 필요하다. 
 
### 그런데?

내가 여태껏 다뤄본 프로젝트들은 죄다 쪼그마내서 사실 Docker Compose까지는 쓸 필요는 없다.

그래도, 있는데 한번쯤은 써봐야겠다 싶어서 시작한다.

### 시작

AWS 계정을 만들었다고 가정하고, ECS를 사용하기위한 사용자가 필요하다.

#### 0. Docker Compose

```yaml
version: '3'
services:
  nginx:
    container_name: nginx
    image: ashekr/crud-webserver-nginx
    ports:
      - 80:80
    depends_on:
      - web  # 해당 컨테이너가 실행되기 위해 먼저 실행되어야하는 컨테이너를 지정
    links:
        - web  # links로 연결해주면 web:8000 으로 접근시 web 컨테이너의 8000번 포트로 접근할 수 있다.
    logging:
      driver: awslogs  # 로컬에서는 안되는 awslogs 설정이지만 CloudWatch에서 로그를 상세하기 찍어보기위한 설정이다.
      options:
        awslogs-group: crud
        awslogs-region: ap-northeast-2
        awslogs-stream-prefix: web-nginx
  web:
    container_name: web
    image: ashekr/crud-was
    working_dir: /srv/app
    command:
      gunicorn config.wsgi:application -c /srv/gunicorn/gunicorn_cfg.py --bind 0.0.0.0:8000
    expose:
      - 8000
    environment:
      - DJANGO_SETTINGS_MODULE=config.settings.production
    logging:
      driver: awslogs
      options:
        awslogs-group: crud
        awslogs-region: ap-northeast-2
        awslogs-stream-prefix: was
```

#### 1. IAM 생성

사용자 생성할 때 정책에 다음것들을 연결해주고 생성하면된다.

- SecretsManagerReadWrite
- IAMFullAccess
- AmazonEC2ContainerRegistryFullAccess
- AmazonECS_FullAccess

완료할 때 액세스 ID, 시크릿 ID 나오는데 누가 못보게 소중히 간직해둔다.

#### 2. ECS Task 역할 생성

자세하게는 AWS에서 CloudWatch로 로그를 보기위해 설정해준다.

1. AWS CLI 설치

2. AWS Configure

이 때 사용되는 액세스 ID 와 시크릿 ID는 위에서 생성했던 Key를 사용한다.

```shell
$ aws configure
$ AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
$ AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
$ Default region name [None]: ap-northeast-2
$ Default output format [None]: json
```

3. 정책 파일 생성

`task-execution-assume-role.json` 파일을 생성한다.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "ecs-tasks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

4. Task Execution Role 생성

여기서 파일 앞에 `file://` 이 반드시 붙어야 파일로 보낼 수 있는것 같다.

```shell
$ aws iam --region ap-northeast-2 create-role --role-name ecsTaskExecutionRole --assume-role-policy-document file://task-execution-assume-role.json
```

5. Task Execution Role을 AWS Role에 붙임

```shell
$ aws iam --region ap-northeast-2 attach-role-policy --role-name ecsTaskExecutionRole --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
```

#### 3. ECS Configure

ECS CLI를 사용하기위한 기본 설정이 필요하다. 이 때 사용되는 액세스 ID, 시크릿 ID도 위에서 생성했던것과 동일한 것을 사용한다.

```shell
$ ecs-cli configure profile --profile-name <설정할 프로필명> --access-key <AWS_ACCESS_KEY_ID> --secret-key <AWS_SECRET_ACCESS_KEY>
```

ECS-CLI를 사용하여 만들 클러스터의 기본을 설정한다.

```shell
ecs-cli configure --cluster <설정할 ECS 클러스터명> --default-launch-type EC2 --region ap-northeast-2
```

#### 3. 클러스터 생성

ECS를 동작하기위한 기본 틀인 Cloudformation, Cluster가 위에서 설정했던대로 생성된다. (클러스터 명, region, EC2)

```shell
$ ecs-cli up --capability-am EC2
```

#### 4. 추가 ECS 설정

Task들의 설정을 각각 할 수 있게 만들어주는 파일이다.

`ecs-params.yml`
```yaml
version: 1
task_definition:
  task_execution_role: ecsTaskExecutionRole
  task_size:
    mem_limit: 0.5GB
    cpu_limit: 256
```

이 때 `ecs_network_mode`를 `awsvps`로 사용하면 Docker간 통신이 컨테이너 명으로 안된다.

#### 5. 시작!

```shell
ecs-cli compose --file <compose.yml 파일> --project-name <task 명> up
```

## 2. Buddy CI

CI 툴 중 가장 예쁘다고 생각한다. (Travis, Circle, Jenkins 써봄)

그리고 YAML파일로 관리 안해도 되고, 모든 설정은 들어가서 선택하고, 드래그 하고.. 암튼 사용자가 사용하기 너무 좋았다.

CI를 선택한다? Buddy CI를 강추한다. 써라, 다른거 못쓴다.

### 사용하기 전에..

Pipelines: 트리거를 사용해서 어떤 이벤트에 파이프라인을 실행할지 정한다.

- master로 푸시되었을 때 실행
- Pull Request가 일어났을 때 실행 

Action: 파이프라인 안에서 실행되는 하나의 동작

- Build Docker
- Test
- Deploy

모든 Action은 도커 위에서 동작한다. Action을 생성할 때 Environment란을 보면 알겠지만
- Pull Docker image from Registry
- Use docker image built in previous action
두가지 환경설정밖에 존재하지 않는다.

이 때 또 주의해야하는게 두번째 옵션인 `Use docker image built in previous action`은 Action 종류 중 
`Build Docker image`로 빌드되어야지만 해당 옵션을 사용할 수 있다. (이거 몰라서 꽤 시간 많이 버렸다.)

#### 사용!

테스트용이라 대충 두개의 파이프라인을 만들어놨다.

1. Pull Request for Master

해당 풀 리퀘스트가 테스트를 통과하는지, 코딩 스타일 여부만 확인하려고 사용했다.

1.1 Trigger

마스터로 풀 리퀘스트 보낼 때 트리거되게했다.

`On Push -> Branches by wildcards`로 트리거 설정해놓으면 풀 리퀘스트에 모두 트리거된다.

1.2 Action

1.2.1 도커 이미지를 빌드
1.2.2 Tox (Test 실행)

2. Deploy on Master

2.1 Trigger

Master에 Push가 일어났을 때 실행된다.

`On Push -> Single branch`

2.1.1 Build Docker Image

2.1.2 Setting CredStash

AWS KMS를 사용하여 Production에 사용되는 Secret Key들을 가져온다.

2.1.3 tox

2.1.4 Push Docker Image

2.1.5 Deploy ESC Compose

## 3. AWS KMS

Django Secret 키를 어떻게 감당해야할지 항상 고민이였다.

1. Encryption

처음에는 secret.json을 사용했고 이를 암호화해서 배포하고, CI에서 복호화해서 배포했다.

불편하다.. 여러 사람이 쓸텐데 동기화도 해야하고, 그럼 암호화 또 해야하고..

2. AWS KMS!

키를 개별관리할 수 있게 해주는 AWS 서비스이다.

여러 Secret Key 가 존재하는 Django 와는 잘 안맞을 수 있겠지만..

매월 20,000 개의 요청이 무료라서 사용하게됐다. (근데.. 마스터 키(고객 키)하나 당 매월 1달러 나간다 하더라.. ㅜㅜ)

아무튼 사용하려면 사용할 수 있다!
 
JSON, dotenv 로 한번에 업로드할수도있고, 가져올 수 있고, 개별 키 업데이트할수도있고 나쁠건 없는것같다.


3. AWS Secret Manager

사실 Django Secret 키를 관리하려면 이거 써야하지 않을까 싶다.

AWS KMS 는 Tree 구조의 JSON 형식을 지원하지 않았지만 이건 지원한다. 개별 키 관리라기보다 전체 키 관리가된다.

여기 Secret Manager 를 편히 사용할 수 있는 오픈소스를 제작중이다. [django-aws-secrets-manager](https://github.com/LeeHanYeong/django-aws-secrets-manager)

### 사용하기 전에,

KMS를 편하게 사용할 수 있는 CLI 라이브러리인 CredStash를 사용한다.

[CredStash](https://github.com/fugue/credstash)

### 준비!

#### 1. Master Key 생성

AWS에서 KMS 들어간 뒤 고객 키 생성에서 이름만 정하고 다 넘긴다.

#### 2. 권한을 위한 그룹 생성

두 그룹을 생성할거다.

참고로 `<KEY-GUID>`는 KMS에서 `키 ID` 컬럼에 존재한다.

**1. KMSSecretWriter**

그룹 이름을 위처럼 생성하고 이후 인라인 정책 두개를 아래걸로 생성한다. 

1.1 SecretWriter

키를 업데이트할 수 있는 권한

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "kms:GenerateDataKey"
            ],
            "Effect": "Allow",
            "Resource": "arn:aws:kms:ap-northeast-2:<AWS-NUMBER-ID>:key/<KEY-GUID>"
        },
        {
            "Action": [
                "dynamodb:PutItem"
            ],
            "Effect": "Allow",
            "Resource": "arn:aws:dynamodb:ap-northeast-2:<AWS-NUMBER-ID>:table/credential-store"
        }
    ]
}
```

1.2 DynamoDBAdmin

키 저장할 때 DynamoDB 사용한다. 이를 생성하고 관리할 수 있는 권한을 준다.

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "dynamodb:CreateTable",
                "dynamodb:DescribeTable"
            ],
            "Effect": "Allow",
            "Resource": "arn:aws:dynamodb:ap-northeast-2:<AWS-NUMBER-ID>:table/credential-store"
        },
        {
            "Action": [
                "dynamodb:ListTables"
            ],
            "Effect": "Allow",
            "Resource": "*"
        }
    ]
}
```

**2. KMSSecretReader**

이번에는 읽기 그룹을 생성한다. 위처럼 인라인 정책 생성

2.1 SecretReader

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "kms:Decrypt"
            ],
            "Effect": "Allow",
            "Resource": "arn:aws:kms:ap-northeast-2:<AWS-NUMBER-ID>:key/<KEY-GUID>"
        },
        {
            "Action": [
                "dynamodb:GetItem",
                "dynamodb:Query",
                "dynamodb:Scan"
            ],
            "Effect": "Allow",
            "Resource": "arn:aws:dynamodb:ap-northeast-2:<AWS-NUMBER-ID>:table/credential-store"
        }
    ]
}
```

#### 3. 사용자를 생성하여 위에서 만들 그룹을 할당

Admin은 읽기, 쓰기 둘다 가능할테니 IAM에서 사용자를 생성할 때 두 그룹을 모두 포함하여 생성한다.

액세스 ID, 시크릿 ID는 당연히 모셔두고 AWS Configure 에서 사용한다.

`~/.aws/credential` 파일에 AWS 새 프로필을 추가한다.

```
[credstash]
aws_access_key_id = <AWS_ACCESS_KEY_ID>
aws_secret_access_key = <AWS_SCRECT_ACCESS_KEY_ID>
```

#### 4. 키들을 담을 DynamoDB 생성

`-p`는 위에서 만든 AWS Profile을 지정하고
`-r`은 Region을 지정한다.

```shell
$ credstash -p credstash -r ap-northeast-2 setup
```

`dynamodb:TagResource` 권한이 없다고 뜨는데 무시해도된다.

#### 5. 키를 다룰 수 있어졌다

5.1 개별 키 넣기

```shell
$ credstash -p credstash -r ap-northeast-2 put <KEY> <VALUE>
```

`<KEY> has been stored` 라고 뜨면 정상적으로 등록된것이다.

5.2 개별 키 가져오기

```shell
$ credstash -p credstash -r ap-northeast-2 get <KEY>
```

5.3 모든 키 넣기

```shell
$ credstash -p credstash -r ap-northeast-2 putall @<filename.json>
```

5.4 모든 키 가져오기

`-f`는 어떻게 가져올지 정할 수 있다. json, dotenv 등등.. 

```shell
$ credstash -p credstash -r ap-northeast-2 getall -f dotenv
```


