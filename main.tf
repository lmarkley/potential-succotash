terraform {
	required_providers {
		docker = {
			source = "kreuzwerker/docker"
			version = "~> 2.13.0"
		}
    docker-utils = {
      source = "Kaginari/docker-utils"
    }
	}
}

provider "docker" {}

resource "docker_image" "flask_api" {
	name = "flask-api:latest"
	keep_locally = true

}

resource "docker_image" "api_test" {
	name = "test-suite:latest"
	keep_locally = true
}


resource "docker_container" "flask_api" {
	image =  docker_image.flask_api.latest
	name = "GamesAPI"
  ports {
		internal = 5000
		external = 5000
	}
  networks_advanced {
    name = "api-testing"
  }
}

resource "docker_container" "api_test" {
  name = "pytest"
  image = docker_image.api_test.latest
  working_dir = "/root"
  entrypoint = ["pytest", "test_suite.py"]
  logs = true
  networks_advanced {
    name = "api-testing"
  }
}