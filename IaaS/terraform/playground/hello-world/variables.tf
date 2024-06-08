variable "filename" {
  default     = "./hello.txt"
  type        = string
  description = "local file name"
}

variable "content" {
  default     = "Hello, World!"
  type        = string
  description = "content of the file"

}