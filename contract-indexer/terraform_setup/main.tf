provider "aws" {
  region = "ap-southeast-1"
}

# Security Group
resource "aws_security_group" "sg" {
  name = "allow-ports"

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# EC2 Instance
resource "aws_instance" "indexer" {
  ami           = "ami-04a5ce820a419d6da"
  instance_type = "t2.micro"
  key_name       = "usdt_indexer"
  security_groups = [aws_security_group.sg.name]

  provisioner "remote-exec" {
    connection {
      type        = "ssh"
      user        = "ec2-user"
      private_key = file("E:/projects/automata-devops-assignment/contract-indexer/usdt_indexer.pem")
      host        = self.public_ip
    }

    inline = [
      "sudo yum update -y",
      "sudo amazon-linux-extras install docker",
      "sudo service docker start",
      "sudo usermod -a -G docker ec2-user",
      "docker pull biance1020/my-indexer:latest",
      "docker run -d -p 8080:80 biance1020/my-indexer:latest"
    ]
  }

  tags = {
    Name = "IndexerInstance"
  }
}
