resource "local_file" "hello" {
    filename = var.filename
    content = "${random_string.random_code.id}"
    file_permission = "0700"
    depends_on = [ random_string.random_code ]
}

resource "random_string" "random_code" {
    length = 5
    special = false
    upper = false
}

output "random_code" {
    value = random_string.random_code.id
}