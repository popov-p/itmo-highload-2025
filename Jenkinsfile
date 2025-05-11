@Library('COSM-Jenkins-libs') _

pipeline {

    agent none

    options {
        skipDefaultCheckout(true)
    }

    stages {
        
        stage('Preparation') {
            agent { node { label 'master' } }
            steps {
                step([$class: 'WsCleanup'])
    
                checkout scm

                sh '''#!/bin/bash
                    git log -n 1 | grep "commit " | sed 's/commit //g' > currentVersion
                '''
                    
                stash name:'workspace', includes:'**'
            }
        }

        stage('Build application') {
            agent {
                docker {
                    image 'python:3.12-slim'
                    reuseNode true
                    args '-u root'
                }
            }
            steps {
                unstash 'workspace'
                sh '''
                    #!/bin/bash
                    TAG=$(cut -c1-8 < currentVersion)
                    echo "-----> Building Docker images with tag ${TAG}"

                    docker build -t controller:${TAG} -f controller/Dockerfile controller
                    docker build -t rule_engine:${TAG} -f rule_engine/Dockerfile rule_engine
                '''
            }
        }
    }

    post {
        always {
            node ('master') {
                script {
                    env.GIT_URL = env.GIT_URL_1
		    notifyRocketChat(
                        channelName: 'dummy',
                        minioCredentialsId: 'jenkins-minio-credentials',
                        minioHostUrl: 'https://minio.cloud.cosm-lab.science'
                    )
                    withCredentials([string(credentialsId: 'CloudRushTlg-token', variable: 'TLG_TOKEN')]) {
                        notifyTelegram(
                            minioHostUrl: 'https://minio.cloud.cosm-lab.science',
                            botIdAndToken: env.TLG_TOKEN,
                            chatId: '-1002474884172',
                            threadId: '2'
                        )
                    }
                }
            }
        }
    }
 }
