resource "local_file" "hello" {
    filename = var.filename
    content = var.content
    file_permission = "0700"
}

resource "random_string" "random_code" {
    length = 5
    special = false
    upper = false
}