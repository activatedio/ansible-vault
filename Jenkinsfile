import groovy.json.JsonOutput

node {

  checkout([$class: 'GitSCM', 
      branches: [[name: '*/master']], 
      doGenerateSubmoduleConfigurations: false, 
      extensions: [[$class: 'RelativeTargetDirectory', 
      relativeTargetDir: 'ansible-activated-vault']], 
      submoduleCfg: [], 
      userRemoteConfigs: [[url: 'git@github.com:activatedio/ansible-activated-vault.git']]])

  try {

    stage('test scenarios') {
      for (scenario in ['default', 'default-plus'] ) {
        sh 'cd ansible-activated-vault && molecule test -s ' + scenario
      }
    }

  } catch (e) {

    currentBuild.result = "FAILED"
    throw e
  }

}

