resource "local_file" "hello" {
    filename = "${path.module}/hello.txt"
    content = "hello world!"
    file_permission = "0777"
}

